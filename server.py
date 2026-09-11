from flask import Flask, render_template, jsonify, send_from_directory, request, session
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "pankaj_secret_key_here"

# Email Configuration
SENDER_EMAIL = "maypaysecure@gmail.com"
SENDER_PASSWORD = "lojq zhtq txqf mmrb"

VIP_USERS = ["pankajkhatik0999@gmail.com", "vipuser@gmail.com"]

# User database store karne ke liye (Email -> {"password": "...", "role": "..."})
REGISTERED_USERS = {
    "pankajkhatik0999@gmail.com": {"password": "adminpassword", "role": "owner"}
}

# Temporary OTP storage (Email -> OTP)
OTP_STORAGE = {}

SONGS_DATABASE = {
    "dhundle manzar": {
        "display_name": "Dhundle Manzar",
        "artist": "Sarckey Kohli",
        "audio_url": "/static/dhundle_song.mp3",
        "video_url": "/static/anime_walk.mp4",
        "official_url": "https://www.youtube.com/results?search_query=Dhundle+Manzar+Sarckey+Kohli",
        "is_premium": False,
        "lyrics_timed": [
            {"time": 0.0, "text": "Dhundle hue hain manzar mere.."},
            {"time": 3.0, "text": "Tu raahein inhehin dikhana..."},
            {"time": 6.0, "text": "Jo zero se vaasta hai mera..."},
            {"time": 8.0, "text": "Tu rehmat ka hai fasana..."},
            {"time": 12.0, "text": "Kaagzon pe jaise, bikhri hai siyahi..."},
            {"time": 17.0, "text": "Kahani tu apni yun kar bayaan..."},
            {"time": 20.0, "text": "Mere dil pe asi chahi..."},
            {"time": 23.0, "text": "Tu hi tu muje mein samaye..."},
            {"time": 26.0, "text": "Ban gyi mere kudayi baliya..."}
        ]
    },
    "rose garden": {
        "display_name": "Rose Garden",
        "artist": "Lata Mangeshkar",
        "audio_url": "/static/Rose_Garden.mp3",
        "video_url": "/static/Rose_Garden_Video.mp4",
        "official_url": "https://www.youtube.com/results?search_query=Rose+Garden+song",
        "is_premium": True,
        "lyrics_timed": [
            {"time": 0.0, "text": "Phoolan aale garden leju tanne main..."},
            {"time": 3.5, "text": "Dil jaan sab kuch deju tanne main..."},
            {"time": 7.0, "text": "Dil aale badala mein pyar bhara se..."},
            {"time": 10.0, "text": "Aaja pyar aali boonda ke mah.."},
            {"time": 10.5, "text": "Bheju tanne main..."},
            {"time": 12.0, "text": "Tere birthday pe karenge.."},
            {"time": 14.0, "text": "Plan tour bahar ka..."},
            {"time": 16.0, "text": "Dekh liye tu bhi badda.."},
            {"time": 16.7, "text": "Kalja se yaar ka.."},
            {"time": 18.0, "text": "A to z sari ae demand poori hovegi..."},
            {"time": 21.0, "text": "Udate tyme dekhda na 100 ka 1000 ka.."},
            {"time": 24.0, "text": "Pyar ka bhi tohra ghana khas bawali.."},
            {"time": 27.0, "text": "Koi ayi ni tere siwa raas bawli..."},
            {"time": 29.0, "text": "Bajrangi ka pujari ib puje bhole ne...."},
            {"time": 32.0, "text": "Tanne paan tahi rakhe upwas bawli..."},
            {"time": 35.0, "text": "Phoolan aale garden leju tanne main...."},
            {"time": 38.0, "text": "Dil jaan sab kuch deju tanne main.."},
            {"time": 41.0, "text": "Dil aale badala mein pyar bhara se.."},
            {"time": 43.0, "text": "Aaja pyar aali boonda ke mah...."},
            {"time": 44.0, "text": "Bheju tanne main...."},
            {"time": 46.0, "text": ".........."},
            {"time": 57.0, "text": "Batue se muh jissi pote ki se bahu..."},
            {"time": 61.0, "text": "Dekh dekh chaa chade dadi kare nyuh.."},
            {"time": 64.0, "text": "Ladiye na kade meri baat maniye...."},
            {"time": 66.0, "text": "Meri maa bhi tane rakhegi re betiya ki jyun.."},
            {"time": 69.0, "text": "Nyun ki re nyun jamma laage tu pari..."},
            {"time": 72.0, "text": "Sar te re pair jamaa rass ki bhari.."},
            {"time": 75.0, "text": "Ndee ndee kundu bass naam ka hi ndee.."},
            {"time": 77.0, "text": "Naa re byah ke tanne delhi te yo..."},
            {"time": 78.0, "text": "Laijega surrey..."},
            {"time": 80.5, "text": "Phoolan aale garden leju tanne main.."},
            {"time": 83.0, "text": "Dil jaan sab kuch deju tanne main.."},
            {"time": 86.0, "text": "Dil aale badala mein pyar bhara se..."},
            {"time": 89.0, "text": "Aaja pyar aali boonda ke mah..."},
            {"time": 90.0, "text": "Bheju tanne main ...."}
        ]
    },
    "The last talk": {
        "display_name": "The last talk",
        "artist": "The Singh",
        "audio_url": "/static/Tha Last Talk.mp3",
        "video_url": "/static/The_Last_Talk_Video.mp4",
        "official_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_premium": False,
        "lyrics_timed": [
            {"time": 0.0, "text": "......."},
            {"time": 25.0, "text": "Sun maa..."},
            {"time": 27.2, "text": "Dekh phasta ja raha hoon"},
            {"time": 29.5, "text": "Duniya ke daldal mein"},
            {"time": 31.5, "text": "Dhasta ja raha hoon"},
            {"time": 33.2, "text": "Daba ke rakhun gham..."},
            {"time": 35.2, "text": "Bata kitne dil mein hai"},
            {"time": 37.2, "text": "Aankhon mein aansu"},
            {"time": 38.8, "text": "Aur hasta ja raha hoon"},
            {"time": 40.2, "text": "Main chahta to tha tujhe"},
            {"time": 42.0, "text": "Sab kuch bata dun"},
            {"time": 43.8, "text": "Laga ke gale"},
            {"time": 45.5, "text": "Sare gham main bhula dun"},
            {"time": 47.5, "text": "Teri aankhon mein aanshu bhate nahi"},
            {"time": 50.5, "text": "Mujhe behtar laga ke"},
            {"time": 52.2, "text": "Main khud ko sula dun"},
            {"time": 54.5, "text": "Tu reh lena mere jaane ke baad"},
            {"time": 57.5, "text": "Zyada na rona mar jaane ke baad"},
            {"time": 60.5, "text": "Has-has ke karna vida mujhko duniya se"},
            {"time": 64.2, "text": "Photo tu lena janaze ke sath"},
            {"time": 67.5, "text": "Dikhane the sath ajube jahan ke"},
            {"time": 70.2, "text": "Dikha bhi na paya, bata bhi na paya"},
            {"time": 73.8, "text": "Batani thi tujhko maa baatein bahut si"},
            {"time": 77.5, "text": "Main kismat ka mara bata bhi na paya"},
            {"time": 81.5, "text": "Saja bhi na paya ma duniya teri"},
            {"time": 85.2, "text": "Teri raahon se kante hata bhi na paya"},
            {"time": 89.0, "text": "Likha tha ek khat bas tere liye"},
            {"time": 92.5, "text": "Tujhe paas bitha ke suna bhi na paya"},
            {"time": 96.0, "text": "......."},
            {"time": 107.0, "text": "Likha tha ek khat bas tere liye"},
            {"time": 110.5, "text": "Tujhe paas bitha ke suna bhi na paya"},
            {"time": 114.0, "text": "Maa main aaunga lekar janam phir dubara"},
            {"time": 118.5, "text": "Main kabil banunga sab hasil karunga"},
            {"time": 122.5, "text": "Tu banna meri maa phir ek janam aur"},
            {"time": 126.5, "text": "Main kabil hoon kitna main sabit karunga"},
            {"time": 130.5, "text": "Tere hisse ke gham main lekar chala"},
            {"time": 134.0, "text": "Mere jaane ke baad tu rona na na"},
            {"time": 137.5, "text": "Mujhe pata hai tu kitna marti hai mujhpe"},
            {"time": 141.5, "text": "Paas photo ko rakh ke tu sona na na"},
            {"time": 145.5, "text": "Tune jhopdi ko ghar banaya hai maa"},
            {"time": 149.5, "text": "Tapti dhoop mein khud ko tapaya hai maa"},
            {"time": 153.5, "text": "Log izzat ya paisa ek hi kamate hain"},
            {"time": 157.5, "text": "Tune to dono kamaya hai maa"},
            {"time": 161.0, "text": "Maa poochti hai to main batata nahi"},
            {"time": 164.5, "text": "Koi bole bhi aur jawab na de"},
            {"time": 168.2, "text": "Uski aankhon mein dekh ke lagta hai mujhko"},
            {"time": 171.8, "text": "Khuda mujh si kisi ko aulaad na de"},
            {"time": 176.0, "text": "Main jitna lad sakta tha khud se lada"},
            {"time": 180.5, "text": "Maa main khud se to jeet gaya magar zindagi se haar gaya"},
            {"time": 187.0, "text": "Mujhe khali jeb aur gareebi ne nahi mara"},
            {"time": 192.5, "text": "Maa tera chhup-chhup ke rona maar gaya"},
            {"time": 198.0, "text": "Maa tera chhup-chhup ke rona maar gaya"},
            {"time": 204.0, "text": "....end😭..."}
        ]
    }
}

