import streamlit as st
import streamlit.components.v1 as components
import sqlite3

st.title("Iloilo City Real-time Weather")
st.markdown("*Catch the freshest, real-time weather updates—right here!*")
st.sidebar.image("klimata_logo.png", width=1000)

st.markdown("""
<style>

/* --- Make sidebar text white --- */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* --- Make navigation tab text white --- */
[data-testid="stNavigation"] div[data-testid="stSidebarNav"] * {
    color: white !important;
}

/* Optional: Make sidebar background dark for contrast */
[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(layout="wide")  # Ensure wide layout

# Hide header, menu, and footer
st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Page background
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://encycolorpedia.com/d2e8ba.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

# Sidebar background
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-image: url("https://www.dictionary.com/e/wp-content/uploads/2016/01/hunter-green-color-paint-code-swatch-chart-rgb-html-hex.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

components.html("""
<div style="
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
">
    <iframe
      src="https://embed.windy.com/embed2.html?lat=10.72&lon=122.56&zoom=10&level=surface&overlay=gust&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&detailLat=10.72&detailLon=122.56"
      style="border:none; width:100%; height:80vh; border-radius:10px;"
      frameborder="0"
      allowfullscreen>
    </iframe>
</div>
""", height=850)  # slightly taller than iframe to include padding

# -------------------------
# Database setup
# -------------------------
conn = sqlite3.connect("theforum.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
# -------------------------
# Forum UI
# -------------------------
st.markdown("""
    <h2 style="color:#000000; text-align:left; margin-bottom:10px;">
        🌿 Climate Resilience Forum
    </h2>
    <p style="text-align:left; color:#4A4A4A;">
        Share insights, ideas, questions, and solutions for climate resilience in Iloilo City.
    </p>
""", unsafe_allow_html=True)

# Reconnect
conn = sqlite3.connect("theforum.db", check_same_thread=False)
c = conn.cursor()


# -------------------------
# New Post Card
# -------------------------
st.markdown("""
<style>
.forum-card {
    background: #FFFFFF;
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid #D9E8C7;
    box-shadow: 1px 1px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.forum-button {
    background-color: #6FAE4F !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='forum-card'>", unsafe_allow_html=True)

st.subheader("📝 Create a new post")

username = st.text_input("Your Name")
content = st.text_area("Write your message", height=120)

if st.button("Post", key="post_button"):
    if username and content:
        c.execute("INSERT INTO posts (username, content) VALUES (?, ?)", (username, content))
        conn.commit()
        st.success("Your message has been posted!")
    else:
        st.warning("Please enter your name and message before posting.")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# Display Posts
# -------------------------
st.markdown("### 📌 Recent Discussions")

c.execute("SELECT username, content, timestamp FROM posts ORDER BY timestamp DESC")
rows = c.fetchall()

if not rows:
    st.info("No posts yet. Be the first to start a discussion! 🌱")

for row in rows:
    st.markdown(f"""
        <div class="forum-card">
            <p style="margin:0; font-weight:600; color:#2E7D32; font-size:16px;">
                {row[0]} 
                <span style="color:#6C6C6C; font-weight:400; font-size:13px;"> • {row[2]}</span>
            </p>
            <p style="margin-top:10px; color:#333;">
                {row[1]}
            </p>
        </div>
    """, unsafe_allow_html=True)

conn.close()