from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Inicializamos el contador en 11 o en cualquier otro valor
Contador = 11

# Define una clase MyHTTPRequestHandler que hereda de BaseHTTPRequestHandler
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Define un método privado para establecer la respuesta HTTP
    def _set_response(self, content_type="text/plain"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    # Define un método para manejar solicitudes GET
    def do_GET(self):
        self._set_response()
        respuesta = "El valor es: " + str(Contador)
        self.wfile.write(respuesta.encode())

    # Define un método para manejar solicitudes POST
    def do_POST(self):
        # Obtén la longitud del contenido de la solicitud POST y lee los datos
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            # Intenta analizar los datos POST como JSON
            body_json = json.loads(post_data.decode())
        except:
            # Si no se puede analizar el JSON, envía un error JSON
            self.throw_custom_error("Invalid JSON")
            return

        global Contador
        
        # Verifica si se proporcionan 'action' y 'quantity' en el JSON
        if (body_json.get('action') is None or body_json.get('quantity') is None):
            self._set_response("application/json")
            self.throw_custom_error("Missing action or quantity")
            return

        # Verifica si 'action' es "asc" o "desc" y si 'quantity' es un número
        if (body_json['action'] != 'asc' and body_json['action'] != 'desc'):
            self.throw_custom_error("Invalid action")
            return

        try:
            int(body_json['quantity'])
        except:
            self.throw_custom_error("Invalid quantity")
            return

        # Realiza la acción correspondiente en el contador
        if (body_json['action'] == 'asc'):
            Contador += int(body_json['quantity'])
        elif (body_json['action'] == 'desc'):
            Contador -= int(body_json['quantity'])

        # Responde al cliente con el valor actual del contador
        response_data = json.dumps({"contador": Contador})
        self._set_response("application/json")
        self.wfile.write(response_data.encode())

# Define una función para ejecutar el servidor
def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=7800):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

# Punto de entrada del programa
if __name__ == "__main__":
    run_server()