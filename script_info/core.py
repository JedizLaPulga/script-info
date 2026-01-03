import platform
import psutil
import socket
import datetime
import os


def get_system_info():
    """
    Collect comprehensive system information.
    Returns a dictionary with various system metadata.
    """
    info = {}

    # Basic OS information
    info['OS'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()
    info['Architecture'] = platform.machine()

    # CPU information
    info['CPU Cores (Physical)'] = psutil.cpu_count(logical=False)
    info['CPU Cores (Logical)'] = psutil.cpu_count(logical=True)
    info['CPU Frequency (MHz)'] = psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'

    # Memory information
    mem = psutil.virtual_memory()
    info['Total Memory (GB)'] = round(mem.total / (1024**3), 2)
    info['Available Memory (GB)'] = round(mem.available / (1024**3), 2)
    info['Memory Usage (%)'] = mem.percent

    # Disk information
    disk = psutil.disk_usage('/')
    info['Total Disk Space (GB)'] = round(disk.total / (1024**3), 2)
    info['Free Disk Space (GB)'] = round(disk.free / (1024**3), 2)
    info['Disk Usage (%)'] = disk.percent

    # Network information
    try:
        hostname = socket.gethostname()
        info['Hostname'] = hostname
        info['IP Address'] = socket.gethostbyname(hostname)
    except:
        info['Hostname'] = 'N/A'
        info['IP Address'] = 'N/A'

    # Boot time
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    info['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")

    # Current user
    info['Current User'] = os.getlogin()

    # Python version
    info['Python Version'] = platform.python_version()

    return info