
# app.py（修正済み）抜粋のイメージです
import streamlit as st

# パスワード認証、初期化などを含む省略部分…

# 「Play Again」ボタン処理の修正
if st.button("もう一回あそぶ / Play Again"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
