# Bash script to install the netwhereis daemon on the system and set it to run on startup using systemd

SCRIPTS_FILENAMES="netwhereisd.py config.py network.py"
SCRIPT_INSTALL_DIR="/usr/bin/netwhereisd"
SERVICE_FILENAME="netwhereisd.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_FILENAME"

# Get username input

echo "User to run daemon as (default $USER):"
read install_user

# Default to running user if none provided

if [ -z "$install_user" ]
then
    install_user=$USER
fi

# Check user exists

id -u "$install_user" > /dev/null

if (( $? == 1 ))
then
    echo "User $install_user doesn't exist"
    exit 1
fi

# Copy daemon scripts to run location

echo "Copying scripts into $SCRIPT_INSTALL_DIR..."

sudo mkdir "$SCRIPT_INSTALL_DIR"

for script in $SCRIPTS_FILENAMES
do
    sudo cp "$script" "$SCRIPT_INSTALL_DIR"
done

# Write service file in systemd directory

echo "Writing service description..."

sudo tee "$SERVICE_PATH" > /dev/null <<EOS
[Unit]
Description=netwhereis daemon
After=network.target
StartLimitIntervalSec=10

[Service]
User=$install_user
WorkingDirectory=$SCRIPT_INSTALL_DIR
ExecStart=/usr/bin/env python3 netwhereisd.py
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
EOS

# Reload systemctl daemons

sudo systemctl daemon-reload

# Enable service for running on start-up

echo "Enabling service for start-up..."

systemctl enable "$SERVICE_FILENAME"

# Start the service now

echo "Starting service..."

systemctl start "$SERVICE_FILENAME"

# End

echo "Done!"
