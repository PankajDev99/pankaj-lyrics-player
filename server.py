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
    },

    "The last talk" :{
        "display_name": "The last talk",
                "artist": " The singh ",
                "audio_url": "/static/Tha Last Talk.mp3",
                "video_url": "/static/.....?",
                "official_url": "....?",
                "is_premium": False,
                "lyrics_timed":[
            {"time": 0.0, "text": "......."},
            {"time": 25.0, "text": "sun maa.."},
            {"time": 27.0, "text": "dekh fasta ja raha hun"},
            {"time": 29.0, "text": "duniya ke daldal mein"},
            {"time": 30.5, "text": " dhasta ja raha hun "},
            {"time": 31.9, "text": "daba ke rukhu gum.."},
            {"time": 32.9, "text": "bata kitne dill mein hani."},
            {"time": 34.8, "text": "Aankho mein aanshu "},
            {"time": 35.9, "text": "or hasta ja raha hun"},
            {"time": 37.0, "text": "Main chahta to tha tujhe.."},
            {"time": 38.0, "text": "sab kuch bata dun"},
            {"time": 39.0, "text": "Laga Ke gale.."},
            {"time": 40.4, "text": "saree gum main bhula dun"},
            {"time": 42.0, "text": "Teri aankho mein aanshu bhate nahi"},
            {"time": 45.0, "text": "Mujhe behtar laga ke.."},
            {"time": 46.3, "text": "main khud ko sula dun"},
            {"time": 48.0, "text": "Tu reh lena mere jane ke baad"},
            {"time": 50.5, "text": "jyada na rona marjane ke baad"},
            {"time": 53.0, "text": "Has has ke karna "},
            {"time": 54.0, "text": "vida mujhko duniya se"},
            {"time": 56.0, "text": "photo tu lena janaze ke sath"},
            {"time": 58.0, "text": "Dikhane the sath ajube jaha ke"},
            {"time": 60.0, "text": "Dikha bhi na paya "},
            {"time": 62.0, "text": "bata bhi na paya"},
            {"time": 63.0, "text": "batani thi tujhko "},
            {"time": 64.9, "text": "maa bate bhuth sii"},
            {"time": 66.7, "text": "Main kismat ka mara.."},
            {"time": 68.0, "text": "bata bhi na paya"},
            {"time": 69.9, "text": "Saja bhi na paya.. "},
            {"time": 71.0, "text": "maa duniya teri"},
            {"time": 72.0, "text": "Teri raho se kaante.."},
            {"time": 73.0, "text": "hata bhi na paya"},
            {"time": 74.9, "text": "likha tha ek khat bas tere liye"},
            {"time": 77.0, "text": "tujhe pass betha ke.."},
            {"time": 78.7, "text": "suna bhi na paya"},            
            {"time": 80.0, "text": "......."},
            {"time": 91.0, "text": "likha tha ek khat bas tere liye"},
            {"time": 93.0, "text": "tujhe pass betha ke.."},
            {"time": 95.0, "text": "suna bhi na paya"},
            {"time": 96.0, "text": "maa main aaunga leke..."},
            {"time": 97.7, "text": "janam fir dubara"},
            {"time": 99.0, "text": "Main kabhil banunga.."},
            {"time": 100.0, "text": "sab hasil karunga"},
            {"time": 102.0, "text": "Tu banna meri maa.."},
            {"time": 103.0, "text": "fir ek janam or"},
            {"time": 104.9, "text": "Main kabhi hun kitna.."},
            {"time": 106.0, "text": "main sabit karunga"},
            {"time": 107.0, "text": "Tere hisse ke gum.."},
            {"time": 108.0, "text": "main leke chala"},
            {"time": 110.0, "text": "Mere jaane ke baad tu rona na na"},
            {"time": 112.0, "text": "Muje pata hai.."},
            {"time": 113.0, "text": "tu kitna marthi hai mujh pe"},
            {"time": 115.0, "text": "Pas photo ko rakh ke.."},
            {"time": 116.0, "text": "tu sona na "},
            {"time": 118.0, "text": "Tune jhopdi ko ghar.."},
            {"time": 119.5, "text": "banaya hai maa"},
            {"time": 120.0, "text": "Tapti dhup mein khud ko.."},
            {"time": 122.0, "text": "tapaya hai maa"},
            {"time": 123.0, "text": "Log ijjat ya paisa.."},
            {"time": 125.0, "text": "ek he kamate hai"},
            {"time": 126.0, "text": "Tune to dono kamaya hai maa"},
            {"time": 129.0, "text": "Maa puchti hai"},
            {"time": 130.0, "text": "to main bata nhi"},
            {"time": 131.3, "text": "koi bole bhi or jawab na de"},
            {"time": 134.0, "text": "Uski aankhon mein.."},
            {"time": 135.0, "text": "dekh ke lagta hai mujhko"},
            {"time": 136.0, "text": "Khuda mujh sii"},
            {"time": 137.0, "text": "kisi ko olad na de"},
            {"time": 140.0, "text": "Main jitna lad sakhta.."},
            {"time": 141.8, "text": "tha khud se lada"},
            {"time": 143.0, "text": "Maa main khud se to zeet gaya"},
            {"time": 146.0, "text": "magar zindagi se haar gaya"},
            {"time": 148.0, "text": "Mujhe khali jeb or"},
            {"time": 149.0, "text": "gareebi ne nahi mara"},
            {"time": 151.0, "text": "Maa tera chhup chuup"},
            {"time": 152.0, "text": "ke rona maar gaya"},
            {"time": 154.0, "text": "Maa tera chhup chuup"},
            {"time": 155.6, "text": "ke rona maar gaya"},
            {"time": 157.0, "text": "....end😭..."},

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