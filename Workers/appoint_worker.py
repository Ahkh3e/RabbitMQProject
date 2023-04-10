import pika
import pymongo
import json

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
mongo_db = mongo_client["project"]
appoints_collection = mongo_db["Appointments"]

# Define the queue names
doctor_queue = 'lookup_doctor'
patient_queue = 'lookup_patient'
all_appoints_queue = 'all_appoints'


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Set up the queues
channel.queue_declare(queue=doctor_queue)
channel.queue_declare(queue=patient_queue)
channel.queue_declare(queue=all_appoints_queue)

# Set up RabbitMQ consumers for patient registration, lookup, and list request

def lookup_doctor(ch, method, properties, body):
    ID = body.decode()
    appoints = []
    for appoint in appoints_collection.find({"DoctorID": int(ID)}):
        appoint['_id'] = str(appoint['_id']) # convert ObjectId to string
        appoints.append(appoint)
    response_body = json.dumps(appoints)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)



def lookup_patient(ch, method, properties, body):
    ID = body.decode()
    appoints = []
    for appoint in appoints_collection.find({"PatientID": int(ID)}):
        appoint['_id'] = str(appoint['_id']) # convert ObjectId to string
        appoints.append(appoint)
    response_body = json.dumps(appoints)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def list_all(ch, method, properties, body):
    appoints = []
    for appoint in appoints_collection.find():
        appoint['_id'] = str(appoint['_id']) # convert ObjectId to string
        appoints.append(appoint)
    response_body = json.dumps(appoints)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='lookup_doctor', on_message_callback=lookup_doctor)
channel.basic_consume(queue='lookup_patient', on_message_callback=lookup_patient)
channel.basic_consume(queue='all_appoints', on_message_callback=list_all)

print("Patient worker started...")
channel.start_consuming()
