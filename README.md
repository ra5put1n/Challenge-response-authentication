# challenge-response-authentication
Challenge-response protocol using a symmetric key cipher.
## Procedure:
1. Client sends uername and password.
2. Server checks if user exists and if he doesn't creates a new user in the database.
3. The server then generates a random number and sends it to the user.
4. The user hashes the concatenated result of password+random number and sends it back to the server. 
5. The server does the same operation and checks if the results are the same.
6. If the results match, the client gets connected else the connection is dropped.
