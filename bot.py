import requests
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


#bot id, generate this when going to soecific group
botID = "af9657d944b5151be2b8689846" 


def SendMessage(textToSend):
    payload = {"bot_id": botID, "text": textToSend}

    try: 
        response = requests.post("https://api.groupme.com/v3/bots/post", json=payload)
        if response.status_code == 202:
            return True;

        # if api fails
        print(f"API Error [{response.status_code}]: {response.text}")
        return False;

     #if the post request fails
    except requests.exceptions.RequestException as e:
        print(f"Network subsystem error: {e}")
        return False



@app.route("/callback", methods=["POST"])
def groupme_callback():
    data = request.get_json()

    # We have to check if there's data!
    if not data:
        return "Missing payload", 400

    #no infinite bot message loops
    if data.get("sender_type") == "bot":
        return "Ignored bot message", 200

    #info about message
    
    incomingText = data.get("text", "").strip()
    senderName = data.get("name", "User")

    if incomingText.lower() == "!ping":
        SendMessage(f"Pong! Hello {senderName}.")

    return "OK", 200




#MAIN LINE
if __name__ == "__main__":
   print("Booting up, made with love by Zach Lima <3")
   app.run(host="0.0.0.0", port=5000, debug=True)

   
    



