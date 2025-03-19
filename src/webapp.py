import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import pandas as pd
from utils import change_txt_filename_to_url
import pickle as pkl
import os
import py7zr

guideline_labels = {
    "A": "Allegiance to the United States",
    "B": "Foreign Influence",
    "C": "Foreign Preference",
    "D": "Sexual Behavior",
    "E": "Personal Conduct",
    "F": "Financial Considerations",
    "G": "Alcohol Consumption",
    "H": "Drug Involvement",
    "I": "Psychological Conditions",
    "J": "Criminal Conduct",
    "K": "Handling Protected Information",
    "L": "Outside Activities",
    "M": "Use of Information Technology Systems",
}

# Set page configuration
st.set_page_config(
    page_title="Security Clearance Appeal Case Lookup",
    page_icon="🔍",
    layout="wide",
)

# Add a header with a description
st.title("🔍 Security Clearance Appeal Case Lookup")
st.markdown(
    """
    Welcome to the **Security Clearance Appeal Case Lookup** tool!  
    Use this app to find similar cases and predict the chances of a successful appeal based on historical data.
    """
)


# Add a sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to interact with the app.")

# Cache the model training process
@st.cache_resource
def load_and_train_models():
    if not os.path.exists("src/data/case_embeddings.csv"):
        with py7zr.SevenZipFile("src/data/case_embeddings.7z", mode="r") as z:
            z.extractall("src/data")
    sf = SentenceTransformer("all-MiniLM-L6-v2")
    lr_models = {}
    lr_data = {}
    for letter in "ABCDEFGHIJKLM":
        with open(f"src/models/lr_model_{letter}.pkl", "rb") as f:
            lr_models[letter] = pkl.load(f)
        lr_data[letter] = pd.read_csv(f"src/data/formal_finding_results_guideline_{letter}.csv", index_col=0).dropna()
    return sf, lr_models, lr_data

# Load models and data
with st.spinner("Loading models..."):
    sf, lr_models, lr_data = load_and_train_models()
st.success("Models trained successfully!")


# Example cases for each guideline
example_cases = {
    "Foreign spouse and drug involvement": "The applicant's wife is a Peruvian citizen. Applicant admits to trying LSD, cocaine, and marijuana in college.",
    "Financial difficulties and gambling": "Applicant has a history of financial difficulties and has been gambling for the past 5 years.",
    "Alcohol abuse and domestic violence": "Applicant has a history of alcohol abuse and was charged with domestic violence against his spouse.",
    "Sexual offenses and psychological conditions": "Applicant was charged with aggravated rape, but successfully pled insanity. He has been diagnosed with PTSD and is undergoing treatment.",
    "Family in Hostile Country": "Applicant's parents are citizens of and currently reside in China",
    "Foreign Influence in Neutral Country": "Applicant's has a close relationship with a citizen of Brazil, who is also a business partner",
    "Foreign Preference in Ally Country": "Applicant has dual citizenship with Canada",
    "Soliciting prostitutes": "Applicant has a history of soliciting prostitutes while on overseas assignments in Southeast Asia",
    "Dual Allegiance": "Applicant has defended acts of espionage against the United States by Israel in private conversations",
    "Pedophilia": "Applicant had been convicted of possession of child pornography 10 years ago. He has been released after registering as a sex offender",
    "Leaker": "Applicant has broken NDA at a previous job by revealing information about a new video game his former employer was developing",
    "Drug Dealing in College": "Applicant was arrested for dealing drugs in college. He has since completed a rehabilitation program and has been clean for 5 years",
    "History of Suicide Attempts": "Applicant has attempted suicide twice in his life",
    "Shady Business": "Applicant runs a private security company with foreign clients in the Middle East",
    "HR Complaints": "Applicant has previously been fired from jobs due to complaints of creating a toxic work environment",
}

# Add example cases to the sidebar
st.sidebar.subheader("Example Cases")
selected_example = st.sidebar.selectbox(
    "Select an example case to auto-fill the input box:",
    options=[""] + [f"{key}" for key in example_cases.keys()],
)

# Auto-fill the text box with the selected example
if selected_example:
    selected_key = selected_example
    user_input = example_cases[selected_key]
else:
    user_input = ""

# Add user input section
st.sidebar.subheader("Case Lookup")
user_input = st.sidebar.text_area(
    "Enter details of a case to look up similar cases", value=user_input, height=150
)


# Function to process user input
def process_user_text_input(user_input):
    st.subheader("🔗 Similar Cases and Appeal Results")
    df = pd.read_csv("src/data/case_embeddings.csv", index_col=0)
    for col in df.columns:
        df[col] = df[col].astype("float32")

    user_input_embedding = sf.encode(user_input,normalize_embeddings=True)

    # Calculate similarity
    for column, u_i in zip(df.columns, user_input_embedding):
        df[column] *= u_i
    similarity_series = df.sum(axis=1).sort_values(ascending=False).head(10).rename_axis("Similarity")

    # Display similar cases
    for url in similarity_series.index:
        st.markdown(f"**Case URL:** {url}")
        for letter in lr_data.keys():
            try:
                st.write(
                    f"**Guideline {letter} ({guideline_labels.get(letter)}):** "
                    f"{'✅ Appeal Accepted' if lr_data[letter].loc[url][letter] else '❌ Appeal Denied'}"
                )
            except KeyError:
                pass

    # Display chances of successful appeal
    st.subheader("📊 Chances of Successful Appeal")
    for letter, model in lr_models.items():
        st.write(
            f"**Guideline {letter} ({guideline_labels.get(letter)}):** "
            f"{model.predict_proba(user_input_embedding.reshape(1, -1))[0][1] * 100:.2f}%"
        )

if st.sidebar.button("Submit"):
    if user_input.strip():
        process_user_text_input(user_input)
    else:
        st.sidebar.error("Please enter case details before submitting.")

# Footer
st.markdown("---")
st.markdown(
    """
    **Disclaimer:** This tool is for informational purposes only and does not constitute legal advice.  
    Developed by [Julius Frank](https://www.linkedin.com/in/julius-frank/).
    [GitHub Repository](https://github.com/Juliusfrank11/security-clearance-classification-webapp).
    """
)