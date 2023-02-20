# Bash script to uninstall the netwhereis daemon from the system

SCRIPT_FILENAME="netwhereisd.py"
SCRIPT_INSTALL_DIR="/usr/bin/netwhereisd"
SERVICE_FILENAME="netwhereisd.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_FILENAME"

# Stop service

sudo systemctl stop netwhereisd.service

# Remove service file

sudo rm "$SERVICE_PATH"

# Remove script from /usr/bin

sudo rm -r "$SCRIPT_INSTALL_DIR"

# Reload systemctl daemons

sudo systemctl daemon-reload
