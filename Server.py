import socket
import datetime as dt
import threading
import Verify as av


# Select an appropriate port number. 
PORT = 5050
# Set The Server's IP Address
SERVER_IP = socket.gethostbyname(socket.gethostname())
print(SERVER_IP)
# Set up the Server's Address
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

# Add code to initialize the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Write Code to bind Address to the server socket.
server.bind(ADDR)

 # This function processes messages that are read through the Socket.
def clientHandler(conn, addr): 
    # Write Code that allows the Server to receive a connection code from an Agent. 
    secretCode = conn.recv(1024).decode('utf-8')
    print(f"[CODE RECEIVED] {secretCode}")


    # Write Code that allows the Server to check if the connection code received is valid. 
    validORNOT = av.check_conn_codes(secretCode)
    print(f"[CODE VALID] {validORNOT}") 
    if type(validORNOT) is str:
        valid = True
        print(f"[NEW CONNECTION] {addr} connected.")
    else:        
        print("[CONNECTION CLOSED] Incorrect response!")
        return 

    
    while valid:

        # Write Code that allows the Server to retrieve a random secret question.
        question = av.getSecretQuestion()

        print(f"[SECRET QUESTION]{question[0]}")
        print(f"[SECRET ANSWER]{question[1]}")
        

        # Write Code that allows the Server to send the random secret question to the Client.
        secretQuestion = question[0]
        conn.send(secretQuestion.encode(FORMAT))
        

        # Write Code that allows the Server to receive an answer from the Client.
        agentAnswer = conn.recv(1024).decode('utf-8')
        print(f"[AGENTANSWER] {agentAnswer}")

        # Write Code that allows the Server to check if the answer received is correct.
        answer = question[1]
        if answer == agentAnswer:
            print(f"[CORRECT ANSWER GIVEN]")
            # Write Code that allows the Server to Send Welcome message to agent -> "Welcome Agent X" 
            """Your Code here"""
            today = dt.datetime.now()
            date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
            message = "Welcome " + validORNOT + " Time Logged-" + date_time
            print(message)
            conn.send(message.encode("utf-8"))
            break
        else:
            print(f"[CONNECTION CLOSED] Incorrect Answer")
            valid = False


def runServer():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=clientHandler, args=(conn,addr) )
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count() - 1}")

print("[STRTING] The Server is Starting...")
runServer()