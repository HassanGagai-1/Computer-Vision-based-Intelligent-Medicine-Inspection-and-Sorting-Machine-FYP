# # cap = cv2.VideoCapture(stream_url)
# # if not cap.isOpened():
# #     print("Unable to open video stream. Check URL and network.")
# #     exit(1)

# # # Read one frame to test
# # ret, frame = cap.read()
# # if ret:
# #     print("Frame captured, resolution:", frame.shape)
# # else:
# #     print("Failed to retrieve frame from stream.")


# import cv2
# stream_url = "http://192.168.0.177:8080/video"  # replace with your phone's IP
# webcam = cv2.VideoCapture(stream_url)


# from ultralytics import YOLO
# model = YOLO("best.pt")  # loads the model (weights)  

# import torch
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# from flask import Flask, Response, render_template

# app = Flask(__name__)

# def generate_frames():
#     """Read frames from the camera, run YOLO, and yield JPEG bytes."""
#     while True:
#         success, frame = webcam.read()
#         if not success:
#             break  # If stream ended, exit loop
#         # Run detection
#         results = model(frame)
#         annotated_frame = results[0].plot()  # draw boxes on the frame
#         # Encode frame to JPEG
#         ret, buffer = cv2.imencode('.jpg', annotated_frame)
#         frame_bytes = buffer.tobytes()
#         # Yield frame in HTTP multipart format
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



# while True:
#     ret, frame = webcam.read()
    
#     if ret == True:
#         cv2.imshow("koolac", frame)
#         key = cv2.waitKey(1)
#         if key == ord("q"):
#             break
        
# webcam.release()
# cv2.destroyAllWindows()


