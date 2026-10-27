"""Git 특강 실습: Iris 데이터를 KNN으로 분류하고 평가 결과를 CSV로 저장합니다.

파일 위치: ai-mini-projects/mini-project-01/code/git_version_demo.py
결과 위치: ai-mini-projects/mini-project-01/results/demo_metrics.csv
"""

import csv
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# Git Diff 실습: 3을 5로 바꾼 뒤 다시 실행하고 Commit해 보세요.
n_neighbors = 3


def main():
    # scikit-learn에 포함된 Iris 데이터셋 사용 (별도 다운로드 불필요)
    X, y = load_iris(return_X_y=True)

    # 실행할 때마다 같은 데이터로 평가할 수 있도록 분할 조건 고정
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # KNN 모델 학습 및 정확도 계산
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # 이 파일이 있는 code/ 폴더의 형제 폴더 results/에 저장
    results_dir = Path(__file__).resolve().parent.parent / "resultx"
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_path = results_dir / "demo_metrics.csv"

    # 매 실행마다 같은 CSV 파일을 덮어써서 Git Diff를 쉽게 비교
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["model", "n_neighbors", "accuracy"])
        writer.writerow(["KNN", n_neighbors, f"{accuracy:.4f}"])

    print(f"모델: KNN | n_neighbors: {n_neighbors} | Accuracy: {accuracy:.4f}")
    print(f"결과 저장: {csv_path}")


if __name__ == "__main__":
    main()
