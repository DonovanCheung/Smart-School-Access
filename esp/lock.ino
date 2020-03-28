#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "USC Guest Wireless";
const char* password = "";
const int check_button = 16;
const int green_led = 15;
const int red_led = 5;


void setup () {
 Serial.begin(115200);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
   delay(1000);
   Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 
 pinMode(green_led, OUTPUT);
 pinMode(red_led, OUTPUT);
}

void loop() {
   if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
     HTTPClient http;  //Declare an object of class HTTPClient
     
     StaticJsonBuffer<1000> jsonBuffer;
     http.begin("http://jigar-cloud.appspot.com/att_case_hacks/smart_access/get_lock_status?lock_id=L1");  //Specify request destination
     int httpCode = http.GET(); 
     if (httpCode > 0) { //Check the returning code
       String payload = http.getString();   //Get the request response payload
       
       JsonObject& root = jsonBuffer.parseObject(payload);   //Actual HTTP Request
       bool working = root["success"];                      
       
       Serial.println(payload);                     //Print the response payload
       if (working == true){ 
        digitalWrite(green_led, HIGH);
        digitalWrite(red_led, LOW);
       }
       else{
        digitalWrite(red_led, HIGH);
        digitalWrite(green_led, LOW);
       }
     }
     http.end();   //Close connection
   }
   else {
    Serial.println("Error on HTTP request");
   }
   delay(1000);    //Waits 3 seconds for next button press
}
