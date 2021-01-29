Remote capture on Win10 PC
--------------------------

To create a wireless sniffer trace with a Win10 PC, one could use a suitable USB Wi-Fi key. 
As I did not have such an USB key, I tried another approach, using a Raspberry Pi.

For this, I used a Raspberry Pi 3B+ which has it's own Wi-Fi and Bluetooth radios.

From https://www.offensive-security.com/kali-linux-arm-images/ downloaded 
**64-bit kali-linux-2020.4-rpi4-nexmon-64.img.xz** and installed this image
on a 64 GB SDCard with Raspberry Pi Imager V1.5.

##### Use plink.exe, part of putty suite to start tcpdump on the Raspberry, and start Wireshark on the PC

    plink.exe -ssh -batch -pw PASSWORD USER@IPADDRESS "tcpdump -ni eth0 -s 0 -w - not port 22" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i -

This might show:

tcpdump: eth0: You don't have permission to capture on that device
(socket: Operation not permitted)

##### To grant permission to capture on the Raspberry

1. Add a capture group and add the user (in this case 'USER') to that group:
   
    `sudo groupadd pcap`
   
    `sudo usermod -a -G pcap USER`


2. Next, change the group of tcpdump and set permissions:
   
    `sudo chgrp pcap /usr/sbin/tcpdump`
   
    `sudo chmod 750 /usr/sbin/tcpdump`


3. Finally, use setcap to give tcpdump the necessary permissions:
   
    `sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump`

##### To stop sudo asking for a password for user USER

To prevent sudo asking for a password for user USER I did edit the file /etc/sudoers.d/kali-grant-root so it has the following contents.
(The line USER ALL=(ALL:ALL) NOPASSWD: ALL was added at the end of this file)

	# Allow members of group kali-trusted to execute any command without a
	# password prompt
	%kali-trusted   ALL=(ALL:ALL) NOPASSWD: ALL
	USER ALL=(ALL:ALL) NOPASSWD: ALL

##### Functional commands to start the capture

	plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "sudo airmon-ng check kill"
	plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "sudo airmon-ng start wlan0"
	plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "tcpdump -ni wlan0mon -s 0 -w - not port 22" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i -

#### Channel hopping

To hop over 2.4 GHz channels instead of just observing one specific channel, the following python script can be run on the Raspberry in the background:

**channel_hop.py**

    import os
    import time
    
    # channel_list = [1,2,3,4,5,6,7,8,9,10,11]
    channel_list = [1,6,11]
    wait = 5
    
    while True:
        for channel in channel_list:
           cmd = 'sudo iw dev wlan0mon set channel %d' % channel
           print(cmd)
           os.system(cmd)
           time.sleep(wait)

