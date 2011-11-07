// http client

#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0x8E, 0xC1 };
byte ip[] = { 192, 168, 1, 120 };
byte gateway[] = { 192, 168, 1, 254 };
byte subnet[] = { 255, 255, 255, 0 };
byte server[] = { 74, 125, 53, 141 };

Client client(server, 80);

void setup()
{
	Ethernet.begin(mac, ip, gateway, subnet);
	Serial.begin(9600);

	// give it a second to start up
	delay(1000);        
}

void loop()
{
	if (client.connect())
	{
		Serial.println("making request...");
		client.println("GET / HTTP/1.0");
		client.println("Host: jorgev-hrd.appspot.com");
		//client.println("Accept: */*");
		client.println();
	
		delay(1000);
		while (client.available())
		{
			char c = client.read();
			Serial.print(c);
		}

		client.stop();
		delay(10000);
	}
	else
	{
		Serial.println("connection failed");
	}
}

