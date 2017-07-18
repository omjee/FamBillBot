![FamBillBot logo](https://gist.githubusercontent.com/aaradhanas/9e3598b4e1cc5cd331b76819d935b44e/raw/da51d9fcb0ae45edb424373b5ab60b061643fbcd/FamBillBot.png)
# Lambda

This project involves the below lambda functions :

## BillPay
This is the lamda function that the bot communicates with to get the slot information, to handle intents and return on fulfillment/error.
 
## DirectMessage
This is a lamda function for reading direct messages from twitter.	

## EmailSender
This lamda function is used for sending emails about the transaction details to the bank account holder.

## GreetUser
This is lambda function which responds to the GreetUser intent (When the user typs Hi, Hello, etc..)

## OTPQueue
This is a lamda function for reading from the SQS and return the latest message.