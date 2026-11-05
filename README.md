# uv 가상환경 설정

모든 명령어는 기존 `ai-mini-projects` 프로젝트의 최상위 폴더에서 실행합니다.

## 1. pyproject.toml 정리

기존 `uv init --package`로 생성된 `src/` 폴더를 삭제합니다. 단, 직접 작성한 코드가 없는 경우에만 삭제합니다.

`pyproject.toml`을 다음 내용으로 변경합니다.

```toml
[project]
name = "ai-mini-projects"
version = "0.1.0"
description = "멀티캠퍼스 AI 엔지니어 트랙 미니 프로젝트 모음"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []
```

기존 `[build-system]` 등 패키지 배포용 설정은 제거합니다. `README.md` 파일이 존재하는지도 확인합니다.

## 2. Python 버전 확인

기존에 생성된 `.python-version` 파일을 열어 다음과 같이 설정되어 있는지 확인합니다.

```text
3.11
```

이미 `3.11`이라면 별도의 설정 명령어는 필요하지 않습니다. 다른 버전이라면 `3.11`로 수정합니다.

## 3. 가상환경 생성 및 패키지 설치

```bash
uv add pandas numpy matplotlib scikit-learn ipykernel joblib
```

명령어를 실행하면 다음 작업이 자동으로 진행됩니다.

- `.venv/` — 가상환경 생성 및 패키지 설치
- `pyproject.toml` — 패키지 의존성 기록
- `uv.lock` — 패키지 버전 잠금

## 4. VS Code Jupyter 커널 설정

Jupyter Notebook을 열고 오른쪽 위 **Select Kernel → Python Environments**에서 `ai-mini-projects/.venv`에 해당하는 Python 3.11 환경을 선택합니다.

커널 이름은 환경에 따라 `ai-mini-projects`, `.venv` 등으로 표시될 수 있습니다.

## 5. Git 관리

`.gitignore`에 다음 항목이 포함되어 있는지 확인합니다.

```gitignore
.venv/
.ipynb_checkpoints/
```

**GitHub에 업로드할 파일**

- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `.gitignore`
- `README.md`

`.venv/` 폴더는 GitHub에 업로드하지 않습니다.

환경 설정을 마쳤다면 해당 파일들을 Commit하고 Push합니다.

---

# AI Mini Projects (수정 중)

AI 엔지니어 과정에서 진행하는 미니프로젝트의
구현 과정과 실험 결과, 의사결정을 기록하는 저장소입니다.

## Mini Project 01

- 진행 상태: 준비 중
- 목표: AI 모델을 실험하고 결과를 분석하여
  적절한 방법을 선택하는 능력 기르기

  ### 프로젝트 자료

- [실험 코드](mini-project-01/code/)
- [실험 결과](mini-project-01/results/)
- [첫 번째 실험 분석](mini-project-01/docs/001_analysis.md)
- [핵심 의사결정(ADR)](mini-project-01/docs/adr.md)

### 문서 관리 원칙

- 실험별 상세 분석은 번호가 붙은 analysis 문서에 기록합니다.
- 주요 기술적 선택과 근거는 adr.md에 요약합니다.
- 프로젝트 결과가 완성되면 이 README에 핵심 성과를 정리합니다.