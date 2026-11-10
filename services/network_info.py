import socket
import requests
import urllib.request

def get_ip_addresses():
    # IP locale v4
    try:
        hostname = socket.gethostname()
        ipv4 = socket.gethostbyname(hostname)
    except:
        ipv4 = "Non disponible"

    # IP locale v6
    try:
        ipv6 = ""
        info = socket.getaddrinfo(hostname, None)
        for addr in info:
            if addr[0] == socket.AF_INET6:
                ipv6 = addr[4][0]
                break
        if not ipv6:
            ipv6 = "Non disponible"
    except:
        ipv6 = "Non disponible"

    # IP publique
    try:
        external_ip = requests.get('https://api.ipify.org').text
    except:
        external_ip = "Non disponible"

    return {
        "ipv4": ipv4,
        "ipv6": ipv6,
        "public": external_ip
    }

def get_network_io():
    import psutil
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv
    }

def get_open_ports():
    import psutil
    ports = []
    try:
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == 'LISTEN':
                ports.append({
                    "port": conn.laddr.port,
                    "type": "TCP" if conn.type == socket.SOCK_STREAM else "UDP",
                    "pid": conn.pid
                })
    except Exception as e:
        print(f"Error getting ports: {e}")
    return ports[:50]  # Limit to 50 ports

