# !/usr/bin/env python3
# ## ###############################################
#
# webserver.py
# Starts a custom webserver and handles all requests
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from http.server import BaseHTTPRequestHandler, HTTPServer

class WebServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><body>Hola Mundo!!!</body></html>", "utf-8"))

def main():
	webServer = HTTPServer(("192.168.1.254", 80), WebServer)
	print("Servidor iniciado")
	print ("\tAtendiendo solicitudes entrantes")
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	print("Server stopped.")

# Punto de anclaje de la función main
if __name__ == "__main__":
	main()
