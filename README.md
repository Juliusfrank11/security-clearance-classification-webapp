# security-clearance-classification
Webapp for finding similar US security clearance appeal cases.

## [Run the Demo Here!](https://juliusfrank11-security-clearance-classificati-srcwebapp-oqbotw.streamlit.app/)
## Problem Description
To safeguard its national security, the United States requires all personnel working with classified information to obtain a security clearance at one of three security levels: **CONFIDENTIAL**, **SECRET**, and **TOP SECRET** (**TS**). Additionally, almost all positions within the federal government require a *Public Trust* clearance, effectively making *Public Trust* a de facto "zeroth" clearance level. Security clearances are granted according to guidelines established by the Department of Defense. By law, if an applicant's security clearance is rejected, they must be issued a Statement of Reasons (SOR) detailing why their clearance application was rejected. The applicant can then choose to appeal the decision to the Defense Office of Hearings and Appeals (DOHA). These appeal cases are posted (with personal identifying information removed) on the [DOHA's Website](https://doha.ogc.osd.mil/Industrial-Security-Program/Industrial-Security-Clearance-Decisions/ISCR-Hearing-Decisions/).

This appeal process can be extremely costly, with one source citing a starting figure of [\$2,500](https://news.clearancejobs.com/2021/02/12/when-to-hire-a-security-clearance-lawyer-and-what-legal-fees-to-expect/). Baring in mind that most appeal cases are rejected, it would be significantly beneficial for applicants to know if they stand a good chance of winning their appeal before paying this cost. 

## Proposed Solution

Luckily, from a modeling prospective, security clearance appeals present a simple problem compared to many legal document retrieval cases. Because the reasons for rejection are so well-defined, cases are easily embeddable into a vector format. This project aims to take advantage of this unique element of security clearance appeals by a document retrieval model focused on efficiency and privacy. This would be used to help inform potential applicants of their likelihood of winning an appeals case before investing into an attorney to argue their case by allowing them to see similar cases 

As a proof of concept, this project will create a web UI where applicants can enter details stated on their SOR and lookup similar cases to theirs and get a predictive statement of their chances of winning an appeal. 


## Tech Stack
The code for the application will be written exclusively in Python and use the following packages:
- `pdfminer.six` used for reading pdf data
- `sentence-transformers` for creation of embeddings
- `pandas` for implementation of quick computation and sorting of cased via cosine similarity
- `streamlit` for display of the web application

## How to run the webapp locally

1. Clone this repo.
2. Set up a virtual environment with python 3.11 or higher (`python3 -m venv venv`) and install packages (`pip install requirements.txt`)
4. Use `streamlit run src/webapp.py` to run the webapp. Make sure you run it with the project root as your working directory.
