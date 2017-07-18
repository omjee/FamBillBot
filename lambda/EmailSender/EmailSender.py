import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

import os
from base64 import b64decode
import boto3

#App password encrypted using KMS
app_password_encrypted = os.environ['app_password']
app_password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(app_password_encrypted))['Plaintext'].decode('utf-8')
fromaddr = os.environ['from_addr']
app_username = os.environ['app_username']

def sendEmail(event):
    #Email id of the bank account holder (We have used the below email id for the prototype)
    toaddr = "Vidhyadharan<it.vidhyadharan@gmail.com>"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mobile Recharge Notification"
    
    trans_date = time.strftime("%d/%m/%Y")
    trans_time = time.strftime("%H:%M:%S")
    amount = event['amount']
    mobile_number = event['mobile_number']
    mobile_operator = event['mobile_operator']
    #body = "Hi,<br><br> The mobile number 12324 has been recharged with Rs.10 on "+ trans_date +" at "+trans_time+"hrs. <br><br> Regards,<br> FamBillBots"
    body = """<div style="margin:0 auto;padding:0;background:#fff;max-width:600px;font-family:Open Sans,Helvetica,Arial,sans-serif;color:#000">
  <div style="margin:0 auto;overflow:hidden">
    <div style="padding:3%;overflow:hidden"></div>
  </div>
  <div style="margin:0 auto;overflow:hidden;border:solid 1px #f4f4f4;background:#fff;margin:0 10px">
    <div style="padding:5%;float:left"><img title="FamBillBot Logo" src="https://gist.githubusercontent.com/aaradhanas/9e3598b4e1cc5cd331b76819d935b44e/raw/da51d9fcb0ae45edb424373b5ab60b061643fbcd/FamBillBot.png" alt="FamBillBot" class="CToWUd"></div>
    <div style="padding:5%;float:right;width:45%;text-align:right">
      <div style="color:#999;font-size:11px;font-weight:300"><span style="color:#666">"""+trans_date+"""</span></div>
      <span style="font-size:11px;font-weight:300;display:block;color:#666;padding-top:5px">"""+trans_time+"""</span> </div>
    <div style="float:left;text-align:center;width:100%">
      <div style="overflow:hidden"> <img src="https://gist.githubusercontent.com/aaradhanas/9e3598b4e1cc5cd331b76819d935b44e/raw/da51d9fcb0ae45edb424373b5ab60b061643fbcd/done.png"
          style="width:10%;margin:25px 0 5px 0" class="CToWUd">
        <div style="width:100%;float:left;color:#040000;margin-bottom:10px;font-size:30px;font-weight:300">&#8377; """+amount+"""<span style="color:#999;font-size:16px;font-weight:300;display:block"> Recharge Successful</span> </div>
      </div>
      <div style="width:90%;margin:0 5%">
        <img src="https://gist.githubusercontent.com/aaradhanas/9e3598b4e1cc5cd331b76819d935b44e/raw/da51d9fcb0ae45edb424373b5ab60b061643fbcd/mobile.png"
          style="width:90%;margin:14px 0 0 0" class="CToWUd">
      </div>
      <div style="width:90%;float:left;color:#040000;margin-top:15px;font-size:24px;margin-left:5%;margin-right:5%;font-weight:300">
      <span class="il">"""+mobile_operator+"""</span>
        <span style="color:#999;font-size:16px;font-weight:300;display:block">Mobile Number - <a style="color:#999;font-size:16px;font-weight:300;text-decoration:none" href="mailto:9003709481" target="_blank"> 9003709481</a></span>
      </div>
    </div>
    <div style="margin:0 auto;float:left;overflow:hidden;width:100%;margin-top:40px">
      <div style="clear:both"></div>
      <div style="background:#56679b;height:7px"></div>
    </div>
    </div>
  </div>
</div>
</div> """
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print('app_password = '+app_password)
    server.login(app_username, app_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def lambda_handler(event, context):
    # TODO implement
    print(str(event))
    sendEmail(event)
    return 'Mail sent'