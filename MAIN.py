import streamlit as st

st.set_page_config(
        page_title='不動産賃貸 家賃推定',
        page_icon="🏠"
        )

# Streamlitのマルチページ機能を使用
st.title('不動産賃貸 家賃推定')
st.subheader('機械学習による家賃推定プログラム')
st.subheader('左欄からエリアを選択')

# 表記内容
markdown_main = '''
【更新内容】\n
2023-09-18 : 東京、福岡の推定モデルを最新化\n
2023-08-20 : 神戸、仙台、札幌の推定モデルを追加\n
2023-08-14 : 家賃推定プログラムを作成（東京23区、大阪24区、名古屋16区、福岡7区、広島8区）\n
'''
st.caption(markdown_main)
