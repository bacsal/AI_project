import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

# CSV 파일로부터 데이터 불러오기 / 코랩 좌측 파일 모양 - 드라이브 모양 파일 누르고 연결 - 경로 갖고오기
csv_file_path = "https://raw.githubusercontent.com/bacsal/AI_project/main/AITest/result.csv?token=GHSAT0AAAAAACLPVTFAKUHBPMLCGO7LU5H6ZL5ZITA"
df = pd.read_csv(csv_file_path)

# 사용자 입력 받기
my_champion = input("내 챔피언 이름을 말해주세요: ")
enemy_champion = input("적의 챔피언 이름을 말해주세요: ")

# 사용자 입력에 해당하는 데이터 추출
matching_rows = df[(df['MY_CHAMPION'] == my_champion) & (df['ENEMY_CHAMPION'] == enemy_champion)]

if matching_rows.empty:
    print("입력한 챔피언 조합이 데이터에 존재하지 않습니다.")
else:
    # 특성 열 선택
    item_col = ['2065', '3001', '3003', '3004', '3011', '3026', '3031', '3033', '3035', '3036', '3040', '3041', '3042', '3046', '3047',
            '3050', '3053', '3065', '3068', '3071', '3072', '3074', '3075', '3078', '3083', '3084', '3085', '3091', '3094', '3095',
            '3100', '3102', '3105', '3107', '3109', '3110', '3115', '3116', '3119', '3121', '3124', '3135', '3139', '3142', '3143',
            '3152', '3153', '3156', '3157', '3161', '3165', '3179', '3181', '3190', '3193', '3222', '3504', '3508', '3742', '3748',
            '3814', '3850', '3851', '3853', '3854', '3855', '3857', '3858', '3859', '3860', '3862', '3863', '3864', '4005', '4628',
            '4629', '4633', '4636', '4637', '4643', '4644', '4645', '6035', '6333', '6609', '6616', '6617', '6620', '6630', '6631',
            '6632', '6653', '6655', '6656', '6657', '6662', '6664', '6665', '6667', '6671', '6672', '6673', '6675', '6676', '6691',
            '6692', '6693', '6694', '6695', '6696', '8001', '8020']

    # ITEM 코드에 대한 이름 매핑
    #item_name = {'ITEM_1000': '사과', 'ITEM_1001': '바나나', 'ITEM_1002': '귤', 'ITEM_1003': '수박', 'ITEM_2000': '망고', 'ITEM_2001': '파인애플', 'ITEM_2002': '배', 'ITEM_2003': '메론'}

    #총 승률 계산
    true_count = df['WIN'].sum()
    total_win_rate = true_count / len(df)

    # 특성과 레이블 추출
    X = matching_rows[item_col].values
    y = matching_rows['WIN'].values

    # 데이터를 훈련 세트와 테스트 세트로 분할
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 퍼셉트론 모델 만들기
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(128, activation='relu', input_shape=(len(item_col),)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid')) # 손실함수 BCE 사용으로 sigmoid 사용

    # 모델 컴파일
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # 레이블이 0, 1로만 구분하기에 손실함수는 BCE를 적용

    # 모델 훈련
    model.fit(X, y, epochs=100)
    #model.fit(X_train, y_train, epochs=10)
    #model.evaluate(X_test, y_test)

    #모델 예측
    predictions = model.predict(X)
    max_win_rate = np.max(predictions) #최대 적합도
    max_index = np.argmax(predictions) #최대 적합도가 나온 레이블 인덱스

    #예측한 값에 대하여 승률 계산
    result_win_rate = (total_win_rate * max_win_rate).round(4)

    #가장 높은 승률에 따른 템트리 나열
    result_item = [ col for col in item_col if df.at[max_index, col] == 1]
                    #item_name[col]
    print("* 계산 결과 *")
    print(my_champion, "이(가) ", enemy_champion, "와 겨룰 때 적합한 템트리는 ", result_item, "이고, 이로 인한 승률은 [", f"{result_win_rate * 100:.2f}", "% ] 로 예측됩니다.")






