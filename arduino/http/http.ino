// http client

#include <SPI.h>
#include <Ethernet.h>
#include "http_client.h"

byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0x8E, 0xC1 };
byte ip[] = { 192, 168, 1, 120 };
byte gateway[] = { 192, 168, 1, 254 };
byte subnet[] = { 255, 255, 255, 0 };
byte server[] = { 74, 125, 224, 147 };

http_client client;

void setup()
{
	// set up ethernet
	Ethernet.begin(mac, ip, gateway, subnet);
	Serial.begin(9600);

	// give it a second to start up
	delay(1000);        
}

void loop()
{
	// make a request
	int ret = client.request(server, 80, "http://www.google.com");

	// sleep a little before the next request
	delay(10000);
}

