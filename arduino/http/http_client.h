// http_client.h - definition of HTTP client class

#ifndef __HTTP_CLIENT_H__
#define __HTTP_CLIENT_H__

#include <Ethernet.h>

class http_client {
public:
	http_client(byte* mac, byte* ip, byte* gateway, byte* subnet);
	~http_client();

	bool init(byte* server, unsigned short port);
};

#endif // __HTTP_CLIENT_H__

