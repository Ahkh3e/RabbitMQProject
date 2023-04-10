import pika
import json
from prettytable import PrettyTable
from time import sleep

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define the queue names
register_queue = 'register_patient'
lookup_queue = 'lookup_patient'
all_patients_queue = 'all_patients'

# Set up the queues
channel.queue_declare(queue=register_queue)
channel.queue_declare(queue=lookup_queue)
channel.queue_declare(queue=all_patients_queue)


# Helper function to send a message to a queue and wait for a response
def send_message(queue_name, message):
    # Set up the callback queue
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    # Send the message to the specified queue with the callback queue specified
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              reply_to=callback_queue,
                              delivery_mode=2  # make message persistent
                          ))

    # Wait for a response on the callback queue
    def callback(ch, method, properties, body):
        if properties.correlation_id == correlation_id:
            response = json.loads(body)
            nonlocal response_message
            response_message = response

    response_message = None
    correlation_id = str(uuid.uuid4())
    channel.basic_consume(queue=callback_queue, on_message_callback=callback, auto_ack=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              reply_to=callback_queue,
                              correlation_id=correlation_id,
                              delivery_mode=2  # make message persistent
                          ))

    while response_message is None:
        connection.process_data_events()

    return response_message

def register_patient():
    # Get user input for patient information
    ID = input("Enter patient ID: ")
    fname = input("Enter patient first name: ")
    lname = input("Enter patient last name: ")
    age = input("Enter patient age: ")
    gender = input("Enter patient gender: ")
    address = input("Enter patient address: ")
    phone_number = input("Enter patient phone number: ")
    
    # Send message to RabbitMQ containing patient data
    channel.basic_publish(exchange="", routing_key="register_patient", body=json.dumps({
        "ID": ID,
        "Firstname": fname,
        "Lastname": lname,
        "age": age,
        "gender": gender,
        "address": address,
        "phone": phone_number
    }))
    
    sleep(1)
    print("Patient registration successful")
    

def lookup_patient():
    # Get user input for patient phone number
    phone_number = input("Enter patient phone number: ")
    
    # Send message to RabbitMQ requesting patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="lookup_patient", body=phone_number, properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving patient data...")

    # Wait for response from worker
    while True:
        
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        response = json.loads(body.decode())
        break
    sleep(1)
    if response:
        print("Patient found:")
        table = PrettyTable()
        table.field_names = ["ID","First Name", "Last Name", "Age", "Gender", "Address", "Phone number"]

        # Add rows to the table
        for patient in response:
            table.add_row([patient['ID'],patient['Firstname'], patient['Lastname'], patient['age'], patient['gender'], patient['address'], patient['phone']])

        # Print the table
        print(table)
    else:
        print("Patient not found")
    

def get_all_patients():
    # Send message to RabbitMQ requesting all patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="all_patients", body="", properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving all patient data...")

    # Wait for response from worker
    while True:
        
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        if method_frame.routing_key == callback_queue:
            response = json.loads(body.decode())
            break
    channel.queue_delete(queue=callback_queue)
    sleep(1)
    if response:
        print("All patients:")
        table = PrettyTable()
        table.field_names = ["ID","First Name", "Last Name", "Age", "Gender", "Address", "Phone number"]

        # Add rows to the table
        for patient in response:
            table.add_row([patient['ID'],patient['Firstname'], patient['Lastname'], patient['age'], patient['gender'], patient['address'], patient['phone']])

        # Print the table
        print(table)
    else:
        print("No patients found")
    