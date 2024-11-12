import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# 데이터 불러오기
df = pd.read_json("./final_target_data.json")

# 특성 리스트 정의
combat_at14 = ["at14killsRatio", "at14deathsRatio", "at14assistsRatio",
               "at14solokillsRatio", "at14solodeathsRatio", "at14dpm", "at14dtpm"]

manage_at14 = ["at14cspmManage", "at14gpmManage", "at14xpmManage", "at14dpdManage", "at14dpgManage"]

diff_at14 = ["at14dpmDiff", "at14dtpmDiff", "at14cspmDiff", "at14gpmDiff", "at14xpmDiff", "at14dpdDiff", "at14dpgDiff"]

combat_af14 = ["af14killsRatio", "af14deathsRatio", "af14assistsRatio",
               "af14solokillsRatio", "af14solodeathsRatio", "af14dpm", "af14dtpm"]

manage_af14 = ["af14cspmManage", "af14gpmManage", "af14xpmManage", "af14dpdManage", "af14dpgManage"]

diff_af14 = ["af14dpmDiff", "af14dtpmDiff", "af14cspmDiff", "af14gpmDiff", "af14xpmDiff", "af14dpdDiff", "af14dpgDiff"]


# 타겟 변수
y = df['targetWin'].astype(int)

# 데이터 스케일링을 위한 표준화
scaler = StandardScaler()

# 모델들 정의
models = {
    '로지스틱 회귀': LogisticRegression(),
    '다중선형 회귀': LinearRegression(),
    '서포트 벡터 머신': SVC(probability=True)
}

# 30명의 플레이어 결과를 담을 리스트
player_results = []

from sklearn.metrics import accuracy_score

# 플레이어별 데이터 그룹화
grouped = df.groupby('gamerName')

# 각 플레이어에 대해 반복
for player_name, group in grouped:
    player_data = {}
    player_data['Player'] = player_name  # 플레이어 이름

    # 각 특성 리스트로 분리하여 모델 학습 및 예측 수행
    for feature_list, model_name in zip([combat_at14, manage_at14, diff_at14, combat_af14, manage_af14, diff_af14],
                                        ['At14 Combat Model', 'At14 Manage Model', 'At14 Diff Model', 'AF14 Combat Model', 'AF14 Manage Model', 'AF14 Diff Model']):
        x_player = group[feature_list]  # 해당 플레이어의 특정 특성 데이터
        x_player_scaled = scaler.fit_transform(x_player)  # 스케일링된 데이터

        # 각 모델에 대해 학습 및 예측 수행
        for model_key, model in models.items():
            model.fit(x_player_scaled, group['targetWin'].astype(int))  # 모델 학습

            # 예측
            y_pred = model.predict(x_player_scaled)
            y_pred_class = (y_pred >= 0.5).astype(int)  # 확률을 이진값으로 변환

            # 정확도 계산
            accuracy = accuracy_score(group['targetWin'].astype(int), y_pred_class)

            # 예측값과 정확도 저장: 각 특성 리스트에 대해 모델별 정확도 저장
            player_data[f'{model_key} - {model_name} Accuracy'] = accuracy  # 정확도 저장

    # 플레이어의 예측 결과 저장
    player_results.append(player_data)

# 최종 예측 결과 표 출력 (각 모델에 대해 예측한 정확도)
player_results_df = pd.DataFrame(player_results)

# CSV 파일로 저장
player_results_df.to_csv('플레이어별 정확도 결과.csv', encoding='utf-8-sig', index=False)

# 출력
print("\n플레이어별 정확도 결과:")
print(player_results_df)
