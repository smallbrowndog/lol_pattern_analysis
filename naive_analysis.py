import pandas as pd
import numpy as np
import json

df = pd.read_json("./final_target_data.json")

combat_at14 = ["at14killsRatio","at14deathsRatio","at14assistsRatio",
               "at14solokillsRatio","at14solodeathsRatio","at14dpm","at14dtpm"]

manage_at14 = ["at14cspmManage","at14gpmManage","at14xpmManage","at14dpdManage","at14dpgManage"]

diff_at14 = ["at14dpmDiff","at14dtpmDiff","at14cspmDiff","at14gpmDiff","at14xpmDiff","at14dpdDiff","at14dpgDiff"]

combat_at14_x = df[combat_at14]
manage_at14_x = df[manage_at14]
diff_at14_x = df[diff_at14]
y = df['targetWin'].astype(int)

# print(x)
# print(y)

from sklearn.preprocessing import StandardScaler

# 데이터 스케일링
scaler = StandardScaler()
x_scaled = scaler.fit_transform(combat_at14_x)
print(combat_at14_x)
print(x_scaled)

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.metrics import confusion_matrix

model = LogisticRegression()
model.fit(combat_at14_x, y)

print("모델 계수 (theta):", model.coef_)
print("모델 절편 (b):", model.intercept_)

y_pred = model.predict(combat_at14_x)
y_pred_class = (y_pred >= 0.5).astype(int)
print("평균 제곱 오차 (MSE):", mean_squared_error(y, y_pred))
print("분류 보고서:")
print(classification_report(y, y_pred_class))
print("혼동 행렬:")
print(confusion_matrix(y, y_pred_class))




combat_af14 = ["af14killsRatio","af14deathsRatio","af14assistsRatio",
               "af14solokillsRatio","af14solodeathsRatio","af14dpm","af14dtpm"]

manage_af14 = ["af14cspmManage","af14gpmManage","af14xpmManage","af14dpdManage","af14dpgManage"]

diff_af14 = ["af14dpmDiff","af14dtpmDiff","af14cspmDiff","af14gpmDiff","af14xpmDiff","af14dpdDiff","af14dpgDiff"]

df_combat_af14 = df[combat_af14]

