// http_client.cpp - implementation of HTTP client class

#include "http_client.h"

const char* USER_AGENT = "arduino-http-client/0.0.1";

http_client::http_client()
: response(NULL), request_headers(NULL)
{
}

http_client::~http_client()
{
	// free the response if we have one
	if (response != NULL)
		free(response);

	// clean up any leftover headers
	free_headers();
}

int http_client::request(byte* server, unsigned short port, const char* url, const char* method, const char* data)
{
	// validate/parse the url
	size_t len = strlen(url);
	char* host = (char*) malloc(len); // allocate string for host
	if (host == NULL)
		return OUT_OF_MEMORY;
	char* path = (char*) malloc(len); // allocate string for path
	if (path == NULL)
		return OUT_OF_MEMORY;
	int ret = parse_url(url, host, path);
	if (ret != SUCCESS)
		return ret;
	
	// make the connection
	if (!client.connect(server, port))
		return CONNECTION_FAILED;
	
	// default method is GET
	if (method == NULL)
		method = "GET";
	
	// send up our request
	char header_buffer[1024];
	sprintf(header_buffer, "%s %s HTTP/1.0", method, path); // don't even think about 1.1
	client.println(header_buffer);
	Serial.println(header_buffer);
	sprintf(header_buffer, "Host: %s", host);
	client.println(header_buffer);
	Serial.println(header_buffer);
	if (data != NULL)
	{
		sprintf(header_buffer, "Content-Length: %d", strlen(data));
		client.println(header_buffer);
		Serial.println(header_buffer);
	}
	client.println("");

	// send up data, if we have any
	if (data != NULL)
		client.println(data);
	
	// now get the response
	char* p = header_buffer;
	bool in_headers = true;
	while (client.available())
	{
		char c = client.read();
		if (in_headers)
		{
			// header end in CRLF, so we'll ignore CR and process the line on LF
			if (c == '\r')
			{
				// ignore and wait for linefeed
			}
			else if (c == '\n')
			{
				// terminate the string and see if we have a header or the body is starting
				*p = 0;
				if (strlen(header_buffer) == 0)
				{
					// if this is an empty line, we've reached the end of the headers
					in_headers = false;
				}
				else
				{
					// this is a header, certain ones are interesting to us
					Serial.println(header_buffer);
				}

				// reset the pointer for the next header
				p = header_buffer;
			}
			else
			{
				// otherwise, this is just part of a header string, append it
				*p++ = c;
			}
		}
		else
		{
			// everything else gets appended to the response body
		}
	}

	// we're done, close the connection
	client.stop();
	
	// clean up
	free(host);
	free(path);

	return SUCCESS;
}

int http_client::parse_url(const char* url, char* host, char* path)
{
	// first, validate the scheme, we only support http right now
	if (strncmp(url, "http://", 7) != 0)
		return BAD_URL;
	
	// extract the host name
	const char* host_start = url + 7;
	const char* host_end = strchr(host_start, '/');
	if (host_end == NULL)
	{
		// there is no path, just copy the host from the url
		strcpy(host, host_start);
		strcpy(path, "/");
	}
	else
	{
		// there is a path, copy only up to the path
		strncpy(host, host_start, host_end - host_start);
		strcpy(path, host_end);
	}

	return SUCCESS;
}

void http_client::append_header(const char* header)
{
	header_list* ph = (header_list*) malloc(sizeof(header_list));
	size_t header_len = strlen(header);
	ph->header = (char*) malloc(header_len + 1);
	strcpy(ph->header, header);
	ph->next = NULL;
	if (request_headers == NULL)
	{
		request_headers = ph;
	}
	else
	{
		header_list* ph2 = request_headers;
		while (ph2->next != NULL)
			ph2 = ph2->next;
		ph2->next = ph;
	}
}

void http_client::free_headers()
{
	header_list* ph = request_headers;
	while (ph != NULL)
	{
		free(ph->header);
		header_list* next_header = ph->next;
		free(ph);
		ph = next_header;
	}
	request_headers = NULL;
}

