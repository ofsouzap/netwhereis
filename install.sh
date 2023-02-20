# Bash script to install the netwhereis daemon on the system and set it to run on startup using systemd

SCRIPT_FILENAME="netwhereisd.py"
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

# Copy daemon script to run location

echo "Copying script into /usr/bin..."

sudo cp "$SCRIPT_FILENAME" "/usr/bin"

# Write service file in systemd directory

echo "Writing service description..."

sudo tee "$SERVICE_PATH" > /dev/null <<EOS
[Unit]
Description=netwhereis daemon
After=network.target
StartLimitIntervalSec=10

[Service]
User=$install_user
WorkingDirectory=/usr/bin
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
