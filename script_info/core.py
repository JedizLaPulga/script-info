import platform
import psutil
import socket
import datetime
import os
import getpass
import locale
import time
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False


def get_system_info():
    """
    Collect comprehensive system information.
    Returns a dictionary with various system metadata.
    """
    info = {}

    # Basic OS information
    info['OS Name'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()
    info['OS Platform'] = platform.platform()
    info['Architecture'] = platform.machine()
    info['Processor'] = platform.processor()

    # CPU information
    info['CPU Physical Cores'] = psutil.cpu_count(logical=False)
    info['CPU Logical Cores'] = psutil.cpu_count(logical=True)
    info['CPU Frequency (MHz)'] = psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'
    info['CPU Usage (%)'] = psutil.cpu_percent(interval=1)

    # CPU times
    cpu_times = psutil.cpu_times()
    info['CPU User Time'] = f"{cpu_times.user:.2f}s"
    info['CPU System Time'] = f"{cpu_times.system:.2f}s"
    info['CPU Idle Time'] = f"{cpu_times.idle:.2f}s"

    # Memory information
    mem = psutil.virtual_memory()
    info['Total Memory (GB)'] = round(mem.total / (1024**3), 2)
    info['Available Memory (GB)'] = round(mem.available / (1024**3), 2)
    info['Used Memory (GB)'] = round(mem.used / (1024**3), 2)
    info['Memory Usage (%)'] = mem.percent

    # Swap memory
    swap = psutil.swap_memory()
    info['Total Swap (GB)'] = round(swap.total / (1024**3), 2)
    info['Used Swap (GB)'] = round(swap.used / (1024**3), 2)
    info['Free Swap (GB)'] = round(swap.free / (1024**3), 2)
    info['Swap Usage (%)'] = swap.percent

    # Disk information
    disk = psutil.disk_usage('/')
    info['Total Disk Space (GB)'] = round(disk.total / (1024**3), 2)
    info['Used Disk Space (GB)'] = round(disk.used / (1024**3), 2)
    info['Free Disk Space (GB)'] = round(disk.free / (1024**3), 2)
    info['Disk Usage (%)'] = disk.percent

    # Disk I/O
    disk_io = psutil.disk_io_counters()
    if disk_io:
        info['Disk Read (MB)'] = round(disk_io.read_bytes / (1024**2), 2)
        info['Disk Write (MB)'] = round(disk_io.write_bytes / (1024**2), 2)

    # Network information
    try:
        hostname = socket.gethostname()
        info['Hostname'] = hostname
        info['FQDN'] = socket.getfqdn()
        info['IP Address (Local)'] = socket.gethostbyname(hostname)
    except:
        info['Hostname'] = 'N/A'
        info['FQDN'] = 'N/A'
        info['IP Address (Local)'] = 'N/A'

    # Network I/O
    net_io = psutil.net_io_counters()
    info['Network Bytes Sent (MB)'] = round(net_io.bytes_sent / (1024**2), 2)
    info['Network Bytes Received (MB)'] = round(net_io.bytes_recv / (1024**2), 2)
    info['Network Packets Sent'] = net_io.packets_sent
    info['Network Packets Received'] = net_io.packets_recv

    # Boot time and uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    info['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
    uptime = datetime.datetime.now() - boot_time
    info['Uptime'] = str(uptime).split('.')[0]  # Remove microseconds

    # Users
    info['Current User'] = getpass.getuser()
    users = psutil.users()
    info['Logged-in Users'] = ', '.join([user.name for user in users]) if users else 'None'

    # Processes
    info['Total Processes'] = len(psutil.pids())

    # Python information
    info['Python Version'] = platform.python_version()
    info['Python Implementation'] = platform.python_implementation()
    info['Python Compiler'] = platform.python_compiler()

    # System load (Unix-like systems)
    try:
        load = psutil.getloadavg()
        info['System Load (1min)'] = round(load[0], 2)
        info['System Load (5min)'] = round(load[1], 2)
        info['System Load (15min)'] = round(load[2], 2)
    except:
        info['System Load'] = 'N/A (Windows)'

    # Battery information
    battery = psutil.sensors_battery()
    if battery:
        info['Battery Percentage (%)'] = battery.percent
        info['Battery Plugged In'] = battery.power_plugged
        info['Battery Time Left'] = str(datetime.timedelta(seconds=battery.secsleft)) if battery.secsleft != -1 else 'Calculating...'
    else:
        info['Battery'] = 'N/A (Desktop)'

    # Fan speeds (if available)
    try:
        fans = psutil.sensors_fans()
        if fans:
            for name, entries in fans.items():
                for entry in entries:
                    info[f'Fan Speed ({name})'] = f"{entry.current} RPM"
        else:
            info['Fan Speeds'] = 'N/A'
    except AttributeError:
        info['Fan Speeds'] = 'N/A (Not supported)'

    # GPU information
    if GPU_AVAILABLE:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for i, gpu in enumerate(gpus):
                    info[f'GPU {i+1} Name'] = gpu.name
                    info[f'GPU {i+1} Memory Total (GB)'] = round(gpu.memoryTotal / 1024, 2)
                    info[f'GPU {i+1} Memory Used (GB)'] = round(gpu.memoryUsed / 1024, 2)
                    info[f'GPU {i+1} Memory Free (GB)'] = round(gpu.memoryFree / 1024, 2)
                    info[f'GPU {i+1} Usage (%)'] = round(gpu.load * 100, 1)
                    info[f'GPU {i+1} Temperature (°C)'] = round(gpu.temperature, 1)
            else:
                info['GPU'] = 'No GPU detected'
        except Exception as e:
            info['GPU'] = f'GPU info unavailable: {str(e)}'
    else:
        info['GPU'] = 'GPUtil not installed'

    # Disk partitions
    partitions = psutil.disk_partitions()
    if partitions:
        info['Disk Partitions Count'] = len(partitions)
        for i, part in enumerate(partitions[:5]):  # Limit to 5 partitions
            info[f'Partition {i+1} Device'] = part.device
            info[f'Partition {i+1} Mount'] = part.mountpoint
            info[f'Partition {i+1} Type'] = part.fstype
            try:
                usage = psutil.disk_usage(part.mountpoint)
                info[f'Partition {i+1} Total (GB)'] = round(usage.total / (1024**3), 2)
                info[f'Partition {i+1} Free (GB)'] = round(usage.free / (1024**3), 2)
            except:
                info[f'Partition {i+1} Usage'] = 'Unable to access'
    else:
        info['Disk Partitions'] = 'None found'

    # Network interfaces
    net_if = psutil.net_if_addrs()
    if net_if:
        info['Network Interfaces Count'] = len(net_if)
        for i, (name, addrs) in enumerate(list(net_if.items())[:3]):  # Limit to 3 interfaces
            info[f'Interface {i+1} Name'] = name
            ipv4 = next((addr.address for addr in addrs if addr.family.name == 'AF_INET'), 'N/A')
            info[f'Interface {i+1} IPv4'] = ipv4
            mac = next((addr.address for addr in addrs if addr.family.name == 'AF_LINK'), 'N/A')
            info[f'Interface {i+1} MAC'] = mac
    else:
        info['Network Interfaces'] = 'None found'

    # System services (Windows)
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            services = c.Win32_Service()
            running_services = [s.Name for s in services if s.State == 'Running']
            info['Running Services Count'] = len(running_services)
            info['Running Services Sample'] = ', '.join(running_services[:5]) + ('...' if len(running_services) > 5 else '')
        except Exception as e:
            info['Services'] = f'Unable to retrieve: {str(e)}'
    else:
        info['Services'] = 'WMI not available or not Windows'

    # Environment variables (key ones)
    key_env_vars = ['PATH', 'HOME', 'USER', 'USERNAME', 'TEMP', 'TMP', 'LANG', 'SHELL', 'COMPUTERNAME', 'USERDOMAIN']
    env_info = {}
    for var in key_env_vars:
        value = os.environ.get(var, 'Not set')
        if var == 'PATH':
            paths = value.split(os.pathsep) if value != 'Not set' else []
            env_info['PATH Entries Count'] = len(paths)
        else:
            env_info[var] = value[:50] + '...' if len(str(value)) > 50 else value
    info['Environment Variables'] = env_info

    # Locale and timezone
    try:
        info['System Locale'] = locale.getlocale()[0] or 'Unknown'
        info['System Encoding'] = locale.getpreferredencoding()
    except:
        info['System Locale'] = 'Unable to determine'
    info['Timezone'] = time.tzname[0] if time.tzname else 'Unknown'

    # BIOS info via WMI
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            bios = c.Win32_BIOS()[0]
            info['BIOS Version'] = bios.Version
            info['BIOS Manufacturer'] = bios.Manufacturer
            info['BIOS Release Date'] = bios.ReleaseDate.split('.')[0] if bios.ReleaseDate else 'Unknown'
        except Exception as e:
            info['BIOS'] = f'Unable to retrieve: {str(e)}'
    else:
        info['BIOS'] = 'WMI not available or not Windows'

    # Installed programs (basic, Windows registry via WMI)
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            programs = c.Win32_Product()
            installed_programs = [p.Name for p in programs[:10]]  # Limit to 10
            info['Installed Programs Count'] = len(programs)
            info['Installed Programs Sample'] = ', '.join(installed_programs) + ('...' if len(programs) > 10 else '')
        except Exception as e:
            info['Installed Programs'] = f'Unable to retrieve: {str(e)}'
    else:
        info['Installed Programs'] = 'WMI not available or not Windows'

    return info