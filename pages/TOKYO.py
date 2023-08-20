import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('東京23区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_tok = list(filter(lambda x: 'tokyo' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_tok = {model_list_tok[0].split('_')[5]: model_list_tok[0],
                model_list_tok[1].split('_')[5]: model_list_tok[1],
                model_list_tok[2].split('_')[5]: model_list_tok[2],
                model_list_tok[3].split('_')[5]: model_list_tok[3],
                model_list_tok[4].split('_')[5]: model_list_tok[4],
                model_list_tok[5].split('_')[5]: model_list_tok[5],
                model_list_tok[6].split('_')[5]: model_list_tok[6],
                model_list_tok[7].split('_')[5]: model_list_tok[7],
                model_list_tok[8].split('_')[5]: model_list_tok[8],
                model_list_tok[9].split('_')[5]: model_list_tok[9],
                model_list_tok[10].split('_')[5]: model_list_tok[10],
                model_list_tok[11].split('_')[5]: model_list_tok[11],
                model_list_tok[12].split('_')[5]: model_list_tok[12],
                model_list_tok[13].split('_')[5]: model_list_tok[13],
                model_list_tok[14].split('_')[5]: model_list_tok[14],
                model_list_tok[15].split('_')[5]: model_list_tok[15],
                model_list_tok[16].split('_')[5]: model_list_tok[16],
                model_list_tok[17].split('_')[5]: model_list_tok[17],
                model_list_tok[18].split('_')[5]: model_list_tok[18],
                model_list_tok[19].split('_')[5]: model_list_tok[19],
                model_list_tok[20].split('_')[5]: model_list_tok[20],
                model_list_tok[21].split('_')[5]: model_list_tok[21],
                model_list_tok[22].split('_')[5]: model_list_tok[22]
                }

# 表記内容
markdown_tokyo = '''
学習データ基準月: 2023-07\n
（注）新築物件は学習から除外
'''
st.write(markdown_tokyo)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_tok = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('港区',
                    '渋谷区',
                    '千代田区',
                    '中央区',
                    '新宿区',
                    '目黒区',
                    '台東区',
                    '品川区',
                    '文京区',
                    '江東区',
                    '墨田区',
                    '豊島区',
                    '中野区',
                    '世田谷区',
                    '大田区',
                    '杉並区',
                    '北区',
                    '荒川区',
                    '板橋区',
                    '練馬区',
                    '足立区',
                    '葛飾区',
                    '江戸川区')
                    )

    # 築年数を入力
    val1_tok = st.slider('築年数', min_value=1, max_value=50)

    # 間取り分類を入力
    val2_tok = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_tok = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_tok = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_tok = pd.DataFrame(
        data={'入力': [val1_tok,val2_tok,val3_tok,val4_tok]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_tok = input_df_tok.copy()
    display_df_tok.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_tok)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_tok = dir_path + '/' + model_dict_tok[area_select_tok]
    model_load_tok = pickle.load(open(filename_path_tok, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_tok = str(round(model_load_tok.predict(input_df_tok)[0], 1))
    st.write(result_tok, '万円')
