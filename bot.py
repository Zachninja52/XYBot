import urllib.error
import urllib.request
import os
import json
import base64

print("made with love by Zach Lima <3")
#bot id, generate this when going to soecific group 
botID = os.environ["GROUPME_BOT_ID"]

def SendMessage(textToSend):
    payload = json.dumps({"bot_id": botID, "text": textToSend}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groupme.com/v3/bots/post",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try: 
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 202:
                return True;

        # if api fails
        print(f"API Error [{response.status}]")
        return False;

     #if the post request fails
    except urllib.error.HTTPError as e:
        print(f"API Error [{e.code}]: {e.read().decode('utf-8', 'replace')}")
        return False
    
        # if the post request fails
    except urllib.error.URLError as e:
        print(f"Network subsystem error: {e}")
        return False


def lambda_handler(event,context):
    body = event.get("body");

    # We have to check if there's data!
    if not body:
       return {"statusCode": 400, "body": "Missing payload"}

    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": "Invalid JSON"}

    #no infinite bot message loops
    if data.get("sender_type") == "bot":
        return {"statusCode": 200, "body": "Ignored bot message"}

    #info about message
    
    incomingText = (data.get("text") or "").strip()
    senderName = data.get("name") or "User"

    if incomingText.lower() == "!ping":
        SendMessage(f"Pong! Hello {senderName}.")

    return {"statusCode": 200, "body": "OK"}

   
    



