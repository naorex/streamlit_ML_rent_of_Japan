import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('名古屋16区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_nago = list(filter(lambda x: 'nagoya' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_nago = {model_list_nago[0].split('_')[5]: model_list_nago[0],
                model_list_nago[1].split('_')[5]: model_list_nago[1],
                model_list_nago[2].split('_')[5]: model_list_nago[2],
                model_list_nago[3].split('_')[5]: model_list_nago[3],
                model_list_nago[4].split('_')[5]: model_list_nago[4],
                model_list_nago[5].split('_')[5]: model_list_nago[5],
                model_list_nago[6].split('_')[5]: model_list_nago[6],
                model_list_nago[7].split('_')[5]: model_list_nago[7],
                model_list_nago[8].split('_')[5]: model_list_nago[8],
                model_list_nago[9].split('_')[5]: model_list_nago[9],
                model_list_nago[10].split('_')[5]: model_list_nago[10],
                model_list_nago[11].split('_')[5]: model_list_nago[11],
                model_list_nago[12].split('_')[5]: model_list_nago[12],
                model_list_nago[13].split('_')[5]: model_list_nago[13],
                model_list_nago[14].split('_')[5]: model_list_nago[14],
                model_list_nago[15].split('_')[5]: model_list_nago[15],
                }

# 表記内容
markdown_nagoya = '''
学習データ基準月: 2023-07
'''
st.write(markdown_nagoya)

st.subheader('家賃予測に必要な変数を入力')

with st.form('家賃予測フォーム'):

    # エリアを選択
    area_select_nago = st.selectbox(
                    '家賃予測するエリアを選択',
                    ('名古屋市中区',
                    '名古屋市東区',
                    '名古屋市中村区',
                    '名古屋市千種区',
                    '名古屋市熱田区',
                    '名古屋市西区',
                    '名古屋市昭和区',
                    '名古屋市北区',
                    '名古屋市瑞穂区',
                    '名古屋市南区',
                    '名古屋市中川区',
                    '名古屋市名東区',
                    '名古屋市天白区',
                    '名古屋市守山区',
                    '名古屋市港区',
                    '名古屋市緑区')
                    )

    # 築年数を入力
    val1_nago = st.slider('築年数', min_value=1, max_value=50)

    # 間取り分類を入力
    val2_nago = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_nago = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_nago = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_nago = pd.DataFrame(
        data={'入力': [val1_nago,val2_nago,val3_nago,val4_nago]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_nago = input_df_nago.copy()
    display_df_nago.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_nago)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_nago = dir_path + '\\' + model_dict_nago[area_select_nago]
    model_load_nago = pickle.load(open(filename_path_nago, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_nago = str(round(model_load_nago.predict(input_df_nago)[0], 1))
    st.write(result_nago, '万円')
