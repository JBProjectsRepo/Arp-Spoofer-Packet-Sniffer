# Spoof DNS Usage
This script basically receives a Scapy Packet object as a parameter and search for DNS data related to the "name" variable specified in the script. Then, it modifies the DNS response coming from the victim's DNS server to associate to it a fake ip (set in the "ip" variable in the script).

### Suggestions for webserver:

- Suggestion #1
  + Edit **server.py** script, located in **https_server** folder
  + Set variable **ip**  to the desired ip
  + (Optional) Edit **index.html** as you wish
  + Run **server.py**

This will start a http and https server on the ip defined in the script (configurations required to respond ipv6 requests are commented in the script).
  
**Note**: In order to generate the server **certificate** and **key** you will need, first, to run the following command:
````
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
````
After that, place the ***cert.pem*** and ***key.pem*** files in the same folder as the script.

- Suggestion #2 Use **setoolkit** to clone a website and start a server:
  + 2.1 - Open a terminal in kali linux
  + 2.2 - Type sudo setoolkit
  + 2.3 - Select option #1 (Social-Engineering Attacks)
  + 2.4 - Select option #2 (Website Attack Vectors)
  + 2.5 - Select option #3 (Credential Harvester Attack Method)
  + 2.6 - Select option #2 (Site Cloner)
  + 2.7 - Type the same ip configured in spoof_dns script
  + 2.8 - Type the same website name you configured in spoof_dns script
  + 2.9 - Get the credentials on the command line.
### TESTING:

A good domain to test the DNS spoof is https://example.com/. Some options for testing are:

- **curl** example.com
- **wget** example.com
- **nslookup** example.com
- **Browsers**: Since browsers behave different between each other and usually enforce security on self-signed certificates, tests here should be done carefully
