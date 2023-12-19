from flask import Flask, render_template, request
import os
import pandas as pd
import tensorflow as tf
import numpy as np

app = Flask(__name__)

data = pd.read_csv('name.csv')

def get_prediction_result(my_champion, enemy_champion):
    # 현재 스크립트 파일의 디렉토리 경로 가져오기
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 전적 CSV 파일로부터 데이터 불러오기 
    csv_file_path = os.path.join(script_dir, 'result.csv')
    df = pd.read_csv(csv_file_path, encoding='cp949')

    # 아이템 이름 매핑 CSV파일로부터 데이터 불러오기
    item_name_mapping_path = os.path.join(script_dir, 'item_name_mapping.csv')
    item_df = pd.read_csv(item_name_mapping_path, encoding='cp949')

    # 아이템 이름 매핑 CSV 파일로부터 갖고 온 아이템 이름 리스트화
    item_col = item_df['id'].values.astype(str).tolist()
    item_names = item_df.loc[:, "name"].values.tolist()
    # 딕셔너리로 id - names 매핑
    dict_item = {id: name for id, name in zip(item_col, item_names)}

    # 사용자 입력에 해당하는 데이터 추출
    matching_rows = df[(df['MY_CHAMPION'] == my_champion) & (df['ENEMY_CHAMPION'] == enemy_champion)]
    matching_index = matching_rows.index.tolist()

    # 입력한 정보에 대하여 일치 여부 확인
    if matching_rows.empty:
        result_message = "입력한 챔피언 조합이 데이터에 존재하지 않습니다."
    else:
        # 특성과 레이블 추출
        X = matching_rows[item_col].values  # 템트리 리스트
        y = matching_rows['WIN'].values     # 이겼는가

        #총 승률 계산
        true_count = matching_rows['WIN'].sum()
        total_win_rate = true_count / len(matching_index)

        # 퍼셉트론 모델 만들기
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(128, activation='relu', input_shape=(len(item_col),)))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        # 모델 컴파일
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # 모델 훈련
        model.fit(X, y, epochs=100)

        # 모델 예측
        predictions = model.predict(X)     # 각 템트리에 대한 적합도
        max_win_rate = np.max(predictions) # 최대 적합도
        max_index = np.argmax(predictions) # 최대 적합도가 나온 레이블 인덱스

        # 예측한 값에 대하여 승률 계산
        result_win_rate = (total_win_rate * max_win_rate).round(4)

        # 가장 높은 승률에 따른 템트리 나열
        result_item = [dict_item[id] for id in item_col if df.at[matching_index[max_index], id] == 1]
        result_message = f"{my_champion}이(가) {enemy_champion}와 겨룰 때 적합한 템트리는 {result_item}이고, 이로 인한 승률은 [{result_win_rate * 100:.2f}%] 로 예측됩니다."

    return result_message

@app.route('/', methods=['GET', 'POST'])
def index():
    result_message = None

    if request.method == 'POST':
        my_champion = request.form['myChampion']
        enemy_champion = request.form['enemyChampion']
        result_message = get_prediction_result(my_champion, enemy_champion)

    return render_template('index.html', result_message=result_message,champions=data['0'].tolist())

#@app.route('/')
def tag_index():
    my_champions = ["Champion1", "Champion2", "Champion3"]  # 실제 데이터로 대체
    enemy_champions = ["Enemy1", "Enemy2", "Enemy3"]  # 실제 데이터로 대체

    return render_template('index.html', my_champions=my_champions, enemy_champions=enemy_champions)

if __name__ == '__main__':
    app.run(debug=True)
