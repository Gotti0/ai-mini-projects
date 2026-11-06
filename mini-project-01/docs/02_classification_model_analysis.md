# 004. 모델 실험 및 오류 분석

**프로젝트:** 온라인 쇼핑 구매 여부 예측 (PyTorch 신경망 분류)  
**작성 범위:** CP-04~CP-08

> Notebook에서 확인한 실제 수치와 관찰을 기록합니다. `___`는 실제 값 또는 1~2문장으로 바꾸세요. Precision·Recall·F1은 구매 클래스(`Revenue=1`) 기준입니다.

## 1. 기준 모델 및 평가 지표 (CP-04)

- **양성 클래스:** 구매 (`Revenue=1`)
- **주 평가 지표:** F1 (구매 클래스)
- **보조 지표:** Precision, Recall, Accuracy
- **모델 비교에 사용한 데이터:** Validation
- **DummyClassifier — Validation Accuracy / F1:** 0.845 / 0.00
- **LogisticRegression — Train F1 / Validation F1:** 0.505 / 0.49
- **LogisticRegression — Validation Precision / Recall:** 0.734 / 0.367
- **LogisticRegression의 Validation 혼동행렬:** TN 1526 / FP 38 / FN 181 / TP 105

**분석:** 불균형 데이터에서 기준 모델의 Accuracy와 F1이 다르게 나타나는 이유를 작성합니다.  
Dummy는 미구매만 맞춰 Accuracy는 높은데, 구매 TP=0이기에 F1은 0이다.

## 2. PyTorch MLP-A 구현 및 학습 (CP-05)

- **신경망 구조:** 입력 → 64 → 32 → 1 (ReLU, Dropout 0.1)
- **손실 함수 / 옵티마이저:** `BCEWithLogitsLoss` / Adam
- **학습 조건:** 최대 25 epoch, batch size 256, learning rate 0.001
- **Validation F1이 가장 높았던 에포크:** 25
- **선택된 MLP-A의 Train F1 / Validation F1:** 0.709 / 0.633
- **MLP-A Validation Precision / Recall:** 0.717 / 0.566

**분석:** Train loss와 Train·Validation F1 그래프에서 확인한 학습 경향을 작성합니다.  
Train loss는 초반(1~5 epoch)에 급격히 떨어진 뒤 완만히 수렴한다. 손실만 보지 않고 Train·Validation F1을 함께 보면, 둘 다 오르며 epoch 25에서 Valid F1이 최고(0.633)이고 Train F1(0.709)과의 차이는 남아 있다.

## 3. 클래스 가중 손실과 MLP 비교 (CP-06)

- **MLP-B 변경 사항:** 양성 클래스 가중치(`pos_weight`)를 적용한 `BCEWithLogitsLoss`
- **Train 데이터의 `pos_weight`(미구매 수 ÷ 구매 수):** 5.46
- **MLP-B의 최적 에포크:** 17
- **MLP-B Train F1 / Validation F1:** 0.692 / 0.645
- **MLP-B Validation Precision / Recall:** 0.575 / 0.734
- **MLP-A와 MLP-B의 Validation F1 차이:** MLP-B가 +0.012 (0.645 − 0.633)
- **LogisticRegression과 두 MLP의 성능 비교에서 발견한 점:** Logistic Valid F1 0.490 대비 MLP-A 0.633·MLP-B 0.645로 F1이 크게 올랐고, 특히 Recall이 크게 개선되었다.
- **Train·Validation F1 차이에서 관찰한 점:** Gap은 MLP-A 0.077, MLP-B 0.047로 B가 더 작다.

**분석:** 양성 클래스 가중치를 적용한 뒤 Precision·Recall·F1이 어떻게 달라졌는지 작성합니다.  
`pos_weight` 적용 후 MLP-B는 A보다 Recall이 올라가고(0.566→0.734) Precision은 내려간다(0.717→0.575). Valid F1은 소폭 상승(+0.012)한다.

> 전체 실험 결과는 Notebook의 `results_df`와 `results/02_model_comparison.csv`를 참고합니다.

