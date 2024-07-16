'''
    Matricola: 0001080677
    Email: michele.farneti@studio.unibo.it
    Anno: 2024

    Traccia 2:
    Creare un web server semplice in Python che possa servire file statici (come HTML, CSS, immagini)
    e gestire richieste HTTP GET di base. Il server deve essere in grado di gestire più richieste
    simultaneamente e restituire risposte appropriate ai client.
'''
#Imports
import sys, signal
import http.server
import socketserver

#Inizializzo un indirizzo e porta standard su cui sarà possibile interfacciarsi col server.
STANDARD_ADDRESS = "localhost"
STANDARD_PORT = 8080

#Verifico gli argomenti passati da linea di comando, se non vengono passati correttamente la porta è impostata ad un valore standrd
if(len(sys.argv) == 1):
    PORT = STANDARD_PORT
else:
    PORT = int(sys.argv[1])

#Descrivo il comportamento da eseguire dal server in caso di richiesta get.
class HTTPHandler(http.server.SimpleHTTPRequestHandler):
     def do_GET(self):
        path = self.path
        client_ip, client_port = self.client_address
        command = self.command
        print(f"Request (Type: {command} for path: {self.path})  received from... {client_ip}:{client_port}")
        return super().do_GET()

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