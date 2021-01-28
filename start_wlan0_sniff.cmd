plink.exe -batch -ssh -pw kali kali@192.168.178.25 "sudo airmon-ng check kill"
plink.exe -batch -ssh -pw kali kali@192.168.178.25 "sudo airmon-ng start wlan0 channel 1"
plink.exe -batch -ssh -pw kali kali@192.168.178.25 "tcpdump -ni wlan0mon -s 0 -w - not port 22" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i -


	