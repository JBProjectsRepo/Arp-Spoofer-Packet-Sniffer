# Arp-Spoofer and Packet-Sniffer
#### This script was developed with python 3 and uses Scapy packet manipulation library in order to spoof two victims MAC address and sniff all the communication between them. 

### After running the script, you will be presented with two options:
## 1- You will be able to sniff on the communication between two hosts and save the exchanged packets, but you won't be able to modify them
## 2- Custom Payload: you will be able to specify a function that receives a Scapy Packet as a parameter and modify it as you wish
## OBS: Some examples for option two are listed under "payloads" folder

## USAGE

### python main.py "x.x.x.x" "y.y.y.y"
#### where x.x.x.x and y.y.y.y are the IPs from two hosts in your network that you want to sniff
### You may also run the script with an option to output a .pcap file with the captured packets:
#### python "x.x.x.x" "y.y.y.y" "pcap"
#### If "pcap" is not specified in the arguments, the capture won't be saved
#### Captured packets will be saved on a folder called packet_captures

### OBS: To sniff traffic between a victim in your network and the internet, one of the IPs in the parameters should be the gateway of your network