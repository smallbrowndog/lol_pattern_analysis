import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score
from sklearn.decomposition import PCA

df = pd.read_json("./final_target_data.json")


combat_at14 = ["at14killsRatio","at14deathsRatio","at14assistsRatio",
               "at14solokillsRatio","at14solodeathsRatio","at14dpm","at14dtpm"]

manage_at14 = ["at14cspmManage","at14gpmManage","at14xpmManage","at14dpdManage","at14dpgManage"]

diff_at14 = ["at14dpmDiff","at14dtpmDiff","at14cspmDiff","at14gpmDiff","at14xpmDiff","at14dpdDiff","at14dpgDiff"]


combat_af14 = ["af14killsRatio","af14deathsRatio","af14assistsRatio",
               "af14solokillsRatio","af14solodeathsRatio","af14dpm","af14dtpm"]

manage_af14 = ["af14cspmManage","af14gpmManage","af14xpmManage","af14dpdManage","af14dpgManage"]

diff_af14 = ["af14dpmDiff","af14dtpmDiff","af14cspmDiff","af14gpmDiff","af14xpmDiff","af14dpdDiff","af14dpgDiff"]

# print(df[combat_at14].head())

from sklearn.preprocessing import StandardScaler  # 표준화 패키지 라이브러리

x = df[combat_at14]
y = df['targetWin'].astype(int)

x = StandardScaler().fit_transform(x) # x객체에 x를 표준화한 데이터를 저장

# print(pd.DataFrame(x, columns=combat_at14).head())



# # 선형회귀
# model = LinearRegression()
# model.fit(x, y)
#
# print("모델 계수 (theta) : ", model.coef_)
# print("모델 절편 (b) : ", model.intercept_)
#
# y_pred = model.predict(x)
#
# threshold = 0.5
# y_pred_class = (y_pred >= threshold).astype(int)
#
# accuracy = accuracy_score(y, y_pred_class)
# auroc = roc_auc_score(y, y_pred)
#
# print(f"정확도 (Accuracy, threshold: {threshold}): {accuracy}")
# print(f"AUROC: {auroc}")