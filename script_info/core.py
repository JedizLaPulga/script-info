from .collectors import collect_all

def get_system_info():
    """
    Collect comprehensive system information.
    Returns a dictionary with various system metadata.
    Refactored to use modular collectors.
    """
    return collect_all()