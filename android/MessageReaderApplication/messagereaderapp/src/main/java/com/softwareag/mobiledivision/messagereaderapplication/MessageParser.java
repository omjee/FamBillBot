package com.softwareag.mobiledivision.messagereaderapplication;

import android.content.ContentResolver;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.telephony.SmsMessage;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by SRAG on 7/11/2017.
 */

public class MessageParser {
    String msgData="";
    Pattern pattern;
    Matcher matcher;
    String OTP="";
    final String regex = "[0-9]{6}";
    String query [] = new String[10];
    String columns[] = new String[2];

    //Get the OTP from message

    public String getLatestOTP( ContentResolver contentResolver) {
        final int REQUEST_CODE_ASK_PERMISSIONS = 123;
        List<String> messages = new ArrayList<String>();
        query[0] ="max(date)";
        columns[0] ="12";

        //crazy hack done for message to get saved
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        Cursor cursor = contentResolver.query(Uri.parse("content://sms/inbox"),null,"read = 0",null, null);
        Log.v("count the value",String.valueOf( cursor.getColumnCount()));

        cursor.getCount();
        cursor.moveToFirst();

        if (cursor.moveToFirst()) { // must check the result to prevent exception
            cursor.getColumnNames();
            msgData = cursor.getString(12);
            Log.v("otp",msgData);


            pattern = Pattern.compile(regex);
            matcher = pattern.matcher(msgData);

            if (matcher.find()&&msgData.contains("Twitter")) {
                OTP = matcher.group(0);
                Log.v("otp",OTP);
                // AndroidClient.post(,rp,null);
            }



        }


        return  OTP;
    }


}
