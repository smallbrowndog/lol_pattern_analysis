import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

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

# 모델 정의 (로지스틱 회귀만 사용)
models = {
    '로지스틱 회귀': LogisticRegression(),
}

# 30명의 플레이어 결과를 담을 리스트
player_results = []

# 플레이어별 데이터 그룹화
grouped = df.groupby('gamerName')

# 각 플레이어에 대해 반복
for player_name, group in grouped:
    player_data = {}  # 플레이어별 결과를 담을 딕셔너리 초기화
    player_data['Player'] = player_name  # 플레이어 이름

    for feature_list_group, model_name in zip(
        [[combat_at14, manage_at14, diff_at14], [combat_af14, manage_af14, diff_af14]],
        ['At14 Combined Model', 'AF14 Combined Model']
    ):
        # 해당 그룹의 특성 데이터
        x_player_group = group[sum(feature_list_group, [])]  # 그룹의 특성 리스트를 모두 합침
        x_player_group_scaled = scaler.fit_transform(x_player_group)  # 스케일링된 데이터

        # 각 모델에 대해 학습 및 예측 수행
        for model_key, model in models.items():
            model.fit(x_player_group_scaled, group['targetWin'].astype(int))  # 모델 학습

            # 예측
            y_pred = model.predict(x_player_group_scaled)
            y_pred_class = (y_pred >= 0.5).astype(int)  # 확률을 이진값으로 변환

            # 정확도 계산
            accuracy = accuracy_score(group['targetWin'].astype(int), y_pred_class)
            f1 = f1_score(group['targetWin'].astype(int), y_pred_class)

            # 정확도, f1-score 저장: 각 특성 그룹에 대해 모델별 정확도 저장
            player_data[f'{model_key} - {model_name} Accuracy'] = accuracy  # 정확도 저장
            player_data[f'{model_key} - {model_name} F1 Score'] = f1  # F1-Score 저장

            # 모델의 특성 중요도 (가장 중요한 특성 추출)
            if model_key == '로지스틱 회귀':  # 로지스틱 회귀 모델은 특성의 중요도 확인 가능
                coef = model.coef_[0]
                importance = dict(zip(sum(feature_list_group, []), coef))  # 특성별 중요도 저장
                player_data[f'{model_key} - {model_name} Feature Importance'] = json.dumps(importance)  # 중요도 저장

    # 플레이어의 예측 결과 저장
    player_results.append(player_data)

# 최종 예측 결과 표 출력 (각 모델에 대해 예측한 정확도 및 f1-score)
player_results_df = pd.DataFrame(player_results)

# CSV 파일로 저장
player_results_df.to_csv('플레이어별 정확도 및 f1-score 결과.csv', encoding='utf-8-sig', index=False)

# 출력
print("\n플레이어별 정확도 및 f1-score 결과:")
print(player_results_df)
