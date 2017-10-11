# Realtime Quiz Game Using Sockets
## Alternating Quiz With Option To Challenge
The quiz server and the client have been written in python 2. To run the quiz, open the server(**server1.py**) and enter the network credentials, followed by opening two instances of the client(**client.py**) and entering the network credentials.
The two players can play on the two instances of the client, alternately answering questions.
There is also a possibility to challenge a question before it is asked, and in case the designated person incorrectly replies to it, reply it correctly to gain bonus marks, but receive heavy peanlty upon giving wrong answer.
The program uses TCP Sockets

## _extra_ Buzzer Round Quiz
This is another implementation of a quiz server which supports a Buzzer round, i.e. two players can simultaneously answer and the person who replies correctly, earlier is rewarded.
The program uses _threading_ and TCP Sockets.
To run the quiz, open the server(**server_buzzer.py**) and enter the network credentials, followed by opening two instances of the client(**client.py**) and entering the network credentials.

## Scoring Scheme
1. Correct Answer : 10 points
2. Incorrect Answer
    * Normal : 0 points
    * Challenge : -10 points