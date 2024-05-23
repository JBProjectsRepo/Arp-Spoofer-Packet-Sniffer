# Spoof DNS Usage
This script was created to be used after the Arp Spoofing was complete, and you are already sniffing the victims traffic. 
Basically it receives a Scapy packet as a parameter and search for DNS data related to the name variable specified in the script. 
Then, it modifies the DNS response coming from the victim's DNS server to associate a fake ip (set in the ip variable in the 
script) to that name.

### Here are two suggestions to create the webserver:

- ### 1- Run the script server.py located in https_server folder. This will start a http and https server on the ip defined in the script (configurations required to respond ipv6 requests are commented in the script).
  
OBS: First, you will need to run the command "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365" in order to generate the server certificate and key. After that, place the ***cert.pem*** and ***key.pem*** files in this folder.

- ### 2- Use setoolkit to clone a website and start a server:
### For this option you should do the following
#### 2.1 - Open a terminal in kali linux
#### 2.2 - Type sudo setoolkit
#### 2.3 - Select option #1 (Social-Engineering Attacks)
#### 2.4 - Select option #2 (Website Attack Vectors)
#### 2.5 - Select option #3 (Credential Harvester Attack Method)
#### 2.6 - Select option #2 (Site Cloner)
#### 2.7 - Type the same ip configured in spoof_dns script
#### 2.8 - Type the same website name you configured in spoof_dns script
#### 2.9 - Get the credentials on the command line.



