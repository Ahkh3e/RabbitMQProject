import pika
import pymongo
import json

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
mongo_db = mongo_client["project"]
staffs_collection = mongo_db["Staff"]

# Define the queue names

lookup_queue = 'lookup_staff'
all_staff_queue = 'all_staff'


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Set up the queues
channel.queue_declare(queue=lookup_queue)
channel.queue_declare(queue=all_staff_queue)

# Set up RabbitMQ consumers for staff registration, lookup, and list requests

def lookup_staff(ch, method, properties, body):
    ID = body.decode()
    print ("looked up "+ID)
    staffs = []
    for staff in staffs_collection.find({"ID": int(ID)}):
        staff['_id'] = str(staff['_id']) # convert ObjectId to string
        staffs.append(staff)
    response_body = json.dumps(staffs)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def list_staff(ch, method, properties, body):
    staffs = []
    for staff in staffs_collection.find():
        staff['_id'] = str(staff['_id']) # convert ObjectId to string
        staffs.append(staff)
    response_body = json.dumps(staffs)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=response_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='lookup_staff', on_message_callback=lookup_staff)
channel.basic_consume(queue='all_staff', on_message_callback=list_staff)

print("Staff worker started...")
channel.start_consuming()
