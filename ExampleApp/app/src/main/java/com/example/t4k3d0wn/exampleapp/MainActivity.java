package com.example.t4k3d0wn.exampleapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    private TelephonyManager tm;
    private BluetoothAdapter ba;

    private Button imeiButton, checkButton;
    private TextView textIMEI;
    private EditText editPIN;

    private String imei;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textIMEI = (TextView) findViewById(R.id.textView);
        checkButton = (Button) findViewById(R.id.sendPIN);
        editPIN = (EditText) findViewById(R.id.editText);

        //Get IMEI button and hide until unlock with PIN
        imeiButton = (Button) findViewById(R.id.button);
        imeiButton.setVisibility(View.INVISIBLE);

        tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        ba = BluetoothAdapter.getDefaultAdapter();
    }

    public void changeActivity(View view){
        Intent intent = new Intent(getApplicationContext(), WebViewActivity.class);
        startActivity(intent);
    }

    public void getIMEI(View view){
        imei = tm.getDeviceId();
        Toast.makeText(view.getContext(),imei, Toast.LENGTH_LONG).show();
        updateTV(imei);
    }

    public void updateTV(String s){
        textIMEI.setText(s);
    }

    public void modifyBluetooth(){
        if(ba.isEnabled()){
            ba.disable();
        }
        else{
            ba.enable();
        }
    }

    public void checkPIN(View view){
        String text = editPIN.getText().toString();
        if(!text.equals("")){
            if(text.equals("1234")){
                hidePinVerification();
            }
        }
    }

    private void hidePinVerification(){
        editPIN.setVisibility(View.INVISIBLE);
        checkButton.setVisibility(View.INVISIBLE);
        imeiButton.setVisibility(View.VISIBLE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 1: {

                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                    // permission was granted, yay! Do the
                    // contacts-related task you need to do.
                } else {

                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.
                    Toast.makeText(MainActivity.this, "Permission denied", Toast.LENGTH_SHORT).show();
                }
                return;
            }

            // other 'case' lines to check for other
            // permissions this app might request
        }
    }
}
