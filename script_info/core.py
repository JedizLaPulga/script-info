import platform
import psutil
import socket
import datetime
import os
import getpass
import locale
import time
import shutil
import subprocess
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
try:
    import browserhistory as bh
    BROWSERHISTORY_AVAILABLE = True
except ImportError:
    BROWSERHISTORY_AVAILABLE = False


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

    # Deeper CPU information
    if CPUINFO_AVAILABLE:
        try:
            cpu_details = cpuinfo.get_cpu_info()
            info['CPU Brand'] = cpu_details.get('brand_raw', 'Unknown')
            info['CPU Architecture'] = cpu_details.get('arch', 'Unknown')
            info['CPU Bits'] = cpu_details.get('bits', 'Unknown')
            info['CPU Vendor'] = cpu_details.get('vendor_id_raw', 'Unknown')
            info['CPU Family'] = cpu_details.get('family', 'Unknown')
            info['CPU Model'] = cpu_details.get('model', 'Unknown')
            info['CPU Stepping'] = cpu_details.get('stepping', 'Unknown')
            info['CPU L2 Cache'] = cpu_details.get('l2_cache_size', 'Unknown')
            info['CPU L3 Cache'] = cpu_details.get('l3_cache_size', 'Unknown')
            info['CPU Flags'] = ', '.join(cpu_details.get('flags', [])[:10]) + ('...' if len(cpu_details.get('flags', [])) > 10 else '')
        except Exception as e:
            info['CPU Details'] = f'Unable to retrieve: {str(e)}'
    else:
        info['CPU Details'] = 'py-cpuinfo not installed'

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

            # System age detection
            if bios.ReleaseDate:
                bios_date = datetime.datetime.strptime(bios.ReleaseDate.split('.')[0], '%Y%m%d%H%M%S')
                current_date = datetime.datetime.now()
                system_age_days = (current_date - bios_date).days
                info['System Age (Days)'] = system_age_days
                info['System Age (Years)'] = round(system_age_days / 365.25, 1)

                # Estimate if system is "new" (less than 2 years old)
                if system_age_days < 730:  # 2 years
                    info['System Status'] = 'New System (BIOS < 2 years old)'
                elif system_age_days < 1825:  # 5 years
                    info['System Status'] = 'Recent System (BIOS 2-5 years old)'
                else:
                    info['System Status'] = 'Older System (BIOS > 5 years old)'

        except Exception as e:
            info['BIOS'] = f'Unable to retrieve: {str(e)}'
    else:
        info['BIOS'] = 'WMI not available or not Windows'

    # Windows Installation Date (for "newness" detection)
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            os_info = c.Win32_OperatingSystem()[0]
            install_date = os_info.InstallDate
            if install_date:
                install_datetime = datetime.datetime.strptime(install_date.split('.')[0], '%Y%m%d%H%M%S')
                current_date = datetime.datetime.now()
                windows_age_days = (current_date - install_datetime).days
                info['Windows Install Date'] = install_datetime.strftime('%Y-%m-%d %H:%M:%S')
                info['Windows Age (Days)'] = windows_age_days
                info['Windows Age (Years)'] = round(windows_age_days / 365.25, 1)

                # Estimate if Windows installation is "new"
                if windows_age_days < 365:  # 1 year
                    info['Windows Freshness'] = 'Very Fresh (installed < 1 year ago)'
                elif windows_age_days < 730:  # 2 years
                    info['Windows Freshness'] = 'Recent (installed 1-2 years ago)'
                elif windows_age_days < 1825:  # 5 years
                    info['Windows Freshness'] = 'Established (installed 2-5 years ago)'
                else:
                    info['Windows Freshness'] = 'Legacy (installed > 5 years ago)'

        except Exception as e:
            info['Windows Installation'] = f'Unable to retrieve: {str(e)}'
    else:
        info['Windows Installation'] = 'WMI not available or not Windows'

    # Virtual Machine Detection
    is_vm = False
    vm_indicators = []

    # Check BIOS manufacturer
    if 'BIOS Manufacturer' in info and info['BIOS Manufacturer']:
        bios_manufacturer = info['BIOS Manufacturer'].lower()
        if any(vm in bios_manufacturer for vm in ['vmware', 'virtualbox', 'qemu', 'xen', 'hyper-v', 'parallels']):
            is_vm = True
            vm_indicators.append('BIOS Manufacturer')

    # Check system model
    try:
        import wmi
        c = wmi.WMI()
        cs = c.Win32_ComputerSystem()[0]
        model = cs.Model.lower() if cs.Model else ''
        manufacturer = cs.Manufacturer.lower() if cs.Manufacturer else ''

        if any(vm in model for vm in ['virtual', 'vmware', 'virtualbox', 'qemu', 'xen']):
            is_vm = True
            vm_indicators.append('System Model')

        if any(vm in manufacturer for vm in ['vmware', 'oracle', 'xen', 'microsoft']):  # Microsoft for Hyper-V
            is_vm = True
            vm_indicators.append('System Manufacturer')

    except:
        pass

    # Check for VM-specific services or processes
    vm_processes = ['vmtoolsd.exe', 'vboxservice.exe', 'qemu-ga.exe']
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in vm_processes:
            is_vm = True
            vm_indicators.append('VM Processes')
            break

    info['Is Virtual Machine'] = 'Yes' if is_vm else 'No'
    if is_vm:
        info['VM Indicators'] = ', '.join(vm_indicators)
        info['System Type'] = 'Virtual Machine'
    else:
        info['System Type'] = 'Physical Hardware'

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

    # Development Tools Detection
    dev_tools = {
        'Python': ['python', 'python3'],
        'Java': ['java', 'javac'],
        'GCC': ['gcc'],
        'Clang': ['clang'],
        'Go': ['go'],
        'Perl': ['perl'],
        'Node.js': ['node', 'npm'],
        'Ruby': ['ruby'],
        'PHP': ['php'],
        'Rust': ['cargo', 'rustc'],
        'Git': ['git'],
        'Docker': ['docker'],
        'VS Code': ['code'],
        'Visual Studio': ['devenv'],
        'Android Studio': ['studio'],
        'Xcode': ['xcode-select']  # macOS
    }

    detected_tools = {}
    for tool_name, executables in dev_tools.items():
        for exe in executables:
            if shutil.which(exe):
                try:
                    # Try to get version
                    result = subprocess.run([exe, '--version'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        version = result.stdout.split('\n')[0].strip()
                        detected_tools[tool_name] = version
                        break
                    else:
                        detected_tools[tool_name] = 'Installed (version unknown)'
                        break
                except:
                    detected_tools[tool_name] = 'Installed (version check failed)'
                    break
        else:
            detected_tools[tool_name] = 'Not detected'

    info['Development Tools'] = detected_tools

    # Browser Information and History
    if BROWSERHISTORY_AVAILABLE:
        try:
            # Get browser history
            history = bh.get_history()
            browser_info = {}
            for browser_name, browser_history in history.items():
                if browser_history:
                    browser_info[f'{browser_name} History Count'] = len(browser_history)
                    if len(browser_history) > 0:
                        # Show last visited site as sample
                        last_visit = max(browser_history, key=lambda x: x[1] if len(x) > 1 else 0)
                        browser_info[f'{browser_name} Last Visit'] = f"{last_visit[0]} ({datetime.datetime.fromtimestamp(last_visit[1]).strftime('%Y-%m-%d %H:%M:%S')})"
                else:
                    browser_info[f'{browser_name} History'] = 'No history found or browser not installed'
            info['Browser History'] = browser_info
        except Exception as e:
            info['Browser History'] = f'Unable to retrieve: {str(e)}'
    else:
        info['Browser History'] = 'browserhistory not installed'

    return info