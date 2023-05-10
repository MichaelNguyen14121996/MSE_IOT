package com.example.demoiot;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView txtTemp, txtHumi, txtAIView;
    LabeledSwitch btnLed, btnPump;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtTemp = findViewById(R.id.txtTemperature);
        txtHumi = findViewById(R.id.txtHumidity);
        txtAIView = findViewById(R.id.textAIView);

        btnLed = findViewById(R.id.btnLed);
        btnPump = findViewById(R.id.btnPump);
//        btnFan = findViewById(R.id.btnFan);

        btnLed.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn) {
                    sendDataMQTT("michaelnguyen/feeds/nutnhan1", "1");
                } else {
                    sendDataMQTT("michaelnguyen/feeds/nutnhan1", "0");
                }
            }
        });

        btnPump.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn) {
                    sendDataMQTT("michaelnguyen/feeds/nutnhan2", "1");
                } else {
                    sendDataMQTT("michaelnguyen/feeds/nutnhan2", "0");
                }
            }
        });

//        btnFan.setOnToggledListener(new OnToggledListener() {
//            @Override
//            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
//                if (isOn) {
//                    sendDataMQTT("michaelnguyen/feeds/nutnhan1", "1");
//                } else {
//                    sendDataMQTT("michaelnguyen/feeds/nutnhan1", "0");
//                }
//            }
//        });

        startMQTT();
    }

    public void startMQTT() {
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("test", topic + "***" + message.toString());
                if (topic.contains("cambien1")) {
                    txtTemp.setText(message.toString() + "°C");
                } else if (topic.contains("cambien2")) {
                    txtHumi.setText(message.toString() + "%");
                } else if (topic.contains("nutnhan1")) {
                    if ("1".equals(message.toString())) {
                        btnLed.setOn(true);
                    } else {
                        btnLed.setOn(false);
                    }
                } else if (topic.contains("nutnhan2")) {
                    if ("1".equals(message.toString())) {
                        btnPump.setOn(true);
                    } else {
                        btnPump.setOn(false);
                    }
                } else if (topic.contains("ai")) {
                    String aiText;
                    if (message.toString().contains("None")) {
                        aiText = "Không có người";
                    } else if (message.toString().contains("NoMask")){
                        aiText = "Có người không mang khẩu trang";
                    } else{
                        aiText = "Có người mang khẩu trang";
                    }
                    txtAIView.setText(aiText);
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }


    public void sendDataMQTT(String topic, String value) {
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        } catch (MqttException e) {
        }
    }


}