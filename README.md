# Postmates Take Home Coding Test - Geocoding Proxy Service

## Overview

Network service that resolves lat, lng coordinates for address using third party geocoding services.

## Configuration

The first few lines of the geocoding_proxy.py file should look like this:

```python

PORT = 8080
gkey = ""
app_id=""
app_code=""

```

PORT defines the port the service will run on. 
gkey is your google API key.
app_id and app_code are your API keys from Here.com 

## Running

This was written for use with Python 3.7. Simply run `python geocoding_proxy.py` in Powershell on Windows or Terminal elsewhere.
To exit, press `^C` (Ctrl+C).

For easy deployment, a Dockerfile has been added. Make sure to configure the port and api keys first. Then run `docker build -t geocoder .` to build the image as `geocoder`. From then on, to run type `docker run -p 8080:8080 geocoder`

## Usage

**Definition**

Requests should have the form

`GET /?address=1+Infinite+Loop,+Cupertino+CA+95014`

**Response**

- `200 OK` on success

```json
{
	"status": "OK"
	"data": {
		"lat":123.13452,
		"lng":-23.32332,
	}
}
```

- `404` otherwise

```json
{"status": "No Result", "data": {}}
```
