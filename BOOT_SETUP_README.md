# LED Board Boot Configuration

This guide helps you configure your LED board project to run automatically on boot using systemd.

## Quick Setup

### Option 1: Using the Python Script (Recommended)
```bash
# Make the script executable
chmod +x configure_boot.py

# Run the configuration script
python3 configure_boot.py

# If you have a different main file name, specify it:
python3 configure_boot.py main_animation_controller.py
```

### Option 2: Using the Shell Script
```bash
# Make the script executable
chmod +x setup_boot_service.sh

# Run the setup script
sudo ./setup_boot_service.sh
```

## What These Scripts Do

1. **Create a systemd service file** at `/etc/systemd/system/led-board.service`
2. **Configure the service** to run your LED board project automatically
3. **Enable the service** to start on boot
4. **Start the service** immediately
5. **Set up proper permissions** and security settings

## Service Configuration

The service will:
- Run as your user account (not root)
- Start after network is available
- Restart automatically if it crashes
- Log output to systemd journal
- Start automatically on boot

## Managing the Service

### Check Status
```bash
sudo systemctl status led-board
```

### View Logs
```bash
# View recent logs
sudo journalctl -u led-board

# Follow logs in real-time
sudo journalctl -u led-board -f
```

### Control the Service
```bash
# Stop the service
sudo systemctl stop led-board

# Start the service
sudo systemctl start led-board

# Restart the service
sudo systemctl restart led-board

# Disable auto-start on boot
sudo systemctl disable led-board

# Re-enable auto-start on boot
sudo systemctl enable led-board
```

## Troubleshooting

### Service Won't Start
1. Check the logs: `sudo journalctl -u led-board -f`
2. Verify your virtual environment exists: `ls venv/bin/python`
3. Test running manually: `./venv/bin/python main.py`

### Permission Issues
1. Make sure you're running as the correct user
2. Check file permissions: `ls -la main.py`
3. Ensure the project directory is accessible

### LED Hardware Issues
1. Check if the service is running: `sudo systemctl status led-board`
2. Verify GPIO permissions: `groups $USER`
3. Test hardware manually first

## Testing the Configuration

### Test 1: Manual Start
```bash
# Stop the service
sudo systemctl stop led-board

# Start manually to test
./venv/bin/python main.py
```

### Test 2: Service Restart
```bash
# Restart the service
sudo systemctl restart led-board

# Check if it's running
sudo systemctl status led-board
```

### Test 3: Boot Test
```bash
# Reboot the system
sudo reboot

# After reboot, check if service started automatically
sudo systemctl status led-board
```

## File Locations

- **Service file**: `/etc/systemd/system/led-board.service`
- **Project directory**: Your current project folder
- **Logs**: Available via `journalctl -u led-board`

## Security Notes

The service is configured with security restrictions:
- Runs as non-root user
- Limited file system access
- No new privileges
- Protected system directories

## Uninstalling

To remove the boot configuration:

```bash
# Stop and disable the service
sudo systemctl stop led-board
sudo systemctl disable led-board

# Remove the service file
sudo rm /etc/systemd/system/led-board.service

# Reload systemd
sudo systemctl daemon-reload
```

## Support

If you encounter issues:
1. Check the service logs: `sudo journalctl -u led-board -f`
2. Verify your project runs manually: `./venv/bin/python main.py`
3. Check systemd status: `sudo systemctl status led-board`
4. Ensure all dependencies are installed in your virtual environment
