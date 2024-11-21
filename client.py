import socket

def client():
    
    server_ip = input("Please input Server IP: ")
    try: 
        server_port = int(input("Please input Server Port: "))
    except ValueError:
        print("Please input a valid port number.")
        return
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    
    while True:
        message = input("Enter message to send ('exit' to leave): ")

        try:
            # send message to server
            client.send(message.encode())

            # receive message from server
            data = client.recv(1024)
            print("Server response: ", data.decode())
        except socket.error as e:
            print("Error: ", e)
        if message.lower() == "exit":
            client.close()
            exit()

if __name__ == "__main__":
    client()