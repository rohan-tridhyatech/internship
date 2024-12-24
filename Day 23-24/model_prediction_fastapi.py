from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import pickle

# Create an instance of the FastAPI application
app = FastAPI()

# Load the trained sentiment analysis model from a pickle file
with open("Trained Models\\movie_review_sentiment_analysis_model.pkl", "rb") as file:
    model = pickle.load(file)  # Load the machine learning model

# Load the trained count vectorizer from a pickle file
with open("Trained Models\\count_vectorizer.pkl", "rb") as file:
    cv = pickle.load(file)  # Load the vectorizer for text transformation

# Define a Pydantic model for the input schema
class TextInput(BaseModel):
    text: str  # Input text field for sentiment analysis

# Endpoint for predicting sentiment of a single text input
@app.post("/predict/")
async def predict_sentiment(text: TextInput):
    try:
        # Prepare the input data for the model
        input_data = [text.text]
        
        # Transform the input text using the loaded count vectorizer
        vectorized_data = cv.transform(input_data)
        
        # Make the prediction using the loaded model
        prediction = model.predict(vectorized_data)
        
        # Map the prediction to the corresponding sentiment
        sentiment = "Positive" if prediction[0] == 1 else "Negative"
        
        # Return the sentiment as a JSON response
        return {"sentiment": sentiment}
    except Exception as e:
        # Handle errors and raise an HTTP exception with a 400 status code
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint for predicting sentiment of multiple text inputs in a batch
@app.post("/predict_batch/")
async def predict_sentiments_batch(texts: list[TextInput]):
    try:
        # Extract the text from each TextInput object in the list
        input_data = [t.text for t in texts]
        
        # Transform the batch of input texts using the loaded count vectorizer
        vectorized_data = cv.transform(input_data)
        
        # Make predictions for all input texts in the batch
        predictions = model.predict(vectorized_data)
        
        # Map predictions to sentiments and prepare the response
        sentiments = [{"text": t.text, "sentiment": "Positive" if p == 1 else "Negative"} for t, p in zip(texts, predictions)]
        
        # Return the batch predictions as a JSON response
        return {"predictions": sentiments}
    except Exception as e:
        # Handle errors and raise an HTTP exception with a 400 status code
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000) 