import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('札幌10区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_spp = list(filter(lambda x: 'sapporo' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_spp = {model_list_spp[0].split('_')[5]: model_list_spp[0],
                model_list_spp[1].split('_')[5]: model_list_spp[1],
                model_list_spp[2].split('_')[5]: model_list_spp[2],
                model_list_spp[3].split('_')[5]: model_list_spp[3],
                model_list_spp[4].split('_')[5]: model_list_spp[4],
                model_list_spp[5].split('_')[5]: model_list_spp[5],
                model_list_spp[6].split('_')[5]: model_list_spp[6],
                model_list_spp[7].split('_')[5]: model_list_spp[7],
                model_list_spp[8].split('_')[5]: model_list_spp[8],
                model_list_spp[9].split('_')[5]: model_list_spp[9]
                }

# 表記内容
markdown_sapporo = '''
学習データ基準月: 2023-08
'''
st.write(markdown_sapporo)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_spp = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('札幌市中央区',
                    '札幌市白石区',
                    '札幌市北区',
                    '札幌市南区',
                    '札幌市東区',
                    '札幌市西区',
                    '札幌市豊平区',
                    '札幌市手稲区',
                    '札幌市厚別区',
                    '札幌市清田区')
                    )

    # 築年数を入力
    val1_spp = st.slider('築年数', min_value=1, max_value=50)
    age_explanation = '''
    【築年数】新築物件は学習から除外しています。
    '''
    st.caption(age_explanation)

    # 間取り分類を入力
    val2_spp = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_spp = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_spp = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_spp = pd.DataFrame(
        data={'入力': [val1_spp,val2_spp,val3_spp,val4_spp]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_spp = input_df_spp.copy()
    display_df_spp.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_spp)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_spp = dir_path + '/' + model_dict_spp[area_select_spp]
    model_load_spp = pickle.load(open(filename_path_spp, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_spp = str(round(model_load_spp.predict(input_df_spp)[0], 1))
    st.write(result_spp, '万円')
