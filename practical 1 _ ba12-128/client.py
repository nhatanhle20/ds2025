import socket

def send_file(server_ip, server_port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))  # Connect to the server

    # Send the filename to the server
    client_socket.send(filename.encode())

    # Send the file content
    with open(filename, 'rb') as file:
        while (data := file.read(1024)):  # Read the file in chunks
            client_socket.send(data)

    print(f"File {filename} sent successfully.")
    client_socket.close()  # Close the client socket

if __name__ == "__main__":
    
    server_ip = '192.168.162.60'  # Server's IP address
    server_port = 33333           # Server's port
    filename = 'example.txt'      # File to send

    send_file(server_ip, server_port, filename)
