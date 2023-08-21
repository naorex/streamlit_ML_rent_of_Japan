import streamlit as st
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

st.title('大阪24区')

# 学習済みモデルを読込
dir_path = './model_save'
model_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
model_list_osa = list(filter(lambda x: 'osaka' in x, model_list))

# エリア選択に対応する辞書を作成
model_dict_osa = {model_list_osa[0].split('_')[5]: model_list_osa[0],
                model_list_osa[1].split('_')[5]: model_list_osa[1],
                model_list_osa[2].split('_')[5]: model_list_osa[2],
                model_list_osa[3].split('_')[5]: model_list_osa[3],
                model_list_osa[4].split('_')[5]: model_list_osa[4],
                model_list_osa[5].split('_')[5]: model_list_osa[5],
                model_list_osa[6].split('_')[5]: model_list_osa[6],
                model_list_osa[7].split('_')[5]: model_list_osa[7],
                model_list_osa[8].split('_')[5]: model_list_osa[8],
                model_list_osa[9].split('_')[5]: model_list_osa[9],
                model_list_osa[10].split('_')[5]: model_list_osa[10],
                model_list_osa[11].split('_')[5]: model_list_osa[11],
                model_list_osa[12].split('_')[5]: model_list_osa[12],
                model_list_osa[13].split('_')[5]: model_list_osa[13],
                model_list_osa[14].split('_')[5]: model_list_osa[14],
                model_list_osa[15].split('_')[5]: model_list_osa[15],
                model_list_osa[16].split('_')[5]: model_list_osa[16],
                model_list_osa[17].split('_')[5]: model_list_osa[17],
                model_list_osa[18].split('_')[5]: model_list_osa[18],
                model_list_osa[19].split('_')[5]: model_list_osa[19],
                model_list_osa[20].split('_')[5]: model_list_osa[20],
                model_list_osa[21].split('_')[5]: model_list_osa[21],
                model_list_osa[22].split('_')[5]: model_list_osa[22],
                model_list_osa[23].split('_')[5]: model_list_osa[23]
                }

# 表記内容
markdown_osaka = '''
学習データ基準月: 2023-07
'''
st.write(markdown_osaka)

st.subheader('家賃推定に必要な変数を入力')

with st.form('家賃推定フォーム'):

    # エリアを選択
    area_select_osa = st.selectbox(
                    '家賃推定するエリアを選択',
                    ('大阪市中央区',
                    '大阪市西区',
                    '大阪市北区',
                    '大阪市浪速区',
                    '大阪市福島区',
                    '大阪市天王寺区',
                    '大阪市淀川区',
                    '大阪市西淀川区',
                    '大阪市港区',
                    '大阪市都島区',
                    '大阪市東成区',
                    '大阪市阿倍野区',
                    '大阪市城東区',
                    '大阪市此花区',
                    '大阪市西成区',
                    '大阪市旭区',
                    '大阪市大正区',
                    '大阪市東淀川区',
                    '大阪市生野区',
                    '大阪市鶴見区',
                    '大阪市東住吉区',
                    '大阪市住之江区',
                    '大阪市住吉区',
                    '大阪市平野区')
                    )

    # 築年数を入力
    val1_osa = st.slider('築年数', min_value=1, max_value=50)
    age_explanation = '''
    【築年数】新築物件は学習から除外しています。
    '''
    st.caption(age_explanation)

    # 間取り分類を入力
    val2_osa = st.slider('間取り分類', min_value=0, max_value=5)
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
    val3_osa = st.slider('部屋面積（m2）', min_value=15, max_value=50)

    # 徒歩をスライダー入力
    val4_osa = st.slider('最寄り駅までの徒歩時間（分）', min_value=1, max_value=30)

    # 入力結果をモデル入力用のdataframeへ格納
    input_df_osa = pd.DataFrame(
        data={'入力': [val1_osa,val2_osa,val3_osa,val4_osa]},
        index=['築年数','間取り分類','面積','徒歩']
        ).T

    # 入力内容を表示
    st.subheader('入力内容')
    display_df_osa = input_df_osa.copy()
    display_df_osa.columns = ['築年数','間取り分類','面積（m2）','徒歩（分）']
    st.dataframe(display_df_osa)

    submit_btn = st.form_submit_button('家賃推定を実行')

# 入力内容が決まったら学習モデルへデータを渡す
if submit_btn:

    # 学習済みモデルを読込
    filename_path_osa = dir_path + '/' + model_dict_osa[area_select_osa]
    model_load_osa = pickle.load(open(filename_path_osa, 'rb'))

    # 予測結果を表示
    st.subheader('家賃推定結果')
    result_osa = str(round(model_load_osa.predict(input_df_osa)[0], 1))
    st.write(result_osa, '万円')