## 4. 예측 오류 및 임계값 분석 (CP-07)

- **비교한 두 신경망:** MLP-A / MLP-B
- **기본 임계값 0.5에서 MLP-A의 FP / FN:** 64 / 124
- **기본 임계값 0.5에서 MLP-B의 FP / FN:** 155 / 76
- **임계값 0.3에서 Precision·Recall 및 FP·FN 변화:** 0.5 대비 Precision↓·Recall↑, FP↑·FN↓ (예: MLP-B P 0.575→0.459, R 0.734→0.839, FP 155→283, FN 76→46)
- **임계값 0.7에서 Precision·Recall 및 FP·FN 변화:** 0.5 대비 Precision↑·Recall↓, FP↓·FN↑ (예: MLP-B P 0.575→0.639, R 0.734→0.612, FP 155→99, FN 76→111)
- **Validation F1이 가장 높은 MLP·임계값 조합:** MLP-B · 0.5 (F1 0.645)
- **선택한 MLP의 최적 에포크 수:** 17
- **(선택) PR 곡선 또는 추가 임계값 실험에서 확인한 점:** 임계값을 낮출수록 Recall·FP가, 높일수록 Precision·FN이 커지는 트레이드오프가 뚜렷했다.

**분석:** 모델과 임계값의 선택에서 Precision·Recall 및 FP·FN을 어떻게 고려했는지 작성합니다.  
Valid F1 기준으로 MLP-B·0.5를 선택했다. B는 A보다 FP가 많지만 FN이 적어 구매를 더 잘 잡으며, 0.3은 FP가 과도하고 0.7은 Recall·F1이 떨어진다.

> 임계값별 상세 결과는 `threshold_df`와 `results/02_threshold_comparison.csv`를 참고합니다.

## 5. 최종 신경망과 Test 평가 (CP-08)

- **Test 확인 전에 확정한 MLP 설정 / 임계값:** MLP-B (weighted BCE) / 0.5
- **최종 재학습 데이터(Train + Validation):** 10480행
- **최종 재학습 에포크 수 / 가중 손실 적용 여부:** 17 / 적용 (`pos_weight`)
- **Test Accuracy / Precision / Recall / F1:** 0.859 / 0.527 / 0.843 / 0.649
- **Test 혼동행렬:** TN 1348 / FP 216 / FN 45 / TP 241
- **모델 번들(`02_final_classifier.joblib`)·설정 JSON 저장 및 재로딩 확인:** 저장·재로딩 후 예측 일치 True
- **`predict_purchase()` 실행 결과:** 확률 0.0058 → 예측 0 (threshold 0.5), 실제 Revenue 0

**해석:** 최종 Test 결과와 동일한 모델·임계값의 Validation 결과를 비교해 알게 된 점을 작성합니다.  
Test F1(0.649)은 Valid(0.645)와 거의 같고, Test는 Recall이 더 높고(0.843 vs 0.734) Precision은 더 낮다(0.527 vs 0.575). 선택 편향 없이 한 번만 본 결과이며, F1 기준으로는 일반화가 무너지지 않았다.

> Test 결과는 모델 선택에 사용하지 않습니다. 최종 Test 수치는 Notebook과 이 문서에만 기록합니다.

## 6. 실험 요약

- **가장 중요한 실험 결과:** 불균형에서 Accuracy보다 F1을 쓰고, `pos_weight` MLP-B·임계값 0.5·epoch 17이 Valid F1 최고였으며 Test F1도 유사했다.
- **남아 있는 모델의 한계:** 구매를 잘 잡는 대신 FP가 많아 Precision이 낮다. 임계값을 낮추거나 `pos_weight`를 키우면 Recall(놓친 구매 FN↓)은 오르지만 Precision(잘못 구매로 찍은 FP↑)은 떨어지고, 반대로 높이면 Precision은 오르고 Recall은 떨어진다. 둘을 동시에 크게 올리기는 어렵다.

> **최종 MLP 설정·임계값의 선택과 근거**는 `adr.md`의 의사결정 ④에 작성합니다.
