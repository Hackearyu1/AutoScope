#!/bin/bash

# AutoScope Installation Script
# Installs dependencies and reconnaissance tools only
# Assumes autoscope.py is already present in current directory

set -e  # Exit on any error

echo "🚀 Starting AutoScope dependency installation..."

# Verify autoscope.py exists in current directory
if [ ! -f "autoscope.py" ]; then
    echo "❌ Error: autoscope.py not found in current directory"
    echo "Please ensure you're running this script from the AutoScope directory"
    echo "Expected files: autoscope.py, install.sh, requirements.txt"
    exit 1
fi

echo "✅ AutoScope files found in current directory"

# Update system packages based on package manager
echo "📦 Updating system packages..."
if command -v apt-get >/dev/null 2>&1; then
    echo "   Detected: Ubuntu/Debian system"
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y build-essential curl wget git python3 python3-pip python3-venv libpcap-dev
elif command -v yum >/dev/null 2>&1; then
    echo "   Detected: RHEL/CentOS system"
    sudo yum update -y
    sudo yum install -y gcc curl wget git python3 python3-pip libpcap-devel
elif command -v brew >/dev/null 2>&1; then
    echo "   Detected: macOS system"
    brew update
    brew install curl wget git python3
elif command -v pacman >/dev/null 2>&1; then
    echo "   Detected: Arch Linux system"
    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm base-devel curl wget git python python-pip
else
    echo "⚠️  Could not detect package manager. Please install these manually:"
    echo "   - build-essential/gcc, curl, wget, git, python3, python3-pip"
fi

# Install Go programming language if not present
if ! command -v go >/dev/null 2>&1; then
    echo "📥 Installing Go programming language..."
    GO_VERSION="1.22.0"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [[ $(uname -m) == "x86_64" ]]; then
            ARCH="amd64"
        elif [[ $(uname -m) == "aarch64" ]]; then
            ARCH="arm64"
        else
            ARCH="386"
        fi
        wget -q "https://golang.org/dl/go${GO_VERSION}.linux-${ARCH}.tar.gz"
        sudo tar -C /usr/local -xzf "go${GO_VERSION}.linux-${ARCH}.tar.gz"
        rm "go${GO_VERSION}.linux-${ARCH}.tar.gz"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if [[ $(uname -m) == "arm64" ]]; then
            ARCH="arm64"
        else
            ARCH="amd64"
        fi
        wget -q "https://golang.org/dl/go${GO_VERSION}.darwin-${ARCH}.tar.gz"
        sudo tar -C /usr/local -xzf "go${GO_VERSION}.darwin-${ARCH}.tar.gz"
        rm "go${GO_VERSION}.darwin-${ARCH}.tar.gz"
    fi
    
    # Add Go to PATH for current session
    export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
    export GOPATH=$HOME/go
    
    # Add Go to PATH permanently
    if ! grep -q "/usr/local/go/bin" ~/.bashrc; then
        echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
        echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    fi
    
    # Also add to .zshrc if it exists (for zsh users)
    if [ -f ~/.zshrc ] && ! grep -q "/usr/local/go/bin" ~/.zshrc; then
        echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.zshrc
        echo 'export GOPATH=$HOME/go' >> ~/.zshrc
    fi
    
    echo "✅ Go ${GO_VERSION} installed successfully"
else
    echo "✅ Go already installed: $(go version)"
    # Ensure Go environment is set for current session
    export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
    export GOPATH=$HOME/go
fi

# Create Go workspace if it doesn't exist
mkdir -p $HOME/go/{bin,src,pkg}

echo "🛠️  Installing reconnaissance tools..."
echo "   This may take a few minutes depending on your internet connection..."

# Install Go-based reconnaissance tools
echo "   📡 Installing subfinder (subdomain enumeration)..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo "   🔍 Installing naabu (port scanner)..."
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest

echo "   🌐 Installing httpx (HTTP toolkit)..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo "   🔨 Installing ffuf (web fuzzer)..."
go install -v github.com/ffuf/ffuf/v2@latest

echo "   📸 Installing gowitness (screenshot tool)..."
go install -v github.com/sensepost/gowitness@latest

echo "   🗺️  Installing amass (advanced subdomain enum)..."
go install -v github.com/owasp-amass/amass/v4/...@master

# Install Python-based tools and dependencies
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "   Installing from requirements.txt..."
    pip3 install --user -r requirements.txt
else
    echo "   Installing basic Python packages..."
    pip3 install --user argparse pathlib pyyaml
fi

echo "   🔍 Installing arjun (parameter discovery)..."
pip3 install --user arjun

# Verify tool installations
echo "🔍 Verifying tool installations..."
tools=("subfinder" "naabu" "httpx" "ffuf" "gowitness" "amass" "arjun")
for tool in "${tools[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "   ✅ $tool: $(command -v $tool)"
    else
        echo "   ⚠️  $tool: Not found in PATH (may need shell restart)"
    fi
done

# Create activation helper script
cat > activate_autoscope.sh << 'EOF'
#!/bin/bash
# AutoScope Environment Activation Helper
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin:$HOME/.local/bin
export GOPATH=$HOME/go

echo "✅ AutoScope environment activated!"
echo "Available tools: subfinder, naabu, httpx, ffuf, gowitness, amass, arjun"
echo ""
echo "🚀 Quick start commands:"
echo "   python3 autoscope.py -t example.com --fast"
echo "   python3 autoscope.py -t target.com --deep"
echo "   python3 autoscope.py -t target.com --only-subdomains"
echo ""
echo "📁 Results will be saved in: output/target_name/"
EOF
chmod +x activate_autoscope.sh

# Final setup and verification
echo ""
echo "🎉 AutoScope installation completed successfully!"
echo ""
echo "📋 Installation Summary:"
echo "   ✅ System packages updated"
echo "   ✅ Go programming language installed/verified"
echo "   ✅ All reconnaissance tools installed"
echo "   ✅ Python dependencies installed"
echo "   ✅ PATH configured for future sessions"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart your terminal OR run: source ~/.bashrc"
echo "   2. Test installation: python3 autoscope.py -t example.com --fast"
echo ""
echo "💡 Quick activation (if tools not found):"
echo "   ./activate_autoscope.sh"
echo ""
echo "⚠️  Important reminders:"
echo "   - Only scan domains you own or have explicit permission to test"
echo "   - Use example.com or httpbin.org for safe testing"
echo "   - Results saved in output/target_name/ directory"
echo ""
echo "✨ Happy reconnaissance!"
