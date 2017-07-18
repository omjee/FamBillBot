package com.softwareag.mobiledivision.messagereaderapplication;

import android.content.DialogInterface;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MessageReader extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_message_reader);

        //Intent for invoking the message operation
        IntentFilter smsFilter = new IntentFilter("android.provider.Telephony.SMS_RECEIVED");
        smsFilter.setPriority(1000);
        SmsReciever reciever = new SmsReciever();
        this.registerReceiver(reciever, smsFilter);

    }

    //onClick Listener for update button
    public void changeSet() {
        Button submitbutton = (Button) findViewById(R.id.button);
        submitbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText url = (EditText)findViewById(R.id.editText);
                EditText apiKey = (EditText) findViewById(R.id.editText3);

                AndroidClient.BASE_URL = url.toString();
                AndroidClient.API_KEY = apiKey.toString();

            }
        });
    }
}
