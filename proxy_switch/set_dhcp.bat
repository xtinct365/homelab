@echo off
netsh interface ip set address "Ethernet" dhcp
netsh interface ip set dns "Ethernet" dhcp
echo IP and DNS have been set to DHCP.
