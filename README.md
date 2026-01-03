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
| **Operating System** | Name, version, release, architecture |
| **CPU** | Physical/logical cores, frequency |
| **Memory** | Total, available, usage percentage |
| **Storage** | Total/free space, usage percentage |
| **Network** | Hostname, IP address |
| **System** | Boot time, current user, Python version |

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
OS: Windows
OS Version: 10.0.26100
OS Release: 11
Architecture: AMD64
CPU Cores (Physical): 4
CPU Cores (Logical): 8
CPU Frequency (MHz): 1198.0
Total Memory (GB): 31.69
Available Memory (GB): 21.51
Memory Usage (%): 32.1
Total Disk Space (GB): 475.57
Free Disk Space (GB): 317.78
Disk Usage (%): 33.2
Hostname: User
IP Address: 192.168.0.102
Boot Time: 2025-12-20 10:25:03
Current User: Windows
Python Version: 3.13.9

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

- 📧 **Email**: your.email@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/script-info/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/script-info/discussions)

---

**Made with ❤️ for developers and system administrators worldwide**
