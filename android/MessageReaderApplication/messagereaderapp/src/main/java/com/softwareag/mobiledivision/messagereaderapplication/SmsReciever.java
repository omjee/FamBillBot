package com.softwareag.mobiledivision.messagereaderapplication;

/**
 * Created by SRAG on 7/11/2017.
 */

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;



public class SmsReciever extends BroadcastReceiver {
    static final String ACTION =
            "android.provider.Telephony.SMS_RECEIVED";


    MessageParser parser;

    AndroidClient client;
    String OTP;

    @Override
    public void onReceive(Context context, Intent intent) {
        // This method is called when the BroadcastReceiver is receiving
        final IntentFilter smsFilter = new IntentFilter("android.provider.Telephony.SMS_RECEIVED");

        // an Intent broadcast.
        Log.v("test","rest");
        if (intent.getAction().equals(ACTION)) {
            StringBuilder buf = new StringBuilder();
            Bundle bundle = intent.getExtras();
            client = new AndroidClient();

            if (bundle != null) {
                parser = new MessageParser();
                OTP =  parser.getLatestOTP(context.getContentResolver());

                client = new AndroidClient();
                client.sendPostRequest(OTP,context);

            }

        }

    }


}
