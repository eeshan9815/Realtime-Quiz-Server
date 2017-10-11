#!/usr/bin/env python
import socket
import threading
import sys
import time
HOST = 'localhost'
PORT = int(raw_input("Enter the port number to bind with: "))
score = [0, 0]
totalQuestions = int(raw_input("Enter the total number of questions: "))
filename = raw_input("Enter the name of the quiz file: ")
f = open(filename, 'r')
def askQuestion(connlist, playerNo, isChallenge, challenger, ques, ans):
    global score
    global f
    connlist[playerNo].sendall("Q\n")
    time.sleep(0.1)
    connlist[playerNo].sendall(ques+"\n")          #sendall question
    time.sleep(0.1)
    data = connlist[playerNo].recv(1024)                    #receive answer
    if ans == data + '\n':
        score[playerNo]+=10
        connlist[playerNo].sendall("Correct Answer\n")
        time.sleep(0.1)
    else:
        if isChallenge:
            askQuestion(connlist, 1-playerNo, False, True, ques, ans)
        if challenger:
            score[playerNo]-=10
        connlist[playerNo].sendall("Incorrect Answer\n")
        time.sleep(0.1)
def sendallScore(connlist):
    global score
    for i, conn in enumerate(connlist):
        conn.sendall("S\n")
        time.sleep(0.1)
        conn.sendall("Player "+str(i+1)+", your score is: "+str(score[i])+"\n")
        time.sleep(0.1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print "Server bound to ", HOST, ":", PORT, "\nConnect both players before continuing..."
(conn1, addr) = s.accept()
print "Connected to Player 1 at ", addr
(conn2, addr) = s.accept()
connlist = [conn1, conn2]
conn1.sendall("A\n")
time.sleep(0.1)
conn1.sendall("You are Player 1\n")
time.sleep(0.1)
conn2.sendall("A\n")
time.sleep(0.1)
conn2.sendall("You are Player 2\n")
time.sleep(0.1)
print "Connected to Player 2 at ", addr
for questionNo in range(totalQuestions):
    conn1.sendall("A\n")
    time.sleep(0.1)
    conn1.sendall("Question Number "+str(questionNo+1)+" for Player "+str(questionNo%2+1)+"\n")
    time.sleep(0.1)
    conn2.sendall("A\n")
    time.sleep(0.1)
    conn2.sendall("Question Number "+str(questionNo+1)+" for Player "+str(questionNo%2+1)+"\n")
    time.sleep(0.1)
    #TODO make function
    connlist[1 - questionNo%2].sendall("C\n")
    time.sleep(0.1)
    connlist[1 - questionNo%2].sendall("Do you want to challenge the next question?(Y/N)\n")
    time.sleep(0.1)
    data = connlist[1 - questionNo%2].recv(1024)
    if data[0] == "Y":
        isChallenge = True
    elif data[0] == "N":
        isChallenge = False
    else:
        print "SOMETHING WEIRD"
    ques = f.readline()
    ans = f.readline()
    askQuestion(connlist, questionNo%2, isChallenge, False, ques, ans)
    sendallScore(connlist)
if score[0]>score[1]:
    print "Player 1 won, with score: ", score
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("YOU WON\n")
    time.sleep(0.1)
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("YOU LOST\n")
    time.sleep(0.1)
elif score[0]<score[1]:
    print "Player 2 won, with score: ", score
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("YOU WON\n")
    time.sleep(0.1)
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("YOU LOST\n")
    time.sleep(0.1)
else:
    print "It's a tie, with score: ", score
    conn1.sendall("X\n")
    time.sleep(0.1)
    conn1.sendall("IT'S A TIE\n")
    time.sleep(0.1)
    conn2.sendall("X\n")
    time.sleep(0.1)
    conn2.sendall("IT'S A TIE\n")
    time.sleep(0.1)
s.close()
