#!/bin/bash

# Update and upgrade the system
echo "Updating and upgrading the system packages..."
sudo apt update
sudo apt upgrade -y

# Install necessary packages
echo "Installing necessary packages..."
sudo apt install git mc xorg xterm scrot python3 feh mpv -y

# Pulling app from git
echo "Pulling app from git"
git clone https://github.com/rstrmensky/rpitv-player.git

# Change user login to X
sudo sed -i 's/^allowed_users=.*/allowed_users=anybody/' "/etc/X11/Xwrapper.config"
sudo sh -c 'echo "needs_root_rights=yes" >> /etc/X11/Xwrapper.config'

# Add user to proper group to run X
sudo /sbin/usermod -aG video pi
sudo /sbin/usermod -aG tty pi

# Create systemd service file
sudo bash -c 'cat > /etc/systemd/system/x11.service <<EOF
[Unit]
Description=StartX Server
After=getty@tty1.service

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/startx
WorkingDirectory=/home/pi
Restart=always

[Install]
WantedBy=getty.target
EOF'

# Create systemd service file
sudo bash -c 'cat > /etc/systemd/system/rpitv.service <<EOF
[Unit]
Description=RPiTV Service
After=network.target x11.service

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/rpitv-player/app.py
WorkingDirectory=/home/pi/rpitv-player/
Environment="DISPLAY=:0"
StandardOutput=append:/var/log/rpitv-service.log
StandardError=append:/var/log/rpitv-service.log
Restart=always

[Install]
WantedBy=getty.target
EOF'

# Disable screensaving
sudo bash -c 'cat > /etc/X11/xorg.conf <<EOF
Section "ServerFlags"
    Option "BlankTime" "0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime" "0"
EndSection
EOF'

# Set Xinit configuration
sudo bash -c 'cat > /home/pi/.xinitrc <<EOF
# .xinitrc

# Set environment variables
export DISPLAY=:0

# Start background processes
xsetroot -solid black &

# Run a specific application, e.g., xterm
exec xterm -bg black
EOF'

# Reload systemd to apply the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling services..."
sudo systemctl enable x11.service
sudo systemctl enable rpitv.service

# Wait for key press and then reboot
echo "Installation complete. Press any key to reboot..."
echo "Don't forget to update app.ini file in conf folder to set api data."
read -p " "
sudo reboot