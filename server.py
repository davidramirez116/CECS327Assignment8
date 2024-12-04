import socket
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ryangallagher01:FtTgpOQcUsDo01o7@cluster0.7mcrx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['test']
collection = db['IOT Devices_virtual']  # Replace with your collection name


def averageMoisture():
    cursor = collection.find({},{"payload.Moisture Meter - Fridge Moisture Meter"})
    moistureVals = []

    for obj in cursor:
        try:
            value = float(obj["payload"]["Moisture Meter - Fridge Moisture Meter"])
            moistureVals.append(value)
        except (KeyError, ValueError):
            continue

    if moistureVals:
        avg = sum(moistureVals)/len(moistureVals)
        print(f"Average Moisture Levels: {avg:.4f}")
    else:
        print("Error, no moisture values")

def averageWaterConsumption():
    cursor = collection.find({}, {"payload.Water Consumption Sensor"})
    consumptionVals = []

    for obj in cursor:
        try:
            value = float(obj["payload"]["Water Consumption Sensor"])
            consumptionVals.append(value)
        except (KeyError, ValueError):
            continue

    if consumptionVals:
        avg = sum(consumptionVals)/len(consumptionVals)
        print(f"Average Water Consumption: {avg:.4f}")
    else:
        print("Error, no consumption values")

def electricityConsumption():
    max_value = float('-inf')
    max_device = None

    # Iterate through all documents in the collection
    cursor = collection.find({})
    for document in cursor:
        payload = document.get("payload", {})
        for key, value in payload.items():
            if "Ammeter" in key:  # Check if the field name contains 'Ammeter'
                try:
                    ammeter_value = float(value)  # Convert to float for comparison
                    if ammeter_value > max_value:
                        max_value = ammeter_value
                        if payload.get("board_name") == "Raspberry Pi 4 - Raspberry Pi 4 - DISHWASHER":
                            device = "Dishwasher"
                        elif payload.get("board_name") == "Raspberry Pi 4 - Raspberry Pi 4 - FRIDGE":
                            device = "Fridge 1"
                        else:
                            device = "Fridge 2"
                        max_device = {
                            "device_name": device,
                            "ammeter_value": ammeter_value
                        }
                except ValueError:
                    continue  # Skip invalid numeric values

    # Output the device with the highest Ammeter value
    if max_device:
        print("Device with the highest Ammeter value:")
        print(f"Device Name: {max_device['device_name']}")
        print(f"Ammeter Value: {max_device['ammeter_value']}")
    else:
        print("No valid Ammeter values found.")

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
            if data == "1":
                averageMoisture()
            elif data == "2":
                averageWaterConsumption()
            elif data == "3":
                electricityConsumption()
            else:
                print("Sorry, this query cannot be processed.")

        except socket.error as e:
            print("Error: ", e)
            break

    incoming_socket.close()

if __name__ == "__main__":
    averageMoisture()
    averageWaterConsumption()
    electricityConsumption()

