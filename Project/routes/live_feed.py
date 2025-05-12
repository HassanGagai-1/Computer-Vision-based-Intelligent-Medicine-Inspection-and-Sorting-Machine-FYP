from flask import Blueprint, Response, render_template, current_app
import cv2
from ultralytics import YOLO

live_feed_bp = Blueprint('live_feed', __name__)
# 2) Open the IP‑Webcam stream once
stream_url = "http://192.168.113.80:8080/video"  # your phone’s IP
cap = cv2.VideoCapture(stream_url)

# 3) Load your YOLO model (just once)
model = YOLO("best.pt")


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break  
        
        # 1. (Optional) resize & letterbox to 640×640 for consistent aspect ratio
        frame_resized = cv2.resize(frame, (640, 640))

        results = model(frame_resized, conf=0.5, iou=0.4, max_det =1)

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf_score = float(box.conf[0].cpu().numpy())
            cls_id      = int(box.cls[0].cpu().numpy())
            label       = model.names[cls_id]
            print(f"[DETECT] {label:<12} conf={conf_score:.2f}  box=({x1:.0f},{y1:.0f})→({x2:.0f},{y2:.0f})")

        results = model(frame)
        
        
        annotated = results[0].plot()

        # 6) JPEG‑encode
        ret, buffer = cv2.imencode('.jpg', annotated)
        if not ret:
            continue
        jpg = buffer.tobytes()

        # 7) Yield in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

@live_feed_bp.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src tag of an img element."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@live_feed_bp.route('/live_feed')
def live_feed():
    """Simple page with an <img> tag pointing to our video feed."""
    return render_template('live_feed.html')