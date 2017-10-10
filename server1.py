import socket
import threading

HOST = 'localhost'
PORT = int(raw_input("Enter the port number to bind with: "))

score = [0, 0]
# questionNo = 0
totalQuestions = int(raw_input("Enter the total number of questions: "))
filename = raw_input("Enter the name of the quiz file: ")
f = open(filename, 'r')
playOn = True
def askQuestion(conn, playerNo):
    # global questionNo
    global totalQuestions
    global score
    global f
    global playOn
    ques = f.readline()
    ans = f.readline()
    conn.sendall("Q")
    conn.sendall(ques)          #send question
    data = conn.recv(1024)      #receive answer
    if ans == data + '\n':
        score[playerNo]+=10
        conn.sendall("Correct Answer")
    else:
        conn.sendall("Incorrect Answer")
    # questionNo+=1
    # if questionNo == totalQuestions:
        # playOn = False
def askChallenge(conn, playerNo):
    # global questionNo
    global totalQuestions
    global score
    global f
    global playOn




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print "Server bound to ", HOST, ":", PORT, "\nConnect both players before continuing\n\n"
(conn1, addr) = s.accept()
print "Connected to Player 1 at ", addr
(conn2, addr) = s.accept()
connlist = [conn1, conn2]
print "Connected to Player 2 at ", addr
for questionNo in range(totalQuestions):
    conn1.sendall("A")
    conn1.sendall("Question Number "+str(questionNo)+" for Player "+str(questionNo%2+1))
    conn2.sendall("A")
    conn2.sendall("Question Number "+str(questionNo)+" for Player "+str(questionNo%2+1))
    playerThread1 = threading.Thread(target = (askQuestion if questionNo%2 == 0 else askChallenge), name = "Thread1", args = (conn1, 0))
    playerThread2 = threading.Thread(target = (askQuestion if questionNo%2 == 1 else askChallenge), name = "Thread2", args = (conn2, 1))
    playerThread1.start()
    playerThread2.start()
    playerThread1.join()
    playerThread2.join()
conn1.sendall("X")
conn2.sendall("X")
s.close()