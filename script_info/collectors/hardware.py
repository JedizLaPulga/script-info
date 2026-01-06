import psutil
import platform
import threading
import datetime
import shutil

# Optional imports
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

try:
    import cpuinfo
    CPUINFO_AVAILABLE = True
except ImportError:
    CPUINFO_AVAILABLE = False

def get_cpu_info():
    info = {}
    info['CPU Physical Cores'] = psutil.cpu_count(logical=False)
    info['CPU Logical Cores'] = psutil.cpu_count(logical=True)
    
    freq = psutil.cpu_freq()
    info['CPU Frequency (MHz)'] = freq.current if freq else 'N/A'
    info['CPU Usage (%)'] = psutil.cpu_percent(interval=0.1) # Reduced interval for speed

    cpu_times = psutil.cpu_times()
    info['CPU User Time'] = f"{cpu_times.user:.2f}s"
    info['CPU System Time'] = f"{cpu_times.system:.2f}s"
    info['CPU Idle Time'] = f"{cpu_times.idle:.2f}s"

    # Deeper CPU information - temporarily disabled in original code "due to hanging issues"
    # Keeping it optional/disabled or improving timeout
    info['CPU Details'] = 'CPU info collection skipped (performance)'
    
    return info

def get_memory_info():
    info = {}
    mem = psutil.virtual_memory()
    info['Total Memory (GB)'] = round(mem.total / (1024**3), 2)
    info['Available Memory (GB)'] = round(mem.available / (1024**3), 2)
    info['Used Memory (GB)'] = round(mem.used / (1024**3), 2)
    info['Memory Usage (%)'] = mem.percent

    swap = psutil.swap_memory()
    info['Total Swap (GB)'] = round(swap.total / (1024**3), 2)
    info['Used Swap (GB)'] = round(swap.used / (1024**3), 2)
    info['Free Swap (GB)'] = round(swap.free / (1024**3), 2)
    info['Swap Usage (%)'] = swap.percent
    return info

def get_gpu_info():
    info = {}
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
    return info

def get_battery_info():
    info = {}
    if not hasattr(psutil, "sensors_battery"):
        info['Battery'] = 'Not supported'
        return info

    battery = psutil.sensors_battery()
    if battery:
        info['Battery Percentage (%)'] = battery.percent
        info['Battery Plugged In'] = battery.power_plugged
        info['Battery Time Left'] = str(datetime.timedelta(seconds=battery.secsleft)) if battery.secsleft != -1 else 'Calculating...'
    else:
        info['Battery'] = 'N/A (Desktop)'
    return info

def get_bios_info():
    info = {}
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            bios_list = c.Win32_BIOS()
            if bios_list:
                bios = bios_list[0]
                info['BIOS Version'] = bios.Version
                info['BIOS Manufacturer'] = bios.Manufacturer
                info['BIOS Release Date'] = bios.ReleaseDate.split('.')[0] if bios.ReleaseDate else 'Unknown'
        except Exception as e:
             info['BIOS'] = f'Unable to retrieve: {str(e)}'
    else:
        info['BIOS'] = 'WMI not available or not Windows'
    return info

def get_hardware_info():
    data = {}
    data.update(get_cpu_info())
    data.update(get_memory_info())
    data.update(get_gpu_info())
    data.update(get_battery_info())
    data.update(get_bios_info())
    return data
