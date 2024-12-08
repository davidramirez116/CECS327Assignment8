# CECS327Assignment8
End-to-End IoT System

Uses TCP Server and TCP Client files published in Google Cloud to query MongoDB Database containing sensor data and metadata from Dataniz.

Usage Instructions:

TCP Client: 
To run the client file: run on the command line: client.py
Upon running, the user will be prompted to enter the server IP address and port number to connect to the server.
Once connected to the server, the user is given a menu of 3 possible queries to choose from, as well as an exit option. Once the query is selected, the query is sent from the server to the database, and the response is then sent to the client.

TCP Server:
To run the server file, run on the command line: server.py
Upon running, the user is prompted to enter the server IP address and port number to connect to the server.
Once set, the server begins to listen for a connection from a client. When the server receives queries from the server, it queries the data from the database then sends the response.

Database:
The MongoDB Database contains the data from the devices under the virtual tab, which we load into our server file using our database link. We load the data in as a collection, which allows us to then run Pymongo queries such as find and filtering, allowing us to efficiently query the collection.
