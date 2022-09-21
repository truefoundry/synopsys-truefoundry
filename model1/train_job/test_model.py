# test_model.py

import pandas as pd
import mlfoundry as mlf
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


#client = mlf.get_client()
client = mlf.get_client(tracking_uri="https://app.devtest.truefoundry.tech", api_key="djE6dHJ1ZWZvdW5kcnk6dXNlci10cnVlZm91bmRyeTo0MTZjOTA=")
run = client.create_run(project_name='synopsys-xgb-classifier')
run.set_tags({'framework': 'xgboost', 'task': 'classification'})

df = pd.read_csv('conf_df.csv')

model = XGBClassifier()
#model.load_model('XGB.model')

run.log_params(model.get_params())

X = df.drop('classification', axis=1)
Y = df['classification']
X_train, X_test, Y_train, Y_test=train_test_split(X, Y, test_size=0.15)

model.fit(X_train, Y_train)


Y_pred_train = model.predict(X_train)
Y_pred_test = model.predict(X_test)



run.log_dataset(
   dataset_name = "train",
   features=X_train,
   predictions=Y_pred_train,
   actuals=Y_train
)
run.log_dataset(
   dataset_name = "test",
   features=X_test,
   predictions=Y_pred_test,
   actuals=Y_test
)

conf_matrix_train = confusion_matrix(Y_train, Y_pred_train)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_train, display_labels=["0","1"]).plot()
run.log_plots({"confusion_matrix_train": plt}, step=1)

conf_matrix_test = confusion_matrix(Y_test, Y_pred_test)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test, display_labels=["0","1"]).plot()
run.log_plots({"confusion_matrix_test": plt}, step=1)


class_report_train = classification_report(Y_train, Y_pred_train, output_dict=True)
class_report_test = classification_report(Y_test, Y_pred_test, output_dict=True)

run.log_model(
   name="synopsys-xgboost-model",
   model=model,
   framework="xgboost",
   description="logging the model",
   metadata = {
      "classification_report_train": class_report_train,
      "classification_report_test": class_report_test
   }
)

metrics = {
    'train/accuracy': accuracy_score(Y_train, Y_pred_train),
    'train/precision': precision_score(Y_train, Y_pred_train),
    'train/recall': recall_score(Y_train, Y_pred_train),
    'train/f1': f1_score(Y_train, Y_pred_train),
    'test/accuracy': accuracy_score(Y_test, Y_pred_test),
    'test/precision': precision_score(Y_test, Y_pred_test),
    'test/recall': recall_score(Y_test, Y_pred_test),
    'test/f1': f1_score(Y_test, Y_pred_test),
}
print(metrics)
run.log_metrics(metrics)

print(conf_matrix_test)
print(class_report_test)

''' Results should match this:
[[ 478  755]
 [  35 9496]]
              precision    recall  f1-score   support

           0       0.93      0.39      0.55      1233
           1       0.93      1.00      0.96      9531

    accuracy                           0.93     10764
   macro avg       0.93      0.69      0.75     10764
weighted avg       0.93      0.93      0.91     10764
'''