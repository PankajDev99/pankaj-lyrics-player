from flask import Flask, render_template, jsonify, send_from_directory, request, session
import os

app = Flask(__name__)
app.secret_key = "pankaj_secret_key_here"

VIP_USERS = ["pankajkhatik0999@gmail.com", "vipuser@gmail.com"]

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
    "kitab": {
        "display_name": "KITAB",
        "artist": "Mr Dutt, Vipin Foji",
        "audio_url": "/static/KITAB.mp3",
        "video_url": "/static/KITAB_VIDEO.mp4",
        "official_url": "https://www.youtube.com/results?search_query=KITAB+Mr+Dutt+Vipin+Foji",
        "is_premium": False,
        "lyrics_timed": [
            {"time": 0.0, "text": "......."},
            {"time": 16.0, "text": "Tane Main Likhu Rani Dil Ki"},
            {"time": 20.1, "text": "Ya Tanne Mumtaj Likhunga"},
            {"time": 24.0, "text": "Je Likhne Mein Baith Gya Tanne"},
            {"time": 27.5, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 30.5, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 34.0, "text": "Re Hothan Ne Gulaab Likh Dyu"},
            {"time": 37.5, "text": "Re Akhya Ne Sharaab Likhunga"},
            {"time": 41.0, "text": "Je Likhne Mein Baith Gya Tanne"},
            {"time": 44.0, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 48.0, "text": "tanne main likhu rani dill ki.."},
            {"time": 52.0, "text": "......"},
            {"time": 70.0, "text": "Chunni Mein Jo Moti Jadre Usne Chhori Taara Likhu"},
            {"time": 77.0, "text": "Chaand Feeka Lagge Se, Yo Roop Kitna Pyaara Likhu"},
            {"time": 84.0, "text": "Ram Ka Ishara Likhu, Dekhya Na Nazaara Likhu"},
            {"time": 90.5, "text": "Baat Chhoti Lage Meri, Kaat Ke Dubaara Likhu.."},
            {"time": 97.0, "text": "Baat Chhoti Lage Meri, Kaat Ke Dubaara Likhu"},
            {"time": 104.0, "text": "Re Baatan Ne Alaap Likhunga"},
            {"time": 108.0, "text": "Jo Dikh Ja Tu Khwab Likhunga"},
            {"time": 112.0, "text": "Je Likhne Mein Baith Gya Tanne"},
            {"time": 115.0, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 118.0, "text": "Ho Puche Na Tu Mere Te Ya Aashiq Ka Haal"},
            {"time": 121.0, "text": "Resham Te Zyada Hai Sunehre Tere Baal"},
            {"time": 125.0, "text": "Ho Pariyan Ke Desh Te Tu Aayi Visa Daal Ke"},
            {"time": 129.0, "text": "Red Moon Jaisi E Tu Lage Se Kamaal"},
            {"time": 132.0, "text": "Can’t Live Without You, You Baby Mind"},
            {"time": 135.5, "text": "If You Touch Me So I’m Feeling Fine"},
            {"time": 139.0, "text": "Likhu Tere Baare Saari Duniya Ke Bol Laaun"},
            {"time": 143.0, "text": "Likhu Tere Baare Saari Duniya Ne Bhool Jaaun"},
            {"time": 146.5, "text": "Likhu Tere Baare Phir Kuch Aur Na Main Likh Paaun"},
            {"time": 154.0, "text": "Tanne Main Meri Radha Likh Dyu"},
            {"time": 157.5, "text": "Maine Main Ghanshyam Likhunga"},
            {"time": 161.5, "text": "Je Likhne Mein Baith Gya Tanne"},
            {"time": 164.5, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 168.0, "text": "Tanne Main Likhu Rani Dil Ki"},
            {"time": 171.0, "text": "...end..."}
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

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    
    session['user'] = email
    if email == "pankajkhatik0999@gmail.com":
        session['role'] = 'owner'
    elif email in VIP_USERS:
        session['role'] = 'vip'
    else:
        session['role'] = 'normal'
        
    return jsonify({"status": "success", "email": email, "role": session['role']})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"status": "success"})

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)