#!/usr/bin/env python
import socket
import sys

def question(s):
    ques = s.recv(1024)
    print ques,
    ans = raw_input("Answer: ")
    while ans not in ['A', 'B', 'C', 'D']:
        print "Enter a valid choice!"
        ans = raw_input("Answer: ")
    s.sendall(ans)
    response = s.recv(1024)
    print response

def scores(s):
    prompt = s.recv(1024)
    print prompt

def challenge(s):
    prompt = s.recv(1024)
    print prompt
    ans = raw_input("Response: ")
    while ans not in ['Y', 'N']:
        print "Enter a valid choice!"
        ans = raw_input("Answer: ")
    s.sendall(ans)

def final(s):
    prompt = s.recv(1024)
    print prompt

HOST = 'localhost'    # The remote host
PORT = int(raw_input("Enter the port number to which the server is bound: "))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    choice = s.recv(1024)
    if choice[0] == "Q":
        question(s)
    elif choice[0] == "S":
        scores(s)
    elif choice[0] == "C":
        challenge(s)
    elif choice[0] == "X":
        final(s)
        break
    elif choice[0] == "A":
        final(s)
    else:
        print "Invalid choice: ", choice