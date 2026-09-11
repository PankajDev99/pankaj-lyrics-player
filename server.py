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
    "The last talk": {
    "display_name": "The last talk",
    "artist": "The Singh",
    "audio_url": "/static/Tha Last Talk.mp3",
    "video_url": "/static/The_Last_Talk_Video.mp4",
    "official_url": "https://www.youtube.com/results?search_query=The+Last+Talk+The+Singh",
    "is_premium": False,
    "lyrics_timed": [
        {"time": 0.0, "text": "......."},
        {"time": 21.5, "text": "Sun maa..."},
        {"time": 24.2, "text": "Dekh phasta ja raha hoon"},
        {"time": 26.5, "text": "Duniya ke daldal mein"},
        {"time": 28.5, "text": "Dhasta ja raha hoon"},
        {"time": 30.2, "text": "Daba ke rakhun gham..."},
        {"time": 32.2, "text": "Bata kitne dil mein hai"},
        {"time": 34.2, "text": "Aankhon mein aansu"},
        {"time": 35.8, "text": "Aur hasta ja raha hoon"},
        {"time": 37.2, "text": "Main chahta to tha tujhe"},
        {"time": 39.0, "text": "Sab kuch bata dun"},
        {"time": 40.8, "text": "Laga ke gale"},
        {"time": 42.5, "text": "Sare gham main bhula dun"},
        {"time": 44.5, "text": "Teri aankhon mein aanshu bhate nahi"},
        {"time": 47.5, "text": "Mujhe behtar laga ke"},
        {"time": 49.2, "text": "Main khud ko sula dun"},
        {"time": 51.5, "text": "Tu reh lena mere jaane ke baad"},
        {"time": 54.5, "text": "Zyada na rona mar jaane ke baad"},
        {"time": 57.5, "text": "Has-has ke karna vida mujhko duniya se"},
        {"time": 61.2, "text": "Photo tu lena janaze ke sath"},
        {"time": 64.5, "text": "Dikhane the sath ajube jahan ke"},
        {"time": 67.2, "text": "Dikha bhi na paya, bata bhi na paya"},
        {"time": 70.8, "text": "Batani thi tujhko maa baatein bahut si"},
        {"time": 74.5, "text": "Main kismat ka mara bata bhi na paya"},
        {"time": 78.5, "text": "Saja bhi na paya ma duniya teri"},
        {"time": 82.2, "text": "Teri raahon se kante hata bhi na paya"},
        {"time": 86.0, "text": "Likha tha ek khat bas tere liye"},
        {"time": 89.5, "text": "Tujhe paas bitha ke suna bhi na paya"},
        {"time": 93.0, "text": "......."},
        {"time": 104.0, "text": "Likha tha ek khat bas tere liye"},
        {"time": 107.5, "text": "Tujhe paas bitha ke suna bhi na paya"},
        {"time": 111.0, "text": "Maa main aaunga lekar janam phir dubara"},
        {"time": 115.5, "text": "Main kabil banunga sab hasil karunga"},
        {"time": 119.5, "text": "Tu banna meri maa phir ek janam aur"},
        {"time": 123.5, "text": "Main kabil hoon kitna main sabit karunga"},
        {"time": 127.5, "text": "Tere hisse ke gham main lekar chala"},
        {"time": 131.0, "text": "Mere jaane ke baad tu rona na na"},
        {"time": 134.5, "text": "Mujhe pata hai tu kitna marti hai mujhpe"},
        {"time": 138.5, "text": "Paas photo ko rakh ke tu sona na na"},
        {"time": 142.5, "text": "Tune jhopdi ko ghar banaya hai maa"},
        {"time": 146.5, "text": "Tapti dhoop mein khud ko tapaya hai maa"},
        {"time": 150.5, "text": "Log izzat ya paisa ek hi kamate hain"},
        {"time": 154.5, "text": "Tune to dono kamaya hai maa"},
        {"time": 158.0, "text": "Maa poochti hai to main batata nahi"},
        {"time": 161.5, "text": "Koi bole bhi aur jawab na de"},
        {"time": 165.2, "text": "Uski aankhon mein dekh ke lagta hai mujhko"},
        {"time": 168.8, "text": "Khuda mujh si kisi ko aulaad na de"},
        {"time": 173.0, "text": "Main jitna lad sakta tha khud se lada"},
        {"time": 177.5, "text": "Maa main khud se to jeet gaya magar zindagi se haar gaya"},
        {"time": 184.0, "text": "Mujhe khali jeb aur gareebi ne nahi mara"},
        {"time": 189.5, "text": "Maa tera chhup-chhup ke rona maar gaya"},
        {"time": 195.0, "text": "Maa tera chhup-chhup ke rona maar gaya"},
        {"time": 201.0, "text": "....end😭..."}
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