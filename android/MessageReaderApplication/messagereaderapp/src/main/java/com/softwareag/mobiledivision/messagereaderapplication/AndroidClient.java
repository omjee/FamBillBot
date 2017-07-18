package com.softwareag.mobiledivision.messagereaderapplication;

import android.content.Context;
import android.util.Log;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.JsonRequest;
import com.android.volley.toolbox.Volley;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;

import javax.ws.rs.core.MediaType;


import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by SRAG on 7/11/2017.
 */

public class AndroidClient {
     public static String BASE_URL = "https://6tegmyq1f0.execute-api.us-east-1.amazonaws.com/test/OTPDBLambda/";
     //public static String BASE_URL = "http://mockbin.org/bin/f05e403b-9ef2-4b99-9fbe-81955506ed9f";

    public static String API_KEY = "VIDHYADHARAN-AARADHANA-SREESARAN";
    private JSONObject otp;
    int POST = 1;


    /**
     *
     * @param OTP
     * @param context
     */
    public void sendPostRequest(String OTP,Context context) {
        final String OTP1 =OTP;
        RequestQueue queue = Volley.newRequestQueue(context);

        try {
            otp = new JSONObject("{ \"otp\":\""+OTP+"\"}");
        } catch (JSONException e) {
            e.printStackTrace();
        }


        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.POST,BASE_URL, otp, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.v("response", String.valueOf(response));
            }
        },new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

               Log.v("Error: ", error.getMessage());
                Log.v("Details","printing details");
                error.printStackTrace();
            }
        }){
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("x-api-key", API_KEY);
                params.put("content-type", "application/json");

                return params;
            }
        };


// Add the request to the RequestQueue.
        queue.add(jsonRequest);
        queue.start();
    }


}
