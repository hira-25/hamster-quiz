import streamlit as st
import os

# ----- パスワード保護 / Password Protection -----
PASSWORD = "hamster"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 ハムスター20問クイズ！ / 20 Hamster Quiz Challenge!")
    st.markdown("このクイズに入るには、**合言葉** が必要だよ！ / Enter the **password** to join the quiz!")
    pw = st.text_input("合言葉を入力してね / Enter Password", type="password")
    if pw == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pw:
        st.error("🐹 うーん、ちがうみたい...！もういっかい がんばってみてね！ / Hmm... that's not it. Try again!")
    st.stop()

# ----- 最初の注意画面 / Intro Screen -----
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.image("hajimeni.PNG", use_container_width=True)
    st.markdown("""
### クイズをはじめる前に読んでね！ / Read this before you start!
- むずかしい問題もあるけど、がんばってね！ / Some questions are tricky, but do your best!
- 1問ずつ、えらんで「こたえを決定！」してね / Choose your answer and click 'Submit Answer!' one by one
- 最後にスコアと称号が出るよ✨ / Your score and title will appear at the end✨
""")
    if st.button("🎮 クイズをはじめる！ / Start the Quiz!"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ----- 称号ルール / Title Rules -----
def get_title(score):
    if score <= 5:
        return "🌱 みならい / Beginner", "minarai.PNG"
    elif score <= 10:
        return "📗 初級 / Novice", "shokyu.PNG"
    elif score <= 14:
        return "🎩 中級 / Intermediate", "chukyu.PNG"
    elif score <= 17:
        return "💎 上級 / Advanced", "jokyu.PNG"
    elif score <= 19:
        return "👑 ハムハムマイスター / Ham-Ham Meister", "meister.PNG"
    else:
        return "🧪 ハムスターはかせ / Hamster Professor", "hakase.PNG"

# ----- クイズデータ（簡略） / Quiz Data (Simplified) -----
quiz_data = [
    {
        "question": "ハムスターが食べられるのはどれ？ / Which of these can a hamster eat?",
        "options": ["チョコ / Chocolate", "グミ / Gummy", "ブロッコリー / Broccoli", "アイス / Ice Cream"],
        "answer": 2,
        "explanation": "ブロッコリーはOK。他はNGです。 / Broccoli is okay. The others are not suitable."
    }
]

# ----- セッション初期化 / Session Initialization -----
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []

# ----- クイズ進行 / Quiz Flow -----
st.title("🐹 ハムスター4択クイズ / 4-Choice Hamster Quiz")
st.markdown("**たべていいのはどれかな？ / Which one is safe to eat?**")

if st.session_state.current_q < len(quiz_data):
    q = quiz_data[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q + 1}. {q['question']}")
    choice = st.radio("えらんでね： / Choose one:", q['options'], key=f"q{st.session_state.current_q}")

    if st.button("こたえを決定！ / Submit Answer!"):
        if choice == "":
            st.warning("選択肢をえらんでからボタンを押してね！ / Please select an option before submitting.")
            st.stop()
        correct = q['answer'] == q['options'].index(choice)
        st.session_state.answers.append((q['question'], choice, correct))
        if correct:
            st.success("⭕️ せいかい！ / Correct!")
            st.session_state.score += 1
        else:
            st.error("❌ ざんねん… / Incorrect…")
        st.info(f"せいかいは：{q['options'][q['answer']]}

{q['explanation']}")
        st.session_state.current_q += 1
        st.rerun()
else:
    st.header("🎉 おつかれさま！ / Well done!")
    st.subheader(f"あなたのスコア：{st.session_state.score} / {len(quiz_data)} / Your Score")
    title, image_file = get_title(st.session_state.score)
    st.markdown(f"## あなたの称号は：**{title}** / Your Title")
    if os.path.exists(image_file):
        st.image(image_file, width=300)
    else:
        st.warning("画像ファイルが見つかりませんでした / Image file not found")

    if st.button("もう一回あそぶ / Play Again"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.started = False
        st.rerun()