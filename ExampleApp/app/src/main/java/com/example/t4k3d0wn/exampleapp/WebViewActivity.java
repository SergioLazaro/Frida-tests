package com.example.t4k3d0wn.exampleapp;

/**
 * Created by t4k3d0wn on 4/12/16.
 */
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;


public class WebViewActivity extends AppCompatActivity {

    private String url = "";
    private WebView w;
    private EditText newurl;
    private Button refreshButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.webview);

        w = (WebView) findViewById(R.id.webviewId);
        w.getSettings().setJavaScriptEnabled(true);

        newurl = (EditText) findViewById(R.id.newUrl);
        refreshButton = (Button) findViewById(R.id.refreshButton);

    }

    public void refreshWebView(View view){
        String text = newurl.getText().toString();
        if(text.contains("http://")){
            url = text;
        }
        else{
            url = "http://" + text;
        }
        updateURL(url);
    }

    private void updateURL(String url){
        w.loadUrl(url);
    }

}






