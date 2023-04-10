import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue', durable=True)

message = 'test'
channel.basic_publish(exchange='', routing_key='my_queue', body=message,
                      properties=pika.BasicProperties(delivery_mode=2))
print("Message sent!")
connection.close()
