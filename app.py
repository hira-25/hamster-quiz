import streamlit as st
import time
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

# ----- クイズデータ / Quiz Data (20 questions) -----
quiz_data = [
    {"question": "ハムスターが食べられるのはどれ？ / Which of these can a hamster eat?", "options": ["チョコ / Chocolate", "グミ / Gummy", "ブロッコリー / Broccoli", "アイス / Ice Cream"], "answer": 2, "explanation": "ブロッコリーはOK。他はNGです。 / Broccoli is okay. The others are not suitable."},
    {"question": "ハムスターが食べられないのはどれ？ / Which of these can a hamster NOT eat?", "options": ["ニンジン / Carrot", "りんご / Apple", "チョコレート / Chocolate", "キャベツ / Cabbage"], "answer": 2, "explanation": "チョコレートは中毒の危険があるためNGです。 / Chocolate is toxic for hamsters."},
    {"question": "たべてもいいのはどれ？ / Which of these is safe to eat?", "options": ["ピーマン / Bell Pepper", "ポテトチップス / Potato Chips", "ケーキ / Cake", "ラムネ / Ramune Candy"], "answer": 0, "explanation": "ピーマンはOK。他は糖分や塩分が多いためNG。 / Bell pepper is okay. The others have too much sugar or salt."},
    {"question": "水分が多くてあげすぎ注意なのは？ / Which has high water content and should be limited?", "options": ["きゅうり / Cucumber", "キャベツ / Cabbage", "にんじん / Carrot", "トマト / Tomato"], "answer": 0, "explanation": "きゅうりは水分が多いので注意。 / Cucumber has high water content."},
    {"question": "たべてはいけないものは？ / What should not be given?", "options": ["ゆで卵の白身 / Boiled Egg White", "パンの耳 / Bread Crust", "たまねぎ / Onion", "オートミール / Oatmeal"], "answer": 2, "explanation": "たまねぎは有毒。 / Onion is toxic."},
    {"question": "たべても大丈夫なのはどれ？ / Which of these is safe?", "options": ["おもち / Rice Cake", "わかめ / Seaweed", "しらす / Whitebait", "チョコ味のアイス / Chocolate Ice Cream"], "answer": 2, "explanation": "しらすはOK。他はNG。 / Whitebait is okay. The others are not."},
    {"question": "あげてもいい果物はどれ？ / Which fruit can be given?", "options": ["チョコバナナ / Chocolate Banana", "もも / Peach", "ぶどう / Grape", "ドライマンゴー / Dried Mango"], "answer": 1, "explanation": "ももは果肉のみ、皮と種をのぞいて少しだけならOK。他の果物はハムスターに向きません。 / Peach (flesh only, no skin or seed) is okay in small amounts. The others are not suitable for hamsters."},
    {"question": "たべてもいい“たね”は？ / Which seed is okay to eat?", "options": ["ひまわりのたね / Sunflower Seed", "アボカドのたね / Avocado Seed", "りんごのたね / Apple Seed", "さくらんぼのたね / Cherry Pit"], "answer": 0, "explanation": "ひまわりのたねは少量OK。 / Sunflower seeds are okay in moderation."},
    {"question": "穀物でOKなのは？ / Which grain is okay?", "options": ["シリアル（無糖） / Unsweetened Cereal", "小麦粉 / Flour", "ドーナツ / Donut", "あまいおかし / Sweets"], "answer": 0, "explanation": "無糖シリアルはOK。 / Unsweetened cereal is okay."},
    {"question": "毒になるのは？ / Which is toxic?", "options": ["にんじん / Carrot", "チョコレート / Chocolate", "かぼちゃ / Pumpkin", "ブロッコリー / Broccoli"], "answer": 1, "explanation": "チョコレートは毒性あり。 / Chocolate is toxic."},
    {"question": "たべてもいい卵料理は？ / Which egg dish is safe?", "options": ["たまごやき（無添加） / Plain Omelet", "オムライス / Omurice", "目玉焼き / Fried Egg", "卵かけごはん / Raw Egg Rice"], "answer": 0, "explanation": "無添加卵焼きはOK。 / Plain omelet is okay."},
    {"question": "豆腐は？ / Is tofu okay?", "options": ["たべていい / Yes", "だめ / No", "毎日OK / Daily OK", "こわい / Dangerous"], "answer": 0, "explanation": "豆腐はOK。 / Tofu is okay."},
    {"question": "危険なのはどれ？ / Which is dangerous?", "options": ["アボカド / Avocado", "大根 / Daikon", "かぼちゃ / Pumpkin", "白菜 / Chinese Cabbage"], "answer": 0, "explanation": "アボカドは毒性あり。 / Avocado is toxic."},
    {"question": "ミルクは？ / What about milk?", "options": ["あげていい / Give", "ちょっとだけOK / Small Amount OK", "だめ / No", "水でうすめればOK / Dilute with Water OK"], "answer": 2, "explanation": "ミルクはNG。 / Milk is not suitable."},
    {"question": "OKな魚は？ / Which fish is okay?", "options": ["しらす / Whitebait", "さけフレーク / Salmon Flakes", "さしみ / Sashimi", "いわしの缶詰 / Canned Sardines"], "answer": 0, "explanation": "しらすはOK。 / Whitebait is okay."},
    {"question": "のりは？ / What about seaweed?", "options": ["味付けのりOK / Seasoned Nori OK", "焼きのりならOK / Roasted Nori OK", "どちらもだめ / Neither", "何枚でもOK / Unlimited"], "answer": 1, "explanation": "焼きのりは少量OK。 / Roasted nori is okay in small amounts."},
    {"question": "NGなスイーツは？ / Which sweet is NOT okay?", "options": ["おはぎ / Sweet Rice Cake", "いちご / Strawberry", "さつまいも / Sweet Potato", "なし / Pear"], "answer": 0, "explanation": "おはぎは糖分が多くNG。 / Sweet rice cake is too sugary."},
    {"question": "おすすめなのは？ / Which is recommended?", "options": ["ブロッコリー / Broccoli", "ハンバーガー / Hamburger", "ポテト / French Fries", "かき氷 / Shaved Ice"], "answer": 0, "explanation": "ブロッコリーは栄養豊富。 / Broccoli is nutritious."},
    {"question": "最も危険な飲み物は？ / Which drink is most dangerous?", "options": ["水 / Water", "牛乳（乳糖を含む） / Milk (contains lactose)", "果汁ジュース / Fruit Juice", "砂糖水 / Sugar Water"], "answer": 3, "explanation": "砂糖水は糖分しかなく、ハムスターの体にとても悪いです。 / Sugar water contains only sugar and is very harmful to hamsters."},
    {"question": "ハムスターが食べてもいい食べ物は？ / Which food is safe for hamsters?", "options": ["ブロッコリー / Broccoli", "ケーキ / Cake", "ラムネ / Ramune", "スナック菓子 / Snack"], "answer": 0, "explanation": "ブロッコリーは安全でおすすめ。 / Broccoli is safe and recommended."}
]

# ----- セッション初期化 -----
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []

st.title("🐹 ハムスター4択クイズ / 4-Choice Hamster Quiz")
st.markdown("**たべていいのはどれかな？ / Which one is safe to eat?**")

# ----- クイズ進行 -----
if st.session_state.current_q < len(quiz_data):
    q = quiz_data[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q + 1}. {q['question']}")
    choice = st.radio("えらんでね： / Choose one:", q['options'], key=f"q{st.session_state.current_q}")

    if st.button("こたえを決定！ / Submit Answer!"):
        if not choice:
            st.warning("選択肢をえらんでからボタンを押してね！ / Please select an option before submitting.")
            st.stop()
        correct = q['answer'] == q['options'].index(choice)
        if correct:
            st.success("⭕️ せいかい！ / Correct!")
            st.session_state.score += 1
        else:
            st.error("❌ ざんねん… / Incorrect…")
        st.info(f"せいかいは：{q['options'][q['answer']]}\n\n{q['explanation']}")
        time.sleep(2)
        st.session_state.current_q += 1
        st.rerun()

# ----- 結果表示 -----
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
        for key in ["current_q", "score", "answers", "started", "authenticated"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
