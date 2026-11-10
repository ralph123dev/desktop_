import psutil
import subprocess
import platform
import os
from typing import List, Dict, Tuple

class SystemMonitor:
    @staticmethod
    def get_ram_info() -> Dict:
        ram = psutil.virtual_memory()
        return {
            "total": ram.total,
            "used": ram.used,
            "available": ram.available,
            "percent": ram.percent,
            "free": ram.free,
        }

    @staticmethod
    def get_disk_info() -> List[Dict]:
        disks = []
        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except PermissionError:
                continue
        return disks

    @staticmethod
    def get_cpu_info() -> Dict:
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
        }

    @staticmethod
    def get_running_processes() -> List[Dict]:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'memory_info'])
                if pinfo['memory_percent'] > 0:
                    processes.append({
                        "pid": pinfo['pid'],
                        "name": pinfo['name'],
                        "memory_percent": pinfo['memory_percent'],
                        "memory_mb": pinfo['memory_info'].rss / (1024 * 1024),
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(processes, key=lambda x: x['memory_mb'], reverse=True)[:20]

    @staticmethod
    def kill_all_processes():
        current_pid = os.getpid()
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    # Skip self
                    if proc.info['pid'] == current_pid:
                        continue
                        
                    # Skip essential windows processes (Basic filter)
                    whitelist = ['explorer.exe', 'svchost.exe', 'csrss.exe', 'winlogon.exe', 'services.exe', 'lsass.exe', 'smss.exe', 'registry', 'System', 'Idle']
                    if proc.info['name'] in whitelist:
                        continue

                    proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return True
        except Exception as e:
            print(f"Error killing processes: {e}")
            return False

    @staticmethod
    def kill_process(pid: int) -> bool:
        try:
            p = psutil.Process(pid)
            p.terminate()
            p.wait(timeout=3)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            try:
                p.kill()
                return True
            except:
                return False

    @staticmethod
    def get_dns_cache() -> List[str]:
        system = platform.system()
        try:
            if system == "Windows":
                result = subprocess.run(["ipconfig", "/displaydns"], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                dns_records = []
                for line in lines:
                    if "Record Name" in line or "A (" in line or "CNAME" in line:
                        dns_records.append(line.strip())
                return dns_records[:100]
            elif system == "Darwin":
                result = subprocess.run(["log", "stream", "--predicate", "process == 'mDNSResponder'"],
                                     capture_output=True, text=True, timeout=2)
                return result.stdout.split('\n')[:100]
            elif system == "Linux":
                result = subprocess.run(["systemctl", "status", "systemd-resolved"],
                                     capture_output=True, text=True)
                return result.stdout.split('\n')[:100]
        except Exception as e:
            return [f"Error reading DNS cache: {str(e)}"]

    @staticmethod
    def clear_dns_cache() -> bool:
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(["ipconfig", "/flushdns"], shell=True, capture_output=True)
                return True
            elif system == "Darwin":
                subprocess.run(["sudo", "dscacheutil", "-flushcache"], capture_output=True)
                return True
            elif system == "Linux":
                subprocess.run(["sudo", "systemctl", "restart", "systemd-resolved"], capture_output=True)
                return True
        except Exception as e:
            print(f"Error clearing DNS cache: {e}")
            return False

    @staticmethod
    def clear_cache() -> bool:
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(["Disk Cleanup", "/sageset:1"], shell=True, capture_output=True)
                subprocess.run(["Disk Cleanup", "/sagerun:1"], shell=True, capture_output=True)
                return True
            elif system == "Darwin":
                subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache")], capture_output=True)
                return True
            elif system == "Linux":
                subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache")], capture_output=True)
                return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
