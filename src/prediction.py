"""Everything regarding making predictions will live here

# Best performing model
model_xgb_reg_0f65fb5c-b0b2-4b67-9082-15609d83cd7d.json is the one with the
best test AUC and the one chosen for the publication.

The current script only works with the best model. But functionality to load
different models will be added in the future.

# Models will be housed in /src/models/

# Prediction accuracy !
The ability to predict laterality from bundles is **not yet validated**. Do
not use these predictions in a way that will influence clinical decusion
making. This work is a proof of concept for future work.
Use with care and caution.

"""
# Silencing Pandas futurewarning for df.udpdate()
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from re import T
import pandas as pd
from metrics import dict_append_suffix
from pprint import pprint
import json
import xgboost

# Load model (only the best one for now)
model = xgboost.XGBRegressor()
model.load_model(
    "src/models/model_xgb_reg_0f65fb5c-b0b2-4b67-9082-15609d83cd7d.json")

# Get feature inputs and generate a dataframe that will be used for predictions
model_features = model.feature_names_in_


def predict_laterality_from_task_data(task_data:dict, pair_index:int, extra_data_present:bool):

    df_prediction = pd.DataFrame(0, index=[0], columns=model_features)
    # if there's extra info, overwrite the values in the subject_data dictionary
    subject_data = task_data["subject_data"]
    if extra_data_present:
        extra_data = task_data["extra_bundle_info"][pair_index][pair_index]

        # if there's keys in the extra key dict that don't match the subject_data keys
        # give feedback that these will not be used.
        subject_keys = set(subject_data.keys())
        extra_keys = set(extra_data.keys())

        same_keys = (subject_keys & extra_keys)
        if len(same_keys) > 0:
            print(
                f"extra info found, these subject values will be \
    overwritten: {same_keys}")

        diff_keys = extra_keys.difference(subject_keys)
        if len(diff_keys) > 0:
            print(f"Keys found in extra info supplied that don't match the subject\
    data these won't be included in the prediction and will \
    not affect it: {diff_keys}")

        # merge subject data and extra data
        subject_data = subject_data | extra_data

    # format the subject data to match feature inputs
    model_subject = {}
    model_subject["tract"] = subject_data["subject_tract"]
    model_subject["subject_age"] = subject_data["subject_age"]
    model_subject["hand"] = subject_data["subject_handedness"]
    model_subject["sex"] = subject_data["subject_sex"]
    model_subject["method"] = subject_data["subject_method"]
    model_subject["ACT"] = subject_data["subject_act"]
    model_subject["clean"] = subject_data["subject_clean"]

    df_model_subject = pd.DataFrame([model_subject])  # brackets around dict!
    df_one_hot_model_subject = pd.get_dummies(df_model_subject)

    # Format the keys of metrics dict to match feature inputs
    tract_left_data = task_data["metrics_left"][pair_index][pair_index]
    tract_right_data = task_data["metrics_right"][pair_index][pair_index]

    model_tract_left = dict_append_suffix(tract_left_data, "_L")
    model_tract_right = dict_append_suffix(tract_right_data, "_R")
    df_model_tract_left = pd.DataFrame([model_tract_left])
    df_model_tract_right = pd.DataFrame([model_tract_right])

    # Get dataframe ready for prediction
    df_model = pd.concat(
        [df_one_hot_model_subject,
         df_model_tract_left,
         df_model_tract_right],
        axis=1)

    # TODO: this gives a future warning, maybe it can be done more efficiently
    df_prediction.update(df_model)  # update the prediction df in place

    # Make prediction, add it to TASK_DATA
    pred_li = float(model.predict(df_prediction))

    if pred_li < 0:
        pred_laterality = "R"
    if pred_li > 0:
        pred_laterality = "L"

    print(f"Bundle index: {pair_index} Predicted LI: {pred_li:0.3f},\
 laterality: {pred_laterality}")

    return {pair_index: {"pred_laterality_index": pred_li,
            "pred_laterality": pred_laterality}}


if __name__ == "__main__":
    # Get the subject specific data for the current task
    # with open("bundle_metrics.json", "r", encoding="utf-8") as f:
    #     task_data = json.load(f)
    # pred = predict_laterality_from_task_data(task_data, pair_index=0)
    # pprint(pred)

    # TODO: the above doesn't work anymore due to how json indices are loaded.
    # one the keys of the indices have to be changed to ints, but now it works
    # with the main app script.
    pass