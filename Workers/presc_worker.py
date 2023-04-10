import pika
import pymongo
import json

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
mongo_db = mongo_client["project"]
presc_collection = mongo_db["Prescription_Hist"]

# Define the queue names

lookup_queue = 'lookup_pres'
all_pres_queue = 'all_pres'


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Set up the queues
channel.queue_declare(queue=lookup_queue)
channel.queue_declare(queue=all_pres_queue)

# Set up RabbitMQ consumers for staff registration, lookup, and list requests

def lookup_pres(ch, method, properties, body):
    ID = body.decode()
    print ("looked up "+ID)
    prescs = []
    print(presc_collection.find({"ID": int(ID)}))
    for presc in presc_collection.find({"ID": int(ID)}):
        presc['_id'] = str(presc['_id']) # convert ObjectId to string
        prescs.append(presc)
    response_body = json.dumps(prescs)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def list_pres(ch, method, properties, body):
    prescs = []
    for presc in presc_collection.find():
        presc['_id'] = str(presc['_id']) # convert ObjectId to string
        prescs.append(presc)
    response_body = json.dumps(prescs)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='lookup_pres', on_message_callback=lookup_pres)
channel.basic_consume(queue='all_pres', on_message_callback=list_pres)

print("Prescription worker started...")
channel.start_consuming()
