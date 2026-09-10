from flask import Flask, render_template, jsonify, send_from_directory, request, session
import os

app = Flask(__name__)
app.secret_key = "pankaj_secret_key_here"

# Database of registered users / VIP list (Aap ise database se bhi replace kar sakte hain)
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
            {"time": 8.0, "text": "Tu rehmat ka hai fasana..."}
        ]
    },
    "rose garden": {
        "display_name": "Rose Garden",
        "artist": "Lata Mangeshkar",
        "audio_url": "/static/Rose_Garden.mp3",
        "video_url": "/static/Rose_Garden_Video.mp4",
        "official_url": "https://www.youtube.com/results?search_query=Rose+Garden+song",
        "is_premium": True,  # VIP Only Song
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
            {"time": 149.5, "text": "Tod Ke Kalam Phir Faansi Pe Main Jhool Jaaun"},
            {"time": 154.0, "text": "Tanne Main Meri Radha Likh Dyu"},
            {"time": 157.5, "text": "Maine Main Ghanshyam Likhunga"},
            {"time": 161.5, "text": "Je Likhne Mein Baith Gya Tanne"},
            {"time": 164.5, "text": "To Pakka Main Kitaab Likhunga"},
            {"time": 168.0, "text": "Tanne Main Likhu Rani Dil Ki"},
            {"time": 171.0, "text": "...end..."}
        ]
    },


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

