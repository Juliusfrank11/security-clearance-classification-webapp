import os
import csv
import pandas as pd
import pickle as pkl

from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

from utils import change_txt_filename_to_url
import subprocess
import py7zr

cases_with_formal_findings = pd.read_csv(r"data\formal_finding_results_guideline_A.csv", index_col=0).index

model = SentenceTransformer("all-MiniLM-L6-v2")

input_directory = "data/findings_of_fact"
output_file = "data/case_embeddings.csv"

with open(output_file, "w", encoding="utf-8") as csv_file:
    csv_file.write("")

with open(output_file, "a", encoding="utf-8", newline="") as csv_file:
    writer = csv.writer(csv_file)

    for file_name in os.listdir(input_directory):


        file_path = os.path.join(input_directory, file_name)
        if os.path.isfile(file_path):
            if change_txt_filename_to_url(file_name) in cases_with_formal_findings:
                with open(file_path, "r", encoding="utf-8") as file:

                    text = file.read()
                    embedding = model.encode(text,normalize_embeddings=True).tolist()
                    if os.stat(output_file).st_size == 0:
                        writer.writerow(
                            ["url"] + [f"embedding_{i}" for i in range(len(embedding))]
                        )
                    writer.writerow([change_txt_filename_to_url(file_name)] + embedding)
                    print(f"Added embedding for: {file_name}")

if os.path.getsize(output_file) > 100 * 1024 * 1024:  # 100 MB
    zip_file = output_file.replace(".csv", ".7z")
    try:
        with py7zr.SevenZipFile(zip_file, 'w') as archive:
            archive.write(output_file, arcname=os.path.basename(output_file))
        print(f"Compressed {output_file} to {zip_file}")
    except Exception as e:
        print(f"Error compressing file: {e}")