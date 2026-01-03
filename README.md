# Script Info 📊

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-orange.svg)](https://pypi.org/project/script-info/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/script-info)

> **Collect comprehensive system information with a single command** 🚀

Script Info is a powerful, cross-platform Python tool that gathers detailed system metadata and information. Whether you're a developer debugging environments, a system administrator monitoring infrastructure, or just curious about your machine's specs, Script Info provides everything you need in one elegant package.

## ✨ Features

- **🔍 Comprehensive System Analysis**: Collects OS details, CPU specs, memory usage, disk space, network information, and more
- **💻 Dual Interface**: Choose between a sleek Command-Line Interface (CLI) or an intuitive Graphical User Interface (GUI)
- **⚡ Fast & Lightweight**: Minimal dependencies, instant results
- **🔧 Extensible**: Easy to add new information collectors and interfaces
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux
- **📊 Rich Output**: Formatted, color-coded results for easy reading

## 📋 System Information Collected

| Category | Details |
|----------|---------|
| **Operating System** | Name, version, release, platform, architecture, processor |
| **CPU** | Physical/logical cores, frequency, usage %, user/system/idle times |
| **Memory** | Total, available, used, usage % (RAM + Swap) |
| **Storage** | Total/used/free space, usage %, read/write I/O |
| **Network** | Hostname, FQDN, IP, bytes/packets sent/received |
| **System** | Boot time, uptime, current/logged-in users, total processes |
| **Battery** | Percentage, plugged status, time remaining (if applicable) |
| **Hardware Sensors** | Temperatures, fan speeds (if supported) |
| **Runtime** | Python version, implementation, compiler |
| **Performance** | System load averages (Unix-like systems) |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from PyPI (Recommended)
```bash
pip install script-info
```

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

Collection complete.
```

### GUI Interface
*GUI screenshot coming soon - intuitive Tkinter-based interface for visual system monitoring*

## 🛠️ Development

### Project Structure
```
script-info/
├── script_info/
│   ├── core.py          # Core system information collection
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py      # CLI interface
│   └── gui/
│       ├── __init__.py
│       └── main.py      # GUI interface
├── tests/               # Unit tests
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
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
