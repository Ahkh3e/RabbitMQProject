import pika
import json
from prettytable import PrettyTable
from time import sleep

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define the queue names
doctor_queue = 'lookup_doctor'
patient_queue = 'lookup_patient'
all_appoints_queue = 'all_appoints'


# Set up the queues
channel.queue_declare(queue=doctor_queue)
channel.queue_declare(queue=patient_queue)
channel.queue_declare(queue=all_appoints_queue)


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


def lookup_patient():
    ID = input("Enter Patient ID: ")
    
    # Send message to RabbitMQ requesting patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="lookup_patient", body=ID, properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving patient data...")

    # Wait for response from worker
    while True:
        
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        response = json.loads(body.decode())
        break
    channel.queue_delete(queue=callback_queue)
    sleep(1)
    
    if response:
        print("Appointments found:")
        table = PrettyTable()
        table.field_names = ["Appointment ID", "Doctor ID", "Time"]

        # Add rows to the table
        for appoint in response:
            table.add_row([appoint['appID'], appoint['DoctorID'], appoint['time']])

        # Print the table
        print(table)
    else:
        print("Appointments not found")



def lookup_my_patient(ID):
    print(ID)
    # Send message to RabbitMQ requesting patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="lookup_patient", body=ID, properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving patient data...")

    # Wait for response from worker
    while True:
        
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        response = json.loads(body.decode())
        break
    channel.queue_delete(queue=callback_queue)
    sleep(1)
    if response:
        print("Appointments found:")
        table = PrettyTable()
        table.field_names = ["Appointment ID", "Doctor ID", "Time"]

        # Add rows to the table
        for appoint in response:
            table.add_row([appoint['appID'], appoint['DoctorID'], appoint['time']])

        # Print the table
        print(table)
    else:
        print("Appointments not found")



def lookup_doctor():
 
    ID = input("Enter Doctor ID: ")
    
    # Send message to RabbitMQ requesting patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="lookup_doctor", body=ID, properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving Doctor data...")

    # Wait for response from worker
    while True:
        
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if method_frame is None:
            continue
        response = json.loads(body.decode())
        break
    channel.queue_delete(queue=callback_queue)
    sleep(1)
    if response:
        print("Appointments found:")
        table = PrettyTable()
        table.field_names = ["Appointment ID", "Patient ID", "Time"]

        # Add rows to the table
        for appoint in response:
            table.add_row([appoint['appID'], appoint['PatientID'], appoint['time']])

        # Print the table
        print(table)
    else:
        print("Appointments not found")

def get_all_appoints():
    # Send message to RabbitMQ requesting all patient data
    response = channel.queue_declare(queue="", exclusive=True)
    callback_queue = response.method.queue

    channel.basic_publish(exchange="", routing_key="all_appoints", body="", properties=pika.BasicProperties(reply_to=callback_queue))

    print("Retrieving all Appointment data...")

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
        table.field_names = ["Appointment ID","Doctor ID", "Patient ID", "Time"]

        # Add rows to the table
        for appoint in response:
            table.add_row([appoint['appID'],appoint['DoctorID'], appoint['PatientID'], appoint['time']])

        # Print the table
        print(table)
    else:
        print("No Appointments found")