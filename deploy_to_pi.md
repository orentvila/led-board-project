# Deploying to Raspberry Pi

## Method 1: Using SCP (Secure Copy)

From your Windows machine, open PowerShell and run:

```powershell
# Create a deployment package
$deployDir = "pi-deploy"
New-Item -ItemType Directory -Path $deployDir -Force

# Copy only the files needed for Raspberry Pi
Copy-Item -Path "*.py" -Destination $deployDir
Copy-Item -Path "requirements.txt" -Destination $deployDir
Copy-Item -Path "README.md" -Destination $deployDir
Copy-Item -Path "HARDWARE_SETUP.md" -Destination $deployDir
Copy-Item -Path "led-display.service" -Destination $deployDir
Copy-Item -Path "start.sh" -Destination $deployDir

# Copy to Raspberry Pi (replace with your Pi's IP address)
scp -r $deployDir pi@192.168.1.100:/home/pi/led-board-project
```

## Method 2: Using Git

If you have Git set up:

```bash
# On Raspberry Pi
git clone https://github.com/yourusername/led-board-project.git
cd led-board-project
```

## Method 3: Using USB Drive

1. Copy project files to a USB drive
2. Insert USB drive into Raspberry Pi
3. Copy files to Pi's home directory 