import re
import pandas as pd

# Function to safely extract the matched text with a fallback to "N/A"
def safe_search(pattern, text, group_num=1, fallback="N/A"):
    match = re.search(pattern, text)
    if match:
        return match.group(group_num)
    else:
        return fallback


# Year 
def yearFunction (text):
    year = safe_search(r'(\d{4})', text)
    
    return year
# Court
def cityFunction(text):
    city = safe_search(r'\[(.*?)\]', text).lower() 
    #city = safe_search(r'\[(.*?)\]', text)
    cityMapping = {
        "Federal Shariat Court":"Federal Shariat Court",
        "karachi": "Karachi High Court",
        "sindh": "Sindh High Court",
        "lahore": "Lahore High Court",
        "peshawar": "Peshawar High Court",
        "islamabad": "Islamabad High Court",
        }
    return cityMapping.get(city, "N/A")
# Judges
def judgesFunction(text):
    judges = safe_search(r'Before (.*?),', text)  # This will capture the judges' names
    return judges
# Applicant
def petitionerFunction(text):
    petitioner = safe_search(r"([A-Za-z\s\.]+(?:and\s\d+\sothers|---\s?(Petitioner|Appellant|Plaintiffs|Plaintiff|Applicants|Applicant|Admiralty)))", text)
    return petitioner.strip()
# Opponents
def opponentFunction(text):
    respondent = safe_search(r"(Versus\s*(.*?)\s*[A-Za-z\s\.]+(?:and\s\d+\sothers|---\s?(Respondents|Respondent|Defendants|Defendant)))",text)
    return respondent.strip()
# Legal Proceeding 1
def legalProceedingOneFunction (text):
    legal_proceeding = safe_search(r'\b(1st Appeal|1st Civil Appeal|Appeal|Appeals|Application for restoration|Bank guarantee|Banking Companies (Recovery of Loans, Advances Credits and Finances) Act|Banking Companies Ordinance|Banking Suit|Banking Tribunals Ordinance|Brokers and Agents Registration Rules|C.M. |C.M.A.|C.O.|C.O.S.|C.P.|Chartered Accountants Ordinance|Civil Appeal|Civil Miscellaneous Appeal|Civil Miscellaneous Application|Civil Procedure|Commercial Appeal|Companies|Companies Ordinance|Constitution Petition|Constitutional Petitions|Contract Act|Corporate and Industrial Restructuring Corporation Ordinance|Criminal Miscellaneous|E.F.A.|Execution First Appeal|Execution Petition|F.A.O.|Financial Institutions (Recovery of Finances) Ordinance|First Appeal|First Appeal from Order|H.C.A.|H.C.As.|High Court Appeal|J. Misc.|J. Miscellaneous|J.M.|Judicial Miscellaneous|Listed-Companies|M.As.|Miscellaneous Appeals|Miscellaneous Petition|Monopolies and Restrictive Trade Practices|Monopoly Appeal|R.A.|R.F.A.|Regular First Appeal|Regular First Appeals|Revision|Revision/Appeal|Securities and Exchange Ordinance|Show-Cause Notice|Sp. H.C.A.|State Bank of Pakistan|Stay order|Suit|Suit for declaration by borrower|Summary Suit|Trade Marks Act|Wealth Tax Appeal|Writ Petition|Writ Petitions|R.A|W.P|I.C.A)\b', text)
    legal_proceeding_mapping = {
    "1st Appeal": "First Appeal",
    "1st Civil Appeal": "First Civil Appeal",
    "Appeal": "General Appeal",
    "Appeals": "General Appeals",
    "Application for restoration": "Application for Restoration",
    "Bank guarantee": "Bank Guarantee",
    "Banking Companies (Recovery of Loans, Advances Credits and Finances) Act": "Banking Companies Recovery Act",
    "Banking Companies Ordinance": "Banking Companies Ordinance",
    "Banking Suit": "Banking Suit",
    "Banking Tribunals Ordinance": "Banking Tribunals Ordinance",
    "Brokers and Agents Registration Rules": "Brokers and Agents Registration Rules",
    "C.M.": "Civil Miscellaneous",
    "C.M.A.": "Civil Miscellaneous Appeal",
    "C.O.": "Company Ordinance",
    "C.O.S.": "Company Ordinance Suit",
    "C.P.": "Constitution Petition",
    "Chartered Accountants Ordinance": "Chartered Accountants Ordinance",
    "Civil Appeal": "Civil Appeal",
    "Civil Miscellaneous Appeal": "Civil Miscellaneous Appeal",
    "Civil Miscellaneous Application": "Civil Miscellaneous Application",
    "Civil Procedure": "Civil Procedure",
    "Commercial Appeal": "Commercial Appeal",
    "Companies": "Companies Ordinance",
    "Companies Ordinance": "Companies Ordinance",
    "Constitution Petition": "Constitution Petition",
    "Constitutional Petitions": "Constitutional Petitions",
    "Contract Act": "Contract Act",
    "Corporate and Industrial Restructuring Corporation Ordinance": "Corporate and Industrial Restructuring Corporation Ordinance",
    "Criminal Miscellaneous": "Criminal Miscellaneous",
    "E.F.A.": "Execution First Appeal",
    "Execution First Appeal": "Execution First Appeal",
    "Execution Petition": "Execution Petition",
    "F.A.O.": "First Appeal Order",
    "Financial Institutions (Recovery of Finances) Ordinance": "Financial Institutions Ordinance",
    "First Appeal": "First Appeal",
    "First Appeal from Order": "First Appeal from Order",
    "H.C.A.": "High Court Appeal",
    "H.C.As.": "High Court Appeals",
    "High Court Appeal": "High Court Appeal",
    "J. Misc.": "Judicial Miscellaneous",
    "J. Miscellaneous": "Judicial Miscellaneous",
    "J.M.": "Judicial Miscellaneous",
    "Judicial Miscellaneous": "Judicial Miscellaneous",
    "Listed-Companies": "Listed Companies",
    "M.As.": "Miscellaneous Appeals",
    "Miscellaneous Appeals": "Miscellaneous Appeals",
    "Miscellaneous Petition": "Miscellaneous Petition",
    "Monopolies and Restrictive Trade Practices": "Monopolies and Restrictive Trade Practices",
    "Monopoly Appeal": "Monopoly Appeal",
    "R.A.": "Review Appeal",
    "R.F.A.": "Regular First Appeal",
    "Regular First Appeal": "Regular First Appeal",
    "Regular First Appeals": "Regular First Appeals",
    "Revision": "Revision",
    "Revision/Appeal": "Revision/Appeal",
    "Securities and Exchange Ordinance": "Securities and Exchange Ordinance",
    "Show-Cause Notice": "Show-Cause Notice",
    "Sp. H.C.A.": "Special High Court Appeal",
    "State Bank of Pakistan": "State Bank of Pakistan",
    "Stay order": "Stay Order",
    "Suit": "Suit",
    "Suit for declaration by borrower": "Suit for Declaration by Borrower",
    "Summary Suit": "Summary Suit",
    "Trade Marks Act": "Trade Marks Act",
    "Wealth Tax Appeal": "Wealth Tax Appeal",
    "Writ Petition": "Writ Petition",
    "Writ Petitions": "Writ Petitions",
    "R.A": "Review Appeal",
    "W.P": "Writ Petition",
    "I.C.A": "Interlocutory Appeal",
    "I.C.A.": "Interlocutory Appeal"
}
    return legal_proceeding_mapping.get(legal_proceeding, "N/A")
