# 002. 모델 실험 및 오류 분석

**프로젝트:** 공유자전거 대여 수요 예측 (회귀)  
**작성 범위:** CP-04~CP-08

> Notebook에서 확인한 실제 성능과 관찰을 작성합니다. 각 항목의 `___`를 실제 값이나 1~2문장으로 바꾸세요.

## 1. 모델 평가 기준 (CP-04)

- **주 평가 지표:** MAE
- **보조 지표:** RMSE, R²
- **모델 비교에 사용한 데이터:** Validation
- **MAE를 주요 지표로 선택한 이유:** `cnt`(대여 건수)와 단위가 같아 “평균 몇 대 틀렸는지”를 바로 해석할 수 있다. 우측 치우침·피크가 있어 RMSE는 큰 오차 몇 개에 휘둘리기 쉽고, Train·Valid처럼 `cnt` 수준이 다른 구간을 비교할 때 R²는 직관이 떨어져 보조 지표로만 둔다.

## 2. 모델별 실험 결과 (CP-04~CP-06)

대표 설정별 Train MAE / Validation MAE를 기록합니다. 전체 실험 결과는 Notebook의 `results_df`에서 확인합니다.

- **DummyRegressor (mean):** Train 119.572 / Validation 194.109
- **LinearRegression:** Train 55.382 / Validation 99.725
- **DecisionTreeRegressor (`max_depth=12`):** Train 32.966 / Validation 79.959
- **RandomForestRegressor (설정 B: n_estimators=100, max_depth=15):** Train 22.255 / Validation 64.517

**실험에서 발견한 점**

- **Decision Tree 깊이 변화에 따른 성능:** 깊이 3→6→12로 Valid MAE가 134.9→106.3→80.0으로 개선되나, Train MAE는 더 빠르게 떨어져 Gap이 53.7→44.8→47.0으로 깊을수록 과대적합 위험이 커진다.
- **Random Forest 두 설정의 차이:** B(100·15)가 A(50·10)보다 Valid MAE가 76.4→64.5로 낮아 최고 성능이다. A는 Gap이 더 작아(38.2 vs 42.3) 상대적으로 덜 과적합하지만 절대 Valid 오차는 B가 유리하다.
- **Train·Validation 성능 차이에서 관찰한 현상:** 모든 모델에서 Valid MAE가 Train보다 크다. Valid 구간 `cnt` 평균(약 281)이 Train(약 160)보다 높아 수준·분포 이동이 있고, 여기에 모델 복잡도까지 겹치면 Gap이 더 벌어질 수 있다.

## 3. 예측 오류 분석 (CP-07)

- **비교한 후보 모델 2개(Validation MAE 상위 2개):** RF_B (Valid MAE 64.517) / RF_A (Valid MAE 76.379)
- **실제값·예측값 그래프에서 관찰한 점:** 두 모델 모두 저·중 대여량에서는 y=x 근처에 모이나, 고대여량(피크)에서 흩어짐이 커진다. RF_B가 RF_A보다 대각선에 더 가깝다.
- **시간대별 MAE가 큰 구간:** 저녁 피크·이후(17·18·19시, MAE 약 120·113·97). 오전 출근(8시)보다 저녁 쪽 절대오차가 훨씬 크다.
- **모델이 상대적으로 잘 예측하지 못하는 상황:** 수요 급증 시간대와 Valid 구간처럼 Train보다 `cnt` 수준이 높은 기간. 심야 저수요 구간은 절대 MAE는 작다.
- **(선택) 특성 중요도에서 확인한 점:** _(미실행)_

**분석:** 이 오류가 최종 모델 선택에 어떤 영향을 주었는지 작성합니다.  
피크 시간 오차는 공통이나 RF_B의 Valid MAE·산점도 밀착도가 더 나아 Gap이 약간 커도 B를 최종으로 선택했다. A는 과적합 완충용 대안이다.

## 4. 최종 모델과 Test 평가 (CP-08)

- **Test 확인 전에 선택한 최종 모델·설정:** RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
- **재학습에 사용한 데이터(Train + Validation) 크기:** 14755행
- **Test MAE:** 66.752
- **Test RMSE:** 96.100
- **Test R²:** 0.800
- **모델 저장·재로딩 및 예측 결과:** `01_final_model.joblib` 저장·재로딩 후 예측 일치(`True`). sample 입력(10월·18시·평일·기온 약 20℃) 예상 대여량 748.

**해석:** 최종 Test 결과로 알게 된 점을 1~2문장으로 작성합니다.  
Valid로 고른 RF(B)가 Test에서도 MAE 66.8·R² 0.80으로 쓸 만한 일반화를 보였고, Valid(64.5)와 크게 어긋나지 않았다. Test는 선택에 쓰지 않았으므로 Valid와 숫자를 개선율처럼 직접 비교하지는 않는다.

> Test는 최종 평가용입니다. 서로 다른 데이터 집합에서 나온 점수를 직접 개선율로 비교하지 않습니다.

## 5. 실험 요약

- **가장 중요한 실험 결과:** Validation MAE로 비교·선택한 RandomForest(B)가 Dummy·Linear·단일 트리보다 낮았고, Train+Valid 재학습 후 Test에서도 MAE 66.752·R² 0.800을 유지했다.
- **남아 있는 모델의 한계:** 저녁 피크(17~19시) 절대오차가 크고, Train보다 Valid/Test의 `cnt` 수준이 높아 Gap이 남는다. 피크 구간 보정이나 시간 순서 교차검증은 후속 과제다.

> 최종 모델을 **왜 선택했는지**는 `adr.md`의 의사결정 ②에 작성합니다.
