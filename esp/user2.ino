#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "USC Guest Wireless";
const char* password = "";
const int check_button = 12;

void setup () {
  //enable pin for button input on a pullup setup
  pinMode(check_button, INPUT_PULLUP);
  //open a serial communication port for debugging
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
}

void loop() {
  if (digitalRead(check_button) == LOW) {
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      HTTPClient http;  //Declare an object of class HTTPClient
      StaticJsonBuffer<1000> jsonBuffer;
      http.begin("http://jigar-cloud.appspot.com/att_case_hacks/smart_access/open_lock?lock_id=L1&user_id=U2");  //Specify request destination
      int httpCode = http.GET();
      if (httpCode > 0) { //Check the returning code
        String payload = http.getString();   //Get the request response payload
        JsonObject& root = jsonBuffer.parseObject(payload);   //Actual HTTP Request
        bool working = root["success"];                      //Using website name as a placeholder
        Serial.println(payload);
        if (working == true){
          Serial.println("Unlocked");
          digitalWrite(green_led, HIGH);
          digitalWrite(red_led, LOW);
        }
        else {
          Serial.println("Locked");
          digitalWrite(red_led, HIGH);
          digitalWrite(green_led, LOW);
        }
      }
      http.end();   //Close connection
    }
    else {
      Serial.println("Error on HTTP request");
    }
    delay(3000);    //Waits 3 seconds for next button press
  }
}