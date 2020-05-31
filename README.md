# vk-bruins
Von Karman Hackathon Project - Rescue Rover<br/>
<br/>
Python | OpenCV | Pyzbar | Sockets | Raspberry Pi<br><br>
FIRST PLACE: Software Lead for a Mars Rescue Rover. Using Raspberry Pis to enable IR Cameras for QR Decoder. Video Streams from Pi to PC with Object Detection and Dimensions using Sockets / OpenCV. Terrain Map of QR Codes.<br><br>
To Start Stream: (https://altax.net/blog/low-latency-raspberry-pi-video-transmission/)<br/>
ON MAC (I don't know about windows) in your current directory: 'netcat -l -p 5000 | mplayer -fps 60 -cache 1024 -'<br/>

ON RASPBERRY PI: cd to the Working Directory and run './streamstart.sh'. If you don't have permissions, run 'sudo chmod 777 streamstart.sh'<br/>

Do the Mac Command First, then the Raspberry Pi Command, since the Mac Acts like a Server to Connect the Client (Raspberry Pi)<br/>

To Start QR Decoder: (https://www.youtube.com/watch?v=u4Gfhrxm1FE&t=2s) | (https://github.com/Polyconseil/zbarlight)<br/>
ON RASPBERRY PI: Make sure the PiCamera is connected.<br/>
Video Mode: python qr_decode_video.py<br/>
Image Processing (NOT REALLY NEEDED - JUST FOR MY TESTS): python qr_decode_image.py --image IMAGE.png<br/>