# Proceeding 1 Number        
def proceeding1Number(text):
    case_number = safe_search(r'No\.(\d+ of \d{4})', text)
    return case_number.strip()
# Legal Proceeding 2
def legalProceeding2 (text):
    legal_proceeding2 = safe_search(r"(Appeal|Civil Revision|Review Petition|Second Appeal)", text)
    return legal_proceeding2
# Proceeding 2 Number 
def proceeding2Number (text):
    proceedind2_number = safe_search(r"(Appeal|Civil Revision|Review Petition|Second Appeal) No\.(.*?)\n", text, 2)
    return proceedind2_number
# Legal Proceeding 3
def legalProceeding3 (text):
    legal_Proceeding3 = safe_search(r"(Third Appeal|Review Application|Special Leave Petition)", text)
    return legal_Proceeding3
# Proceeding 2 Number
def proceeding3Number (text):
    proceedind3_number = safe_search(r"(Third Appeal|Review Application|Special Leave Petition) No\.(.*?)\n", text, 2)
    return proceedind3_number
# Date of decision
def dateOfDecision (text):
    Date_of_decision = safe_search(r"decided on (.*?)(?:\n|$)", text)
    return Date_of_decision


def extract_case_data(text):
    case_data = {
        
        'Year': yearFunction (text),
        'Court' : cityFunction(text),
        'Judges' : judgesFunction(text),
        'Applicant' : petitionerFunction(text),
        'Opponent' : opponentFunction(text),
        'Legal Proceeding 1' : legalProceedingOneFunction(text),
        'Processing1 Numbers' : proceeding1Number(text),
        "Legal Proceeding2": legalProceeding2(text),
        "Proceeding2 Numbers": proceeding2Number (text),
        "Legal Proceeding3": legalProceeding3 (text),
        "Proceeding3 Numbers": proceeding3Number (text),
        "Date of Decision": dateOfDecision(text),
        "Statute1": safe_search(r"([A-Za-z\s]+? Rules? \(\d{4}\))", text),
        "Statute1_sections": safe_search(r"R\.\s?(\d+)", text),
        "Statute2": safe_search(r"([A-Za-z\s]+? (?:Constitution|Act) \(\d{4}\))", text),
        "Statute2_sections": safe_search(r"Art\.\s?(\d+)", text),
        "Statute3": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute3_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        "Statute4": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute4_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        "Statute5": safe_search(r"([A-Za-z\s]+? (?:Act|Law|Rules?) \(\d{4}\))", text),
        "Statute5_sections": safe_search(r"R\.\s?(\d+)|Art\.\s?(\d+)", text),
        "Category": safe_search(r"([A-Za-z\s]+(?:petition|case|suit|appeal))", text),
        "Petitioner_lawyer": safe_search(r"for Petitioner\.\n\n(.*?)\n", text),
        "Respondent_lawyer": safe_search(r"for Respondents.*?\.\n\n(.*?)\n", text),
        "Departmental_representative": "N/A",  
        "Date_of_hearing": safe_search(r"Date of hearing: (.*?)\n", text),
        "Decision_type": "Judgment" if "JUDGMENT" in text else "Order"
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
print ("" )
# Input text (This should be the entire raw input text provided)
input_text = """


"""

# Process the input text
df_case_data = process_cases(input_text)

# Change output path to a valid directory on your local machine
output_file = "C:/Users/xiHawks 1002/Documents/legal_judgments.csv"

# Save the results to a CSV file
df_case_data.to_csv(output_file, index=False)

output_file  # This will return the path to your CSV file

