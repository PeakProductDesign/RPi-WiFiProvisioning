# RPi-WiFiProvisioning by Bluetooth Serial terminal

This application is tested in Raspberry Pi 4B using raspbian buster

# Step1 : Install bluetooth packages for python application and download github app

sudo apt-get install bluetooth bluez python-bluez

git clone ....

chmod 755 -R ./RPi-WiFiProvisioning

# Step2 Raspberry pi Bluetooth configuration
- Setup the SPP(Serial port profile)

sudo nano /etc/systemd/system/dbus-org.bluez.service

...

ExecStart=/usr/lib/bluetooth/bluetoothd -C \
ExecStartPost=/usr/bin/sdptool add SP

...

sudo reboot

- Add the followings in /etc/rc.local before "exit 0"

sudo bluetoothctl <<EOF \
power on \
discoverable on \
pairable on \
default-agent \
agent NoInputNoOutput \
EOF \
sudo hciconfig hci0 sspmode 0 \
bash /home/{username, ex:pi}/RPi-WiFiProvisioning/remove_all_paired_devices.sh

- Set bluetooth discoverable permanently

sudo nano /etc/bluetooth/main.conf

...

DiscoverableTimeout = 0

...

- Copy/Paste Service files to /etc/systemd/system/

sudo cp ./RPi-WiFiProvisioning/simple_agent.service /etc/systemd/system

this is a bluetooth agent service with PIN Code Authentication

sudo cp ./RPi-WiFiProvisioning/rfcomm_server.service /etc/systemd/system 

this is a bluetooth terminal server

sudo systemctl daemon-reload \
sudo systemctl enable simple_agent.service \
sudo systemctl enalbe rfcommn_server.service \

sudo reboot

# Mobile App

- Install the serial bluetooth terminal app on the phone

https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal&hl=en_US&gl=US

- Connect to Raspberry pi

Goto bluetooth setting on the phone \
Scan the devices. You can see "raspberrypi" device. Click the "raspberrypi" \
Input PIN Code: 1234

- Open the Serial Bluetooth Terminal app

Open menu. \
Click Devices. \
Click Bluetooth Classic tag. You can see the "raspberrypi" device connected to phone \
Connect to "raspberrypi device" \
You can send wifi info to raspberrypi. {"ssid":"...","pw":"..."} \
If wifi is configured successfully, the Pi return "OK"
You can send other terminal commands to Raspberry Pi.

