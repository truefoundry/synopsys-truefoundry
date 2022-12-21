import typer
from typing import Optional

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def train(
    test_size: float = 0.2, 
    C: float = 1.0, 
    n_jobs: Optional[int] = None, 
    max_iter: int = 100,
    random_state: int = 42,
):
    X, y = load_iris(as_frame=True, return_X_y=True)
    X = X.rename(columns={
            "sepal length (cm)": "sepal_length",
            "sepal width (cm)": "sepal_width",
            "petal length (cm)": "petal_length",
            "petal width (cm)": "petal_width",
    })

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    clf = LogisticRegression(solver="liblinear")
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    # You can push these metrics to external DB, or experiment tracking system like mlfoundry
    print(classification_report(y_true=y_test, y_pred=preds))


if __name__ == '__main__':
    typer.run(train)
