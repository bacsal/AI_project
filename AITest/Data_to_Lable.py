import pandas as pd

# api로부터 수집한 데이터 csv 파일 로드
df = pd.read_csv('C:/Users/pass0/OneDrive/Desktop/tes.csv')

# 아이템 컬럼 초기화
item_col = [2065, 3001, 3003, 3004, 3006, 3009, 3011, 3020, 3026, 3031, 3033, 3035, 3036, 3040, 3041, 3042, 3046, 3047, 3050, 3053, 3065, 3068, 3071, 3072, 3074, 3075, 3078, 3083, 3084, 3085, 3091, 3094, 3095, 3100, 3102, 3105, 3107, 3109, 3110, 3111, 3115, 3116, 3117, 3119, 3121, 3124, 3135, 3139, 3142, 3143, 3152, 3153, 3156, 3157, 3158, 3161, 3165, 3179, 3181, 3190, 3193, 3222, 3504, 3508, 3742, 3748, 3814, 3850, 3851, 3853, 3854, 3855, 3857, 3858, 3859, 3860, 3862, 3863, 3864, 4005, 4628, 4629, 4633, 4636, 4637, 4643, 4644, 4645, 6035, 6333, 6609, 6616, 6617, 6620, 6630, 6631, 6632, 6653, 6655, 6656, 6657, 6662, 6664, 6665, 6667, 6671, 6672, 6673, 6675, 6676, 6691, 6692, 6693, 6694, 6695, 6696, 8001, 8020
]

# 결과 데이터프레임 초기화
result_df = pd.DataFrame(columns=['MY_CHAMPION', 'ENEMY_CHAMPION'] + item_col + ['WIN'])

# 수집한 데이터 csv의 각 행을 순회
for index, row in df.iterrows():
    my_champion = row['championName']   #챔피언 이름
    match_id = row['matchId']           #해당 챔피언이 치룬 경기
    win = row['win']                    #이겼는지?
    items = [row['item1'], row['item2'], row['item3'], row['item4'], row['item5'], row['item6']]    #해당 챔피언이 간 아이템(완성템만 취급)

    # 적 챔피언 찾기
    enemy_champions = df[(df['matchId'] == match_id) & (df['win'] != win)]['championName'].tolist()

    # 각 적 챔피언에 대해
    for enemy_champion in enemy_champions:
        # MY_CHAMPION과 ENEMY_CHAMPION을 조합하여 행 생성
        result_row = {'MY_CHAMPION': my_champion, 'ENEMY_CHAMPION': enemy_champion}
        
        # MY_CHAMPION이 해당 아이템을 구매했는지 확인
        for item_column in item_col:
            for i in items:
                if item_column == i:
                    result_row[item_column] = 1
                    break
                else:
                    result_row[item_column] = 0

        # 이긴 여부 설정
        result_row['WIN'] = win

        # 결과 데이터프레임에 행 추가
        result_df = pd.concat([result_df, pd.DataFrame([result_row])], ignore_index=True)

# 결과 데이터프레임을 csv로 저장
result_df.to_csv('C:/Users/pass0/OneDrive/Desktop/result.csv', index=False)