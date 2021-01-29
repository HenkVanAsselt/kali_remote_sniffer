plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "sudo airmon-ng check kill"
plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "sudo airmon-ng start wlan0"
plink.exe -batch -ssh -pw PASSWORD USER@IPADDRESS "tcpdump -ni wlan0mon -s 0 -w - not port 22" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i -


	