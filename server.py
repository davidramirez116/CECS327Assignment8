import socket
from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('mongodb+srv://ryangallagher01:FtTgpOQcUsDo01o7@cluster0.7mcrx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['test']
main_collection = db['IOT Devices_virtual']
metadata_collection = db['IOT Devices_metadata']

def averageMoisture():
    fridge_uids = metadata_collection.find(
        {
            "customAttributes.type": "DEVICE",
            "customAttributes.name": "Fridge",
            "customAttributes.additionalMetadata.location": "Kitchen"
        })

    # extract uids into list
    fridge_uids = [device["assetUid"] for device in fridge_uids]

    # Calculate the timestamp for 3 hours ago
    three_hours_ago = datetime.now() - timedelta(hours=3)
    three_hours_ago_timestamp = int(three_hours_ago.timestamp())  # Convert to UNIX timestamp

    # Query to find documents from the last 3 hours
    cursor = main_collection.find(
        {"payload.timestamp": {"$gte": str(three_hours_ago_timestamp)},
         "payload.parent_asset_uid": fridge_uids[0]
         },  # Match timestamps >= 3 hours ago
        {"payload.Moisture Meter - Moisture Meter": 1, "payload.timestamp": 1}  # Only fetch relevant fields
    )

    # Calculate the average moisture level
    moisture_values = []

    for document in cursor:
        try:
            value = float(document["payload"]["Moisture Meter - Moisture Meter"])  # Extract and convert moisture values
            moisture_values.append(value)
        except (KeyError, ValueError):
            # Skip documents with missing or invalid values
            continue

    # Compute the average
    if moisture_values:
        average = sum(moisture_values) / len(moisture_values)
        return f"Average Moisture Level (Last 3 Hours): {average:.4f} % wfv"
    else:
        return "No valid moisture level readings found in the last 3 hours."


def averageWaterConsumption():
    cursor = main_collection.find({}, {"payload.Water Consumption Sensor"})
    consumptionVals = []

    for obj in cursor:
        try:
            value = float(obj["payload"]["Water Consumption Sensor"]) 
            consumptionVals.append(value)
        except (KeyError, ValueError):
            continue

    if consumptionVals:
        avg = sum(consumptionVals)/len(consumptionVals) #currently ml/s
        converted_avg = avg / 3786.41 # 1 gal = 3785.41 mls. Cycle has been set to 1 hour in dataniz, no need to multiply by time value
        #converted_avg = avg / 3785.41 * 1800 #converts mL/s to G/Cycle
        return f"Average Water Consumption: {converted_avg:.4f} G/Cycle"
    else:
        return "Error, no consumption values"

def electricityConsumption():
    # map assetUID to device name
    metadata = metadata_collection.find({}, {"assetUid": 1, "customAttributes.name": 1, "_id": 0})
    device_names = {doc["assetUid"]: doc["customAttributes"]["name"] for doc in metadata}

    cursor = main_collection.find(
        {},
        {"payload": 1} #retreive payload of each document
    )

    max = 0
    device_uid = None

    # find max ammeter value, update max and device uid
    for document in cursor:
        payload = document.get("payload",{})
        for key, value in payload.items():
            if "Ammeter" in key:
                try:
                    energy_value = float(value)
                    if energy_value > max:
                        max = energy_value
                        device_uid = payload.get("parent_asset_uid")
                except (ValueError, KeyError):
                    continue

    # Output the device with the highest Ammeter value
    if device_uid and device_uid in device_names:
        max_device = device_names[device_uid]
        maxKWH = max * 120 / 1000 #kw is amps * volts/1000
        return f"Device with the highest Ammeter value: \nDevice Name: {max_device}\nAmmeter Value: {maxKWH} kWh"
    else:
        return "No valid Ammeter values found."

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
            if data == "What is the average moisture inside my kitchen fridge in the past three hours?":
                response = averageMoisture()
                incoming_socket.sendall(response.encode('utf-8'))
            elif data == "What is the average water consumption per cycle in my smart dishwasher?":
                response = averageWaterConsumption()
                incoming_socket.sendall(response.encode('utf-8'))
            elif data == "Which device consumed more electricity among my three IoT devices?":
                response = electricityConsumption()
                incoming_socket.sendall(response.encode('utf-8'))
            elif data == "exit":
                response = "Exiting"
                incoming_socket.sendall(response.encode('utf-8'))
                break
            else:
                print("Sorry, this query cannot be processed.")

        except socket.error as e:
            print("Error: ", e)
            break

    incoming_socket.close()

if __name__ == "__main__":
    #server()
    server()
