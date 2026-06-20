import streamlit as st
import os
import json
import base64

# पेज सेटिंग्स
st.set_page_config(page_title="PANKAJ LYRICS - OFFICIAL PLAYER", layout="wide")

st.markdown("""
    <style>
    .main .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    h1 { 
        color: #ff4b4b; font-family: 'Poppins', sans-serif; font-weight: 800; 
        font-size: 28px; margin: 0px; text-shadow: 0px 0px 10px rgba(255, 75, 75, 0.4);
        text-align: center;
    }
    .stButton>button {
        background-color: #ff4b4b; color: white; border-radius: 6px; 
        font-weight: bold; width: 100%; border: none; padding: 6px 12px;
    }
    .stButton>button:hover { background-color: #ff3333; }
    
    .song-box, .confirm-box {
        background: linear-gradient(135deg, #1f1f2e 0%, #111122 100%);
        padding: 25px; border-radius: 12px; border-left: 6px solid #ff4b4b;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        text-align: center;
    }
    .video-dummy {
        background: radial-gradient(circle, #1a1c23 0%, #0f1015 100%);
        border: 2px dashed #ff4b4b; border-radius: 12px;
        height: 380px; display: flex; flex-direction: column; justify-content: center;
        align-items: center; color: #aaa; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

songs_database = {
    "dhundle manzar": {
        "display_name": "Dhundle Manzar",
        "artist": "Sarckey Kohli",
        # 👑 क्योंकि फाइल गिटहब पर 'song app' फोल्डर के अंदर है, इसलिए इसे ऐसे लिखो:
        "audio_file_path": "song app/dhundle_song.mp3",
        "video_file_path": "song app/anime_walk.mp4",
        "lyrics_timed": [
            {"time": 0.0, "text": "Dhundle hue hain manzar mere.."},
            {"time": 3.0, "text": "Tu raahein inhehin dikhana..."},
            {"time": 6.0, "text": "Jo zero se vaasta hai mera..."},
            {"time": 8.0, "text": "Tu rehmat ka hai fasana..."},
            {"time": 12.0, "text": "Kaagzon pe jaise, bikhri hai siyahi..."},
            {"time": 17.0, "text": "Kahani tu apni yun kar bayaan..."},
            {"time": 20.0, "text": "Mere dil pe asi chahi..."},
            {"time": 23.0, "text": "Tu hi tu muje mein samaye..."},
            {"time": 26.0, "text": "Ban gyi mere kudayi soniye..."}
        ]
    },

    #yahan agle song ko likne ke liye uper , lagana hoga
    "Rose Garden": {
        "display_name": "Rose Garden",
        "artist": "Lata Mangeshkar",
        "audio_file_path": "song app/Rose_Garden.mp3",
        "video_file_path": "song app/Rose_Garden_Video.mp4",
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
            {"time": 90.0, "text": "Bheju tanne main ...."},
            {"time": 90.7, "text": ".........."},

        ]
    }
}

if "screen" not in st.session_state:
    st.session_state.screen = "main"
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# --- 1. मुख्य सर्च स्क्रीन ---
if st.session_state.screen == "main":
    st.markdown("<h1>👑 PANKAJ LYRICS- OFFICIAL PLAYER</h1>", unsafe_allow_html=True)
    st.write("---")
    
    left_col, mid_col, right_col = st.columns([1, 2, 1])
    with mid_col:
        st.markdown('<div class="song-box">', unsafe_allow_html=True)
        st.subheader("🎵 Available list:")
        for key, val in songs_database.items():
            st.markdown(f"🔥 **Type this:** `{key}` <br><small style='color:#ff4b4b;'>Artist: {val['artist']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        search_query = st.text_input("(गाने का नाम लिखें):", "").strip().lower()
        
        if st.button("🚀 FIND & PLAY"):
            if search_query in songs_database:
                st.session_state.current_song = search_query
                st.session_state.screen = "confirm"
                st.rerun()
            elif search_query == "":
                st.warning("कृपया पहले बॉक्स में गाने का नाम टाइप करें!")
            else:
                st.error("❌ यह गाना अभी उपलब्ध नहीं है!")

# --- 2. बीच की कन्फर्मेशन स्क्रीन ---
elif st.session_state.screen == "confirm":
    st.markdown("<h1>🔍 SONG FOUND!</h1>", unsafe_allow_html=True)
    st.write("---")
    
    left_col, mid_col, right_col = st.columns([1, 2, 1])
    with mid_col:
        song_info = songs_database[st.session_state.current_song]
        st.markdown(f"""
            <div class="confirm-box">
                <span style="font-size: 50px;">🎵</span>
                <h3 style="color:#ff4b4b; margin:10px 0;">{song_info['display_name']}</h3>
                <p style="color:#aaa;">Artist: {song_info['artist']}</p>
                <p style="font-size:14px; color:#666;">क्या आप इस गाने को प्ले करना चाहते हैं?</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("▶️ YES, PLAY NOW"):
                st.session_state.screen = "player"
                st.rerun()
        with btn_col2:
            if st.button("⬅️ NO, GO BACK"):
                st.session_state.screen = "main"
                st.session_state.current_song = None
                st.rerun()

# --- 3. असली प्लेयर स्क्रीन ---
elif st.session_state.screen == "player":
    song_data = songs_database[st.session_state.current_song]
    
    top_col1, top_col2 = st.columns([2, 10])
    with top_col1:
        if st.button("⬅️ Back"):
            st.session_state.screen = "main"
            st.session_state.current_song = None
            st.rerun()
    with top_col2:
        st.markdown(f"<h1 style='text-align: left; margin-left: 20px;'>🎶 Now Playing: {song_data['display_name']}</h1>", unsafe_allow_html=True)
            
    st.write("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    video_col, lyrics_col = st.columns([1, 1])
    
    with video_col:
        current_video_path = song_data["video_file_path"]
        
        import os
        if os.path.exists(current_video_path):
            # 👑 यहाँ हम Streamlit के डिफ़ॉल्ट प्लेयर की जगह HTML5 प्लेयर यूज़ करेंगे 
            # जो वीडियो को बिना रुके बार-बार (Infinity Loop) चलाता रहेगा
            with open(current_video_path, 'rb') as video_file:
                video_bytes = video_file.read()
            
            st.video(video_bytes, autoplay=True, loop=True, muted=True)
        else:
            st.error(f"वीडियो फाइल मिसिंग है: {current_video_path}") 
        
        
            # 👑 पुराने ग्लोबल audio_path को हटाकर अब हम सीधे चुने हुए गाने का पाथ यहाँ पढ़ेंगे
    current_song_path = song_data["audio_file_path"]
    
    # ऑडियो बाइट्स को सेफली लोड करना
    audio_base64 = ""
    if os.path.exists(current_song_path):
        with open(current_song_path, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
    else:
        st.error(f"फाइल मिसिंग है: {current_song_path}")
        
        # 👑 ये लाइन मिसिंग है, इसे 'with lyrics_col:' के ठीक ऊपर डाल दो
    lyrics_json = json.dumps(song_data["lyrics_timed"])
    with lyrics_col:
        # 👑 नया एडवांस सिंकिंग इंजन
        st.components.v1.html(f"""
            <div style="display: flex; flex-direction: column; gap: 10px; font-family: 'Poppins', sans-serif;">
                
                <button id="js-replay-btn" style="background-color: #ff4b4b; color: white; border-radius: 6px; font-weight: bold; border: none; padding: 10px; width: 100%; cursor: pointer; font-size: 14px;">
                    🔄 Replay Song & Lyrics (शुरू से चलाएं)
                </button>

                <audio id="main-audio" controls autoplay style="width: 100%; border-radius: 8px;">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>

                <div id="lyrics-box" style="background: #0d0e12; border-radius: 12px; padding: 20px; border: 2px solid #ff4b4b; height: 250px; box-shadow: inset 0 0 30px rgba(0,0,0,0.9); overflow-y: auto; text-align: center; scroll-behavior: smooth;">
                    <div id="lyrics-content" style="display: flex; flex-direction: column; gap: 18px; padding-top: 90px; padding-bottom: 90px;"></div>
                </div>
            </div>

            <script>
                const lyricsData = {lyrics_json};
                const box = document.getElementById('lyrics-box');
                const container = document.getElementById('lyrics-content');
                const audio = document.getElementById('main-audio');
                const replayBtn = document.getElementById('js-replay-btn');
                
                // स्क्रीन पर सारी लाइन्स पहले से रेंडर कर देना (पर धुंधली रहेंगी)
                lyricsData.forEach((item, index) => {{
                    let div = document.createElement('div');
                    div.innerText = item.text;
                    div.id = 'line-' + index;
                    div.style.fontSize = '22px';
                    div.style.fontWeight = '800';
                    div.style.color = '#444'; // बिना चली हुई लाइन्स डार्क ग्रे रहेंगी
                    div.style.transition = 'all 0.3s ease';
                    div.style.transform = 'scale(0.9)';
                    container.appendChild(div);
                }});

                // 👑 असली जादू: ऑडियो टाइम अपडेट इवेंट लिस्नर
                audio.addEventListener('timeupdate', () => {{
                    let currentTime = audio.currentTime;
                    let activeIndex = -1;

                    // चेक करना कि करंट टाइम के हिसाब से कौन सी लाइन बज रही है
                    for (let i = 0; i < lyricsData.length; i++) {{
                        if (currentTime >= lyricsData[i].time) {{
                            activeIndex = i;
                        }}
                    }}

                    // सभी लाइन्स को रीसेट करना और सिर्फ एक्टिव लाइन को चमकाना
                    for (let i = 0; i < lyricsData.length; i++) {{
                        let lineDiv = document.getElementById('line-' + i);
                        if (i === activeIndex) {{
                            // एक्टिव लाइन चमकीली ग्रेडिएंट बन जाएगी और बड़ी दिखेगी
                            lineDiv.style.background = 'linear-gradient(45deg, #ff4b4b, #ff6e40, #fbc02d, #00f2fe)';
                            lineDiv.style.webkitBackgroundClip = 'text';
                            lineDiv.style.webkitTextFillColor = 'transparent';
                            lineDiv.style.transform = 'scale(1.15)';
                            lineDiv.style.textShadow = '0 0 15px rgba(255, 75, 75, 0.5)';
                            
                            // 👑 परफेक्ट ऑटो-सेंटर स्क्रॉल: लाइन हमेशा डिब्बे के बीच में रहेगी, नीचे नहीं छुपेगी!
                            let offsetTop = lineDiv.offsetTop - box.offsetTop;
                            box.scrollTop = offsetTop - (box.clientHeight / 2) + (lineDiv.clientHeight / 2);
                        }} else if (i < activeIndex) {{
                            // जो लाइन्स गाई जा चुकी हैं, उन्हें थोड़ा हल्का (dim) कर दो ताकि फोकस करंट लाइन पर रहे
                            lineDiv.style.background = 'none';
                            lineDiv.style.webkitTextFillColor = '#666';
                            lineDiv.style.transform = 'scale(0.95)';
                            lineDiv.style.textShadow = 'none';
                        }} else {{
                            // आगे आने वाली लाइन्स डार्क रहेंगी
                            lineDiv.style.background = 'none';
                            lineDiv.style.webkitTextFillColor = '#333';
                            lineDiv.style.transform = 'scale(0.9)';
                            lineDiv.style.textShadow = 'none';
                        }}
                    }}
                }});

                // रीप्ले बटन फंक्शन
                replayBtn.addEventListener('click', () => {{
                    audio.currentTime = 0;
                    audio.play();
                    box.scrollTop = 0;
                }});
            </script>
        """, height=380)