"""
        .container { max-width: 1000px; margin: 25px auto 0 auto; padding: 0 15px; }
        .glass-card {
            background: rgba(7, 14, 10, 0.85); border: 1px solid rgba(0, 255, 128, 0.25);
            border-radius: 24px; padding: 25px; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
        }
        .song-item {
            display: inline-block; background: rgba(0, 255, 128, 0.08);
            border: 1px solid rgba(0, 255, 128, 0.4); color: #00ff80;
            padding: 8px 18px; border-radius: 20px; margin: 6px; cursor: pointer; font-size: 13px; font-weight: 600;
        }
        .player-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }
        @media (max-width: 768px) { .player-grid { grid-template-columns: 1fr; } }
        video { width: 100%; border-radius: 18px; border: 1px solid rgba(0, 255, 128, 0.3); }
        audio { width: 100%; margin-bottom: 10px; filter: invert(100%) hue-rotate(90deg); }
        #visualizer { width: 100%; height: 50px; background: rgba(3, 7, 5, 0.6); border-radius: 12px; border: 1px solid rgba(0, 255, 128, 0.2); margin-bottom: 15px; }
        #lyrics-box { background: rgba(4, 9, 6, 0.95); border: 1px solid rgba(0, 255, 128, 0.4); border-radius: 18px; height: 250px; overflow-y: auto; text-align: center; padding: 20px; }
        .lyric-line { font-size: 16px; font-weight: 700; color: #1e3828; margin: 16px 0; cursor: pointer; }
        .lyric-line.active { color: #00ff80; transform: scale(1.22); text-shadow: 0 0 20px #00ff80; }
    </style>
</head>
<body>

    <div class="sticky-header">
        <div class="header-content">
            <div class="nav-brand">👁️ PLP PLAYER</div>
            <div class="search-box">
                <input type="text" id="search-input" placeholder="Search track name...">
                <button class="neon-btn" onclick="searchSong()">SEARCH</button>
            </div>
            
            <div class="user-section">
                <a id="apk-download-btn" href="/static/PankajLyricsPlayer.apk" download class="neon-btn apk-btn" style="padding:6px 12px; font-size:10px;">📲 APK</a>
                
                {% if user %}
                    <div class="profile-container" onclick="toggleProfileMenu()">
                        {% if role == 'owner' %}
                            <div class="badge-owner">👑 OWNER</div>
                        {% elif role == 'vip' %}
                            <div class="badge-vip">⭐ VIP USER</div>
                        {% else %}
                            <div class="badge-normal">👤 NORMAL</div>
                        {% endif %}
                        <span style="font-size:11px; color:#00ff80;">▼</span>
                    </div>

                    <!-- Profile Dropdown (Settings & Logout) -->
                    <div id="profile-dropdown" class="profile-dropdown">
                        <div style="padding:10px; font-size:11px; border-bottom:1px solid rgba(0,255,128,0.2); color:#aaa; word-break:break-all;">{{ user }}</div>
                        <button onclick="openSettings()">⚙️ Settings</button>
                        <button onclick="logoutUser()" style="color:#ff4d4d;">🚪 Logout</button>
                    </div>
                {% else %}
                    <button class="neon-btn" onclick="openAuthModal('login')" style="padding:6px 14px; font-size:10px;">LOGIN</button>
                    <button class="neon-btn" onclick="openAuthModal('register')" style="padding:6px 14px; font-size:10px; background:linear-gradient(135deg, #00e5ff 0%, #0088cc 100%);">REGISTER</button>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Login/Register Modal -->
    <div id="auth-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:3000; justify-content:center; align-items:center;">
        <div class="glass-card" style="width:90%; max-width:400px; text-align:center;">
            <h3 id="auth-title" style="color:#00ff80; font-family:'Orbitron'; margin-bottom:15px;">LOGIN TO PLP</h3>
            <input type="email" id="auth-email" placeholder="Enter your email..." style="margin-bottom:15px;">
            <div style="display:flex; gap:10px; justify-content:center;">
                <button class="neon-btn" onclick="submitAuth()">SUBMIT</button>
                <button class="neon-btn" onclick="closeAuthModal()" style="background:rgba(255,255,255,0.1); color:#fff;">CANCEL</button>
            </div>
        </div>
    </div>

    <!-- Settings Modal -->
    <div id="settings-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:3000; justify-content:center; align-items:center;">
        <div class="glass-card" style="width:90%; max-width:400px; text-align:center;">
            <h3 style="color:#00ff80; font-family:'Orbitron'; margin-bottom:15px;">⚙️ APP SETTINGS</h3>
            <p style="font-size:13px; color:#aaa; margin-bottom:15px;">Role: <span style="color:#00ff80; text-transform:uppercase;">{{ role }}</span></p>
            <button class="neon-btn" onclick="closeSettings()">CLOSE</button>
        </div>
    </div>

    <div class="container">
        <div id="screen-main">
            <div class="glass-card">
                <h3 style="color:#00ff80; font-family:'Orbitron'; text-align:center; font-size:16px; margin-bottom:15px;">⚡ TRACK LIBRARY</h3>
                <div id="tracks-list" style="text-align:center;"></div>
            </div>
        </div>

        <div id="screen-player" style="display:none;">
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <button class="neon-btn" onclick="goBack()" style="padding:6px 16px;">⬅ BACK</button>
                    <h3 id="song-title" style="color:#00ff80; font-family:'Orbitron'; font-size:16px;"></h3>
                </div>
                <div class="player-grid">
                    <div><video id="video-player" autoplay loop muted></video></div>
                    <div>
                        <audio id="audio-player" controls autoplay crossorigin="anonymous"></audio>
                        <canvas id="visualizer"></canvas>
                        <div id="lyrics-box"><div id="lyrics-content"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let songsData = {};
        let currentLyrics = [];
        let currentSongKey = '';
        let userRole = "{{ role }}";

        fetch('/api/songs')
            .then(res => res.json())
            .then(data => {
                songsData = data;
                let listHtml = '';
                for(let key in songsData) {
                    let song = songsData[key];
                    let lockIcon = song.is_premium && userRole === 'normal' ? ' 🔒 (VIP)' : ' 🎵';
                    listHtml += '<span class="song-item" onclick="playSong(\'' + key + '\')">' + lockIcon + ' ' + song.display_name + '</span>';
                }
                document.getElementById('tracks-list').innerHTML = listHtml;
            });

        function toggleProfileMenu() {
            let menu = document.getElementById('profile-dropdown');
            menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        }

        function openAuthModal(type) {
            document.getElementById('auth-modal').style.display = 'flex';
            document.getElementById('auth-title').innerText = type === 'register' ? 'REGISTER TO PLP' : 'LOGIN TO PLP';
        }

        function closeAuthModal() {
            document.getElementById('auth-modal').style.display = 'none';
        }

        function submitAuth() {
            const email = document.getElementById('auth-email').value.trim();
            if(!email) return alert("Please enter email!");
            
            fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
            .then(res => res.json())
            .then(data => {
                if(data.status === 'success') location.reload();
                else alert("Failed!");
            });
        }

        function logoutUser() {
            fetch('/api/logout', { method: 'POST' }).then(() => location.reload());
        }

        function openSettings() {
            document.getElementById('profile-dropdown').style.display = 'none';
            document.getElementById('settings-modal').style.display = 'flex';
        }

        function closeSettings() {
            document.getElementById('settings-modal').style.display = 'none';
        }

        function playSong(key) {
            let song = songsData[key];
            if(!song) return;

            if(song.is_premium && userRole === 'normal') {
                alert("🔒 यह गाना केवल VIP / Owner users के लिए है! कृपया VIP एक्सेस लें।");
                return;
            }

            currentSongKey = key;
            document.getElementById('screen-main').style.display = 'none';
            document.getElementById('screen-player').style.display = 'block';
            document.getElementById('song-title').innerText = song.display_name + " - " + song.artist;
            
            let audio = document.getElementById('audio-player');
            let video = document.getElementById('video-player');
            audio.src = song.audio_url;
            video.src = song.video_url;
            currentLyrics = song.lyrics_timed;
            
            renderLyrics();
            audio.play().catch(() => {});
            audio.ontimeupdate = () => syncLyrics(audio.currentTime);
        }

        function renderLyrics() {
            let container = document.getElementById('lyrics-content');
            container.innerHTML = '';
            currentLyrics.forEach((line, index) => {
                const lyric = document.createElement('div');
                lyric.className = 'lyric-line';
                lyric.textContent = line.text;
                lyric.onclick = () => { document.getElementById('audio-player').currentTime = line.time; };
                container.appendChild(lyric);
            });
        }

        function syncLyrics(currentTime) {
            const lines = document.querySelectorAll('.lyric-line');
            let activeIndex = -1;
            currentLyrics.forEach((line, index) => {
                if (Number(line.time) <= currentTime) activeIndex = index;
            });
            lines.forEach((line, index) => {
                line.classList.toggle('active', index === activeIndex);
            });
            if (activeIndex >= 0 && lines[activeIndex]) {
                lines[activeIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        function goBack() {
            document.getElementById('screen-player').style.display = 'none';
            document.getElementById('screen-main').style.display = 'block';
        }
    </script>
</body>
</html>
"""
