import streamlit as st
import os

# ----- パスワード保護 -----
PASSWORD = "hamster"  # 合言葉
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 はむはむクイズルームへようこそ")
    st.markdown("このクイズに入るには、**合言葉** が必要だよ！")
    pw = st.text_input("合言葉を入力してね", type="password")
    if pw == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pw != "":
        st.error("🐹 うーん、ちがうみたい...！もういっかい がんばってみてね！")
    st.stop()

# ----- 最初の注意画面 -----
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.image("hajimeni.PNG", use_column_width=True)
    st.markdown("### クイズをはじめる前に読んでね！\n- むずかしい問題もあるけど、がんばってね！\n- 1問ずつ、えらんで「こたえを決定！」してね\n- 最後にスコアと称号が出るよ✨")
    if st.button("🎮 クイズをはじめる！"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ----- 称号ルール -----
def get_title(score):
    if score <= 5:
        return "🌱 みならい", "minarai.PNG"
    elif score <= 10:
        return "📗 初級", "shokyu.PNG"
    elif score <= 14:
        return "🎩 中級", "chukyu.PNG"
    elif score <= 17:
        return "💎 上級", "jokyu.PNG"
    elif score <= 19:
        return "👑 ハムハムマイスター", "meister.PNG"
    else:
        return "🧪 ハムスターはかせ", "hakase.PNG"

# ----- クイズデータ（ダミー1問だけ） -----
quiz_data = [{"question": "ハムスターが食べられるのはどれ？", "options": ["チョコ", "グミ", "ブロッコリー", "アイス"], "answer": 2, "explanation": "ブロッコリーはOK。他はNGです。"}]

# ----- セッション管理 -----
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []

st.title("🐹 ハムスター4択クイズ")
st.markdown("**たべていいのはどれかな？**")

# クイズ進行
if st.session_state.current_q < len(quiz_data):
    q = quiz_data[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q + 1}. {q['question']}")
    choice = st.radio("えらんでね：", q['options'], key=f"q{st.session_state.current_q}")

    if st.button("こたえを決定！"):
        if not choice:
            st.warning("選択肢をえらんでからボタンを押してね！")
            st.stop()
        correct = q['answer'] == q['options'].index(choice)
        st.session_state.answers.append((q['question'], choice, correct))
        if correct:
            st.success("⭕️ せいかい！")
            st.session_state.score += 1
        else:
            st.error("❌ ざんねん…")
        st.info(f"せいかいは：{q['options'][q['answer']]}\n\n{q['explanation']}")
        st.session_state.current_q += 1
        st.rerun()

# 結果表示
else:
    st.header("🎉 おつかれさま！")
    st.subheader(f"あなたのスコア：{st.session_state.score} / {len(quiz_data)}")
    title, image_file = get_title(st.session_state.score)
    st.markdown(f"## あなたの称号は：**{title}**")
    if os.path.exists(image_file):
        st.image(image_file, width=300)
    else:
        st.warning("画像ファイルが見つかりませんでした")

    if st.button("もう一回あそぶ"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.started = False
        st.rerun()
