import os
import pandas as pd
import tensorflow as tf
import numpy as np

# 현재 스크립트 파일의 디렉토리 경로 갖고 오기
script_dir = os.path.dirname(os.path.abspath(__file__))

# 전적 CSV 파일로부터 데이터 불러오기 
csv_file_path = os.path.join(script_dir, 'Lable.csv')
df = pd.read_csv(csv_file_path, encoding='cp949')

# 아이템 이름 매핑 CSV파일로부터 데이터 불러오기
item_name_mapping_path = os.path.join(script_dir, 'item_name_mapping.csv')
item_df = pd.read_csv(item_name_mapping_path, encoding='cp949')

# 아이템 이름 매핑 CSV 파일로부터 갖고 온 아이템 이름 리스트화
item_col = item_df['id'].values.astype(str).tolist()
item_names = item_df.loc[:, "name"].values.tolist()
# 딕셔너리로 id - names 매핑
dict_item = {id: name for id, name in zip(item_col, item_names)}
# 사용자 입력 받기
my_champion = input("내 챔피언 이름을 말해주세요: ")
enemy_champion = input("적의 챔피언 이름을 말해주세요: ")

# 사용자 입력에 해당하는 데이터 추출
matching_rows = df[(df['MY_CHAMPION'] == my_champion) & (df['ENEMY_CHAMPION'] == enemy_champion)]
matching_index = matching_rows.index.tolist()
print(matching_index)

# 입력한 정보에 대하여 일치 여부 확인
if matching_rows.empty:
    print("입력한 챔피언 조합이 데이터에 존재하지 않습니다.")
else:

    # 특성과 레이블 추출
    X = matching_rows[item_col].values
    y = matching_rows['WIN'].values

    #총 승률 계산
    true_count = matching_rows['WIN'].sum()
    total_win_rate = true_count / len(matching_index)

    print("true_count = ", true_count)
    print(total_win_rate)

    print("X = ", X)    # 템트리 리스트
    print("y = ", y)    # 이겼는가

    # 퍼셉트론 모델 만들기
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(128, activation='relu', input_shape=(len(item_col),)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid')) # 손실함수 BCE 사용으로 sigmoid 사용

    # 모델 컴파일
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # 레이블이 0, 1로만 구분하기에 손실함수는 BCE를 적용

    # 모델 훈련
    model.fit(X, y, epochs=100)

    #모델 예측
    predictions = model.predict(X)     # 각 템트리에 대한 적합도
    max_win_rate = np.max(predictions) # 최대 적합도
    max_index = np.argmax(predictions) # 최대 적합도가 나온 레이블 인덱스
    
    #예측한 값에 대하여 승률 계산
    result_win_rate = (total_win_rate * max_win_rate).round(4)

    #가장 높은 승률에 따른 템트리 나열
    result_item = [ dict_item[id] for id in item_col if df.at[matching_index[max_index], id] == 1]
    print("* 계산 결과 *")
    print(my_champion, "이(가) ", enemy_champion, "와 겨룰 때 적합한 템트리는 ", result_item, "이고, 이로 인한 승률은 [", f"{result_win_rate * 100:.2f}", "% ] 로 예측됩니다.")






