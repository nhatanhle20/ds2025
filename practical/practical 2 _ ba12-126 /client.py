import xmlrpc.client
import base64

def send_file(server_url, filename):
    with open(filename, 'rb') as file:
        file_bytes = file.read()
        file_data = base64.b64encode(file_bytes).decode('utf-8')

    server = xmlrpc.client.ServerProxy(server_url)
    response = server.receive_file(filename, file_data)
    print(response)

if __name__ == "__main__":
    server_url = "http://192.168.1.20:8000/"
    filename = "example.txt"
    send_file(server_url, filename)
