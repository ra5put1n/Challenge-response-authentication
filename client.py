#client program
import socket
import sys
import hashlib

HOST = '127.0.0.1'
PORT = 6969

def new_account(conn):
    username = input("Enter username: ")
    conn.send(username.encode())
    password = input("Enter password: ")
    conn.send(password.encode())
    status = conn.recv(1024).decode()
    if(status == "success"):
        print("Account successfully created.")
    elif(status == "fail"):
        print("Account already exists.")

def login(conn):
    username = input("Enter username: ")
    password = input("Enter password: ")
    conn.send(username.encode())
    status = conn.recv(1024).decode()
    if status == "no_acc":
        print("Account not found! Make an account")
        sys.exit()
    rand_str = conn.recv(1024).decode()
    auth_string = hashlib.md5((password+rand_str).encode())
    conn.send(auth_string.hexdigest().encode())
    status = conn.recv(1024).decode()
    if(status == "success"):
        print("Authentication successful.")
    elif(status == "fail"):
        print("Authentication failed.")

def main():

    conn = socket.socket()
    conn.connect((HOST,PORT)) 
    choice = input("1. Create account\n2. Login\n3. Exit\n Choice: ")
    if choice == "1":
        conn.send("new_account".encode())
        new_account(conn)
    elif choice == "2":
        conn.send("login".encode())
        login(conn)
    elif choice == "3":
        sys.exit()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
