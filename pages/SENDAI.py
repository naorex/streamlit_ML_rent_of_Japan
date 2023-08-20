import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('仙台5区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_sen = list(filter(lambda x: 'sendai' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_sen = {model_list_sen[0].split('_')[5]: model_list_sen[0],
                model_list_sen[1].split('_')[5]: model_list_sen[1],
                model_list_sen[2].split('_')[5]: model_list_sen[2],
                model_list_sen[3].split('_')[5]: model_list_sen[3],
                model_list_sen[4].split('_')[5]: model_list_sen[4]
                }

# 表記内容
markdown_sendai = '''
学習データ基準月: 2023-08\n
（注）新築物件は学習から除外
'''
st.write(markdown_sendai)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_sen = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('仙台市太白区',
                    '仙台市泉区',
                    '仙台市若林区',
                    '仙台市青葉区',
                    '仙台市宮城野区')
                    )

    # 築年数を入力
    val1_sen = st.slider('築年数', min_value=1, max_value=50)

    # 間取り分類を入力
    val2_sen = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_sen = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_sen = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_sen = pd.DataFrame(
        data={'入力': [val1_sen,val2_sen,val3_sen,val4_sen]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_sen = input_df_sen.copy()
    display_df_sen.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_sen)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_sen = dir_path + '/' + model_dict_sen[area_select_sen]
    model_load_sen = pickle.load(open(filename_path_sen, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_sen = str(round(model_load_sen.predict(input_df_sen)[0], 1))
    st.write(result_sen, '万円')
