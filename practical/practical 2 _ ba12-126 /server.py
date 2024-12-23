from xmlrpc.server import SimpleXMLRPCServer
import base64


def receive_file(filename, filedata):
    # Decode the file data
    file_bytes = base64.b64decode(filedata)
    with open(filename, 'wb') as file:
        file.write(file_bytes)
    print(f"File {filename} received successfully.")
    return f"File {filename} received successfully."


if __name__ == "__main__":
    server_ip = "0.0.0.0"
    server_port = 8000
    server = SimpleXMLRPCServer((server_ip, server_port))
    print(f"Server is listening on {server_ip}:{server_port}...")

    server.register_function(receive_file, "receive_file")
    server.serve_forever()
