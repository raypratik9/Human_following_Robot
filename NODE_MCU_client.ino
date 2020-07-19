#include <ESP8266WiFi.h>
#define m1 D1
#define m2 D2
#define m3 D3
#define d1 D5
#define d2 D6
#define d3 D7
int s1, s2, s3;
int d_1, d_2, d_3;
int rpm=100;
const char* ssid = "pratik";    // Enter SSID here
const char* password = "87654321";  //Enter Password here
const char* server = "192.168.43.12";

WiFiClient server1;

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
    Serial.println("WiFi connected");
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(d1, OUTPUT);
  pinMode(d2, OUTPUT);
  pinMode(d3, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (! server1.connect(server, 2000))
    Serial.println("Failed to connect to server");
  while (1)
  {
    while (server1.available()) {
      s1 = server1.readStringUntil(',').toInt();
      s2 = server1.readStringUntil(',').toInt();
      s3 = server1.readStringUntil('*').toInt();
      Serial.println(s1);
      Serial.println(s2);
      Serial.println(s3);
      Serial.println();
      yield();
  int d_1 = (s1 > 0 ? 1 : 0);
  int d_2 = (s2 > 0 ? 1 : 0);
  int d_3 = (s3 > 0 ? 1 : 0);
  digitalWrite(d1, d_1);
  digitalWrite(d2, d_2);
  digitalWrite(d3, d_3);
  analogWrite(m1,rpm+abs(s1));
  analogWrite(m2,rpm+abs(s2));
  analogWrite(m3,rpm+abs(s3));
    }
  }
 
}
