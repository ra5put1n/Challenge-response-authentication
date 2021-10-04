#server program
import socket
import os
import hashlib
import threading
import sqlite3
import random
import string

HOST = ''
PORT = 6969

#function to generate random string
def random_string():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def create_user(db_conn,username,password):
	cursor = db_conn.cursor()
	cursor.execute('insert into usernames (name, password) values (?, ?)', (username, password,))
	db_conn.commit()

def fetch_user(db_conn,username):
	cursor = db_conn.cursor() 
	cursor.execute('select password from usernames where name = ?', (username,))
	rows = cursor.fetchall()
	return rows

def new_account(conn,db_conn):
	username = conn.recv(1024).decode()
	password = conn.recv(1024).decode()
# 	print(username,password)
# 	print(fetch_user(db_conn,username))
	if fetch_user(db_conn,username) == []:
		create_user(db_conn,username,password)
		conn.send("success".encode())
	else:
		conn.send("fail".encode())

def login(conn,db_conn):

	username = conn.recv(1024).decode()
	user_data = fetch_user(db_conn,username)
	password = user_data[0][0]
	rand_str = random_string()
	conn.send(rand_str.encode())
	auth_string = hashlib.md5((password+rand_str).encode()).hexdigest()
	challenge_response = conn.recv(1024).decode()
	if auth_string == challenge_response:
		conn.send("success".encode())
	else:
		conn.send("fail".encode())
		conn.close()

def on_connect(conn,addr):

	database = "users.db"

	db_conn = create_connection(database)
	if db_conn is not None:
	# create projects table
		create_table(db_conn)
		print("Table created.")
	else:
		print("Error! cannot create the database connection.")

	print("Connected to database")
	print('Connected by', addr)
	choice = conn.recv(1024).decode()
	if choice == "new_account":
		new_account(conn,db_conn)
	elif choice == "login":
		login(conn,db_conn)
	else:
		return
	
def create_connection(db_file):

	try:
		db_conn = sqlite3.connect(db_file)
		return db_conn
	except:
		print("Error in connection creation.")

	return None

def create_table(db_conn):

	create_table_sql = """ CREATE TABLE IF NOT EXISTS usernames(
										id integer primary key AUTOINCREMENT,
										name nvarchar(40) not null,
										password nvarchar(32) not null
						); """
	try:
		c = db_conn.cursor()
		c.execute(create_table_sql)
	except:
		print("Cannot Create Table")

def main():

	sock = socket.socket()
	print("Socket successfully created")
	port = 6969
	sock.bind(('', port))
	print("Listening for connections")

	while True:
		sock.listen(5)    
		conn, addr = sock.accept()
		threading.Thread(target=on_connect, args=(conn,addr,)).start()

if __name__ == "__main__":
	main()
	
