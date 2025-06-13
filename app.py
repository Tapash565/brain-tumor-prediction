from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import numpy as np
from keras.models import load_model
import cv2
import os
import shutil

app = FastAPI()

# Mount static directory for CSS and assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load the Keras model
model = load_model("model2.keras")

# Ensure 'uploads' directory exists
os.makedirs("uploads", exist_ok=True)

# Preprocessing helper

def preprocess_image(img_path: str):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Image loading failed.")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = img.reshape(1, 128, 128, 3).astype('float32')
    return img

@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', { 'request': request })

@app.post('/predict', response_class=HTMLResponse)
async def post_predict(request: Request, file: UploadFile = File(...)):
    # Save uploaded file
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        img = preprocess_image(filepath)
        prediction = model.predict(img)
        predicted_class = int(np.argmax(prediction[0]))
        confidence = (prediction[0] / np.sum(prediction[0])) * 100
        labels = ['Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']
        result = labels[predicted_class] if predicted_class < len(labels) else 'Unknown'
        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'prediction_text': result,
                'confidence_text': f"Probability: {confidence[predicted_class]:.2f} %"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            'index.html',
            { 'request': request, 'error_message': str(e) }
        )

# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)