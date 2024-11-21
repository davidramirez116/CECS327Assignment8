import socket

def server():
    server_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Please input Server IP: ")
    server_port = int(input("Please input Server Port: "))
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    incoming_socket, incoming_address = server_socket.accept()

    while True:
        try:
            data = incoming_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received message: ", data)
            response = "Message received: " + data.upper()
            incoming_socket.sendall(response.encode('utf-8'))
        except socket.error as e:
            print("Error: ", e)
            break

    incoming_socket.close()

if __name__ == "__main__":
    server()