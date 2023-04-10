import pika
from pymongo import MongoClient
import uuid
import os
from time import sleep
# Connect to the MongoDB instance
client = MongoClient('mongodb://admin:secret@localhost:27017/')

# Set the database and collection names
db = client['project']
users_collection = db['users']

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbitmq_channel = connection.channel()
rabbitmq_channel.queue_declare(queue='login')



# Main function that prompts user to enter username and password
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Send message to RabbitMQ containing username and password
    response = rabbitmq_channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue
    
    rabbitmq_channel.basic_publish(exchange="", routing_key="login", body=f"{username},{password}", properties=pika.BasicProperties(reply_to=callback_queue))
    print("\n")
    
    print("Authenticating...")
    sleep(1)
    # Wait for response from worker
    while True:
        method_frame, _, body = rabbitmq_channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        if method_frame.routing_key == callback_queue:
            response = body.decode()
            break
    # Delete the callback queue
    rabbitmq_channel.queue_delete(queue=callback_queue)
    if response.startswith("success"):
        account_type = response.split(",")[1]
        account_ID = response.split(",")[2]
        print("Login successful")
        return True, account_type, account_ID
    else:
        print("Login failed")
        return False, None, None


# Start the main application
if __name__ == "__main__":
    # Start the login loop
    while True:
        login()