@app.route('/')
def home():
    user = session.get('user', None)
    role = session.get('role', 'normal')
    return render_template('index.html', user=user, role=role)

@app.route('/api/songs')
def get_songs():
    return jsonify(SONGS_DATABASE)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and Password are required!"}), 400
    
    if email in REGISTERED_USERS:
        return jsonify({"status": "error", "message": "Email already registered! Please login."}), 400
    
    # Role decide karna
    if email == "pankajkhatik0999@gmail.com":
        role = 'owner'
    elif email in VIP_USERS:
        role = 'vip'
    else:
        role = 'normal'
        
    REGISTERED_USERS[email] = {"password": password, "role": role}
    
    session['user'] = email
    session['role'] = role
        
    return jsonify({"status": "success", "email": email, "role": role})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and Password are required!"}), 400
        
    if email not in REGISTERED_USERS:
        return jsonify({"status": "error", "message": "Email not found! Please register first."}), 400
        
    if REGISTERED_USERS[email]["password"] != password:
        return jsonify({"status": "error", "message": "Wrong password! Please check."}), 400
        
    session['user'] = email
    session['role'] = REGISTERED_USERS[email]["role"]
        
    return jsonify({"status": "success", "email": email, "role": session['role']})

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email', '').strip().lower()
    
    if email not in REGISTERED_USERS:
        return jsonify({"status": "error", "message": "This email is not registered!"}), 400
        
    # 6 digit random OTP generate karna
    otp = str(random.randint(100000, 999999))
    OTP_STORAGE[email] = otp
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = "PLP Player - Password Reset OTP"
        
        body = f"Your 6-digit OTP for password reset is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email sending error: {e}")
        return jsonify({"status": "error", "message": "Failed to send OTP email!"}), 500
    
    return jsonify({"status": "success", "message": "6-digit OTP sent to your email!"})

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email', '').strip().lower()
    entered_otp = data.get('otp', '').strip()
    new_password = data.get('new_password', '').strip()
    
    if email in OTP_STORAGE and OTP_STORAGE[email] == entered_otp:
        REGISTERED_USERS[email]["password"] = new_password
        del OTP_STORAGE[email] # OTP use hone ke baad delete
        return jsonify({"status": "success", "message": "Password updated successfully!"})
    
    return jsonify({"status": "error", "message": "Wrong OTP entered!"}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"status": "success"})

@app.route('/api/delete-account', methods=['POST'])
def delete_account():
    user = session.get('user')
    if user in REGISTERED_USERS:
        del REGISTERED_USERS[user]
    session.clear()
    return jsonify({"status": "success"})

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    if session.get('role') != 'owner':
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    return jsonify({"status": "success"})

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)