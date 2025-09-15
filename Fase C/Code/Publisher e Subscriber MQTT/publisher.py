import time
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
BROKER = "broker.hivemq.com"
#BROKER = "10.0.0.2"  # Subscriber-1
#BROKER = "10.0.0.10" # Subscriber-2 (Replicação do 1)
PORT = 1883           # MQTT broker port
TOPIC = "parking"  # Topic to publish to

# File Configuration
INPUT_FILE = "CupCarbon/Cupcarbon_G2/results/SINK_45.txt"  # File to monitor for new lines

# Callback for when the publisher connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully!")
    else:
        print(f"Failed to connect, return code {rc}")

# Function to publish new lines from the file
# Necessário adicionar para ele publicar linha a linha as linhas q já se encontravam no ficheiro (Culpa do cupcarbon q só funciona se ninguém tiver a aceder ao ficheiro)
def monitor_and_publish(client, file_path):
    try:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Move to the end of the file
            file.seek(0, 2)
            
            print(f"Monitoring file: {file_path} for new lines...")
            while True:
                # Read the next line
                line = file.readline()
                if line:
                    # Clean the line and publish
                    message = line.strip()
                    client.publish(TOPIC, message)
                    print(f"Published: {message}")
                else:
                    # Wait briefly before checking again
                    time.sleep(0.1)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    # Create an MQTT client instance
    client = mqtt.Client()
    client.on_connect = on_connect

    # Connect to the MQTT broker
    client.connect(BROKER, PORT, 60)

    # Start the MQTT loop in a separate thread
    client.loop_start()

    # Monitor the file and publish new lines
    monitor_and_publish(client, INPUT_FILE)

    # Stop the MQTT loop and disconnect (if the loop ends, e.g., due to an exception)
    client.loop_stop()
    client.disconnect()
