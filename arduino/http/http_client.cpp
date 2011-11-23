// http_client.cpp - implementation of HTTP client class

#include "http_client.h"

http_client::http_client(byte* mac, byte* ip, byte* gateway, byte* subnet)
{
	Ethernet.begin(mac, ip, gateway, subnet);
}

http_client::~http_client()
{
}

bool http_client::init(byte* server, unsigned short port)
{
	return true;
}

