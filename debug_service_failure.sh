#!/bin/bash
# Debug Service Failure
# This script will help debug why the service is failing

set -e

echo "🔍 Debugging LED Board Service Failure"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER=$(whoami)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Current user: $CURRENT_USER"

# Check service logs
echo ""
echo "📄 Service logs (last 20 lines):"
sudo journalctl -u led-board --no-pager -n 20

echo ""
echo "📄 Service logs (last 50 lines):"
sudo journalctl -u led-board --no-pager -n 50

# Test the command manually
echo ""
echo "🧪 Testing the command manually..."

# Check if venv python exists
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    print_info "Testing with venv Python: $VENV_PYTHON"
    echo "Running: $VENV_PYTHON $PROJECT_DIR/main.py"
    echo "---"
    $VENV_PYTHON "$PROJECT_DIR/main.py" || print_warning "Command failed with venv Python"
else
    print_warning "venv Python not found, testing with system Python"
    SYSTEM_PYTHON=$(which python3)
    print_info "Testing with system Python: $SYSTEM_PYTHON"
    echo "Running: $SYSTEM_PYTHON $PROJECT_DIR/main.py"
    echo "---"
    $SYSTEM_PYTHON "$PROJECT_DIR/main.py" || print_warning "Command failed with system Python"
fi

echo ""
echo "🔍 Checking file permissions..."
ls -la "$PROJECT_DIR/main.py"
ls -la "$PROJECT_DIR/venv/bin/python" 2>/dev/null || print_warning "venv Python not found"

echo ""
echo "🔍 Checking Python dependencies..."
echo "Testing Python import:"
$VENV_PYTHON -c "import sys; print('Python path:', sys.path)" 2>/dev/null || print_warning "Python import test failed"

echo ""
echo "🔍 Checking if main.py has proper shebang..."
head -1 "$PROJECT_DIR/main.py"

echo ""
echo "="*60
echo -e "${YELLOW}🔧 Debugging complete. Check the output above for errors.${NC}"
echo -e "${BLUE}Common issues:${NC}"
echo "• Missing dependencies in virtual environment"
echo "• Import errors in main.py"
echo "• Permission issues"
echo "• GPIO access problems"
echo "• Missing hardware libraries"
echo "="*60
