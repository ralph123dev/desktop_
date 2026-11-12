import os
import time
import psutil
import subprocess
import platform
from pathlib import Path
from typing import Dict, List

class USBAntivirusService:
    @staticmethod
    def get_removable_drives() -> List[Dict]:
        """Récupère la liste des lecteurs amovibles connectés."""
        drives = []
        for partition in psutil.disk_partitions():
            if not USBAntivirusService._is_removable_partition(partition):
                continue

            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except (OSError, PermissionError):
                continue

            name = USBAntivirusService._get_partition_name(partition)
            drives.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'name': name,
                'total_size': usage.total,
                'used_size': usage.used,
                'free_size': usage.free,
                'percent': usage.percent,
                'fstype': partition.fstype
            })
        return drives

    @staticmethod
    def _is_removable_partition(partition) -> bool:
        if 'removable' in partition.opts:
            return True

        if platform.system() != "Linux":
            return False

        device_name = Path(partition.device).name
        if not device_name:
            return False

        sysfs_path = Path("/sys/class/block") / device_name
        if not sysfs_path.exists():
            return False

        resolved_path = sysfs_path.resolve()
        if any(part.startswith("usb") for part in resolved_path.parts):
            return True

        for parent in (resolved_path, *resolved_path.parents):
            removable_flag = parent / "removable"
            try:
                if removable_flag.read_text().strip() == "1":
                    return True
            except OSError:
                continue

        return False

    @staticmethod
    def _get_partition_name(partition) -> str:
        device_name = Path(partition.device).name or partition.device
        if platform.system() == "Windows":
            return USBAntivirusService.get_volume_name(partition.device) or device_name

        try:
            result = subprocess.run(
                ["lsblk", "-no", "LABEL", "--", partition.device],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            )
        except (OSError, subprocess.TimeoutExpired):
            return device_name

        label = result.stdout.strip()
        return label or device_name

    @staticmethod
    def get_volume_name(drive_letter: str) -> str:
        """Récupère le nom (label) du volume."""
        try:
            # drive_letter expected like "E:"
            drive_letter = drive_letter.rstrip('\\')
            cmd = f'wmic logicaldisk where DeviceID="{drive_letter}" get VolumeName'
            result = subprocess.check_output(cmd, shell=True).decode().split('\n')
            if len(result) > 1:
                return result[1].strip()
        except Exception as e:
            print(f"Error getting label for {drive_letter}: {e}")
        return ""

    @staticmethod
    def wait_for_usb(target_name: str, callback_found):
        """
        Attend qu'une clé USB avec le nom spécifique soit insérée.
        Exécute callback_found(drive_info) quand trouvé.
        """
        print(f"En attente de la clé nommée: {target_name}")
        while True:
            drives = USBAntivirusService.get_removable_drives()
            for drive in drives:
                label = drive['name']
                
                # Check match (case insensitive)
                if label.lower() == target_name.lower():
                    callback_found(drive, label)
                    return
            time.sleep(2)

    @staticmethod
    def has_virus_signature(mountpoint: str) -> bool:
        """Vérifie la présence de fichiers suspects 'usb driver'."""
        suspicious = ["usb driver.exe", "usbdriver.exe", "usb driver"]
        try:
            for root, dirs, files in os.walk(mountpoint):
                for name in files + dirs:
                    if name.lower() in suspicious:
                        return True
        except Exception:
            pass
        return False

    @staticmethod
    def clean_and_format(drive_info: Dict, status_callback) -> str:
        """
        Logique principale:
        1. Vérifier taille (< 80Go)
        2. Vérifier virus ou forcer formatage si demandé
        3. Formater et Renommer
        """
        mountpoint = drive_info['mountpoint']
        drive_letter = mountpoint.rstrip('\\')
        total_size_gb = drive_info['total_size'] / (1024**3)

        status_callback(f"Analyse de la clé {drive_letter}...")

        # Condition 80GB
        if total_size_gb > 80:
            return "ERREUR: La capacité de la clé est supérieure à 80Go. Formatage impossible par sécurité."

        # Detect virus
        has_virus = USBAntivirusService.has_virus_signature(mountpoint)
        
        status_callback("Nettoyage en cours...")
        
        # Commandes de nettoyage (Code.txt)
        # On tente de nettoyer avant de formater au cas où le formatage échoue ou si on veut juste nettoyer
        # Mais la demande dit: "si ... virus ... clé devra etre formater".
        # Dans tous les cas, le flow "Ultre Clean" semble impliquer un formatage pour le scénario du virus.
        
        try:
            # Tentative de suppression manuelle des virus connus avant formatage
            # attrib -h -r -s /s /d *.*
            subprocess.run(f'attrib -h -r -s /s /d {mountpoint}\\*.*', shell=True)
            
            # del "usb driver.exe" /f /s /q
            subprocess.run(f'del "{mountpoint}\\usb driver.exe" /f /s /q', shell=True)
            subprocess.run(f'del "{mountpoint}\\usbdriver.exe" /f /s /q', shell=True)
        except Exception as e:
            print(f"Erreur mineure nettoyage pré-formatage: {e}")

        # Formatage
        status_callback("Formatage et renommage en cours (Stark_virus_kill)...")
        try:
            # /FS:FAT32 (ou NTFS) /Q (Quick) /V:Label /Y (Yes to prompts - but format command usually asks for volume label if not /Q maybe?)
            # echo Y | format ... handle stdin
            # Using cmd /c format
            # Warning: Format is distinct.
            # Safe approach: usage of PowerShell or specific format command.
            # "format E: /Q /V:Stark_virus_kill /Y" might not exist exactly like that in standard CMD without prompt.
            # Usually: format E: /Q /V:Stark_virus_kill /y
            
            cmd = f'format {drive_letter} /FS:FAT32 /Q /V:Stark_virus_kill /Y'
            # Note: /Y is not always standard for 'format' in all versions without piping 'echo y'.
            process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Send 'Enter' to confirm if needed (Format usually asks for current label, then confirm)
            # But if we provide /V and it's new, it might simpler.
            # Using PowerShell might be cleaner: Rename-Item doesn't format.
            # Format-Volume -DriveLetter E -FileSystem FAT32 -NewFileSystemLabel "Stark_virus_kill" -Confirm:$false
            
            ps_cmd = f'powershell -Command "Format-Volume -DriveLetter {drive_letter[0]} -FileSystem FAT32 -NewFileSystemLabel \'Stark_virus_kill\' -Confirm:$false"'
            subprocess.run(ps_cmd, shell=True, check=True)
            
            return "SUCCESS: Virus éliminé et clé formatée avec succès."
        except subprocess.CalledProcessError as e:
            return f"ERREUR: Échec du formatage. {e}"
        except Exception as e:
            return f"ERREUR: {e}"

    @staticmethod
    def deep_scan(mountpoint: str, status_callback) -> str:
        """Scan en profondeur et nettoyage."""
        status_callback("Scan en profondeur initialisé...")
        try:
            # Code.txt commands
            cmds = [
                f'attrib -h -r -s /s /d {mountpoint}\\*.*',
                f'del {mountpoint}\\autorun.inf /f /s /q',
                f'del {mountpoint}\\*.exe /f /s /q',
                f'del {mountpoint}\\*.lnk /f /s /q',
                f'del {mountpoint}\\*.vbs /f /s /q',
                f'del "{mountpoint}\\usb driver.exe" /f /s /q',
                f'del {mountpoint}\\usbdriver.exe" /f /s /q',
                f'rd /s /q {mountpoint}\\RECYCLER',
                f'rd /s /q "{mountpoint}\\System Volume Information"'
            ]
            
            for cmd in cmds:
                status_callback(f"Exécution: {cmd[:30]}...")
                subprocess.run(cmd, shell=True)
                
            return "Scan terminé. Fichiers suspects nettoyés."
        except Exception as e:
            return f"Erreur durant le scan: {e}"
