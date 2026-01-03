import platform
import psutil
import socket
import datetime
import os
import getpass


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

    # Temperatures (if available)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    info[f'Temperature ({name})'] = f"{entry.current}°C"
        else:
            info['Temperatures'] = 'N/A'
    except AttributeError:
        info['Temperatures'] = 'N/A (Not supported)'

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

    return info