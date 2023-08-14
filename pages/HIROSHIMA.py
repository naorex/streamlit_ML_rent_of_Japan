import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('広島8区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_hiro = list(filter(lambda x: 'hiroshima' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_hiro = {model_list_hiro[0].split('_')[5]: model_list_hiro[0],
                model_list_hiro[1].split('_')[5]: model_list_hiro[1],
                model_list_hiro[2].split('_')[5]: model_list_hiro[2],
                model_list_hiro[3].split('_')[5]: model_list_hiro[3],
                model_list_hiro[4].split('_')[5]: model_list_hiro[4],
                model_list_hiro[5].split('_')[5]: model_list_hiro[5],
                model_list_hiro[6].split('_')[5]: model_list_hiro[6],
                model_list_hiro[7].split('_')[5]: model_list_hiro[7]
                }

# 表記内容
markdown_hiroshima = '''
学習データ基準月: 2023-07
'''
st.write(markdown_hiroshima)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_hiro = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('広島市中区',
                    '広島市南区',
                    '広島市東区',
                    '広島市西区',
                    '広島市佐伯区',
                    '広島市安佐南区',
                    '広島市安芸区',
                    '広島市安佐北区')
                    )

    # 築年数を入力
    val1_hiro = st.slider('築年数', min_value=1, max_value=50)

    # 間取り分類を入力
    val2_hiro = st.slider('間取り分類', min_value=0, max_value=5)
    madori_explanation = '''
    【間取り分類】基本的に部屋数を表しています。以下例参照。\n
    - 分類 0: 下記以外
    - 分類 1: 1R, 1K, 1DK, 1LDK
    - 分類 2: 2K, 2DK, 2LDK
    - 分類 3: 3DK, 3LDK
    - 以下同様
    '''
    st.caption(madori_explanation)

    # 面積をスライダー入力
    val3_hiro = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_hiro = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_hiro = pd.DataFrame(
        data={'入力': [val1_hiro,val2_hiro,val3_hiro,val4_hiro]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_hiro = input_df_hiro.copy()
    display_df_hiro.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_hiro)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_hiro = dir_path + '/' + model_dict_hiro[area_select_hiro]
    model_load_hiro = pickle.load(open(filename_path_hiro, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_hiro = str(round(model_load_hiro.predict(input_df_hiro)[0], 1))
    st.write(result_hiro, '万円')
