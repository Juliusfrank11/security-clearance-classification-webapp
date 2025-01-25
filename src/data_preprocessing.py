import os
import re

if not os.path.exists('src/data/findings_of_fact'):
    os.makedirs('src/data/findings_of_fact')
if not os.path.exists('src/data/formal_findings'):
    os.makedirs('src/data/formal_findings')

def get_FoF_and_formal_findings_text(text):
    lines = [l.strip() for l in text if l.strip()]
    finding_of_fact = ""
    formal_findings = ""
    scanning_FoF = False
    scanning_formal_findings = False
    for line in lines:
        if line not in "123456798": #skip page numbers
          alphabetic_only_line = re.sub(r"[^A-Za-z]+", "", line).strip()
          if alphabetic_only_line == "findingsoffact":
              scanning_FoF = True
              continue
          if alphabetic_only_line == "analysis" or alphabetic_only_line == "policies":
              scanning_FoF = False
          if alphabetic_only_line in ("formalfindings","formalfinding"):
              scanning_formal_findings = True
              continue
          if scanning_FoF:
              finding_of_fact += line
              finding_of_fact += "\n"
          if scanning_formal_findings:
              formal_findings += line
              formal_findings += "\n"
    #assert finding_of_fact, "No Findings of Fact found"
    #assert formal_findings, "No Formal Findings found"
    return finding_of_fact, formal_findings




formal_findings_dict = {}

for file in os.listdir(r'src\data\text'):
    with open(os.path.join(r'src\data\text', file), 'r',encoding='utf-8') as f:
        text = [line.strip().lower() for line in f.readlines() if line.strip()]
    findings_of_fact, formal_findings = get_FoF_and_formal_findings_text(text)
    if findings_of_fact and formal_findings:
        with open(os.path.join(r'src\data\findings_of_fact', file), 'w',encoding='utf-8') as f:
            f.write(findings_of_fact)
        with open(os.path.join(r'src\data\formal_findings', file), 'w',encoding='utf-8') as f:
            f.write(formal_findings)