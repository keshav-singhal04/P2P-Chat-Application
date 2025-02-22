

# Peer-to-Peer Chat Application
## Team Details

**Team Name**: Synergy

**Team Members**:
- Kartik Hiranandani (230001037)
- Keshav Singhal (230001039)
- Kumar Prince (230008019)

---
## Overview
This repository contains a Python implementation of a peer-to-peer  chat application which enables users to send and receive messages simultaneously, connect with multiple peers, and query active peers.
  
We have assumed <b>fixed port numbers</b> for all users (which they are asked to enter at startup) in order to avoid repeated entries for the same peer. The project has been developed using <b>TCP sockets</b> and a standardized message format to ensure reliable communication between peers. 

Our code also <b>handles the bonus question</b> by allowing users to connect to those active peers with whom connection has not yet been established.

---
![Data flow chart at the user's end](FlowChart.png)
## Implementation Details

### 1. List of Active Peers
The program maintains a dynamic list of active peers (peers that are  online and eligible for connection) at each user’s end. Each peer in this list has a connection status (Connected/ Yet to connect):  
- If the user **receives a message** from a peer not already in the list, then it is added to the list with <i>Yet to connect</i> connection status.  

- If the user successfully **sends a message** to a peer (IP address and port number to be known beforehand) that is not already in the list, then it is added to the list with <i>Yet to connect</i> status if the message is not a connection message, or with <i>Connected</i> status if it is a connection message.

- If the user **sends the message <i>exit</i> to a peer**, then he gets disconnected from that peer. Both users are removed from each other's active peers list.
- If the user **chooses to quit** (terminate his program), the message <i>exit</i> is automatically sent to all peers in his  list to remove him from their active peers lists.  

### 2. Connection Status of Peers
In the active peers list, each active peer has a connection status:  

- **Connected**: If the user has successfully sent a connection message to that peer.  

- **Yet to connect**: If the user has not successfully sent a connection message to that peer yet.  

A message is considered as a connection message  if the message is <i>connect</i>. The program provides a dedicated function to send this connection message to some or all of those active peers which are yet to be connected.  

### 3. Message Notifications
A dedicated listener thread is used to receive messages in real-time, which keeps the user updated by notifying whenever:  

- A new peer is identified (by receiving a message for the first time).  
- A peer connects by sending a connection message.  
- A message is received from an active peer.  
- An active peer disconnects.  

---

## Customizations

### 1. Response Time Limit
The program is based on a synchronous networking model. By default, it assumes a maximum time limit of **15 seconds** for sending a message over the network. This limit can be adjusted in the `settimeout()` method inside the `send_message()` function.  

### 2. Mandatory Peer List
The program initializes a list of already known peers and sends a greeting message to all of them at startup. The contents of the `mandatory_peers` list can be adjusted to include more mandatory peers.  

---
## How To Run ?
1. The program requires you to have Python 3.7.0 or any above version installed on your device.
2. The Python installation directory must be added to the system's `PATH` environment variable.
3. Run the Python file in a code editor like `Visual Studio Code`. In the output terminal, enter your name and a port number (say 8080). If a pop-up asks for firewall access permission, click `Allow` and proceed.
4. In order to run multiple instances in different terminals on your device, open the file in `Visual Studio Code` and for each instance,  press `Ctrl+F5`  to run the code in a new terminal. Make sure to use different port numbers for each terminal. 


5. The menu options can be used to chat with peers:
   - **Send message:** Enter the recipient's IP address and port number and send a message 
   - **Query active peers:** Display the list of active peers showing their details and connection status
   - **Connect to active peers:** Select some or all of the <i>Yet to connect</i> active peers to connect to
   - **Quit:** Disconnect from all active peers and terminate the program
 6. If running the code on different devices, ensure that the devices are on a network without any VPN. There seems to be some issue with the code compatibility on IIT Wi-Fi networks. Hence, using a personal hotspot network is recommended.
---
## Sample Run
```sh
Enter your name (without spaces): Synergy
Enter your port number: 8080

Server listening on port 8080

Message sent to Ma'am [10.206.5.228:6555]: Hello Ma'am!

***** Menu *****
1. Send message
2. Query active peers
3. Connect to active peers
0. Quit
Enter choice: 1

Enter recipient's IP address: 10.18.4.39
Enter recipient's port number: 9090
Enter your message (type exit to disconnect): Let us connect

Message sent to Unknown [10.18.4.39:9090]: Let us connect
```

---
## Acknowledgement  
- Prof. Subhra Mazumdar, for the project idea and concepts of peer-to-peer networks.  
- A helpful documentation of socket programming at [GeeksforGeeks](https://www.geeksforgeeks.org/socket-programming-python/).  
