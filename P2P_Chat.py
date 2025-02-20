import socket, threading, json, time

active_peers = []
known_peers = set()
connected_peers = set()
peer_names = {}
lock = threading.Lock()
mandatory_peers = [('10.206.5.228', 6555)]

def listen(port, name):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"\nServer listening on port {port}\n")
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=receive_message, args=(client_socket, addr, name)).start()

def receive_message(client_socket, addr, name):
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return
        message = json.loads(data)
        sender_ip = addr[0]
        sender_port = message['sender_port']
        sender_name = message.get('sender_name', 'Unknown')
        content = message['content']
        with lock:
            peer_names[(sender_ip, sender_port)] = sender_name
            if content.lower() == 'exit':
                if (sender_ip, sender_port) in active_peers:
                    active_peers.remove((sender_ip, sender_port))
                known_peers.discard((sender_ip, sender_port))
                connected_peers.discard((sender_ip, sender_port))
            else:
                if (sender_ip, sender_port) not in active_peers:
                    active_peers.append((sender_ip, sender_port))
                    print(f"\n\nNew peer found: {sender_name} [{sender_ip}:{sender_port}]")
                known_peers.add((sender_ip, sender_port))
        if content.lower() == 'exit':
            print(f"\n{sender_name} [{sender_ip}:{sender_port}] disconnected\n")
        elif content.lower() == 'connect':
            print(f"\n{sender_name} [{sender_ip}:{sender_port}] connected with you\n")
        else:
            print(f"\nMessage from {sender_name} [{sender_ip}:{sender_port}]: {content}\n")
    finally:
        client_socket.close()

def send_message(ip, port, sender_name, sender_port, message):
    with lock:
        remote_name = peer_names.get((ip, port), "Unknown")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(20)
            s.connect((ip, port))
            data = json.dumps({
                'type': 'message',
                'sender_name': sender_name,
                'sender_port': sender_port,
                'content': message
            })
            s.send(data.encode())
        with lock:
            if message.lower() == 'exit':
                known_peers.discard((ip, port))
                connected_peers.discard((ip, port))
                if (ip, port) in active_peers:
                    active_peers.remove((ip, port))
            else:
                if (ip, port) not in known_peers:
                    known_peers.add((ip, port))
            remote_name = peer_names.get((ip, port), "Unknown")
        if message.lower() == 'connect':
            print(f"Successfully connected to {remote_name} [{ip}:{port}]")
        elif message.lower() == 'exit':
            print(f"Disconnected from {remote_name} [{ip}:{port}]")
        else:
            print(f"Message sent to {remote_name} [{ip}:{port}]:",message)
        return True
    except:
        print(f"Failed to contact {remote_name} [{ip}:{port}]")
        return False

def connect(ip, port_peer, sender_name, sender_port):
    success = send_message(ip, port_peer, sender_name, sender_port, "connect")
    if success:
        with lock:
            connected_peers.add((ip, port_peer))

def main():
    name = input("Enter your name: ")
    port = int(input("Enter your port number: "))
    server = threading.Thread(target=listen, args=(port, name), daemon=True)
    server.start()
    time.sleep(0.2)
    with lock:
        peer_names[('10.206.5.228', 6555)] = "Ma'am"
    mandatory_threads = []
    for ip, peer_port in mandatory_peers:
        t = threading.Thread(target=send_message, args=(ip, peer_port, name, port, f"Hello!"))
        t.start()
        mandatory_threads.append(t)
    for t in mandatory_threads:
        t.join()
    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            ip = input("\nEnter recipient's IP address: ")
            port_peer = int(input("Enter recipient's port number: "))
            message = input("Enter your message (type exit to disconnect): ")
            print()
            t = threading.Thread(target=send_message, args=(ip, port_peer, name, port, message))
            t.start()
            t.join()
        elif choice == '2':
            with lock:
                known_peers_list = list(known_peers)
                current_connected = connected_peers.copy()
            if known_peers_list:
                print("\nActive Peers:")
                for i, (peer_ip, peer_port) in enumerate(known_peers_list, 1):
                    with lock:
                        peer_name = peer_names.get((peer_ip, peer_port), "Unknown")
                    status = "Connected" if (peer_ip, peer_port) in current_connected else "Yet to connect"
                    print(f"{i}. {peer_name} [{peer_ip}:{peer_port}] - {status}")
            else:
                print("\nNo active peers.")
        elif choice == '3':
            with lock:
                peers_to_connect = [peer for peer in known_peers if peer not in connected_peers]
            if not peers_to_connect:
                print("\nNo peers remaining for connection.")
                continue
            print(" \nActive Peers remaining for connection: \n")
            for idx, (peer_ip, peer_port) in enumerate(peers_to_connect, 1):
                with lock:
                    peer_name = peer_names.get((peer_ip, peer_port), "Unknown")
                print(f"{idx}. {peer_name} [{peer_ip}:{peer_port}]")
            selection = input("\nEnter the index of the peer to connect to (Enter 0 to connect to all): ").strip()
            print()
            try:
                selection = int(selection)
            except ValueError:
                print("Invalid input")
                continue
            threads = []
            if selection == 0:
                for peer in peers_to_connect:
                    peer_ip, peer_port = peer
                    t = threading.Thread(target=connect, args=(peer_ip, peer_port, name, port))
                    t.start()
                    threads.append(t)
            else:
                if selection < 1 or selection > len(peers_to_connect):
                    print("Invalid input")
                    continue
                peer_ip, peer_port = peers_to_connect[selection - 1]
                t = threading.Thread(target=connect, args=(peer_ip, peer_port, name, port))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            print()
        elif choice == '0':
            with lock:
                peers_to_exit = list(known_peers)
            for peer_ip, peer_port in peers_to_exit:
                send_message(peer_ip, peer_port, name, port, "exit")
            with lock:
                known_peers.clear()
                connected_peers.clear()
                active_peers.clear()
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()