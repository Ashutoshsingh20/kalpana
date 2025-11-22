
# 🤖 Kalpana - AI-Powered System Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**A Jarvis-level AI assistant with real-time system monitoring, voice interaction, and intelligent automation capabilities.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

Kalpana is an advanced AI assistant that combines the power of real-time system monitoring with intelligent voice interaction and automation. Inspired by J.A.R.V.I.S., Kalpana provides a beautiful HUD interface to monitor your system vitals while offering voice-controlled assistance for various tasks.

### ✨ Key Highlights

- 🎯 **Real-time System Monitoring**: Track CPU, memory, disk, and network usage with stunning visualizations
- 🎤 **Voice Interaction**: Natural language processing for hands-free control
- 🧠 **AI-Powered Brain**: Intelligent decision-making and task automation
- 🔒 **Security Features**: Built-in firewall management and security monitoring
- 🌐 **Web Scraping**: Automated data collection and analysis
- 🔧 **Modular Architecture**: Easily extensible with plugins
- 🎨 **Beautiful UI**: Modern, responsive dashboard with animations

---

## 🚀 Features

### System Monitoring
- **CPU Monitoring**: Real-time CPU usage, temperature, and per-core statistics
- **Memory Tracking**: RAM and swap usage with detailed breakdowns
- **Disk Management**: Storage usage, I/O statistics, and health monitoring
- **Network Stats**: Upload/download speeds, active connections, and bandwidth usage
- **Process Management**: View and manage running processes

### AI & Automation
- **Voice Engine**: Speech recognition and text-to-speech capabilities
- **Natural Language Understanding**: Process commands in natural language
- **Task Scheduler**: Automated task execution with APScheduler
- **Smart Alerts**: Intelligent notifications based on system thresholds

### Security
- **Firewall Manager**: Configure and manage firewall rules
- **Security Core**: Monitor security events and threats
- **Encryption**: Built-in cryptography support

### Web & Network
- **Web Scraper**: Extract data from websites with BeautifulSoup4
- **Network Scanner**: Discover devices and scan network topology
- **API Server**: RESTful API built with FastAPI and WebSocket support

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Ashutoshsingh20/kalpana.git
cd kalpana
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Kalpana**
```bash
# Using the startup script
./run_kalpana.sh

# Or manually
python backend/main.py
```

5. **Access the Dashboard**

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 🎮 Usage

### Starting the Backend

```bash
# Start with default settings
python backend/main.py

# Custom port
python backend/main.py --port 8080
```

### Voice Commands

Activate voice mode and try:
- "Kalpana, what's my CPU usage?"
- "Show memory statistics"
- "Scan the network"
- "Open system control panel"

### API Endpoints

#### System Information
```bash
# Get CPU stats
curl http://localhost:8000/api/system/cpu

# Get memory info
curl http://localhost:8000/api/system/memory

# Get disk usage
curl http://localhost:8000/api/system/disk
```

#### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('System stats:', data);
};
```

---

## 🏗️ Architecture

```
kalpana/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── kalpana_core/          # Core AI brain logic
│   ├── modules/               # System monitoring modules
│   │   ├── system_monitor.py  # CPU, memory, disk monitoring
│   │   └── network_scanner.py # Network utilities
│   ├── voice/                 # Voice engine
│   ├── security/              # Security features
│   ├── web/                   # Web scraping
│   └── tools/                 # System control tools
├── frontend/
│   ├── index.html             # Main dashboard
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript modules
├── requirements.txt           # Python dependencies
└── run_kalpana.sh            # Startup script
```

---

## 🔧 Configuration

Create a `config.yaml` in the root directory:

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false

monitoring:
  update_interval: 1  # seconds
  cpu_threshold: 80    # percent
  memory_threshold: 85 # percent

voice:
  enabled: true
  language: "en-US"
  wake_word: "kalpana"

security:
  firewall_enabled: true
  scan_interval: 300  # seconds
```

---

## 📊 Dashboard Features

The Kalpana HUD provides:

1. **System Vitals Panel**: Real-time CPU, memory, and disk usage
2. **Network Activity**: Live network traffic graphs
3. **Process Monitor**: Running processes and resource usage
4. **Voice Assistant**: Interactive voice command panel
5. **System Clock**: Current time and system uptime
6. **Quick Actions**: One-click system controls

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python test_all_features.py

# Test specific modules
python -m pytest tests/test_system_monitor.py
python -m pytest tests/test_voice_engine.py
```

---

## 🛠️ Development

### Adding New Modules

1. Create your module in `backend/modules/`
2. Import in `backend/main.py`
3. Add API endpoints as needed
4. Update documentation

### Example Module Structure

```python
# backend/modules/my_module.py
class MyModule:
    def __init__(self):
        self.name = "MyModule"
    
    async def process(self, data):
        # Your logic here
        return result
```

---

## 📚 Documentation

For detailed documentation, visit:

- [API Documentation](docs/API.md)
- [Module Development Guide](docs/MODULES.md)
- [Voice Commands Reference](docs/VOICE_COMMANDS.md)
- [Security Best Practices](docs/SECURITY.md)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ashutosh Singh**
- GitHub: [@Ashutoshsingh20](https://github.com/Ashutoshsingh20)
- LinkedIn: [ashutosh-singh-6b2120248](https://www.linkedin.com/in/ashutosh-singh-6b2120248/)
- - Email: [imashutoshingh15@gmail.com](mailto:imashutoshingh15@gmail.com)
---

## 🙏 Acknowledgments

- Inspired by J.A.R.V.I.S. from Iron Man
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI animations powered by CSS3 and JavaScript
- System monitoring with [psutil](https://github.com/giampaolo/psutil)

---

## 📞 Support

If you have any questions or run into issues:

- Open an [Issue](https://github.com/Ashutoshsingh20/kalpana/issues)
- Start a [Discussion](https://github.com/Ashutoshsingh20/kalpana/discussions)
- Email: [imashutoshingh15@gmail.com](mailto:imashutoshingh15@gmail.com)
---

## 🌟 Star History

If you find Kalpana useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by Ashutosh Singh**

*Kalpana - Your Personal AI Assistant*

</div>
