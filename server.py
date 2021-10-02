#server program
import socket
import sys
import threading

HOST = ''
PORT = 6969

def auth_user():
    pass

def on_connect(conn,addr):
    with conn:
        print('Connected by', addr)

def main():

    sock = socket.socket()
    print("Socket successfully created")
    port = 6969
    sock.bind(('', port))
    
    while True:
        sock.listen(5)
        print("Listening for connections")
        conn, addr = sock.accept()
        threading.Thread(target=on_connect, args=(conn,addr,)).start()
        print(".",end="")

if __name__ == "__main__":
    main()
    
