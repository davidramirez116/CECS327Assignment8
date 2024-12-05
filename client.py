import socket

def client():
    # List of valid queries (as well as exit command)
    queries = [
        "What is the average moisture inside my kitchen fridge in the past three hours?",
        "What is the average water consumption per cycle in my smart dishwasher?",
        "Which device consumed more electricity among my three IoT devices?", "exit"]
    
    server_ip = input("Please input Server IP: ")
    try: 
        server_port = int(input("Please input Server Port: "))
    except ValueError:
        print("Please input a valid port number.")
        return
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    
    while True:
        valid_q = False
        choice = int(input("Select query: \n1. What is the average moisture inside my kitchen fridge in the past three hours?\n2. What is the average water consumption per cycle in my smart dishwasher?\n3. Which device consumed more electricity among my three IoT devices?\n4. Exit\n"))

        if type(choice) is not int or choice < 1 or choice > 4:
            print("Invalid input, please select menu option.")
        else:
            valid_q = True
        # Only send query if it is valid
        if valid_q:
            query = queries[choice - 1]
            try:
                # send message to server
                client.send(query.encode())

                # receive message from server
                data = client.recv(1024)
                print("Server response: \n", data.decode())
            except socket.error as e:
                print("Error: ", e)
            if query.lower() == "exit":
                client.close()
                exit()

if __name__ == "__main__":
    client()