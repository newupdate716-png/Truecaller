import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Developer Information
DEVELOPER = "@sakib01994"
GROUP_LINK = "@publicgroup5s"

def get_truecaller_info(phone_number):
    # Main API URL
    api_url = f"https://prod-api.telebothost.com/ownlang/webapp/64472422/apix?number={phone_number}&key=truecallerinfolookupbot-5556909453-IR2s3K"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data.get("ok") and data.get("data", {}).get("success"):
            info = data["data"]
            # Formatting Premium JSON
            premium_response = {
                "status": "success",
                "developer": DEVELOPER,
                "community": GROUP_LINK,
                "results": {
                    "name": info.get("name", "N/A"),
                    "number": phone_number,
                    "international_format": info.get("international_format", "N/A"),
                    "carrier": info.get("carrier", "Unknown"),
                    "location": info.get("location", "Unknown"),
                    "country": info.get("country", "N/A"),
                    "image": info.get("image_url", ""),
                    "social_links": {
                        "facebook": info.get("facebook", ""),
                        "whatsapp": f"https://wa.me/{phone_number}",
                        "telegram": f"https://t.me/{phone_number}"
                    }
                },
                "credits": "Powered by SB Sakib"
            }
            return premium_response
        else:
            return {"status": "error", "message": "Information not found or API limit reached."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/lookup', methods=['GET'])
def lookup():
    number = request.args.get('number')
    if not number:
        return jsonify({
            "status": "error", 
            "message": "Please provide a phone number with country code. Example: /lookup?number=+911234567890"
        }), 400
    
    result = get_truecaller_info(number)
    return jsonify(result)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Welcome to Premium Number Lookup API",
        "developer": DEVELOPER
    })

if __name__ == '__main__':
    app.run(debug=True)
