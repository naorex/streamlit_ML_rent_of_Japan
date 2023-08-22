import streamlit as st

st.set_page_config(
        page_title='不動産賃貸 家賃推定',
        page_icon="🏠"
        )

# Streamlitのマルチページ機能を使用
st.title('不動産賃貸 家賃推定 (Real estate rental rent estimation)')
st.subheader('機械学習による家賃推定プログラム (Machine learning program for rent estimation)')
st.subheader('左欄からエリアを選択 (Select an area from the left column.)')

# 表記内容
markdown_main = '''
【更新内容 (Updates) 】\n
2023-08-20 : 神戸、仙台、札幌の推定モデルを追加\n
(Added estimation models for Kobe, Sendai, and Sapporo.)\n
2023-08-14 : 家賃推定プログラムを作成（東京23区、大阪24区、名古屋16区、福岡7区、広島8区）\n
(Created rent estimation program (Tokyo 23 wards, Osaka 24 wards, Nagoya 16 wards, Fukuoka 7 wards, Hiroshima 8 wards))
'''
st.caption(markdown_main)
