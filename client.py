import socket

def client():
    # List of valid queries (as well as exit command)
    valid_queries = [
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
        query = input("Enter query: (type 'exit' to quit)\n")

        if query not in valid_queries:
            print("Sorry, this query cannot be processed. Please try one of the following:\n", valid_queries)
        else:
            valid_q = True
        # Only send query if it is valid
        if valid_q:
            try:
                # send message to server
                client.send(query.encode())

                # receive message from server
                data = client.recv(1024)
                print("Server response: ", data.decode())
            except socket.error as e:
                print("Error: ", e)
            if query.lower() == "exit":
                client.close()
                exit()

if __name__ == "__main__":
    client()