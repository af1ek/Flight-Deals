from twilio.rest import Client

TWILIO_NUMBER = "" #Your Twilio number
TWILIO_SID = "" #Your Twilio SID
AUTH_TOKEN = "" #Your Twilio Auth token
MY_NUMBER = "" #Your Phone number

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, AUTH_TOKEN)

    def send_message(self, message):
        message = self.client.messages.create(
            from_= TWILIO_NUMBER,
            to= MY_NUMBER,
            body= message)

        print(message.sid)
