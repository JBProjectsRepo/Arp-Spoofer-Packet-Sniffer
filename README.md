# Arp-Spoofer and Packet-Sniffer
 This script was developed with python 3 and uses Scapy packet manipulation library in order to spoof two victims MAC address and sniff all the communication between them. 

### After running the script, you will be presented with two options:
- OPTION 1 (No Payload)# You will be able to sniff on the communication between two hosts and save the exchanged packets, but you won't be able to modify them
2. OPTION 2 (Custom Payload)# You will be able to specify a function that receives a Scapy Packet as a parameter and modify it as you wish

**Note**: Some examples for option #2 are listed under "payloads" folder

## USAGE
````
sudo python main.py x y
````

Where x and y are IPs from two hosts in your network which you want to sniff on communications
### You may also run the script with an option to output a .pcap file with the captured packets:
````
- sudo python x y pcap
````

#### Note:
+ If "pcap" is not specified in the arguments, the capture won't be saved
+ Captured packets will be saved on a folder called packet_captures
+ To sniff traffic between a victim in your network and the internet, one of the IPs in the arguments should be the gateway of your network
