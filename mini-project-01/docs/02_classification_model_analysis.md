# 004. 모델 실험 및 오류 분석

**프로젝트:** 온라인 쇼핑 구매 여부 예측 (PyTorch 신경망 분류)  
**작성 범위:** CP-04~CP-08

> Notebook에서 확인한 실제 수치와 관찰을 기록합니다. `___`는 실제 값 또는 1~2문장으로 바꾸세요. Precision·Recall·F1은 구매 클래스(`Revenue=1`) 기준입니다.

## 1. 기준 모델 및 평가 지표 (CP-04)

- **양성 클래스:** 구매 (`Revenue=1`)
- **주 평가 지표:** F1 (구매 클래스)
- **보조 지표:** Precision, Recall, Accuracy
- **모델 비교에 사용한 데이터:** ___
- **DummyClassifier — Validation Accuracy / F1:** ___ / ___
- **LogisticRegression — Train F1 / Validation F1:** ___ / ___
- **LogisticRegression — Validation Precision / Recall:** ___ / ___
- **LogisticRegression의 Validation 혼동행렬:** TN ___ / FP ___ / FN ___ / TP ___

**분석:** 불균형 데이터에서 기준 모델의 Accuracy와 F1이 다르게 나타나는 이유를 작성합니다.  
___

## 2. PyTorch MLP-A 구현 및 학습 (CP-05)

- **신경망 구조:** 입력 → 64 → 32 → 1 (ReLU, Dropout 0.1)
- **손실 함수 / 옵티마이저:** `BCEWithLogitsLoss` / Adam
- **학습 조건:** 최대 25 epoch, batch size 256, learning rate 0.001
- **Validation F1이 가장 높았던 에포크:** ___
- **선택된 MLP-A의 Train F1 / Validation F1:** ___ / ___
- **MLP-A Validation Precision / Recall:** ___ / ___

**분석:** Train loss와 Train·Validation F1 그래프에서 확인한 학습 경향을 작성합니다.  
___

## 3. 클래스 가중 손실과 MLP 비교 (CP-06)

- **MLP-B 변경 사항:** 양성 클래스 가중치(`pos_weight`)를 적용한 `BCEWithLogitsLoss`
- **Train 데이터의 `pos_weight`(미구매 수 ÷ 구매 수):** ___
- **MLP-B의 최적 에포크:** ___
- **MLP-B Train F1 / Validation F1:** ___ / ___
- **MLP-B Validation Precision / Recall:** ___ / ___
- **MLP-A와 MLP-B의 Validation F1 차이:** ___
- **LogisticRegression과 두 MLP의 성능 비교에서 발견한 점:** ___
- **Train·Validation F1 차이에서 관찰한 점:** ___

**분석:** 양성 클래스 가중치를 적용한 뒤 Precision·Recall·F1이 어떻게 달라졌는지 작성합니다.  
___

> 전체 실험 결과는 Notebook의 `results_df`와 `results/02_model_comparison.csv`를 참고합니다.

## 4. 예측 오류 및 임계값 분석 (CP-07)

- **비교한 두 신경망:** MLP-A / MLP-B
- **기본 임계값 0.5에서 MLP-A의 FP / FN:** ___ / ___
- **기본 임계값 0.5에서 MLP-B의 FP / FN:** ___ / ___
- **임계값 0.3에서 Precision·Recall 및 FP·FN 변화:** ___
- **임계값 0.7에서 Precision·Recall 및 FP·FN 변화:** ___
- **Validation F1이 가장 높은 MLP·임계값 조합:** ___
- **선택한 MLP의 최적 에포크 수:** ___
- **(선택) PR 곡선 또는 추가 임계값 실험에서 확인한 점:** ___

**분석:** 모델과 임계값의 선택에서 Precision·Recall 및 FP·FN을 어떻게 고려했는지 작성합니다.  
___

> 임계값별 상세 결과는 `threshold_df`와 `results/02_threshold_comparison.csv`를 참고합니다.

## 5. 최종 신경망과 Test 평가 (CP-08)

- **Test 확인 전에 확정한 MLP 설정 / 임계값:** ___ / ___
- **최종 재학습 데이터(Train + Validation):** ___행
- **최종 재학습 에포크 수 / 가중 손실 적용 여부:** ___ / ___
- **Test Accuracy / Precision / Recall / F1:** ___ / ___ / ___ / ___
- **Test 혼동행렬:** TN ___ / FP ___ / FN ___ / TP ___
- **모델 번들(`02_final_classifier.joblib`)·설정 JSON 저장 및 재로딩 확인:** ___
- **`predict_purchase()` 실행 결과:** ___

**해석:** 최종 Test 결과와 동일한 모델·임계값의 Validation 결과를 비교해 알게 된 점을 작성합니다.  
___

> Test 결과는 모델 선택에 사용하지 않습니다. 최종 Test 수치는 Notebook과 이 문서에만 기록합니다.

## 6. 실험 요약

- **가장 중요한 실험 결과:** ___
- **남아 있는 모델의 한계:** ___

> **최종 MLP 설정·임계값의 선택과 근거**는 `adr.md`의 의사결정 ④에 작성합니다.
