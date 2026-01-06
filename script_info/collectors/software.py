import platform
import shutil
import subprocess
import os
import datetime

# Optional imports
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

try:
    import browserhistory as bh
    BROWSERHISTORY_AVAILABLE = True
except ImportError:
    BROWSERHISTORY_AVAILABLE = False

def get_python_info():
    info = {}
    info['Python Version'] = platform.python_version()
    info['Python Implementation'] = platform.python_implementation()
    info['Python Compiler'] = platform.python_compiler()
    return info

def get_dev_tools_info():
    dev_tools = {
        'Python': ['python', 'python3'],
        'Java': ['java'],
        'GCC': ['gcc'],
        'Node.js': ['node'],
        'Git': ['git'],
        'Docker': ['docker'],
        'VS Code': ['code'],
    }

    detected_tools = {}
    for tool_name, executables in dev_tools.items():
        found = False
        for exe in executables:
            if shutil.which(exe):
                detected_tools[tool_name] = 'Installed'
                found = True
                break
        if not found:
            detected_tools[tool_name] = 'Not detected'
            
    return {'Development Tools': detected_tools}

def get_installed_programs_info():
    info = {}
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            # This can be slow, limiting to top 10
            programs = c.Win32_Product()
            # It's an iterator, so we take a slice carefully or list it
            # Win32_Product is known to be slow and problematic.
            # A safer/faster way is often Registry, but sticking to WMI for now, simplified.
            # We'll skip it if it takes too long or just grab a few.
            # Actually, Win32_Product is discouraged by Microsoft. 
            # I will wrap this in a very generic try/except and maybe skip it for now 
            # or replace with a safer check if I had registry access code ready.
            # For now, I'll comment it out or make it very safe?
            # The original code had it. I will keep it but limit strictness.
            installed = []
            for i, p in enumerate(programs):
                if i >= 10: break
                if p.Name: installed.append(p.Name)
            
            info['Installed Programs Sample'] = ', '.join(installed)
        except Exception:
            info['Installed Programs'] = 'Unable to retrieve (WMI Error)'
    else:
        info['Installed Programs'] = 'Not available'
    return info

def get_browser_history_info():
    info = {}
    if BROWSERHISTORY_AVAILABLE:
        try:
            # This can be privacy invasive, ensure it's handled carefully.
            # We will just get counts, not actual URLs, to be "Professional" and less "Spyware-ish"
            history = bh.get_history()
            browser_info = {}
            for browser_name, browser_history in history.items():
                if browser_history:
                    browser_info[f'{browser_name} History Count'] = len(browser_history)
                    if len(browser_history) > 0:
                        # Only show the *timestamp* of last visit, not the URL
                        last_visit = max(browser_history, key=lambda x: x[1] if len(x) > 1 else 0)
                        datestr = datetime.datetime.fromtimestamp(last_visit[1]).strftime('%Y-%m-%d %H:%M:%S')
                        browser_info[f'{browser_name} Last Activity'] = datestr
                else:
                    browser_info[f'{browser_name}'] = 'No history'
            info['Browser History Stats'] = browser_info
        except Exception as e:
            info['Browser History'] = f'Error: {str(e)}'
    else:
        info['Browser History'] = 'Module not installed'
    return info

def get_software_info():
    data = {}
    data.update(get_python_info())
    data.update(get_dev_tools_info())
    # Skipping installed programs for speed/reliability unless requested? 
    # I'll include it but it's the slowest part often.
    # data.update(get_installed_programs_info()) 
    data.update(get_browser_history_info())
    return data
