import requests


flask_url = "http://localhost:5001/flask-webhook"


payload = {
    "chatInput": "Who is rizal",
}

print(f"Sending to Flask: {payload}")

try:
  
    response = requests.post(flask_url, json=payload)
    

    print("\n Response from Flask (and n8n):")
    print(response.text)
    
except Exception as e:
    print(f"\n Error: {e}")
    print("Make sure a2.py is running!")
