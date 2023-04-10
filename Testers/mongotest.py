import pymongo

client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
db = client["project"]
# Dummy data for Patient
info = messages = [
     {    "messageID": 1,    "senderID": 6,    "recipientID": 1,    "message": "Hello, how are you feeling today?",    "datetime": "2023-04-10T10:30:00Z"  }, 
    {    "messageID": 2,    "senderID": 1,    "recipientID": 6,    "message": "I'm feeling a bit better, thanks for asking.",    "datetime": "2023-04-10T11:00:00Z"  },  
    {    "messageID": 3,    "senderID": 7,    "recipientID": 2,    "message": "Hi, just wanted to check in and see how you're doing.",    "datetime": "2023-04-11T09:15:00Z"  }, 
  {    "messageID": 4,    "senderID": 2,    "recipientID": 7,    "message": "I'm still experiencing some pain in my lower back.",    "datetime": "2023-04-11T09:45:00Z"  },  
  {    "messageID": 5,    "senderID": 8,    "recipientID": 3,    "message": "Hey there, just wanted to remind you about your appointment tomorrow at 2PM.",    "datetime": "2023-04-12T14:30:00Z"  }, 
   {    "messageID": 6,    "senderID": 3,    "recipientID": 8,    "message": "Thanks for the reminder, I'll be there on time.",    "datetime": "2023-04-12T15:00:00Z"  },  
   {    "messageID": 7,    "senderID": 9,    "recipientID": 4,    "message": "Hello, just checking in to see if you have any questions about your medication.",    "datetime": "2023-04-13T11:45:00Z"  },
     {    "messageID": 8,    "senderID": 4,    "recipientID": 9,    "message": "Yes, I was wondering about the side effects of the medication.",    "datetime": "2023-04-13T12:15:00Z"  },  
     {    "messageID": 9,    "senderID": 10,    "recipientID": 5,    "message": "Hi, just wanted to let you know that your lab results came back and everything looks good.",    "datetime": "2023-04-14T16:00:00Z"  },  
{    "messageID": 10,    "senderID": 5,    "recipientID": 10,    "message": "That's great news, thanks for letting me know.",    "datetime": "2023-04-14T16:30:00Z"  }]
db["Messages"].insert_many(info)

print("Inserted patient with ID:", insert_result.inserted_id)