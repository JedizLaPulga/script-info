import socket
import psutil
import subprocess

def get_basic_network_info():
    info = {}
    try:
        hostname = socket.gethostname()
        info['Hostname'] = hostname
        info['FQDN'] = socket.getfqdn()
        info['IP Address (Local)'] = socket.gethostbyname(hostname)
    except Exception:
        info['Hostname'] = 'N/A'
        info['FQDN'] = 'N/A'
        info['IP Address (Local)'] = 'N/A'
    return info

def get_network_io_info():
    info = {}
    net_io = psutil.net_io_counters()
    info['Network Bytes Sent (MB)'] = round(net_io.bytes_sent / (1024**2), 2)
    info['Network Bytes Received (MB)'] = round(net_io.bytes_recv / (1024**2), 2)
    info['Network Packets Sent'] = net_io.packets_sent
    info['Network Packets Received'] = net_io.packets_recv
    return info

def get_interfaces_info():
    info = {}
    try:
        net_if = psutil.net_if_addrs()
        if net_if:
            info['Network Interfaces Count'] = len(net_if)
            # Limit to 3 interfaces to avoid clutter
            for i, (name, addrs) in enumerate(list(net_if.items())[:3]):
                info[f'Interface {i+1} Name'] = name
                ipv4 = next((addr.address for addr in addrs if addr.family == socket.AF_INET), 'N/A')
                info[f'Interface {i+1} IPv4'] = ipv4
                # MAC address lookup can vary by platform in psutil
                # Usually AF_LINK on Unix, but on Windows it's handled differently or psutil maps it.
                # simpler to just look for the hardware address format if possible, 
                # but psutil usually provides AF_LINK or similar.
                # We'll just try to find a reasonable MAC-like address if AF_LINK isn't available directly by name 
                # (psutil constants vary by OS).
                # safely getting the first address that looks like a MAC or isn't IPv4/6
                mac = 'N/A'
                for addr in addrs:
                     if addr.family not in (socket.AF_INET, socket.AF_INET6):
                         mac = addr.address
                         break
                info[f'Interface {i+1} MAC'] = mac
        else:
            info['Network Interfaces'] = 'None found'
    except Exception as e:
        info['Network Interfaces Error'] = str(e)
    return info

def get_dns_info():
    info = {}
    try:
        import dns.resolver
        # This might fail if no internet
        dns_servers = dns.resolver.get_default_resolver().nameservers
        info['DNS Servers'] = ', '.join(dns_servers)
    except ImportError:
        info['DNS Servers'] = 'dnspython not installed'
    except Exception:
        info['DNS Servers'] = 'Unable to retrieve'
    return info

def get_wifi_info():
    info = {}
    try:
        # Windows specific
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0 and 'Name' in result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'SSID' in line and 'BSSID' not in line:
                    info['WiFi SSID'] = line.split(':')[1].strip() if ':' in line else 'Connected'
                elif 'Signal' in line:
                    info['WiFi Signal'] = line.split(':')[1].strip() if ':' in line else 'Unknown'
        else:
            # Not strict failure, just maybe not wifi or not windows
            pass
    except Exception:
        pass
    return info

def get_open_ports_sample():
    # Reduced logic for speed
    info = {}
    open_ports = []
    # Reduced list of ports
    common_ports = [80, 443, 3389, 22] 
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05) # Very fast timeout
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
            
    info['Open Ports (Local Sample)'] = ', '.join(map(str, open_ports)) if open_ports else 'None found'
    return info

def get_network_info():
    data = {}
    data.update(get_basic_network_info())
    data.update(get_network_io_info())
    data.update(get_interfaces_info())
    data.update(get_dns_info())
    data.update(get_wifi_info())
    data.update(get_open_ports_sample())
    return data
