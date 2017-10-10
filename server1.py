#!/usr/bin/env python
import socket
import threading
#TODO remove global variables
HOST = 'localhost'
PORT = int(raw_input("Enter the port number to bind with: "))
score = [0, 0]
totalQuestions = int(raw_input("Enter the total number of questions: "))
filename = raw_input("Enter the name of the quiz file: ")
f = open(filename, 'r')
def askQuestion(connlist, playerNo, isChallenge, challenger):
    global totalQuestions
    global score
    global f
    ques = f.readline()
    ans = f.readline()
    connlist[playerNo].sendall("Q")
    connlist[playerNo].sendall(ques)          #send question
    data = conn.recv(1024)                    #receive answer
    if ans == data + '\n':
        score[playerNo]+=10
        connlist[playerNo].sendall("Correct Answer")
    else:
        if isChallenge:
            askQuestion(connlist, 1-playerNo, False, True)
        if challenger:
            score[playerNo]-=10
        conn.sendall("Incorrect Answer")
def sendScore(connlist):
    global score
    for i, conn in enumerate(connlist):
        conn.sendall("S")
        conn.sendall("Player "+str(i+1)+", your score is: "+str(score[i]))
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
    #TODO make function
    connlist[1 - questionNo%2].sendall("C")
    connlist[1 - questionNo%2].sendall("Do you want to challenge the next question? ")
    data = connlist[1 - questionNo%2].recv(1024)
    if data[0] == "Y":
        isChallenge = True
    else if data[0] == "N":
        isChallenge = False
    else:
        print "SOMETHING WEIRD"
    askQuestion(connlist, questionNo%2, isChallenge, False)
    sendScore(connlist)
    # playerThread1 = threading.Thread(target = (askQuestion if questionNo%2 == 0 else askChallenge), name = "Thread1", args = (conn1, 0))
    # playerThread2 = threading.Thread(target = (askQuestion if questionNo%2 == 1 else askChallenge), name = "Thread2", args = (conn2, 1))
    # playerThread1.start()
    # playerThread2.start()
    # playerThread1.join()
    # playerThread2.join()
    # TODO Buzzer Round Implementation using threading, threading not required for current task
if score[0]>score[1]:
    conn1.sendall("X")
    conn1.sendall("YOU WON")
    conn2.sendall("X")
    conn2.sendall("YOU LOST")
elif score[0]<score[1]:
    conn2.sendall("X")
    conn2.sendall("YOU WON")
    conn1.sendall("X")
    conn1.sendall("YOU LOST")
else:
    conn1.sendall("X")
    conn1.sendall("IT'S A TIE")
    conn2.sendall("X")
    conn2.sendall("IT'S A TIE")
s.close()