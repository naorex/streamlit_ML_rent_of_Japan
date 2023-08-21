import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('神戸9区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_kob = list(filter(lambda x: 'koube' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_kob = {model_list_kob[0].split('_')[5]: model_list_kob[0],
                model_list_kob[1].split('_')[5]: model_list_kob[1],
                model_list_kob[2].split('_')[5]: model_list_kob[2],
                model_list_kob[3].split('_')[5]: model_list_kob[3],
                model_list_kob[4].split('_')[5]: model_list_kob[4],
                model_list_kob[5].split('_')[5]: model_list_kob[5],
                model_list_kob[6].split('_')[5]: model_list_kob[6],
                model_list_kob[7].split('_')[5]: model_list_kob[7],
                model_list_kob[8].split('_')[5]: model_list_kob[8]
                }

# 表記内容
markdown_koube = '''
学習データ基準月: 2023-08
'''
st.write(markdown_koube)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_kob = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('神戸市中央区',
                    '神戸市灘区',
                    '神戸市須磨区',
                    '神戸市北区',
                    '神戸市兵庫区',
                    '神戸市東灘区',
                    '神戸市垂水区',
                    '神戸市西区',
                    '神戸市長田区')
                    )

    # 築年数を入力
    val1_kob = st.slider('築年数', min_value=1, max_value=50)
    age_explanation = '''
    【築年数】新築物件は学習から除外しています。
    '''
    st.caption(age_explanation)

    # 間取り分類を入力
    val2_kob = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_kob = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_kob = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_kob = pd.DataFrame(
        data={'入力': [val1_kob,val2_kob,val3_kob,val4_kob]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_kob = input_df_kob.copy()
    display_df_kob.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_kob)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_kob = dir_path + '/' + model_dict_kob[area_select_kob]
    model_load_kob = pickle.load(open(filename_path_kob, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_kob = str(round(model_load_kob.predict(input_df_kob)[0], 1))
    st.write(result_kob, '万円')
