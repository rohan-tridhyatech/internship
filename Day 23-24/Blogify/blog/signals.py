from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Post

@receiver(post_save, sender=Post)
def predict_sentiment(sender, instance, created, **kwargs):
    if created: 
        api_url = "http://127.0.0.1:5000/predict/" 
        payload = {"text": instance.content}
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()  
            sentiment = response.json().get("sentiment", "Neutral")  
            instance.sentiment = sentiment
            instance.save(update_fields=["sentiment"]) 
        except requests.RequestException as e:
            print(f"Failed to fetch sentiment: {e}")
