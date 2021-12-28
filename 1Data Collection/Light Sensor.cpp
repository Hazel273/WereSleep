/*
This code is written for the ESP-32 microcontroller with the LDRs attached to it
It samples the light values once a minute, and each time it tries to connect to the WiFi
If it cannot connect it it will store the data for the next time it gets a connection
*/
//import relevant libraries
//connectivity libraries
#include <WiFi.h>
#include <HTTPClient.h>
//time for backdating the samples
#include "time.h"

//Network credentials (removed for submission for security)
const char* ssid     = "";
const char* password = "";

//The server used to check the time
const char* ntpServer = "pool.ntp.org";

//Data structure for a FIFO queue to be stored in semi-persistant memory
RTC_DATA_ATTR String measurements[10];
RTC_DATA_ATTR int queueDepth = -1 ;

//LDR pin assignment
const int Red = A2;  
const int Green = A3; 
const int Blue = A1; 

//logic defining if the ESP-32 is measuring the light in the room or outside the window
#define room; 
#ifdef room
  //The target of the HTTP request, in this case the PHP script
  const char* serverName = "http://192.168.0.110/post-room-data.php";
  //Each ESP has a different API key (just in case)
  const String apiKeyValue = "tPmAT5Ab3j7F9Room";
#else
  //The target of the HTTP request, in this case the PHP script
  const char* serverName = "http://192.168.0.110/post-window-data.php";
  //Each ESP has a different API key (just in case)
  const String apiKeyValue = "tPmAT5Ab3j7F9Window";
#endif

//Get the time from the ntp server, and return zero if there is an error 
unsigned long Get_Epoch_Time() {
  //define the time as a time variable (fancy long)
  time_t now;
  //a required variable
  struct tm timeinfo;
  //try to get the time
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  //convert the result to a time varable
  time(&now);
  //return the time
  return now;
}

void setup() {
  //Wake up ESP-32 from deep sleep in 50 seconds (will be paused with the delay function later)
  esp_sleep_enable_timer_wakeup(50000000);
  //Tell the WiFi coprocessor to try to connect
  WiFi.begin(ssid, password);
  //give the coprocessor time to connect to the WiFi
  delay(10000);
  //increment the size of the queue as a new measurement is to be taken
  queueDepth += 1;
  //store the measurements as a string ready to be sent as http
  String  measurements[queueDepth]= "api_key=" + apiKeyValue + "&value1=" + String(analogRead(Red))
                          + "&value2=" + String(analogRead(Green)) + "&value3=" + String(analogRead(Blue)) + "";
  
  //if the WiFi connection succeeds then send the data
  if(WiFi.status()== WL_CONNECTED){
    //declare the HTTP client
    WiFiClient client;
    HTTPClient http;
    //get the time
    unsigned long timeNow = Get_Epoch_Time();
    //for each data sample we have in the queue
    for (int i = queueDepth; i >= 0; i--){
      //start the HTTP connection to the server
      http.begin(client, serverName);
      //define what the HTTP request consists of
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");

      //using how long the queue is the time that the sample was taken is calculated
      unsigned long timeDifference = timeNow - ((queueDepth - i)*60);
      //and this time is appended to the sample
      String httpRequestData = measurements[i] + String(timeDifference);
    
      //Then the POST request is sent to the server, the result is stored but unused once deployed
      int httpResponseCode = http.POST(httpRequestData);
      //close the HTTP connection(allows us to trigger the .php script again)
      http.end();
      //reset that measurement to be empty 
      measurements[i] = "";
    }
    //once the transmission has finished reset the queueDepth
    queueDepth = -1;
  }
  //once that is done go to sleep
  esp_deep_sleep_start();
}

//deep sleep prevents the loop from ever running
void loop() {
}