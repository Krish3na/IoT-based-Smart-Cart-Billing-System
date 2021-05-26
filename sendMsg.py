import twilio
# Download the helper library from https://www.twilio.com/docs/python/install
#Your new Phone Number is +16235526625
from twilio.rest import Client
import random # generate random number

account_sid='ACeb73922eaab2bd3efc309a615f34d251'
auth_token='f7164e19b9b4097011c610ced5ec0cc3'

client = Client(account_sid, auth_token)

def sendOtp(phno):
    otp = random.randint(1000,9999)
    print("Your OTP is - ",otp)
    print('+91'+str(phno))
                                  
    message = client.messages.create(
         body='Dear Smart Kart Customer, your OTP is : ' + str(otp)+'. Valid for 5 minutes',
         from_='+16235526625',
         to='+91'+str(phno))
    
    #print(message.sid)
    return otp

def sendThanks(phno):
    
    message = client.messages.create(
         body='Dear Smart Kart Customer, Thank You For Shopping With Us !.',
         from_='+16235526625',
         to='+91'+str(phno)
     )
    
    print('Sent Msg')


    
