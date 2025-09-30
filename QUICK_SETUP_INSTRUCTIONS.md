# Quick LED Board Boot Setup

## 🚀 One-Command Setup

Copy this script to your Raspberry Pi and run it:

```bash
# On your Raspberry Pi, in your project directory:
chmod +x auto_setup_boot.sh
./auto_setup_boot.sh
```

## What This Script Does Automatically:

1. ✅ **Checks requirements** (virtual environment, files, permissions)
2. ✅ **Creates systemd service** for `main_animation_controller.py` (or `main.py` if not found)
3. ✅ **Configures auto-start** on boot
4. ✅ **Starts the service** immediately
5. ✅ **Shows status** and logs
6. ✅ **Provides management commands**

## The Script Will:

- Look for `main_animation_controller.py` first, then fall back to `main.py`
- Create `/etc/systemd/system/led-board.service`
- Enable the service for boot startup
- Start the service right away
- Show you the status and recent logs

## After Running:

Your LED board will start automatically every time the Pi boots!

## Management Commands:

```bash
# Check if running
sudo systemctl status led-board

# View live logs
sudo journalctl -u led-board -f

# Restart if needed
sudo systemctl restart led-board

# Stop the service
sudo systemctl stop led-board
```

## That's It! 

Just run `./auto_setup_boot.sh` on your Raspberry Pi and everything will be configured automatically.
