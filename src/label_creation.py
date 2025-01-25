import os
import re
import json
import numpy as np
from typing import List
from utils import change_txt_filename_to_url


def create_formal_findings_dict(text: List[str]) -> dict:
    def get_guideline_letter(line: str) -> str:
        return re.findall(r"Guideline\W+[A-M]",line,flags=re.IGNORECASE)[0].split()[-1].upper()[-1]
    def get_guideline_result(line: str) -> str:
        if "for" in line.lower().split():
            return 1 #True #"Accepted"
        elif "against" in line.lower().split():
            return 0 #False#"Denied"
        else:
            return np.nan#"Withdrawn" or not listed

    formal_findings_dict = {}
    for i, line in enumerate(text):
        if "guideline" in line.lower():
            try:
                guideline = get_guideline_letter(line)
                guideline_result = get_guideline_result(text[i+1])
                j = 2
                while np.isnan(guideline_result):
                    try:
                        guideline_result = get_guideline_result(text[i+j])
                        j += 1
                        if j > 10:
                            break
                    except IndexError:
                        break
                formal_findings_dict[guideline] = guideline_result
            except IndexError:
                pass
    return formal_findings_dict

for letter in "ABCDEFGHIJKLM":
    with open(f'data/formal_finding_results_guideline_{letter}.csv', 'w',encoding='utf-8') as f:
        f.write(f"text,{letter}\n")

formal_findings_dict = {}
for file in os.listdir(r'data\formal_findings'):
    with open(os.path.join(r'data\formal_findings', file), 'r',encoding='utf-8') as f:
        formal_findings = f.read()
    formal_findings_dict = create_formal_findings_dict(formal_findings.splitlines())
    if formal_findings_dict:
        for letter in "ABCDEFGHIJKLM":
            with open(f'data/formal_finding_results_guideline_{letter}.csv', 'a',encoding='utf-8') as f:
                f.write(f"{change_txt_filename_to_url(file)},{formal_findings_dict.get(letter,np.nan)}\n")
        print(f"Added formal findings for: {file}")
