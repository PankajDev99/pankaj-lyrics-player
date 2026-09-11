from flask import Flask, render_template, jsonify, send_from_directory, request, session
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import razorpay

# Razorpay Client Initialization
razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_RAZORPAY_SECRET"))

app = Flask(__name__)
app.secret_key = "pankaj_secret_key_here"

# Email Configuration
SENDER_EMAIL = "maypaysecure@gmail.com"
SENDER_PASSWORD = "lojq zhtq txqf mmrb"

VIP_USERS = ["pankajkhatik0999@gmail.com", "vipuser@gmail.com"]

# Registered Users Database (Email -> {"password": "...", "role": "...", "name": "...", "phone": "..."})
REGISTERED_USERS = {
    "pankajkhatik0999@gmail.com": {"password": "Pankaj khatik0999", "role": "owner", "name": "Pankaj Khatik", "phone": "9999999999"}
}

# Temporary Storage for OTP and Registration Data
OTP_STORAGE = {}
TEMP_REG_STORAGE = {}

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
        "official_url": "https://youtu.be/OYf9NlA8AeU?si=UkAN-KuMOWg5vSaz",
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
            {"time": 44.0, "text": "Bheju tanne main ...."}
        ]
    },
    "The last talk": {
        "display_name": "The last talk",
        "artist": "The Singh",
        "audio_url": "/static/Tha Last Talk.mp3",
        "video_url": "/static/The_Last_Talk_Video.mp4",
        "official_url": "https://youtu.be/Tvo8dTFopIA?si=VWNfWX8FA0CtkjZR",
        "is_premium": False,
        "lyrics_timed": [
            {"time": 0.0, "text": "......."},
            {"time": 25.0, "text": "Sun maa..."},
            {"time": 27.5, "text": "Dekh phasta ja raha hoon"},
            {"time": 29.5, "text": "Duniya ke daldal mein"},
            {"time": 31.0, "text": "Dhasta ja raha hoon"},
            {"time": 32.5, "text": "Daba ke rakhun gham..."},
            {"time": 34.5, "text": "Bata kitne dil mein hai"},
            {"time": 37.0, "text": "Aankhon mein aansu"},
            {"time": 38.8, "text": "Aur hasta ja raha hoon"},
            {"time": 40.5, "text": "Main chahta to tha tujhe"},
            {"time": 42.0, "text": "Sab kuch bata dun"},
            {"time": 43.5, "text": "Laga ke gale"},
            {"time": 45.2, "text": "Sare gham main bhula dun"},
            {"time": 47.5, "text": "Teri aankhon mein aanshu bhate nahi"},
            {"time": 50.0, "text": "Mujhe behtar laga ke"},
            {"time": 52.0, "text": "Main khud ko sula dun"},
            {"time": 53.8, "text": "Tu reh lena mere jaane ke baad"},
            {"time": 56.0, "text": "Zyada na rona mar jaane ke baad"},
            {"time": 59.2, "text": "Has-has ke karna vida mujhko duniya se"},
            {"time": 62.8, "text": "Photo tu lena janaze ke sath"},
            {"time": 66.0, "text": "Dikhane the sath ajube jahan ke"},
            {"time": 68.5, "text": "Dikha bhi na paya, bata bhi na paya"},
            {"time": 71.8, "text": "Batani thi tujhko maa baatein bahut si"},
            {"time": 75.0, "text": "Main kismat ka mara bata bhi na paya"},
            {"time": 78.2, "text": "Saja bhi na paya ma duniya teri"},
            {"time": 80.8, "text": "Teri raahon se kante hata bhi na paya"},
            {"time": 84.0, "text": "Likha tha ek khat bas tere liye"},
            {"time": 86.5, "text": "Tujhe paas bitha ke suna bhi na paya"},
            {"time": 90.5, "text": "......."},
            {"time": 99.5, "text": "Likha tha ek khat bas tere liye"},
            {"time": 102.2, "text": "Tujhe paas bitha ke suna bhi na paya"},
            {"time": 105.0, "text": "Maa main aaunga lekar janam phir dubara"},
            {"time": 109.0, "text": "Main kabil banunga sab hasil karunga"},
            {"time": 112.0, "text": "Tu banna meri maa phir ek janam aur"},
            {"time": 116.0, "text": "Main kabil hoon kitna main sabit karunga"},
            {"time": 118.5, "text": "Tere hisse ke gham main lekar chala"},
            {"time": 121.5, "text": "Mere jaane ke baad tu rona na na"},
            {"time": 124.0, "text": "Mujhe pata hai tu kitna marti hai mujhpe"},
            {"time": 128.0, "text": "Paas photo ko rakh ke tu sona na na"},
            {"time": 131.0, "text": "Tune jhopdi ko ghar banaya hai maa"},
            {"time": 134.0, "text": "Tapti dhoop mein khud ko tapaya hai maa"},
            {"time": 136.8, "text": "Log izzat ya paisa ek hi kamate hain"},
            {"time": 140.5, "text": "Tune to dono kamaya hai maa"},
            {"time": 144.0, "text": "Maa poochti hai to main batata nahi"},
            {"time": 146.5, "text": "Koi bole bhi aur jawab na de"},
            {"time": 150.0, "text": "Uski aankhon mein dekh ke lagta hai mujhko"},
            {"time": 153.2, "text": "Khuda mujh si kisi ko aulaad na de"},
            {"time": 157.0, "text": "Main jitna lad sakta tha khud se lada"},
            {"time": 162.0, "text": "Maa main khud se to jeet gaya magar zindagi se haar gaya"},
            {"time": 167.0, "text": "Mujhe khali jeb aur gareebi ne nahi mara"},
            {"time": 170.5, "text": "Maa tera chhup-chhup ke rona maar gaya"},
            {"time": 175.0, "text": "Maa tera chhup-chhup ke rona maar gaya"},
            {"time": 178.0, "text": "....end😭..."}
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

@app.route('/api/register-send-otp', methods=['POST'])
def register_send_otp():
    data = request.json
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    
    if not email or not name or not phone:
        return jsonify({"status": "error", "message": "All fields are required!"}), 400
    
    if email in REGISTERED_USERS:
        return jsonify({"status": "error", "message": "Email already registered! Please login."}), 400
    
    otp = str(random.randint(100000, 999999))
    OTP_STORAGE[email] = otp
    TEMP_REG_STORAGE[email] = {"name": name, "phone": phone}
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = "PLP Player - Registration OTP"
        
        body = f"Your 6-digit verification OTP for registration is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email sending error: {e}")
        return jsonify({"status": "error", "message": "Failed to send OTP email!"}), 500
    
    return jsonify({"status": "success", "message": "OTP sent to email!"})

@app.route('/api/register-verify-otp', methods=['POST'])
def register_verify_otp():
    data = request.json
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()
    
    if email in OTP_STORAGE and OTP_STORAGE[email] == otp:
        reg_info = TEMP_REG_STORAGE.get(email, {})
        role = 'owner' if email == "pankajkhatik0999@gmail.com" else ('vip' if email in VIP_USERS else 'normal')
        
        REGISTERED_USERS[email] = {
            "password": "password123", 
            "role": role,
            "name": reg_info.get("name", ""),
            "phone": reg_info.get("phone", "")
        }
        
        session['user'] = email
        session['role'] = role
        
        del OTP_STORAGE[email]
        if email in TEMP_REG_STORAGE:
            del TEMP_REG_STORAGE[email]
            
        return jsonify({"status": "success", "message": "Registration verified!"})
    
    return jsonify({"status": "error", "message": "Invalid OTP!"}), 400

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
        del OTP_STORAGE[email]
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

@app.route('/api/create-order', methods=['POST'])
def create_order():
    if not session.get('user'):
        return jsonify({"status": "error", "message": "Please login first!"}), 401
    
    data = { "amount": 9900, "currency": "INR", "payment_capture": 1 }
    order = razorpay_client.order.create(data=data)
    return jsonify({"status": "success", "order_id": order['id'], "amount": data['amount']})

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    user_email = session.get('user')
    
    if user_email and user_email in REGISTERED_USERS:
        REGISTERED_USERS[user_email]["role"] = "vip"
        session['role'] = "vip"
        return jsonify({"status": "success", "message": "VIP subscription activated for 1 month!"})
    
    return jsonify({"status": "error", "message": "Verification failed!"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)