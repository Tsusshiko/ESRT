import paho.mqtt.client as mqtt
import mysql.connector
import re

# MQTT Broker Configuration
#BROKER = "localhost"  # Mosquitto encontra-se nos proprios subscribers
BROKER = "broker.hivemq.com"
PORT = 1883           # MQTT port (default is 1883)
TOPIC = "parking"  # Topic to subscribe to

# MySQL Database Configuration
DB_CONFIG = {
    "host": "10.0.0.3",
    #host : 10.0.0.11" Para a DatabaseWebserver-2 (Replicação de DatabaseWebserver-1)
    "auth_plugin": "mysql_native_password",
    "user": "root",
    "passwd": "lol",
    "database": "teste"
}


# Connect to the MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        print("Connected to the MySQL database successfully!")
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Insert or update parking spot information
def update_parking_spot(db, spot_id, status):
    try:
        cursor = db.cursor()
        # SQL command to insert or update
        sql = """
        INSERT INTO parking_spots (spot_id, status, last_update)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON DUPLICATE KEY UPDATE
        status = VALUES(status), last_update = CURRENT_TIMESTAMP;
        """
        cursor.execute(sql, (spot_id, status))
        db.commit()  # Save changes
        print(f"Parking spot {spot_id} updated to status {status}")
    except mysql.connector.Error as err:
        print(f"Error updating parking spot: {err}")

# Callback when the client connects to the broker
def handle_on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully!")
        client.subscribe(TOPIC)  # Subscribe to the topic
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received
def handle_on_message(client, userdata, msg):
    try:
        # Decode the message
        message = msg.payload.decode().strip()  # Remove any extra spaces or newlines
        print(f"Received message: {message} on topic {msg.topic}")

        # Parse the message (e.g., "1 : 0")
        match = re.search(r"([0-9]+)\s*:\s*([0-9])", message)
        if match:
            spot_id = int(match.group(1))
            status = int(match.group(2))
            # Update the parking spot in the database
            db = connect_to_database()
            if db:
                update_parking_spot(db, spot_id, status)
                db.close()  # Close the database connection
        else:
            print("Message format invalid, skipping update.")

    except Exception as e:
        print(f"Failed to process message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Attach the callbacks
client.on_connect = handle_on_connect
client.on_message = handle_on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Start the MQTT client loop
client.loop_forever()