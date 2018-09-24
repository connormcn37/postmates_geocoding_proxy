"""
geocoding_proxy.py: Acts as a proxy for the Google and Here.com geocoding services.
"""
__author__ = "Connor McNeill"
__email__  = "connormcn37@gmail.com" 


PORT = 8080
gkey = ""
app_id=""
app_code=""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pprint import pprint
import json, re, http.client

def GoogleGeocode(address,apikey=gkey):
	"""
	Wrapper function for the Google geocoding service.
	https://maps.googleapis.com/maps/api/geocode/json
	  ?address=1+Infinite+Loop
	  &key={YOUR_API_KEY}
	"""
	base = r"maps.googleapis.com"
	path = r"/maps/api/geocode/json?"
	addr = "address=" + address
	url = path + addr + "&key=" + apikey
	j = getUrl(base, url)
	if j['status'] == 'OK':
		return { "status": "OK", "data": j['results'][0]['geometry']['location'] }
	else:
		return None

def HereGeocode(address,appid=app_id,appcode=app_code):
	"""
	Wrapper function for the Here.com geocoding service.
	https://geocoder.api.here.com/6.2/geocode.json
	  ?app_id={YOUR_APP_ID} 
	  &app_code={YOUR_APP_CODE} 
	  &searchtext=425+W+Randolph+Chicago
	"""
	base = r"geocoder.api.here.com"
	path = r"/6.2/geocode.json?"
	addr = "&searchtext=" + address
	url = path + "app_id=" + appid + "&app_code=" + appcode + addr
	j = getUrl(base,url)
	geolocation = j['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
	nudict = {"status": "OK", "data": {"lat": geolocation['Latitude'], "lng": geolocation['Longitude']}}
	return nudict

def getUrl(base, url):
	"""
	Helper function that makes the HTTP requests
	"""
	conn = http.client.HTTPSConnection(base)
	conn.request("GET", url)
	response = conn.getresponse()
	data = response.read()
	return json.loads(data)

class GeocodingProxyHandler(BaseHTTPRequestHandler):
	"""
	Class to handle HTTP requests to the server. Bulk of the code.
	"""
	def sendCode(self,code,message):
		"""
		Helper function that sends headers, response code, and content to the client
		"""
		self.send_response(code)
		self.send_header('Content-type','text/json;charset=utf-8')
		self.end_headers()
		self.wfile.write(bytes(str(message),'utf-8'))
		return

	def do_GET(self):
		"""
		Handles the incoming GET requests and attempts to look up addresses. Otherwise, sends 404.
		"""
		urlObject = urlparse(self.path)
		if urlObject.path == '/':
			query = parse_qs(urlObject.query)
			if 'address' in query:	
				addr = re.sub('\s+', '+', query['address'][0].strip())
				response = None
				lookup_services = [GoogleGeocode, HereGeocode]
				for service in lookup_services:
					try:
						response = service(addr)
						if response['status'] == "OK":
							break
					except Exception as e:
						pprint(e)
				if response:
					pprint(response)
					return self.sendCode(200,json.dumps(response))
		return self.sendCode(404, json.dumps({"status": "No Result", "data":{}}))				  

if __name__ == '__main__':
	try:
		server_address = ('', PORT)
		httpd = HTTPServer(server_address, GeocodingProxyHandler)
		httpd.serve_forever()
	except KeyboardInterrupt:
		httpd.server_close()