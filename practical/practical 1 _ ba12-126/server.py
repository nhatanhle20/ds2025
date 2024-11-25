import socket

def start_server():
    server_ip = '0.0.0.0'  # Listen on all available interfaces
    server_port = 33333    # Port to listen on

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))  # Bind to the specified IP and port
    server_socket.listen(1)  # Allow one client connection at a time
    print(f"Server is listening on {server_ip}:{server_port}...")

    # Accept a connection from the client
    conn, addr = server_socket.accept()
    print(f"Connection accepted from {addr}")

    # Receive the filename from the client
    filename = conn.recv(1024).decode()
    print(f"Receiving file: {filename}")

    # Receive the file content and save it
    with open(filename, 'wb') as file:
        while True:
            data = conn.recv(1024)  # Receive data in chunks
            if not data:
                break
            file.write(data)

    print(f"File {filename} received successfully.")
    conn.close()  # Close the connection
    server_socket.close()  # Close the server socket

if __name__ == "__main__":
    start_server()
