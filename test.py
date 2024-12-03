# 필요한 라이브러리 불러오기
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score

df = pd.read_json("./final_target_data.json")

# 데이터프레임 열 이름 리스트 정의
combat_at14 = ["at14killsRatio", "at14deathsRatio", "at14assistsRatio",
               "at14solokillsRatio", "at14solodeathsRatio", "at14dpm", "at14dtpm"]

manage_at14 = ["at14cspmManage", "at14gpmManage", "at14xpmManage", "at14dpdManage", "at14dpgManage"]

diff_at14 = ["at14dpmDiff", "at14dtpmDiff", "at14cspmDiff", "at14gpmDiff", "at14xpmDiff", "at14dpdDiff", "at14dpgDiff"]

combat_af14 = ["af14killsRatio", "af14deathsRatio", "af14assistsRatio",
               "af14solokillsRatio", "af14solodeathsRatio", "af14dpm", "af14dtpm"]

manage_af14 = ["af14cspmManage", "af14gpmManage", "af14xpmManage", "af14dpdManage", "af14dpgManage"]

diff_af14 = ["af14dpmDiff", "af14dtpmDiff", "af14cspmDiff", "af14gpmDiff", "af14xpmDiff", "af14dpdDiff", "af14dpgDiff"]

at14 = combat_at14 + manage_at14 + diff_at14
af14 = combat_af14 + manage_af14 + diff_af14

all = at14 + af14

# 특징 변수와 타깃 변수 추출
x = df[all]
y = df['targetWin'].astype(int)  # 타깃 변수를 정수형으로 변환

# 특징 변수 표준화
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# PCA 적용 (주성분 2개로 축소)
pca = PCA(n_components=3)
x_pca = pca.fit_transform(x_scaled)

# 훈련 데이터와 테스트 데이터로 분할
x_train, x_test, y_train, y_test = train_test_split(x_pca, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 분류기 모델 학습
model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

# 테스트 데이터로 예측 수행
y_pred = model.predict(x_test)

threshold = 0.6
y_pred_class = (y_pred >= threshold).astype(int)

accuracy = accuracy_score(y_test, y_pred)
auroc = roc_auc_score(y_test, y_pred)

print(f"정확도 (Accuracy, threshold: {threshold}): {accuracy}")
print(f"AUROC: {auroc}")

# 모델 성능 평가
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)

# 한글 폰트 설정
plt.rcParams['font.family'] ='Malgun Gothic'

# PCA 결과 시각화
plt.figure(figsize=(10,6))
scatter = plt.scatter(x_pca[:,0], x_pca[:,1], c=y, cmap='viridis', edgecolor='k', s=40)
plt.xlabel('주성분 1')
plt.ylabel('주성분 2')
plt.title('플레이어 통계의 PCA')
plt.colorbar(scatter, label='타깃 결과 (승/패)')
plt.show()


# 3D 시각화를 위한 Figure 생성
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# 3D 산점도 생성
scatter = ax.scatter(x_pca[:, 0], x_pca[:, 1], x_pca[:, 2], c=y, cmap='viridis', edgecolor='k', s=40)

# 레이블 및 타이틀 설정
ax.set_xlabel('주성분 1')
ax.set_ylabel('주성분 2')
ax.set_zlabel('주성분 3')
ax.set_title('플레이어 통계의 PCA (3D)')

# 색상바 추가
cbar = plt.colorbar(scatter, ax=ax, label='타깃 결과 (승/패)')
plt.show()