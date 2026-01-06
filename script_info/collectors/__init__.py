from .basic import get_basic_info
from .hardware import get_hardware_info
from .storage import get_storage_info
from .network import get_network_info
from .software import get_software_info
from .security import get_security_info

def collect_all():
    data = {}
    data.update(get_basic_info())
    data.update(get_hardware_info())
    data.update(get_storage_info())
    data.update(get_network_info())
    data.update(get_software_info())
    data.update(get_security_info())
    return data
