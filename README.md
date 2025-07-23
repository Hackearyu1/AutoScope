# AutoScope 🔍

**Modular Reconnaissance Automation Framework for Penetration Testing and Bug Bounty Hunting**

AutoScope is a powerful, single-file Python framework that automates the reconnaissance phase of security testing by orchestrating industry-standard tools through a unified command-line interface. Transform hours of manual reconnaissance into minutes of automated intelligence gathering.

## ✨ Features

### 🎯 **Complete Attack Surface Discovery**
- **Subdomain Enumeration**: Comprehensive discovery using subfinder and amass
- **Port Scanning**: Fast and thorough scanning with naabu and nmap integration
- **HTTP Service Detection**: Live host probing and technology fingerprinting with httpx
- **JavaScript Analysis**: Hidden endpoint discovery from JS files and APIs
- **Directory/File Fuzzing**: Web content discovery using ffuf with smart wordlists
- **Parameter Discovery**: HTTP parameter hunting with arjun
- **Visual Documentation**: Automated screenshot capture with gowitness

### 🚀 **Advanced Capabilities**
- **Modular Architecture**: Enable/disable specific reconnaissance stages
- **Multiple Scan Profiles**: Fast mode for quick assessment, deep mode for comprehensive analysis
- **Organized Output**: Structured results in target-specific directories
- **Multiple Report Formats**: Markdown, JSON, and CSV output options
- **Resume Functionality**: Continue interrupted scans from where they left off
- **Cross-Platform**: Works on Linux, macOS, and Windows

**Installation**
Clone the repository
git clone https://github.com/yourusername/autoscope.git
cd autoscope
**Installation part.2**
Run the automated installer
chmod +x install.sh
./install.sh

**Reload your shell environment**
source ~/.bashrc

**Test the installation**
python3 autoscope.py -t example.com --fast

### ⚡ **User-Friendly Design**
- **One-Command Installation**: Automated setup script handles all dependencies
- **Single-File Framework**: No complex directory structures or configurations
- **Rich CLI Interface**: Intuitive command-line arguments and help system
- **Professional Reports**: Clean, structured output perfect for documentation

## 🔧 Requirements

### System Requirements
- **Python 3.8+**
- **Go 1.19+** (for external tools)
- **Linux/macOS recommended** (Windows supported with limitations)
- **4GB RAM minimum** for large-scale scans

### External Tools
AutoScope integrates with these industry-standard tools:
- [subfinder](https://github.com/projectdiscovery/subfinder) - Fast subdomain enumeration
- [naabu](https://github.com/projectdiscovery/naabu) - Port discovery tool
- [httpx](https://github.com/projectdiscovery/httpx) - HTTP toolkit
- [ffuf](https://github.com/ffuf/ffuf) - Fast web fuzzer
- [arjun](https://github.com/s0md3v/Arjun) - HTTP parameter discovery
- [gowitness](https://github.com/sensepost/gowitness) - Web screenshot utility

All tools are automatically installed by the `install.sh` script.

## 🎯 Use Cases

### Penetration Testing
- **Reconnaissance Phase**: Automate the initial information gathering
- **Asset Discovery**: Find all attack surfaces quickly
- **Report Generation**: Professional documentation for clients

### Bug Bounty Hunting
- **Scope Mapping**: Comprehensive target enumeration
- **Continuous Monitoring**: Regular scans for new assets
- **Efficient Workflow**: Focus time on exploitation, not enumeration

### Red Team Operations
- **OSINT Collection**: Gather intelligence on target organizations
- **Attack Surface Analysis**: Identify potential entry points
- **Operational Security**: Organized, repeatable methodologies

## 🛡️ Security & Legal Considerations

**⚠️ IMPORTANT: Use AutoScope responsibly and legally**

- **Authorization Required**: Only scan domains, IPs, and systems you own or have explicit written permission to test
- **Respect Rate Limits**: The framework includes reasonable delays, but monitor your scanning behavior
- **Follow Responsible Disclosure**: Report vulnerabilities through proper channels
- **Compliance**: Ensure your use complies with local laws and regulations

### Safe Testing Targets
For learning and testing AutoScope:
- `example.com` - Safe domain for testing
- `httpbin.org` - HTTP service testing
- Your own infrastructure and domains

## 🤝 Contributing

We welcome contributions to improve AutoScope! Here's how you can help:

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed error messages and system information
- Include steps to reproduce the problem

### Feature Requests
- Suggest new reconnaissance modules
- Propose CLI improvements
- Request additional tool integrations

### Development
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add your enhancements
5. Submit a pull request

### Adding New Modules
AutoScope's modular design makes it easy to add new reconnaissance techniques:

## 📊 Performance

### Benchmark Results
Based on testing against medium-sized targets (500-1000 subdomains):

| Scan Type | Duration | Memory Usage | Output Files |
|-----------|----------|-------------|--------------|
| Fast | 2-5 minutes | 200-500 MB | 5-7 files |
| Deep | 10-30 minutes | 500MB-1GB | 7-10 files |

Performance varies based on:
- Target size and complexity
- Network conditions
- System resources
- Selected modules

## 🐛 Troubleshooting

### Common Issues

**Tools not found in PATH**

