# ADR — 핵심 의사결정 기록

**프로젝트:** 모듈 1 ML/DL 기초 미니프로젝트 — 회귀·분류

> 실험 결과를 반복해서 옮겨 적지 않습니다. **선택 → 근거 → 한계**를 중심으로 각 항목을 1~2문장으로 작성합니다.
>
> 이 파일은 프로젝트 전체의 의사결정을 순서대로 쌓는 기록입니다. 1일차(회귀)는 의사결정 ①·②, 2일차(분류)는 ③·④를 아래에 이어서 작성합니다.

---

## 1일차 — 회귀 (공유자전거 대여 수요 예측)

### 의사결정 ① 입력 특성 선택 (CP-02)

**문제**

예측 시점에 사용할 수 없거나 누수가 발생할 수 있는 특성이 있습니다.

- **검토한 선택지:** `casual`·`registered` 포함 여부, `atemp` 포함 여부, `windspeed` 제거 여부, `instant`·`dteday`를 입력으로 쓸지 여부
- **최종 선택(사용·제외한 특성):** 사용 — `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `hum`, `windspeed` (+ CP-03에서 `is_commute_hour` 추가). 제외 — `cnt`(타깃), `casual`/`registered`(누수), `instant`/`dteday`(식별·분할 키), `atemp`(`temp`와 중복)
- **선택 근거(누수 확인, 예측 시점, 상관관계 등):** `casual + registered == cnt`가 전 행에서 성립하고 `registered`–`cnt` 상관이 약 0.97이라 대여 후 집계는 누수다. `temp`–`atemp` 상관 0.992로 하나만 유지했고, `windspeed`는 `cnt`와 약한 상관(0.094)이지만 예측 시점에 알 수 있는 날씨 신호라 남겨 두었다.
- **감수한 한계 또는 추후 확인할 점:** 선형 상관만으로 특성을 고르면 `hr` 등 범주형의 비선형 효과가 과소평가될 수 있다. `windspeed`·캘린더 변수의 실제 기여는 이후 모델 오류·특성 중요도로 재확인한다.

**분석 근거:** `01_regression_data_analysis.md`

### 의사결정 ② 최종 회귀 모델 선택 (CP-07)

**문제**

서로 다른 회귀 모델 및 설정 중 하나를 최종 모델로 선택해야 합니다.

- **비교한 모델·설정:** Dummy(mean), LinearRegression, DecisionTree(max_depth=3/6/12), RandomForest A(n_estimators=50, max_depth=10)·B(100, 15). 오류 분석 후보는 Valid MAE 상위 2개 RF_B·RF_A
- **최종 선택한 모델·설정:** RandomForestRegressor — `n_estimators=100`, `max_depth=15`, `random_state=42`, `n_jobs=-1` (설정 B)
- **선택 근거(Validation MAE, 과대적합 가능성, 시간대별 오류 등):** RF_B의 Validation MAE는 64.517로, RF_A(76.379)와 DecisionTree(max_depth=12, 79.959)보다 낮았다. 검증 데이터에서 예측 오차가 가장 작았기 때문에 RF_B를 최종 모델로 선택했다.
- **선택 모델의 장점:** 여러 트리 평균으로 단일 깊은 트리보다 Valid 오차·분산이 작고, 비선형·교호(시간대×날씨 등)를 선형 모델보다 잘 잡는다.
- **남아 있는 한계 또는 개선 방향:** Train–Valid `cnt` 수준 이동으로 Gap이 남고, 저녁 피크(17~19시) 절대오차가 크다. depth=15에서 n_estimators를 늘려도 Valid 이득은 없었다. 시간 순서 CV·피크 보정은 추후 과제다.

**분석 근거:** `01_regression_model_analysis.md`

---

## 2일차 — 분류 (온라인 쇼핑 구매 여부 예측 · PyTorch MLP)

### 의사결정 ③ 평가 지표 선택 (CP-04)

**문제**

구매 세션이 전체의 약 15%뿐인 불균형 데이터이므로, Accuracy만으로 구매 클래스를 얼마나 잘 예측하는지 판단하기 어렵습니다.

- **검토한 선택지:** Accuracy, 구매 클래스 F1, Precision, Recall
- **최종 선택한 주 지표와 보조 지표:** 주 지표 — 구매 F1 / 보조 — Precision, Recall (Accuracy는 참고만)
- **선택 근거(DummyClassifier와 LogisticRegression 결과, FP·FN 등):** Dummy는 Valid Accuracy가 0.845인데 구매 F1은 0이다. Accuracy만 보면 안 되고, 구매를 얼마나 균형 있게 찾는지는 F1으로 본다.
- **감수한 한계 또는 추후 확인할 점:** Logistic은 Precision 0.734로 구매라고 할 땐 조심하지만, Recall 0.367·FN 181으로 막상 구매로 맞춘 횟수는 적다. 이후 MLP·임계값에서 Recall 개선 여부를 확인한다.

**분석 근거:** `02_classification_data_analysis.md`, `02_classification_model_analysis.md`

### 의사결정 ④ PyTorch MLP 설정 및 분류 임계값 선택 (CP-07)

**문제**

기본 손실 함수로 학습한 MLP-A와 클래스 가중 손실을 적용한 MLP-B를 비교하고, 구매 확률을 0/1로 구분하는 임계값(0.3·0.5·0.7)을 선택해야 합니다.

- **검토한 선택지:** 미구매·구매 건수비로 가중 손실을 둔 MLP-B와 가중 없는 MLP-A를 비교했고, 임계값 0.3·0.5·0.7도 함께 격자 조사하였다.
- **최종 선택한 MLP 설정·임계값·재학습 에포크:** MLP-B(weighted BCE), 임계값 0.5, 재학습 에포크 17(Valid F1 최고 에포크)
- **선택 근거(Validation F1, Precision·Recall, FP·FN 및 가중 손실의 영향):** MLP-B·임계값 0.5의 Valid F1이 가장 높았다. 주 지표를 F1으로 둔 이유는 Accuracy만 보면 미구매를 많이 맞춰도 점수가 높아져 구매 쪽 실패(FN)가 가려지기 때문이다.
- **LogisticRegression과 비교했을 때 선택한 MLP의 특징:** Logistic보다 Precision은 낮게 나왔지만, F1과 Recall은 더 높았다.
- **감수한 한계 또는 추후 개선 방향:** MLP-B·0.5는 구매를 더 잡는 대신 FP가 늘어난 점을 감수한다.

**분석 근거:** `02_classification_model_analysis.md`
