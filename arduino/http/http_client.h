// http_client.h - definition of HTTP client class

#pragma once

#include <Ethernet.h>

enum ERROR_CODE {
	SUCCESS = 0,
	OUT_OF_MEMORY,
	BAD_URL,
	CONNECTION_FAILED,
};

struct header_list {
	char* header;
	header_list* next;
};

class http_client {
public:
	http_client();
	~http_client();
	
	int request(byte* server, unsigned short port, const char* url, const char* method = NULL, const char* data = NULL);
	const char* get_response() { return response; }
	void append_header(const char* header);
	void free_headers();

private:
	int parse_url(const char* url, char* host, char* path);

private:
	EthernetClient client;
	char* response;
	header_list* request_headers;
	short http_status_code;
};

