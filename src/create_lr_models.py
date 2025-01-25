from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle as pkl
import os
import py7zr

if not os.path.exists("data/case_embeddings.csv"):
    with py7zr.SevenZipFile("data/case_embeddings.7z", mode="r") as z:
        z.extractall("data")

lr_models = {
    letter: LogisticRegression(solver="liblinear", class_weight="balanced", penalty="l1")
    for letter in "ABCDEFGHIJKLM"
}
lr_data = {
    letter: pd.read_csv(f"data/formal_finding_results_guideline_{letter}.csv", index_col=0).dropna()
    for letter in "ABCDEFGHIJKLM"
}
for letter, model in lr_models.items():
    model.fit(
        pd.read_csv("data/case_embeddings.csv", index_col=0).loc[lr_data[letter].index],
        lr_data[letter][letter],
    )
    with open(f"models/lr_model_{letter}.pkl", "wb") as f:
      pkl.dump(model, f)