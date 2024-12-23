from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle


app = FastAPI()

# Load the trained model and vectorizer
with open("Trained Models\\movie_review_sentiment_analysis_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("Trained Models\\count_vectorizer.pkl", "rb") as file:
    cv = pickle.load(file)  

class TextInput(BaseModel):
    text: str

@app.post("/predict/")
async def predict_sentiment(text: TextInput):
    try:
        input_data = [text.text]
        vectorized_data = cv.transform(input_data)
        prediction = model.predict(vectorized_data)
        
        sentiment = "Positive" if prediction[0] == 1 else "Negative"
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict_batch/")
async def predict_sentiments_batch(texts: list[TextInput]):
    try:
        input_data = [t.text for t in texts]
        vectorized_data = cv.transform(input_data)
        predictions = model.predict(vectorized_data)
        
        sentiments = [{"text": t.text, "sentiment": "Positive" if p == 1 else "Negative"} for t, p in zip(texts, predictions)]
        return {"predictions": sentiments}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

