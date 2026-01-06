import psutil

def get_disk_info():
    info = {}
    try:
        disk = psutil.disk_usage('/')
        info['Total Disk Space (GB)'] = round(disk.total / (1024**3), 2)
        info['Used Disk Space (GB)'] = round(disk.used / (1024**3), 2)
        info['Free Disk Space (GB)'] = round(disk.free / (1024**3), 2)
        info['Disk Usage (%)'] = disk.percent
    except Exception as e:
        info['Disk Info'] = f'Error: {str(e)}'

    disk_io = psutil.disk_io_counters()
    if disk_io:
        info['Disk Read (MB)'] = round(disk_io.read_bytes / (1024**2), 2)
        info['Disk Write (MB)'] = round(disk_io.write_bytes / (1024**2), 2)
    
    return info

def get_partitions_info():
    info = {}
    try:
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
                except Exception:
                    info[f'Partition {i+1} Usage'] = 'Unable to access'
        else:
            info['Disk Partitions'] = 'None found'
    except Exception as e:
        info['Partitions'] = f'Error: {str(e)}'
        
    return info

def get_storage_info():
    data = {}
    data.update(get_disk_info())
    data.update(get_partitions_info())
    return data
