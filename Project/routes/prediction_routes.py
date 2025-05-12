# # routes/prediction_routes.py
# from flask import Blueprint, request, jsonify, render_template_string
# from ultralytics import YOLO
# from PIL import Image
# import numpy as np
# import cv2
# prediction_bp = Blueprint("prediction", __name__)

# # Load your model once (you can also set up lazy loading if preferred)
# model_path = 'models/best.pt'
# model = YOLO(model_path)

# @prediction_bp.route('/predict', methods=['GET'])
# def predict_form():
#     form_html = """
#     <!doctype html>
#     <html lang="en">
#       <head>
#         <title>Medicine Inspection - Upload Image</title>
#       </head>
#       <body>
#         <h2>Upload an Image for Prediction</h2>
#         <form action="/predict" method="post" enctype="multipart/form-data">
#           <input type="file" name="file">
#           <input type="submit" value="Upload">
#         </form>
#       </body>
#     </html>
#     """
#     return render_template_string(form_html)

# @prediction_bp.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
    
#     try:
#         image = Image.open(file.stream).convert('RGB')
#     except Exception:
#         return jsonify({'error': 'Invalid image format.'}), 400
    
    
    
#     # Convert the image to a NumPy array since YOLO expects it
#     image_np = np.array(image)

#     # Run the model on the image; results is a list of inference results for the input(s)
#     results = model(image_np, verbose=False)

#     predictions = []
#     if results and len(results) > 0:
#         boxes = results[0].boxes
#         for box in boxes:
#             coords = box.xyxy[0].tolist()  # [xmin, ymin, xmax, ymax]
#             conf = box.conf.item()
#             cls = int(box.cls.item())
#             predictions.append({
#                 'box': coords,
#                 'confidence': round(conf, 3),
#                 'class': cls
#             })
        
            

#     return jsonify({'predictions': predictions})




