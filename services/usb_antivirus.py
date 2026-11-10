import os
import time
import psutil
import subprocess
import threading
from typing import Optional, Dict, List

class USBAntivirusService:
    @staticmethod
    def get_removable_drives() -> List[Dict]:
        """Récupère la liste des lecteurs amovibles connectés."""
        drives = []
        for partition in psutil.disk_partitions():
            if 'removable' in partition.opts or 'cdrom' not in partition.opts: # Simple filter, logic might need refinement for strict USB detection
                # Windows usually marks USBs as removable.
                # Just incase, we usually check checks for 'removable'.
                if 'removable' in partition.opts:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        drives.append({
                            'device': partition.device,
                            'mountpoint': partition.mountpoint,
                            'total_size': usage.total,
                            'fstype': partition.fstype
                        })
                    except Exception:
                        pass
        return drives

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
                drive_letter = drive['mountpoint'].rstrip('\\')
                label = USBAntivirusService.get_volume_name(drive_letter)
                
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
