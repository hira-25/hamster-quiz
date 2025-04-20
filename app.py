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
    st.image("hajimeni.PNG", use_container_width=True)
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

# ----- クイズデータ（20問） -----
quiz_data = [{'question': '次のうち、ハムスターが食べられるのはどれ？', 'options': ['チョコ', 'グミ', 'ブロッコリー', 'アイス'], 'answer': 2, 'explanation': 'ブロッコリーはOK。他はNGです。'}, {'question': '次のうち、ハムスターが食べられないのはどれ？', 'options': ['ニンジン', 'りんご', 'チョコレート', 'キャベツ'], 'answer': 2, 'explanation': 'チョコレートはNG。他はOK。'}, {'question': 'ハムスターがたべてもいいのは？', 'options': ['ピーマン', 'ポテトチップス', 'ケーキ', 'ラムネ'], 'answer': 0, 'explanation': 'ピーマンはOK。他は糖分・塩分が多くてNG。'}, {'question': '次のうち、水分が多くてあげすぎ注意なのは？', 'options': ['きゅうり', 'キャベツ', 'にんじん', 'トマト'], 'answer': 0, 'explanation': 'きゅうりは水分が多く、あげすぎ注意。'}, {'question': 'ハムスターがたべてはいけないものはどれ？', 'options': ['ゆで卵の白身', 'パンの耳', 'たまねぎ', 'オートミール'], 'answer': 2, 'explanation': 'たまねぎはNG。中毒を起こす可能性があります。'}, {'question': '次のうち、たべても大丈夫なのは？', 'options': ['おもち', 'わかめ', 'しらす', 'チョコワ'], 'answer': 2, 'explanation': 'しらすはOK。他は糖分や消化の問題あり。'}, {'question': '果物であげてもいいのは？', 'options': ['みかん', 'もも', 'ぶどう', 'ドライマンゴー'], 'answer': 1, 'explanation': 'ももは少量ならOK。他は糖分や中毒のリスク。'}, {'question': '次のうち、たべていい“たね”は？', 'options': ['ひまわりのたね', 'アボカドのたね', 'りんごのたね', 'さくらんぼのたね'], 'answer': 0, 'explanation': 'ひまわりのたねはOK（与えすぎ注意）。他はNG。'}, {'question': '穀物でOKなのは？', 'options': ['シリアル（無糖）', '小麦粉', 'ドーナツ', 'あまいおかし'], 'answer': 0, 'explanation': '無糖のシリアルはOK。他は糖分多めでNG。'}, {'question': 'ハムスターにとって毒なものは？', 'options': ['にんじん', 'チョコレート', 'かぼちゃ', 'ブロッコリー'], 'answer': 1, 'explanation': 'チョコレートは中毒を起こすためNG。'}, {'question': 'たべてもいい“たまご料理”は？', 'options': ['たまごやき（無添加）', 'オムライス', '目玉焼き', '卵かけごはん'], 'answer': 0, 'explanation': '添加物のない卵焼きは少量ならOK。'}, {'question': '豆腐はどう？', 'options': ['たべていい', 'だめ', '毎日OK', 'こわい'], 'answer': 0, 'explanation': '豆腐はOK。ただし少量を時々がベスト。'}, {'question': '次のうち、あぶないのは？', 'options': ['アボカド', '大根', 'かぼちゃ', '白菜'], 'answer': 0, 'explanation': 'アボカドは中毒の危険あり。'}, {'question': 'ハムスターにミルクは？', 'options': ['あげていい', 'ちょっとだけOK', 'だめ', '水でうすめればOK'], 'answer': 2, 'explanation': '牛乳はNG。下痢や中毒のリスク。'}, {'question': '魚でOKなのは？', 'options': ['しらす', 'さけフレーク', 'さしみ', 'いわしの缶詰'], 'answer': 0, 'explanation': 'しらすはOK。他は塩分・油分が多すぎる。'}, {'question': 'ハムスターにのりは？', 'options': ['味付けのりOK', '焼きのりならOK', 'どちらもだめ', '何枚でもOK'], 'answer': 1, 'explanation': '焼きのりは少量ならOK。味付けはNG。'}, {'question': 'たべてはいけないスイーツは？', 'options': ['おはぎ', 'いちご', 'さつまいも', 'なし'], 'answer': 0, 'explanation': 'おはぎは砂糖ともち米でNG。'}, {'question': '次のうち、おすすめなのは？', 'options': ['ブロッコリー', 'ハンバーガー', 'ポテト', 'かき氷'], 'answer': 0, 'explanation': 'ブロッコリーは栄養豊富で◎'}, {'question': 'ハムスターにとって危険な飲み物は？', 'options': ['水', '牛乳', '果汁100%ジュース', '砂糖水'], 'answer': 1, 'explanation': '牛乳はお腹をこわす原因になります。'}, {'question': '最後の問題！ハムスターにいい食べ物は？', 'options': ['ブロッコリー', 'ケーキ', 'ラムネ', 'スナック菓子'], 'answer': 0, 'explanation': 'ブロッコリーは正義！他は全部NG。'}]

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
