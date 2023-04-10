import pika
import pymongo

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
mongo_db = mongo_client["project"]
users_collection = mongo_db["UserInfo"]

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbitmq_channel = connection.channel()
rabbitmq_channel.queue_declare(queue='login')

# Separate worker function that authenticates user and sends response
def login_worker(ch, method, properties, body):
    username, password = body.decode().split(",")
    user_data = users_collection.find_one({"username": username, "password": password})
    
    if user_data:
        account_type = user_data.get("type")
        account_ID = user_data.get("ID")
       
        response_body = f"success,{account_type},{account_ID},"
        print("Successfull attempt")
    else:
        response_body = "failure"
        print("Failed attempt")
    
    # Send response back to main application
    rabbitmq_channel.basic_publish(exchange="", routing_key=properties.reply_to, body=response_body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up RabbitMQ worker to consume login messages
rabbitmq_channel.basic_qos(prefetch_count=1)
rabbitmq_channel.basic_consume(queue="login", on_message_callback=login_worker)

print("Login worker started...")
rabbitmq_channel.start_consuming()


