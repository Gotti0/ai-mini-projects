# 004. 검색 성능 실험 및 오류 분석

**프로젝트:** BERT 기반 한국어 의미 검색 시스템 개발 및 성능 비교 (NLP)  
**작성 범위:** CP-02~CP-10

> Notebook에서 확인한 실제 수치와 관찰을 기록합니다. 각 `___`를 실제 값 또는 1~2문장으로 바꾸세요. 상세한 선택 이유와 트레이드오프는 `ADR.md`에 작성합니다.

## 1. 검색기 구현 및 임베딩 확인 (CP-02~CP-06, CP-08)

| 검색 방식 | 사용 모델·표현 방식 | 전체 문서 벡터 Shape |
|---|---|---|
| TF-IDF | 문자 2~3-gram, `max_features=30000` | ___ |
| BERT | `klue/bert-base` + Masked Mean Pooling | ___ |
| Sentence-BERT | `snunlp/KR-SBERT-V40K-klueNLI-augSTS` | ___ |

- **BERT Encoder 출력 / Attention Mask / Pooling 결과 Shape (CP-03~04의 질문 2개):** ___ / ___ / ___
- **BERT와 Sentence-BERT의 최대 입력 길이:** 256토큰
- **Padding을 평균 계산에서 제외하는 이유:** ___
- **BERT와 Sentence-BERT 문서 벡터를 혼합하지 않는 이유:** ___
- **Pooling·코사인 유사도·검색 결과 검증 셀 실행 결과:** ___

## 2. 검색 평가 기준 (CP-07)

- **평가에 사용하는 검색 결과:** Top-5 문서
- **질문별 지정된 정답 문서 수:** 1개
- **Hit@1이 평가하는 내용:** ___
- **Recall@3이 평가하는 내용:** ___
- **MRR@5가 평가하는 내용:** ___
- **검색 지표 단위 테스트 결과:** ___

## 3. 세 검색 방식의 성능 비교 (CP-07~CP-08)

`comparison_df`의 Validation 결과를 기록합니다.

| 검색 방식 | Hit@1 | Recall@3 | MRR@5 |
|---|---:|---:|---:|
| TF-IDF | ___ | ___ | ___ |
| BERT | ___ | ___ | ___ |
| Sentence-BERT | ___ | ___ | ___ |

**분석:** 지표별 성능 차이와 예상과 달랐던 결과가 있다면 그 가능 원인을 작성합니다.  
___

> 참고 결과: `outputs/tables/cp08_validation_comparison.csv`, `outputs/figures/cp08_validation_comparison.png`

## 4. 검색 오류 분석 및 가설 검증 (CP-09)

`error_cases`의 대표 분석 질문 5개를 기록합니다. 질문과 지정된 정답 문단, 실제 검색 문단의 본문을 비교하여 검색 결과의 차이와 원인 후보를 작성합니다. 정답이 Top-5에 없으면 순위를 '없음'으로 표시하세요. 실패 질문이 5개보다 적다면 실제 실패 건수와 나머지 성공 사례를 구분합니다.

| 질문 ID | 정답 문서 ID | TF-IDF 정답 순위 | BERT 정답 순위 | SBERT 정답 순위 | 겹침 비율 | 관찰한 결과 및 원인 후보 |
|---|---|---:|---:|---:|---:|---|
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |

- **대표 실패 질문의 겹침 비율과 전체 Validation 평균의 차이:** ___
- **겹침 비율이 낮은 대표 질문에서 상대적으로 잘 검색한 방식(관찰 가능한 범위):** ___

**가설 검증:** `02_nlp_data_analysis.md`의 4절에서 세운 두 가설이 실제 결과와 일치했는지, 검색 순위와 문서 내용에 근거하여 작성합니다.  
___

> 참고 결과: `outputs/tables/cp09_error_cases.csv`, `outputs/tables/cp01_validation_overlap.csv`
>
> (선택) 전체 Validation 질문을 겹침 비율에 따라 두 그룹으로 나누어 추가 비교했다면 발견한 점을 작성하세요: ___

## 5. 최종 검색기 및 Test 평가 (CP-10)

- **Test 평가 전에 확정한 검색 방식(`SELECTED_METHOD`):** ___
- **직접 입력한 새로운 질문:** ___
- **`search_docs()`의 Top-3 문서 ID와 검색 결과에서 관찰한 점:** ___

동일한 검색 방식에서 `final_compare`의 결과를 기록합니다.

| 데이터 | 질문 수 | Hit@1 | Recall@3 | MRR@5 |
|---|---:|---:|---:|---:|
| Validation | 60 | ___ | ___ | ___ |
| 보류 Test | 20 | ___ | ___ | ___ |

**해석:** Validation과 Test의 지표 차이를 실제 수치로 비교하고, Test에서 실패한 질문의 특징과 예상 원인을 작성합니다.  
___

**평가의 한계:** 동일한 Corpus에서 새로운 질문을 평가했다는 점, 데이터 규모와 질문별 단일 정답 문서의 한계를 고려하여 실제 업무 검색에서 추가로 확인할 점을 작성합니다.  
___

> 참고 결과: `outputs/tables/cp10_validation_test_comparison.csv`, `outputs/tables/cp10_test_query_results.csv`, `outputs/reports/cp10_final_report.json`
>
> Test 결과를 확인한 뒤 검색 방식을 다시 선택하지 않습니다. 활용 목적·우선 지표·최종 검색 방식의 선택 근거는 `ADR.md`의 NLP 의사결정에 작성합니다.
