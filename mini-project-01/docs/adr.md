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
- **선택 근거(Validation MAE, 과대적합 가능성, 시간대별 오류 등):** Valid MAE 64.517로 전 실험 최저(차순위 RF_A 76.379, Tree-12 79.959). Gap(42.3)은 RF_A(38.2)보다 다소 크지만 Valid 절대 오차 우위가 분명하고, 후보 비교에서도 RF_B가 일관되게 낮다. Valid `cnt` 평균이 Train보다 높아 Gap 자체는 전 모델 공통 현상이다.
- **선택 모델의 장점:** 여러 트리 평균으로 단일 깊은 트리보다 Valid 오차·분산이 작고, 비선형·교호(시간대×날씨 등)를 선형 모델보다 잘 잡는다.
- **남아 있는 한계 또는 개선 방향:** Train–Valid 수준 이동과 출퇴근 피크 구간의 잔차가 남아 있다. 시간 순서 CV·피크 시간 전용 보정·하이퍼파라미터 추가 탐색으로 일반화를 더 점검할 수 있다.

**분석 근거:** `01_regression_model_analysis.md`

---

## 2일차 — 분류 (온라인 쇼핑 구매 여부 예측 · PyTorch MLP)

### 의사결정 ③ 평가 지표 선택 (CP-04)

**문제**

구매 세션이 전체의 약 15%뿐인 불균형 데이터이므로, Accuracy만으로 구매 클래스를 얼마나 잘 예측하는지 판단하기 어렵습니다.

- **검토한 선택지:** ___ (예: Accuracy, 구매 클래스 F1, Precision, Recall)
- **최종 선택한 주 지표와 보조 지표:** ___
- **선택 근거(DummyClassifier와 LogisticRegression 결과, FP·FN 등):** ___
- **감수한 한계 또는 추후 확인할 점:** ___

**분석 근거:** `02_classification_data_analysis.md`, `02_classification_model_analysis.md`

### 의사결정 ④ PyTorch MLP 설정 및 분류 임계값 선택 (CP-07)

**문제**

기본 손실 함수로 학습한 MLP-A와 클래스 가중 손실을 적용한 MLP-B를 비교하고, 구매 확률을 0/1로 구분하는 임계값(0.3·0.5·0.7)을 선택해야 합니다.

- **검토한 선택지:** ___ (MLP-A / MLP-B의 학습 결과, 임계값 0.3·0.5·0.7)
- **최종 선택한 MLP 설정·임계값·재학습 에포크:** ___
- **선택 근거(Validation F1, Precision·Recall, FP·FN 및 가중 손실의 영향):** ___
- **LogisticRegression과 비교했을 때 선택한 MLP의 특징:** ___
- **감수한 한계 또는 추후 개선 방향:** ___

**분석 근거:** `02_classification_model_analysis.md`
