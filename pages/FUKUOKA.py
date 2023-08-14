import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('福岡7区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_fuk = list(filter(lambda x: 'fukuoka' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_fuk = {model_list_fuk[0].split('_')[5]: model_list_fuk[0],
                model_list_fuk[1].split('_')[5]: model_list_fuk[1],
                model_list_fuk[2].split('_')[5]: model_list_fuk[2],
                model_list_fuk[3].split('_')[5]: model_list_fuk[3],
                model_list_fuk[4].split('_')[5]: model_list_fuk[4],
                model_list_fuk[5].split('_')[5]: model_list_fuk[5],
                model_list_fuk[6].split('_')[5]: model_list_fuk[6]
                }

# 表記内容
markdown_fukuoka = '''
学習データ基準月: 2023-07
'''
st.write(markdown_fukuoka)

st.subheader('家賃予測に必要な変数を入力')

with st.form('家賃予測フォーム'):

    # エリアを選択
    area_select_fuk = st.selectbox(
                    '家賃予測するエリアを選択',
                    ('福岡市中央区',
                    '福岡市博多区',
                    '福岡市早良区',
                    '福岡市南区',
                    '福岡市東区',
                    '福岡市西区',
                    '福岡市城南区')
                    )

    # 築年数を入力
    val1_fuk = st.slider('築年数', min_value=1, max_value=50)

    # 間取り分類を入力
    val2_fuk = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_fuk = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_fuk = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_fuk = pd.DataFrame(
        data={'入力': [val1_fuk,val2_fuk,val3_fuk,val4_fuk]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_fuk = input_df_fuk.copy()
    display_df_fuk.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_fuk)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_fuk = dir_path + '/' + model_dict_fuk[area_select_fuk]
    model_load_fuk = pickle.load(open(filename_path_fuk, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_fuk = str(round(model_load_fuk.predict(input_df_fuk)[0], 1))
    st.write(result_fuk, '万円')
