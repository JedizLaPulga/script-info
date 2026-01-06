import platform

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False

def get_security_info():
    info = {}
    if WMI_AVAILABLE and platform.system() == 'Windows':
        try:
            c = wmi.WMI()
            
            # Antivirus (Generic check via SecurityCenter2 is better but complex, sticking to simple Defender check)
            # Checking Registry or WMI for Defender
            try:
                # Simple loose check
                products = c.Win32_Product(Name="Windows Defender")
                if products:
                     info['Windows Defender'] = 'Installed'
                else:
                     info['Windows Defender'] = 'Not found explicitly'
            except:
                pass

            # Firewall
            try:
                firewall = c.Win32_Firewall()
                if firewall:
                    fw = firewall[0]
                    info['Firewall Enabled'] = 'Yes' if fw.Enabled else 'No'
            except:
                pass
            
            # UAC
            if WINREG_AVAILABLE:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
                    uac_level = winreg.QueryValueEx(key, "EnableLUA")[0]
                    info['UAC Enabled'] = 'Yes' if uac_level else 'No'
                    winreg.CloseKey(key)
                except:
                    pass

        except Exception as e:
            info['Security Info Error'] = str(e)
            
    else:
        info['Security Status'] = 'Platform not supported or WMI missing'
        
    return info
