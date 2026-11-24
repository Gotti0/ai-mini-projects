# 002. 탐지 성능 실험 및 오류 분석

**프로젝트:** YOLO 객체 탐지 성능 평가 및 최적화 (CV)  
**작성 범위:** CP-02~CP-10

> Notebook에서 확인한 실제 수치와 관찰을 기록합니다. 각 `___`를 실제 값 또는 1~2문장으로 바꾸세요. 상세한 선택 이유와 트레이드오프는 `ADR.md`에 작성합니다.

## 1. 모델 및 평가기 구현 (CP-02~CP-06)

- **사용 모델:** YOLO26 Nano (`yolo26n.pt`), 사전학습 가중치 사용
- **기본 입력 이미지 크기(`imgsz`):** 640
- **평가용 IoU Threshold:** 0.5
- **기준 Confidence Threshold:** 0.30
- **평가 지표:** TP, FP, FN, Precision, Recall, F1
- **예측–정답 매칭에서 TP로 판정하는 조건:** ___
- **여러 이미지의 TP·FP·FN 집계 방법:** ___
- **IoU·매칭·집계·성능 지표 검증 셀 실행 결과:** ___

## 2. Confidence Threshold별 성능 비교 (CP-07)

`threshold_df`의 Validation 전체 성능을 기록합니다. Confidence 0.30은 CP-06의 기준 설정입니다.

| Confidence | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| 0.15 | ___ | ___ | ___ | ___ | ___ | ___ |
| 0.30 | ___ | ___ | ___ | ___ | ___ | ___ |
| 0.60 | ___ | ___ | ___ | ___ | ___ | ___ |

- **Validation F1이 가장 높은 Confidence:** ___

**분석:** Confidence를 높였을 때 FP·FN과 Precision·Recall이 실제로 어떻게 변했으며, 그 이유는 무엇인지 작성합니다.  
___

> 참고 결과: `outputs/tables/cp07_threshold_comparison.csv`, `outputs/figures/cp07_threshold_metrics.png`

## 3. 클래스별 성능 및 탐지 오류 분석 (CP-08)

기준 Confidence 0.30에서 `class_error_df`의 결과를 기록합니다. 정답 객체 수는 TP+FN입니다.

| 클래스 | 정답 객체 수 | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Person | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| Bicycle | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| Car | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| Bus | ___ | ___ | ___ | ___ | ___ | ___ | ___ |

- **FN이 가장 많은 클래스 / Recall이 가장 낮은 클래스(정답이 있는 클래스 기준):** ___ / ___

### 대표 오류 이미지 3건

`error_images`에서 선정한 이미지의 정답과 예측을 비교합니다. 원인은 객체 크기·가림·복잡한 배경 등 실제 이미지에서 관찰한 근거를 바탕으로 추정합니다.

| 이미지 ID | FP / FN | 관찰한 탐지 오류 및 원인 후보 |
|---|---|---|
| ___ | ___ / ___ | ___ |
| ___ | ___ / ___ | ___ |
| ___ | ___ / ___ | ___ |

**가설 검증:** `01_cv_data_analysis.md`의 3절에서 세운 가설이 실제 결과와 일치했는지, 클래스별 정답 수·Small 비율·Recall·대표 오류를 근거로 작성합니다.  
___

> 참고 결과: `outputs/tables/cp08_class_error_analysis.csv`, `outputs/figures/cp08_error_<image_id>.png`

## 4. 최종 장면 분석기 확인 (CP-09)

- **`analyze_scene()`에 입력한 이미지 ID 또는 파일명:** ___
- **탐지된 클래스별 객체 수:** ___
- **탐지 목록(`detections`), 클래스별 개수(`counts`), 결과 이미지(`rendered_path`) 반환 확인:** ___

> 활용 목적·우선 평가 지표·최종 Confidence의 선택 근거는 `ADR.md`의 CV 의사결정에 작성합니다.

## 5. 최종 Validation·Test 성능 (CP-10)

- **Test 평가 전에 확정한 Confidence(`SELECTED_CONF`):** ___
- **평가 이미지 수:** Validation ___장 / 보류 Test ___장

동일한 Confidence에서 `final_df`의 결과를 기록합니다.

| 데이터 | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Validation | ___ | ___ | ___ | ___ | ___ | ___ |
| 보류 Test | ___ | ___ | ___ | ___ | ___ | ___ |

**해석:** Validation과 Test의 Precision·Recall·F1 차이를 실제 수치로 설명하고, Test의 클래스별 정답 객체 수(`test_class_df`의 TP+FN)와 데이터 규모를 고려해 차이의 원인을 추정합니다.  
___

**평가의 한계:** 이 소규모 데이터로 실제 교통 환경의 탐지 성능을 보장할 수 없는 이유와 추가로 확인할 점을 작성합니다.  
___

> 참고 결과: `outputs/tables/cp10_final_validation_vs_test.csv`, `outputs/tables/cp10_test_per_class.csv`, `outputs/reports/cp10_final_summary.json`
>
> Test 결과를 확인한 뒤 Confidence를 다시 선택하지 않습니다.
