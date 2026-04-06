import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Branding Information
DEVELOPER = "@sakib01994"
GROUP_LINK = "@publicgroup5s"

def get_truecaller_info(phone_number):
    # Main API URL
    api_url = f"https://prod-api.telebothost.com/ownlang/webapp/64472422/apix?number={phone_number}&key=truecallerinfolookupbot-5556909453-IR2s3K"
    
    # ব্রাউজার হিসেবে নিজেকে উপস্থাপন করার জন্য হেডার (এটি এরর ফিক্স করবে)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # চেক করা হচ্ছে রেসপন্স খালি কি না
        if not response.text:
            return {"status": "error", "message": "Main API returned empty response."}
            
        data = response.json()
        
        if data.get("ok") and data.get("data", {}).get("success"):
            info = data["data"]
            
            # প্রিমিয়াম জেসন ফরম্যাট
            premium_response = {
                "ok": True,
                "developer": DEVELOPER,
                "group": GROUP_LINK,
                "results": {
                    "name": info.get("name", "No Name Found"),
                    "number": phone_number,
                    "international_format": info.get("international_format", "N/A"),
                    "carrier": info.get("carrier", "N/A"),
                    "location": info.get("location", "N/A"),
                    "country": info.get("country", "N/A"),
                    "image": info.get("image_url", ""),
                    "social": {
                        "facebook": info.get("facebook", "N/A"),
                        "whatsapp": f"https://wa.me/{phone_number.replace('+', '')}",
                        "telegram": f"https://t.me/{phone_number.replace('+', '')}"
                    }
                },
                "status": "Success"
            }
            return premium_response
        else:
            # যদি এপিআই লিমিট শেষ হয় বা নাম্বার না পাওয়া যায়
            return {
                "ok": False,
                "status": "error", 
                "message": "Data not found or API Limit reached."
            }
            
    except requests.exceptions.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON from source API."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/lookup', methods=['GET'])
def lookup():
    number = request.args.get('number')
    if not number:
        return jsonify({"ok": False, "message": "Number parameter is missing!"}), 400
    
    result = get_truecaller_info(number)
    return jsonify(result)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Truecaller Premium API is running",
        "developer": DEVELOPER
    })

# Vercel এর জন্য প্রয়োজনীয়
if __name__ == '__main__':
    app.run(debug=True)
