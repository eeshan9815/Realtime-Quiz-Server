# Video RTC App
I built a web-app using [Easy RTC](https://github.com/priologic/easyrtc) for a simple video/audio call with the help of official documentation. 
It works locally, but apparently apps running on Chrome browsers can't access local cameras and microphones unless the application is hosted from localhost or an SSL server (https), and the SSL port 22 is blocked on the campus network, so video calling was not possible on the campus network, and I was unsuccessful in finding any viable workarounds for it.
I also tried to build it using [PeerJS](https://github.com/peers/peerjs), but faced similar issues. Even the demo of PeerJS was unable to run on the campus network, which works on mobile data. 
I don't have any experience with web development yet, and this was my first web project. Also, I didn't know a lot about how to set up STUN/TURN servers for the communication.
