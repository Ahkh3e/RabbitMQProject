import pika
import pymongo
import json

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
mongo_db = mongo_client["project"]
patients_collection = mongo_db["Patient"]

# Define the queue names
register_queue = 'register_patient'
lookup_queue = 'lookup_patient'
all_patients_queue = 'all_patients'


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Set up the queues
channel.queue_declare(queue=register_queue)
channel.queue_declare(queue=lookup_queue)
channel.queue_declare(queue=all_patients_queue)

# Set up RabbitMQ consumers for patient registration, lookup, and list requests
def register_patient(ch, method, properties, body):
    patient_data = json.loads(body)
    
    print(patient_data)
    patients_collection.insert_one(patient_data)
    print("Registered new patient:", patient_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def lookup_patient(ch, method, properties, body):
    phone = body.decode()
    patients = []
    for patient in patients_collection.find({"phone": phone}):
        patient['_id'] = str(patient['_id']) # convert ObjectId to string
        patients.append(patient)
    response_body = json.dumps(patients)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def list_patients(ch, method, properties, body):
    patients = []
    for patient in patients_collection.find():
        patient['_id'] = str(patient['_id']) # convert ObjectId to string
        patients.append(patient)
    response_body = json.dumps(patients)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='register_patient', on_message_callback=register_patient)
channel.basic_consume(queue='lookup_patient', on_message_callback=lookup_patient)
channel.basic_consume(queue='all_patients', on_message_callback=list_patients)

print("Patient worker started...")
channel.start_consuming()
