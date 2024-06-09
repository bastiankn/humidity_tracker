#include <Arduino.h>
#include "dht11.h"

#define DHT11PIN 4

dht11 DHT11;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  Serial.println();

  int chk = DHT11.read(DHT11PIN);

  switch (chk)
  {
  case DHTLIB_OK:
    Serial.println("DHT11 OK");
    break;
  case DHTLIB_ERROR_CHECKSUM:
    Serial.println("DHT11 Checksum error");
    break;
  case DHTLIB_ERROR_TIMEOUT:
    Serial.println("DHT11 Time out error");
    break;
  default:
    Serial.println("DHT11 Unknown error");
    break;
  }

  Serial.print("Humidity (%): ");
  Serial.println(DHT11.humidity);

  Serial.print("Temperature (C): ");
  Serial.println(DHT11.temperature);

  delay(2000);
}
