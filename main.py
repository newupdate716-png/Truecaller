import requests
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Branding Information
DEVELOPER = "@sakib01994"
GROUP_LINK = "@publicgroup5s"
TEMP_IMAGE_NAME = "profile_temp.jpg"
TEMP_DIR = "/tmp"  # Vercel supports writing only in /tmp/

def download_and_replace_image(image_url):
    """ইমেজ ডাউনলোড করবে এবং আগেরটি থাকলে ডিলিট করে দিবে"""
    if not image_url:
        return None
    
    file_path = os.path.join(TEMP_DIR, TEMP_IMAGE_NAME)
    
    try:
        # আগের ফাইল থাকলে ডিলিট করে নতুনটা ডাউনলোড করবে
        if os.path.exists(file_path):
            os.remove(file_path)
            
        response = requests.get(image_url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Image Error: {e}")
    return False

def get_truecaller_info(phone_number, base_url):
    api_url = f"https://prod-api.telebothost.com/ownlang/webapp/64472422/apix?number={phone_number}&key=truecallerinfolookupbot-5556909453-IR2s3K"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("ok") and data.get("data", {}).get("success"):
            info = data["data"]
            original_image = info.get("image_url", "")
            
            # ইমেজ ডাউনলোড প্রসেস
            local_image_url = ""
            if original_image:
                success = download_and_replace_image(original_image)
                if success:
                    # আমাদের ডোমেইনের ইমেজ লিঙ্ক তৈরি
                    local_image_url = f"{base_url}get_image"

            # প্রিমিয়াম জেসন স্ট্রাকচার
            premium_response = {
                "ok": True,
                "developer": DEVELOPER,
                "community": GROUP_LINK,
                "results": {
                    "name": info.get("name", "No Name Found"),
                    "number": phone_number,
                    "international_format": info.get("international_format", "N/A"),
                    "carrier": info.get("carrier", "N/A"),
                    "location": info.get("location", "N/A"),
                    "country": info.get("country", "N/A"),
                    "image": local_image_url,  # আপনার নিজস্ব এপিআই এর ইমেজ লিঙ্ক
                    "social": {
                        "facebook": info.get("facebook", "N/A"),
                        "whatsapp": f"https://wa.me/{phone_number.replace('+', '')}",
                        "telegram": f"https://t.me/{phone_number.replace('+', '')}"
                    }
                },
                "status": "Success",
                "message": "Data fetched and image updated successfully."
            }
            return premium_response
        else:
            return {"ok": False, "status": "error", "message": "Data not found or API Limit reached."}
            
    except Exception as e:
        return {"ok": False, "status": "error", "message": str(e)}

@app.route('/lookup', methods=['GET'])
def lookup():
    number = request.args.get('number1')
    if not number:
        return jsonify({"ok": False, "message": "Number parameter is missing!"}), 400
    
    # বর্তমান ডোমেইন ইউআরএল গেট করা
    base_url = request.host_url
    result = get_truecaller_info(number, base_url)
    return jsonify(result)

@app.route('/get_image')
def get_image():
    """এই রাউটটি সেভ করা ইমেজটি প্রদর্শন করবে"""
    return send_from_directory(TEMP_DIR, TEMP_IMAGE_NAME)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Truecaller Premium Local Image API",
        "developer": DEVELOPER,
        "endpoint": "?number="
    })

if __name__ == '__main__':
    app.run(debug=True)
