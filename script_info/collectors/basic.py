import platform
import datetime
import psutil
import getpass
import time
import locale
import os

def get_os_info():
    info = {}
    info['OS Name'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()
    info['OS Platform'] = platform.platform()
    info['Architecture'] = platform.machine()
    info['Processor'] = platform.processor()
    
    # Locale and timezone
    try:
        info['System Locale'] = locale.getlocale()[0] or 'Unknown'
        info['System Encoding'] = locale.getpreferredencoding()
    except Exception:
        info['System Locale'] = 'Unable to determine'
    info['Timezone'] = time.tzname[0] if time.tzname else 'Unknown'
    
    return info

def get_users_info():
    info = {}
    info['Current User'] = getpass.getuser()
    try:
        users = psutil.users()
        info['Logged-in Users'] = ', '.join([user.name for user in users]) if users else 'None'
    except Exception:
        info['Logged-in Users'] = 'Unable to determine'
    return info

def get_boot_info():
    info = {}
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        info['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
        uptime = datetime.datetime.now() - boot_time
        info['Uptime'] = str(uptime).split('.')[0]  # Remove microseconds
    except Exception:
        info['Boot Time'] = 'Unknown'
        info['Uptime'] = 'Unknown'
    return info

def get_basic_info():
    data = {}
    data.update(get_os_info())
    data.update(get_users_info())
    data.update(get_boot_info())
    return data
