from learntools.ml_explainability.ex4 import *
print("Setup Complete")
import pandas as pd
data = pd.read_csv('../input/hospital-readmissions/train.csv')
data.columns
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv('../input/hospital-readmissions/train.csv')

y = data.readmitted

base_features = [c for c in data.columns if c != "readmitted"]

X = data[base_features]

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
my_model = RandomForestClassifier(n_estimators=30, random_state=1).fit(train_X, train_y)
import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(my_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = val_X.columns.tolist())
from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots
feature_name = 'number_inpatient'
my_pdp = pdp.pdp_isolate(model=my_model, dataset=val_X, model_features=val_X.columns, feature=feature_name)
pdp.pdp_plot(my_pdp, feature_name)
plt.show()
from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots
feature_name = 'time_in_hospital'
my_pdp = pdp.pdp_isolate(model=my_model, dataset=val_X, model_features=val_X.columns, feature=feature_name)
pdp.pdp_plot(my_pdp, feature_name)
plt.show()
all_train = pd.concat([train_X, train_y], axis=1)
all_train.groupby(['time_in_hospital']).mean().readmitted.plot()
plt.show()
import shap  
sample_data_for_prediction = val_X.iloc[0].astype(float)  # to test function
def patient_risk_factors(model, patient_data):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(patient_data)
    shap.initjs()
    return shap.force_plot(explainer.expected_value[1], shap_values[1], patient_data)
