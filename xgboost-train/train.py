import pandas as pd
import requests
import time
import mlfoundry as mlf
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Initialize Experiment Tracking and Start a Run
client = mlf.get_client()
run = client.create_run(project_name='synopsys-xgb-classifier', run_name="xgb-classifier")
run.set_tags({'framework': 'xgboost', 'task': 'classification'})

# Read the Dataset
df = pd.read_csv('conf_df.csv')

# Create a Model
model = XGBClassifier()

# Log the hyperparameters
run.log_params(model.get_params())

# Create dataset splits
X = df.drop('classification', axis=1)
Y = df['classification']
X_train, X_test, Y_train, Y_test=train_test_split(X, Y, test_size=0.15)

time.sleep(10)

# Train the model
model.fit(X_train, Y_train)

# Generate Predictions
Y_pred_train = model.predict(X_train)
Y_pred_test = model.predict(X_test)

# Log the training split
run.log_dataset(
   dataset_name="train",
   features=X_train,
   predictions=Y_pred_train,
   actuals=Y_train
)

# Log the Test split
run.log_dataset(
   dataset_name="test",
   features=X_test,
   predictions=Y_pred_test,
   actuals=Y_test
)

time.sleep(10)

# Calculate confusion matrices and log them as plots
conf_matrix_train = confusion_matrix(Y_train, Y_pred_train)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_train, display_labels=["0","1"]).plot()
run.log_plots({"confusion_matrix_train": plt}, step=1)

conf_matrix_test = confusion_matrix(Y_test, Y_pred_test)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test, display_labels=["0","1"]).plot()
run.log_plots({"confusion_matrix_test": plt}, step=1)

# Log the Model
class_report_train = classification_report(Y_train, Y_pred_train, output_dict=True)
class_report_test = classification_report(Y_test, Y_pred_test, output_dict=True)

time.sleep(10)

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

# Log important metrics for the model
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
