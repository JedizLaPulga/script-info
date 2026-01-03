# Script Info 📊

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-orange.svg)](https://pypi.org/project/script-info/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/script-info)

> **Collect comprehensive system information with a single command** 🚀

Script Info is a powerful, cross-platform Python tool that gathers detailed system metadata and information. Whether you're a developer debugging environments, a system administrator monitoring infrastructure, or just curious about your machine's specs, Script Info provides everything you need in one elegant package.

## ✨ Features

- **🔍 Ultra-Comprehensive System Analysis**: Collects 90+ system metrics including hidden BIOS data, GPU telemetry, installed software inventory, browser history, development tools detection, system age analysis, VM detection, and complete hardware topology
- **💻 Dual Interface**: Choose between a sleek Command-Line Interface (CLI) or an intuitive Graphical User Interface (GUI) with copy functionality
- **⚡ Fast & Lightweight**: Minimal core dependencies with optional advanced libraries for deep extraction
- **🔧 Extensible**: Easy to add new information collectors and interfaces
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux with platform-specific enhancements
- **📊 Rich Output**: Formatted, color-coded results for easy reading and copying
- **🔒 Deep System Access**: Uses WMI, GPU libraries, and system APIs for hidden information extraction
- **📋 Copy & Export**: GUI includes copy-to-clipboard functionality for individual or bulk data export

## � Deep System Extraction

Script Info goes beyond standard system monitoring with advanced extraction capabilities:

### Hardware Intelligence
- **GPU Monitoring**: Real-time GPU usage, memory, and temperature (via GPUtil)
- **BIOS Information**: Firmware version, manufacturer, release date (via WMI)
- **Deep CPU Details**: Brand, architecture, cache sizes, flags, vendor info (via cpuinfo)
- **Sensor Data**: CPU/GPU temperatures, fan speeds (when available)

### System Architecture
- **Disk Partitions**: Detailed partition information and usage
- **Network Interfaces**: Complete network adapter enumeration
- **System Services**: Running services and their status (Windows)

### Software & Environment
- **Installed Programs**: Software inventory from system registry
- **Development Tools**: Detection and versioning of GCC, Go, Clang, Perl, Java, Python, Node.js, etc.
- **Browser History**: History counts and last visited sites for Chrome, Firefox, Edge, etc.
- **Environment Variables**: Complete environment configuration
- **System Configuration**: Locale, encoding, timezone details

### Performance & Health
- **Battery Analytics**: Charge status, time remaining, power source
- **Process Monitoring**: Total running processes and system load
- **I/O Statistics**: Disk and network read/write operations
- **System Age Detection**: BIOS age, Windows installation date, system freshness status
- **Virtual Machine Detection**: Hardware virtualization detection with indicators

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from PyPI (Recommended)
```bash
pip install script-info
```

*Note: For full deep system extraction (GPU, BIOS, services, CPU details, browser history), additional optional dependencies may be required. The app gracefully handles missing libraries.*

### Install from Source
```bash
git clone https://github.com/yourusername/script-info.git
cd script-info
pip install -e .
```

## 📖 Usage

### Command Line Interface (CLI)

Get all system information:
```bash
script-info-cli -all
```

Show help:
```bash
script-info-cli -help
```

### Graphical User Interface (GUI)

Launch the GUI application:
```bash
script-info-gui
```

**GUI Features:**
- Visual system information display with color-coded formatting
- One-click collection, refresh, and clear functions
- **Copy All** button to export complete system data to clipboard
- Selectable text for copying individual information pieces
- Real-time status updates during data collection

### Development Usage

Run directly from source:
```bash
# CLI
python -m script_info.cli.main -all

# GUI
python -m script_info.gui.main
```

## 📸 Screenshots

### CLI Output
```
Collecting system information...

System Information:
==================================================
OS Name: Windows
OS Version: 10.0.26100
OS Release: 11
OS Platform: Windows-11-10.0.26100-SP0
Architecture: AMD64
Processor: Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
CPU Physical Cores: 4
CPU Logical Cores: 8
CPU Frequency (MHz): 2995.0
CPU Usage (%): 15.2
CPU User Time: 20879.12s
CPU System Time: 14460.30s
CPU Idle Time: 195582.52s
Total Memory (GB): 31.69
Available Memory (GB): 21.03
Used Memory (GB): 10.66
Memory Usage (%): 33.6
Total Swap (GB): 2.0
Used Swap (GB): 0.0
Free Swap (GB): 2.0
Swap Usage (%): 0.0
Total Disk Space (GB): 475.57
Used Disk Space (GB): 158.07
Free Disk Space (GB): 317.5
Disk Usage (%): 33.2
Disk Read (MB): 31813.12
Disk Write (MB): 46247.67
Hostname: User
FQDN: User
IP Address (Local): 192.168.0.102
Network Bytes Sent (MB): 406.1
Network Bytes Received (MB): 5782.13
Network Packets Sent: 1901872
Network Packets Received: 3241501
Boot Time: 2025-12-20 10:25:03
Uptime: 13 days, 20:23:01
Current User: Windows
Logged-in Users: Windows
Total Processes: 274
Python Version: 3.13.9
Python Implementation: CPython
Python Compiler: MSC v.1944 64 bit (AMD64)
System Load (1min): 0.0
System Load (5min): 0.0
System Load (15min): 0.0
Battery Percentage (%): 75
Battery Plugged In: False
Battery Time Left: 4:14:43
Temperatures: N/A (Not supported)
Fan Speeds: N/A (Not supported)
GPU 1 Name: NVIDIA GeForce RTX 4060 Laptop GPU
GPU 1 Memory Total (GB): 8.0
GPU 1 Memory Used (GB): 1.2
GPU 1 Memory Free (GB): 6.8
GPU 1 Usage (%): 5.0
GPU 1 Temperature (°C): 45.0
Disk Partitions Count: 3
Partition 1 Device: C:
Partition 1 Mount: C:
Partition 1 Type: NTFS
Partition 1 Total (GB): 475.57
Partition 1 Free (GB): 317.5
Network Interfaces Count: 5
Interface 1 Name: Ethernet
Interface 1 IPv4: 192.168.0.102
Interface 1 MAC: 00:00:00:00:00:00
Running Services Count: 128
Running Services Sample: AdobeARMservice, AGMService, AGSService...
Environment Variables: {'PATH Entries Count': 25, 'HOME': 'Not set', 'USER': 'Not set', 'USERNAME': 'Windows', 'TEMP': 'C:\\Users\\Windows\\AppData\\Local\\Temp', ...}
System Locale: English_United States
System Encoding: cp1252
Timezone: Eastern Standard Time
BIOS Version: BIOS Version
BIOS Manufacturer: Manufacturer
BIOS Release Date: 20230101
Installed Programs Count: 85
Installed Programs Sample: 7-Zip 23.01, Adobe Acrobat Reader DC, Microsoft Edge...

Collection complete.
```

### GUI Interface
*GUI screenshot coming soon - intuitive Tkinter-based interface for visual system monitoring*

## 🛠️ Development

## 🛠️ Development

### Project Structure
```
script-info/
├── script_info/
│   ├── core.py          # Core system information collection (psutil, GPUtil, WMI)
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py      # CLI interface
│   └── gui/
│       ├── __init__.py
│       └── main.py      # GUI interface with copy functionality
├── tests/               # Unit tests
├── docs/                # Documentation
├── requirements.txt     # Python dependencies (psutil, colorama, GPUtil, WMI, cpuinfo, browserhistory)
├── pyproject.toml       # Package configuration
└── README.md           # This file
```

### Setting up Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/script-info.git
cd script-info

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

### Adding New Features
1. **New System Information**: Add collection logic to `script_info/core.py`
2. **New CLI Flags**: Extend argument parsing in `script_info/cli/main.py`
3. **GUI Enhancements**: Modify `script_info/gui/main.py`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil) for system information
- CLI colors powered by [colorama](https://github.com/tartley/colorama)
- GUI created with Python's built-in [tkinter](https://docs.python.org/3/library/tkinter.html)

## 📞 Support

- 📧 **Email**: jedizlapulga@proton.me
- 🐛 **Issues**: [GitHub Issues](https://github.com/jedizlapulga/script-info/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jedizlapulga/script-info/discussions)

---

**Made with ❤️ for developers and system administrators worldwide**
