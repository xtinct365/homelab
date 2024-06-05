@echo off
netsh interface ip set address "Ethernet" static 10.16.100.50 255.255.255.0 10.16.100.1
netsh interface ip set dns "Ethernet" static 10.16.100.1
echo IP and DNS have been set to static.
