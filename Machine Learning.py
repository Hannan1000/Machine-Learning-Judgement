import re
import pandas as pd

# Function to safely extract the matched text with a fallback to "N/A"
def safe_search(pattern, text, group_num=1, fallback="N/A"):
    match = re.search(pattern, text)
    if match:
        return match.group(group_num)
    else:
        return fallback

# Function to extract the legal judgment information using re.search()
def extract_case_data(text):
    case_data = {
      # Year
        "Year": safe_search(r"(\d{4}) C L C", text),
        
        # Court
        "Court": safe_search(r"\[(.*?)\]", text),
        
        # Judges
        #"Judges": safe_search(r"Before (.*?),", text),
        "Judges": safe_search(r"Before (.*?,\s?J)", text),
        
        # Applicant (Ensuring Applicant is never N/A, extracting the full applicant name)
        #"Applicant": safe_search(r"([A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+\sand\s\d+\sothers)", text),
        #"Applicant_2": safe_search(r"([A-Za-z\s]+)", text)
        
        #"Applicant": safe_search(r"([A-Za-z\s]+(?:and\s\d+\sothers|---Petitioner))", text)
        "Applicant": safe_search(r"([A-Za-z\s\.]+(?:and\s\d+\sothers|---\s?Petitioner))", text),
        #safe_search(r"([A-Za-z\s]+(?:and\s\d+\sothers|---\s?Petitioner))", text) #safe_search(r"([A-Za-z\s]+(?:and\s\d+\sothers|---Petitioner))", text)

        # Opponent (Ensuring Opponent is never N/A)
        "Opponent": re.findall(r"versus\s+([^\n]+?)(?=\s*(?:Writ\s+Petition|Review\s+Petition|Case|---Respondents|First\s+Appeal))", text, re.IGNORECASE),

            #re.findall(r"versus\s+([^\n]+?)(?=\s*(?:Writ\s+Petition|Review\s+Petition|Case|---Respondents))", text, re.IGNORECASE)

            #re.findall(r"Versus\s+([^\n]+?)(?=\s*(?:Writ\s+Petition|Review\s+Petition|Case|---Respondents))", text)

            #re.findall(r"Versus\s+([^\n]+?)(?=\s*(?:Writ\s+Petition|Review\s+Petition|Case))", text)
            #safe_search(r"Versus\s+([^\n]+)(?=\s*Writ\s+Petition\s+No\.)", text)
        # safe_search(r"Versus\s+([^\n]+(?:\s+[\w\s\.\-]+)*)", text),
        
        # Legal_proceeding1
        "Legal_proceeding1": re.findall(r"(Writ Petition|Civil Suit|Criminal Case|Family Case|Constitutional Petition|Civil Revision|Appeal|Review Petition|Second Appeal|First Appeal)", text),

            #re.findall(r"(Writ Petition|Civil Suit|Criminal Case|Family Case|Constitutional Petition|Civil Revision)", text)
            #safe_search(r"(Writ Petition|Civil Suit|Criminal Case|Family Case|Constitutional Petition)", text),
            
         # Proceeding1_numbers
         #"Proceeding1_numbers": re.findall(r"(\w[\w\s]+(?:Petition|Case|Revision))\s+No\.\s*(\d+)", text, re.IGNORECASE)
         "Proceeding1_numbers": re.findall(r"(No\.\s*\d+\s+of\s+\d+)", text),
             #re.findall(r"(\w[\w\s]+(?:Petition|Case|Revision))\s+No\.\s*(\d+)", text, re.IGNORECASE)
  
             #re.findall(r"(Writ Petition|Civil Suit|Criminal Case|Family Case|Constitutional Petition|Civil Revision)\s+No\.\s*(\d+)", text, re.IGNORECASE)
         #safe_search(r"(Writ Petition|Civil Suit|Criminal Case|Family Case|Constitutional Petition) No\.(.*?)\n", text, 2),
            
         # Legal_proceeding2
         "Legal_proceeding2": re.findall(r"([A-Za-z\s\(\)\-]+(?:Rules|Act|Ordinance)[^,\n]*)", text),
#re.findall(r"([A-Za-z\s\(\)\-]+(?:Rules|Act|Ordinance)[^,]*)", text)
             #safe_search(r"(Appeal|Civil Revision|Review Petition|Second Appeal)", text),
        # Legal_proceeding2
        "Legal_proceeding2": safe_search(r"(Appeal|Civil Revision|Review Petition|Second Appeal)", text),
        
        # Proceeding2_numbers
        "Proceeding2_numbers": safe_search(r"(Appeal|Civil Revision|Review Petition|Second Appeal) No\.(.*?)\n", text, 2),
        
        # Legal_proceeding3
        "Legal_proceeding3": safe_search(r"(Third Appeal|Review Application|Special Leave Petition)", text),
        
        # Proceeding3_numbers
        "Proceeding3_numbers": safe_search(r"(Third Appeal|Review Application|Special Leave Petition) No\.(.*?)\n", text, 2),
        
        # Date_of_decision
        "Date_of_decision": safe_search(r"decided on (.*?)(?:\n|$)", text),
        
        # Statutes extraction directly with re.search()
        "Statute1": safe_search(r"([A-Za-z\s]+? Rules? \(\d{4}\))", text),
        "Statute1_sections": safe_search(r"R\.\s?(\d+)", text),
        
        "Statute2": safe_search(r"([A-Za-z\s]+? (?:Constitution|Act) \(\d{4}\))", text),
        "Statute2_sections": safe_search(r"Art\.\s?(\d+)", text),
        
        # Dynamically extract Statute 3, 4, 5 if present
        "Statute3": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute3_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        
        "Statute4": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute4_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        
        "Statute5": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute5_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        
        # Category
        "Category": safe_search(r"([A-Za-z\s]+(?:petition|case|suit|appeal))", text),
        
        # Petitioner Lawyer
        "Petitioner_lawyer": safe_search(r"for Petitioner\.\n\n(.*?)\n", text),
        
        # Respondent Lawyer
        "Respondent_lawyer": safe_search(r"for Respondents.*?\.\n\n(.*?)\n", text),
        
        # Departmental Representative
        "Departmental_representative": "N/A",  # Based on provided examples, no data found for this field
        
        # Date of hearing
        "Date_of_hearing": safe_search(r"Date of hearing: (.*?)\n", text),
        
        # Decision type (Judgment or Order)
        "Decision_type": "Judgment" if "JUDGMENT" in text else "Order"  # Based on content found in the text
    }
    
    return case_data

# Function to parse and process multiple cases
def process_cases(input_texts):
    case_list = []
    
    # Split the input text into individual case texts based on 'Case' keyword
    cases = input_texts.split('Case')
    
    # Process each case
    for case in cases:
        if case.strip():  # If the case has content
            case_data = extract_case_data(case)
            case_list.append(case_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(case_list)
    
    return df
# Input text (This should be the entire raw input text provided)
input_text = """


"""

# Process the input text
df_case_data = process_cases(input_text)

# Change output path to a valid directory on your local machine
output_file = "C:/Users/Documents/legal_judgments_summary_output.csv"

# Save the results to a CSV file
df_case_data.to_csv(output_file, index=False)

output_file  # This will return the path to your CSV file
