![FamBillBot logo](https://gist.githubusercontent.com/aaradhanas/9e3598b4e1cc5cd331b76819d935b44e/raw/da51d9fcb0ae45edb424373b5ab60b061643fbcd/FamBillBot.png)
# Lex

This project holds the bot definition and version details of the bot and intents:

The bot handles the below 2 intents:
```md
1. GreetUser - This intent responds to the greetings of the user.
2. MobileRecharge - This intent is responsible for the recharge of the given mobile 
   number with the provided amount.
```

The bot expects the below slot values for the Mobile Recharge intent :
```md
1. Mobile number
2. Mobile operator
3. Recharge amount
```
In case of any error in the transaction, the bot does the error handling and responds to the user with appropriate message.