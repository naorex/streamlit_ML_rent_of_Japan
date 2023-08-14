import streamlit as st

# Streamlitのマルチページ機能を使用
st.title('不動産賃貸 家賃予測')
st.subheader('機械学習による家賃予測プログラム')
st.subheader('左欄からエリアを選択')

# 表記内容
markdown_main = '''
【更新内容】\n
2023-08-14 : 家賃予測プログラムを公開（東京23区、大阪24区、名古屋16区、福岡7区、広島8区）
'''
st.caption(markdown_main)
