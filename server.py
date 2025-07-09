'''
    Matricola: 0001080677
    Email: michele.farneti@studio.unibo.it
    Anno: 2025

    Traccia 1 – Web Server + Sito Web Statico (livello base/intermedio)
    Titolo: "Realizzazione di un Web Server minimale in Python e pubblicazione di un sito statico"

    Obiettivo:
    Progettare un semplice server HTTP in Python (usando socket) e servire un sito web statico con HTML/CSS.
    Requisiti minimi:

    Il server deve rispondere su localhost:8080.
    Deve servire almeno 3 pagine HTML statiche.
    Gestione di richieste GET e risposta con codice 200.
    Implementare risposta 404 per file inesistenti.

    Estensioni opzionali:
    Gestione dei MIME types (.html, .css, .jpg, ecc.).
    Logging delle richieste.
    Aggiunta di animazioni o layout responsive.

'''
#Imports
import sys, signal
import http.server
import socketserver
import os
from datetime import datetime


#Setto la radice dei file serviti
os.chdir('www')

#Inizializzo un indirizzo e porta standard su cui sarà possibile interfacciarsi col server.
STANDARD_ADDRESS = "localhost"
STANDARD_PORT = 8080

#Verifico gli argomenti passati da linea di comando, se non vengono passati correttamente la porta è impostata ad un valore standrd
if(len(sys.argv) == 1):
    PORT = STANDARD_PORT
else:
    PORT = int(sys.argv[1])

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        client_ip, client_port = self.client_address
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GET {self.path} from {client_ip}:{client_port}")

        # Gestione speciale per documentazione.pdf
        if path == "/documentazione.pdf":
            file_path = "." + path  # assuming current directory root
            if not os.path.exists(file_path):
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>404 Not Found</h1><p>Il file documentazione.pdf non esiste.</p>")
                return

        return super().do_GET()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            try:
                with open("404.html", "rb") as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"<h1>404 Not Found</h1><p>La pagina richiesta non esiste.</p>")
        else:
            super().send_error(code, message, explain)

#Realizzo il server HTTP in grado di gestire più richieste
server = socketserver.ThreadingTCPServer((STANDARD_ADDRESS,PORT),HTTPHandler)

#Assicurro la corretta chiusura di tutti i threads alla chiusura dell'applicazione con Ctrl+C
server.daemon_threads = True  
#Imposto il server in modo da permettere di associarvi un socket anche se già presente un altro 
#soket associato alla stessa porta.
server.allow_reuse_address = True  

#Imposto il meccanismo di chiusura con Ctrl+C
def signal_handler(signal, frame):
    print( "Exiting http server (Ctrl+C pressed)")
    try:
        if( server ):
            server.server_close()
    finally:
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Loop infinito di gestione delle richieste, interrompibile solo dal segnale da tastiera.
try:
    while True:
        print(f"Server set up on Address: http://{STANDARD_ADDRESS}:{PORT}")
        print("Server waiting for requests....")
        server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()