from flask import Flask, request, render_template
import numpy as np
from keras.models import load_model
import cv2
import os

app = Flask(__name__)
model = load_model("best_model.keras")
model1 = load_model("model1.keras")
model2 = load_model("model2.keras")
model3 = load_model("model3.keras")

models = [model, model1, model2, model3]

os.makedirs('uploads', exist_ok=True)

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Image loading failed.")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)         
    img = cv2.resize(img, (128, 128))
    img = img / 255.0                                  
    img = img.reshape(1, 128, 128, 3).astype('float32') 
    return img
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error_message="No file uploaded")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error_message="No selected file")

    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    img = preprocess_image(filepath)
    predictions = [model.predict(img) for model in models]
    predicted_classes = [prediction[0].argmax() for prediction in predictions]
    predicted_class = max(set(predicted_classes), key=predicted_classes.count)

    if predicted_class == 0:
        result = 'Glioma Tumor'
    elif predicted_class == 1:
        result = 'Meningioma Tumor' 
    elif predicted_class == 2:
        result = 'No Tumor'
    elif predicted_class == 3:
        result = 'Pituitary Tumor'
    else:
        result = 'Unknown'
    confidence = [(prediction[0]/ np.sum(prediction))* 100 for prediction in predictions]
    return render_template('index.html', prediction_text=result, confidence_text=f"Probability: {np.mean([conf[predicted_class] for conf in confidence]):.2f} %")

if __name__ == '__main__':
    app.run(debug=True)