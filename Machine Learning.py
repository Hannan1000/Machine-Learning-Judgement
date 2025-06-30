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
Case 1

 
2006 C L C 262
 
[Board of Revenue, Punjab]
 
Before Muhammad Saeed Sheikh, Member (Judicial-V)
 
HABIB ULLAH----Petitioner
 
Versus
 
GHULAM RASOOL and others----Respondents
 
R.O.R. No.1160 of 2002, decided on 3rd March, 2005.
 
West Pakistan Land Revenue Act (XVII of 1967)---
 
----Ss. 44, 163(iv) & 164---Mutation---Decree of Civil Court---Mutation in question was sanctioned and shares were allocated to widow and collaterals in pursuance of said decree---No appeal was filed against said mutation and review application against same was also rightly rejected on the ground that application for change/correction of record was filed after 13 years and no application for condonation of said delay was filed---Executive District Officer (Revenue), however, accepted appeal against order of District Collector on the ground that lower Court should have condoned the delay---Delay of 13 years in filing application against impugned mutation was not explained---Delay of each day had to be explained---Respondent could not explain before Courts below as to how he had no knowledge of mutation sanctioned 13 years ago--Petitioners had rightly contended that no appeal lay against review under S.163(iv) of West Pakistan Land Revenue Act, 1967---Impugned order passed by Executive District Officer (Revenue), being not maintainable, was set aside, in circumstances.
 
Ch. Iqbal Ahmad Khan and Ch. Muhammad Nawaz Sulehria for Petitioner.
 
Mian Muhammad Nawaz for Respondents Nos. 1 to 3, 5 to 19.
 
Ex parte for other Respondents.
 
Date of hearing: 3rd March, 2005.
 
ORDER
 
—----------------------------------------------
Case 1
2006 C L C 193
 
[High Court (AJ&K)]
 
Before Sardar Muhammad Nawaz Khan, J
 
MUHAMMAD AZAM and 5 others----Appellants
 
Versus
 
Mst. JANAT BI and 48 others----Respondents
 
Civil Appeal No.110 of 2004, decided on 29th October, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 42---Declaratory suit---Limitation---Islamic Law---Inheritance---Declaratory suit with prayer for joint possession was decreed by Trial Court, but on appeal same was dismissed on ground of limitation---Validity---Parties were contesting over their ancestral property under law of inheritance and plaintiffs had claimed to be owners of suit land being legal heirs of their deceased grandfather---If plaintiffs succeeded to establish that father of defendant, who was son of grandfather of plaintiffs, died in life time of their grandfather, then plaintiffs were owners of suit land under law of inheritance and any entry in revenue record disentitling them from their share in the joint estate, could not stay in their way simply on the ground of delay---If under law of inheritance a property had devolved upon a muslim owner, mere entry in revenue record negating his legal share, could be challenged as and when it would come to the knowledge of plaintiffs---Plaintiffs as soon as they acquired knowledge, had filed suit without any delay---Every denial, in such-like cases, whether it was through an entry in the revenue record or otherwise would give plaintiffs a new cause of action---Finding of Appellate Court below regarding bar of limitation being erroneous, was set aside and suit filed by plaintiffs was declared to be within time.
 
Farman Bi's case 2005 YLR 1814 and 13ostan and others v. Mst. Sattar Bibi and others PLD 1993 SC (AJ&K) 24 ref.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. XLI, Rr. 22 & 33 & 5.100---Second appeal---Powers of Court of appeal---Respondent had attacked the findings of both Courts below on issue dealing with controversy about death of father of one respondent alleging that Courts below by misreading and non-reading of evidence, had arrived at a wrong conclusion which resulted into a grave injustice to the respondent---Contention of appellant was that since respondent had neither filed a cross appeal against findings of the Courts below on said issue nor had filed any cross-objection, he could not be allowed to challenge said findings during arguments in second appeal---Validity---Respondent under provisions of R.22 of O.XLI, C.P.C., could support a decree appealed from, not only on any of grounds decided in his favour, but also on grounds decided against him and for that purpose it was not necessary for respondent to file any cross-objection---Respondent would be competent to support judgment of Court below even on grounds which were not decided in his favour and it could not be said that respondent could not assail findings on issue decided against her---Respondent was fully competent to attack finding on issue decided against her in presence of a favourable decree appealed against by appellants---Provisions of R.33 of O.XLI, C.P.C., also empowered Appellate Court to pass any decree and make any order which ought to have been passed or made---Said provision had also authorized Appellate Court to pass such further order or decree as case required---Such power of Appellate Court was not qualified with the fact that appeal was only against a part of decree and it could be exercised in favour of all or any of the respondents or parties even if they could not have filed any appeal or objection---Order XLI, R.33, C.P.C. was the singular power which sets Court free from clutches of procedural law and empowered it to do complete justice---Said provision of law, in circumstances had given wide discretionary powers to Appellate Court to adjust the rights of parties as and when it was demanded to have been done---Order XLI, Rr.22 & 33, C. P. C. had allowed respondent to attack findings on issues decided against him.
 
1998 MLD 450 ref.
 
(c) Specific Relief Act (I of 1877)---
 
----S. 42---Suit for declaration---Islamic law---Inheritance---Material issue in the case was whether father of respondent who was grandfather of appellants, died during life time of his father/grandfather of appellants---Onus to prove that issue was placed on appellants, but verbal evidence for and against on that issue, except the Court statement of witness, was of hearsay nature, which was not admissible' under law---Documentary evidence which was available on record, was under challenge, and stood excluded from evidence---Courts below, though were unanimous on point that father of respondent died during life time of his father/grandfather of appellants, but that concurrent finding on question of fact was based on no evidence, which, under law, was not sustainable---In order to deprive a Muslim, who was prima facie a legal heir in the legacy of his predecessor-in-interest, a very strong, cogent and credible evidence was required---Evidence, in the present case being contradictory in nature, suggested to decide issue against appellants as they had failed to prove their claim about death of father of respondent---Suit filed by appellants, though was within time, but, they had failed to discharge burden placed upon them in respect of issue involved in the case, which dealt with controversy of death of father of respondent---Judgments and decrees of Courts below to the extent of resolution about controversy regarding death of father of respondent, were set aside and it was declared that father of respondent died after death 'of his father---Respondent was entitled to her share out of legacy of her father---Appeal was disallowed for want of proof in circumstances.
?
(d) Islamic Law---
 
----Inheritance.
 
Rafiullah Sultani for Appellants.
 
Respondent No.1 in person.
 
ORDER
 
Case 2
 
2006 C L C 690
 
[High Court (AJ&K]
 
Before Sardar Muhammad Nawaz Khan, J
 
SULLAH MUHAMMAD---Appellant
 
Versus
 
MUHAMMAD SHARIF and another---Respondents
 
Civil Appeal No.58 of 2005, decided on 23rd February, 2006.
 
Azad Jammu & Kashmir Right of Prior Purchase Act (1993 B.K.)---
 
----Ss. 6 & 14--Limitation Act (IX of 1908), S.I8 & Art.10---Suit for pre-emption-Limitation---Condonation of delay---Suit, despite being barred by time, was allowed to continue by the Trial Court holding that issue of limitation required evidence--Appellate Court, however, dismissed suit declaring same as time-barred---Validity--Suit, admittedly had been filed with a delay of four days after expiry of specified period of four months from registration of sale-deed--Possession of suit-land was handed over to vendee on the very same date when sale was registered---Pre-emptor's case was not that sale-deed was concealed by way of any fraud or that he was kept away from knowledge of his right or title on which it was founded--Pre-emptor had not pleaded fraud--Vendor being full owner having transferred suit-land for consideration through a registered sale-deed, pre-emptor could not be benefited under S.18 of Limitation Act, 1908---Appellate Court, in circumstances, had rightly declared the suit as time-barred as same was filed with a delay of four days-Plaintiff seeking condonation of delay in filing suit, could not prove that during that period he was sick and was under treatment---False story had been made to cover up limitation---Appeal against judgment of Appellate Court below, was disallowed, in circumstances.
 
1998 CLC 711; 2000 MLD 1329; 2001 CLC 1149; 2004 MLD 943; PLD 1992 (AJ&K) 62 and 1998 CLC 371 ref.
 
Rafiullah Sultani for Appellant.
 
Ch. Mehboob Ellahi for Respondents.
 
ORDER
 
Case 3
2006 C L C 697
 
[High Court (AJ&K)]
 
Before Sardar Muhammad Nawaz Khan, J
 
MUHAMMAD RAZAQ KHAN-Appellant
 
Versus
 
Mst. SHAMIM AKHTAR and 8 others----Respondents
 
Civil Appeal No. 100 of 2004, decided on 23rd February, 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 39--Transfer of Property Act (IV of 1882), S.54---Qanun-e-Shahadat (10 of I 984), Art. 114--Suit for cancellation of sale-deed--Estoppel-Appellant in his suit sought cancellation of sale-deed in respect of suit property---Trial Court decreed suit, but Appellate Court setting aside judgment and decree passed by Trial Court, dismissed suit---Validity-Held, land in dispute was gifted to appellant by his real uncle, and subsequently said uncle along with his other brother and appellant sold land in favour of predecessor-in-interest of respondents--Sufficient evidence was available on record regarding consent of appellant to the sale of his share--All three vendors, including appellant appeared before Sub-Registrar concerned for registration of sale-deed executed in favour of predecessor-in-interest of respondents and said document was registered in their presence and appellant being an adult and sane person, raised no objection to the sale by his real uncle in favour of respondent/vendee---Possession of entire land including share of appellant sold out to the said vendee, was handed over to vendee/respondent in presence and knowledge of the appellant-All vendors including appellant having transferred land deliberately and with mutual consent in favour of respondent/vendee, appellant was estopped to challenge the impugned sale---Provisions of Art.114 of Qanun-e-Shahadat, 1984 would come to rescue the respondents/vendees which would debar appellant to bring suit against respondents--Impugned judgment and decree of Appellate Court was allowed to continue and appeal against said judgment and decree, was disallowed.
 
(b) Civil Procedure Code (V of 1908)---
 
--O. XLI, R.24---Re-settling of issue and determining suit finally--If the evidence on record was sufficient to enable the Appellate Court to pronounce the judgment, the Court was empowered to re-settle issue/issues, if necessary to finally determine the suit.
 
Rafiullah Sultani for Appellant.
 
Raja Mirdad for Respondents.
 
ORDER
 
Case 4
2006 C L C 1204
 
[High Court (AJ&K)]
 
Before Ghulam Mustafa Mughal, J
 
Mst. ZAMEER BEGUM and 2 others----Petitioners
 
Versus
 
SHAKEELA BEGUM and 7 others----Respondents
 
Civil Revision No.22 of 2005, decided on 18th April, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 104, O.XLI, Rr.23 & 25 & O.XLIII, R.1(u)---Appeal against order---Remand order---Section 104, C.P.C. was restrictive in character and was applicable only to the orders mentioned in the said section---Where a decree had been prepared by the Trial Court or impugned order had force of the decree, then clause (2) of S.104, C.P.C. would have no application and appeal would be competent if impugned order was covered by O.XLIII, R.1(u), C.P.C.---Second appeal would also be competent even from the orders, if same was allowed under some other Rule of C.P.C.---Appellate Court could pass remand order in two eventualities; i.e. under R.23 of O.XLI or under R.25 of O.XLI, C.P.C.---Remand order passed under R.23 of O.XLI, C.P.C. was appealable under O.XLIII, R.1(u), C.P.C., whereas remand order passed under R.25 of O.XLI, C.P.C. was revisable---Revision having been converted into appeal, contention that remand order was not appealable in view of S.104(2), C.P.C., was devoid of any force, in circumstances.
 
PLD 1970 SC 506; Muhammad Yasin v. Mst. Hassan Jan and 15 others PLD 1982 SC (AJK) 85; Abdul Rashid v. Gulzar 1995 SCR 307; Jane Margrete William v. Abdul Hamid Mian 1994 SCMR 1555; Muhammad Hanif v. Muhammad and others PLD 1990 SC 859; Fazal Ellahi and 5 others v. Alain Din PLD 1979 SC (AJK) 109; Fazal Elahi v. Jalal Din and 17 others PLD 1989 (H.C. AJK) 42; Ali Ahmed v. Mst. Ghulam Zohra PLD 1987 Quetta 189; Muhammad Akhtar v. Abdul Aziz, and 2 others PLD 1996 Lah. 232; Muhammad Sharif and another v. Mst. Rasul Bibi and others 1981 CLC 533; Syed Shah v. Khuda Bakhsh known as Maulvi Shah and others PLD 1954 Lah. 606; Kh. Akbar's case 2000 SCR' 211; Abdul Rashid's case PLD 1984 SC 164; PLD 1987 SC 139; 1994 SCMR 1555; Haridas and another v. Banshidhar and another AIR_ 1962 Rajasthan 57; Gokul Prasad v. Ram Kumar AIR 1922 All. 254; Firm Shaw Hari Dial and Sons; Madras through H.R. Bagdy v. Messrs Sohna Mal Beli Ram through Arjan Das AIR 1942 Lah. 95 and 1991 CLC 360 ref.
 
(b) Civil Procedure Code (V of 1908)---
 
----S. 9---Specific Relief Act (I of 1877), S.42---Jurisdiction of Civil Court---Petition---Civil Court being the Court of ultimate jurisdiction, was competent to try all the suits of civil nature, except barred expressly or impliedly---Ouster of jurisdiction of civil court in respect of suits of civil nature was not to be readily inferred---Acts of Executive or quasi-judicial Tribunals, could be challenged before a Civil Court if it appeared that assumption of jurisdiction by such forum was violative of law or they had acted in violation of provisions of the statute which conferred jurisdiction on them or on the ground of mala fide--Jurisdiction exercised and orders passed by such forums under special law, however, were immune from challenge, if those were passed strictly in accordance with provisions of that Statute---Serious question of title having been agitated by plaintiffs in the present case, and proceedings having also been challenged for having been conducted in violation of settled principles of partition proceedings, jurisdiction of the Court was not ousted.
 
Zafar-ul-Ahsan's case PLD 1960 SC 113; Abdul Rauf's case PLD 1965 SC 671; 1997 MLD 1309; Mir Rehman Khan's case PLD 1983 Quetta 52; Chhajju and others v. Dallu and another AIR 1919 Lah. 9; Tirath Ram and others v. Mt. Nihal Devi AIR 1931 Lah. 664 ref.
 
Ch. Muhammad Sabir for Petitioners.
 
Ch. Mumtaz Ahmed for Respondents.
 
ORDER
 
Case 5
2006 C L C 1244
 
[High Court (AJ&K)]
 
Before Ghulam Mustafa Mughal, J
 
Mst. ROZMAN and 8 others----Appellants
 
Versus
 
JALALUDDIN and 23 others----Respondents
 
Civil Appeal No.8 of 2005, decided on 6th February, 2006.
 
Civil Procedure Code (V of 1908)---
 
----Ss. 47 & 100---Limitation Act (IX of 1908), Art.182---Execution of decree---Determination of questions relating to execution---Earlier, predecessor of appellants obtained pre-emption decree, but no step was taken by him for execution of decree within prescribed period of limitation as provided by Art.182 of Limitation Act, 1908---Mutation was sanctioned on the basis of said decree after about fifteen years, and decree-holder/predecessor of appellants and two others again brought a suit in respect of same land on basis of the title---Plaint averred that appellants were owners of land in question on basis of decree passed in favour of their predecessor and that suit land was delivered to them on basis of compromise after rejection of their execution application and that respondents were allowed to cultivate land as appellants were outside the country---Adjudication of the question arising between the parties to the suit in which decree was passed or their representatives, and matter relating to the execution, discharge or satisfaction of decree, would be determined by the Court executing the decree and separate suit would be barred---Pleadings of the parties did not show that question relating to execution of decree was involved---Both subordinate courts, were not, justified in applying S.47, C.P.C. to the controversy as appellants had taken categoric stand that they had obtained possession from respondents on the basis of compromise; and thereafter handed over same to respondents as appellants were out of the country---Appellants had further claimed that they demanded possession of suit land from respondents in 1997 which having been refused by respondents, suit for possession on the basis of fresh cause of action had been filed; and that S.47, C.P.C. was not at all attracted as executing court after disposing of execution application had become functus officio---Accepting appeal, suit filed by appellants was decreed by the High Court and appellants were declared to be entitled to the possession of suit land.
 
Maqbool Ahmed Khan's case 1991 SCMR 2063; Moazam and others v. Panah and 9 others PLD 1958 Lah. 147; Mst. Reham Noor and others v. Wazir Muhammad and others PLD 1955 Pesh. 56; Ramanand and . others v. Jai Ram and others AIR 1921 All. 369; Barkat Ali's case PLD 1952 Lah. 82; Janada Sundari Nandi's case PLD 1958 Dhaka 198; Ali Ahmed's case PLD 1973 Lah. 207; PLD 1974 Lah. Note 56; Muhammad Saddiq's case AIR 1946 Lah. 322; Muhammad Rafique's case 2003 YLR 1434 and Kalu Maigi's case PLD 1967 Dacca 148 ref.
 
Raja Hassan Akhter for Appellants.
 
Ch. Muhammad Sabir for Respondents.
 
ORDER
 
—----------------------------------------------

Case 1
2006 C L C 5
 
[Karachi]
 
Before Zia Perwaz, J
 
MUHAMMAD ABDUL VAKEEL---Petitioner
 
Versus
 
GHULAM AKBAR SHAIKH and others---RespondentsZ
 
C.P. No. 1063 of 2002, decided on 14th June, 2005.
 
(a) Sindh Rented Premises Ordinance (XVII of 1979)---
 
----S. 15---Ejectment of tenant---Security amount, adjustment of---Principles---Amount of security deposited is adjustable in the manner and for the purpose it was originally deposited under the terms of rent agreement, if it is not in violation of rent laws.
 
Mrs. Zarina Khawaja v. Agha Mahboob Shah PLD 1988 SC 190 rel.
 
(b) Sindh Rented Premises Ordinance (XVII of 1979)---
 
----S. 15---Constitution of Pakistan (1973), Art. 199---Constitutional petition---Bona fide personal need of landlord---Ejectment of tenant---Adjustment of security deposit towards monthly rent---Landlord sought ejectment of tenant on the ground of bona fide personal need and default in payment of monthly rent---Order of ejectment passed by Rent Controller against tenant was maintained by Lower Appellate Court---Plea raised by tenant was that after expiry of tenancy agreement, he became statutory tenant and amount of security deposit could be adjusted towards monthly rent---Validity---According to mutual agreement of the parties, security amount deposited under tenancy agreement was for the protection of landlord against any outstanding dues, losses or damages and it was not meant for adjustment of rent for defaulted period---Such clause of tenancy agreement was not in any way violative of rent laws---Even after expiry of tenancy agreement between the parties, though the tenant had become statutory tenant of landlord but the clause which was regarding security deposit for protecting landlord's interest, continued to remain in force and effective as it was not otherwise unlawful under general law---Such clause of the agreement could not be varied under the law and had to be applied for the purpose provided in tenancy agreement and not otherwise---Amount of security deposit under such clause of tenancy agreement was not liable to be adjusted towards arrears of rent on expiry of the agreement---Sufficient material was produced in evidence to support the personal need of landlord, who was a Government servant and had been residing in Government accommodation for the past about 25 years, who was in need of his own house---High Court in exercise of Constitutional jurisdiction declined to interfere in the eviction order passed by Rent Controller and maintained by Lower Appellate Court---Constitutional petition was dismissed in circumstances.
?
Mrs. Zarina Khawaja v. Agha Mahboob Shah PLD 1988 SC 190 and Mst. Fatima Gul v. Malik Saeed Akhtar PLD 2005 SC 34 rel.
 
(c) Constitution of Pakistan (1973)---
 
----Art. 199---Sindh Rented Premises Ordinance (XVII of 1979), S.15---Constitutional jurisdiction of High Court---Scope---Ordinarily High Court in its Constitutional jurisdiction does not undertake to reappraise the evidence in rent matters to disturb findings of facts but it can interfere if such findings are found to be based on non-reading or misreading of evidence, erroneous assumption of facts, misapplication of law, excess or abuse of jurisdiction and arbitrary exercise of powers.
 
Muhammad Lehrasab Khan v. Mst. Aqeel-un-Nisa and others 2001 SCMR 338 rel.
 
Zahid Margoub for Petitioner.
 
Ms. Soofia Saeed for Respondent.
 
Date of hearing: 2nd June, 2005.
 
JUDGMENT
 
Case 2
 
2006 C L C 20
 
[Karachi]
 
Before Sabihuddin Ahmed, C.J. and Muhammad Afzal Soomro, J
 
ZULFIQAR ALI KHAN and another-Petitioners
 
Versus
 
DISTRICT GOVERNMENT, GHOTKI AT MIRPUR MATHELO and others---Respondents
 
C.Ps. Nos.D-876 and 877 of 2005, decided on 19th August, 2005.
 
(a) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Alternate and efficacious remedy---Failure to read a particular newspaper or official gazette---Effect---At times High Courts have declined to exercise constitutional jurisdiction when alternate equally efficacious remedy had not be availed of---Such rule, however, is not an inflexible and jurisdiction can be exercised when impugned order is without jurisdiction and alternate remedy is not efficacious---In absence of personal notice, an aggrieved person cannot be non-suited merely because of his failure to read a particular newspaper or official gazette.
 
(b) Sindh Local Government Ordinance (XXVII of 2001)---
 
----Ss. 6 & 11---Constitution of Pakistan (1973), Art.199---Constitutional petition---Limits of Union Council, changing of---Objections---Locus standi---Whenever it is alleged that Union Councils are created to give greater representation to residents of a particular area within a district and thereby reduced the representative capacity of residents of other areas in violation of law, every resident has locus standi to question the dispensation---Electoral college for Nazim and Naib Nazim of district consists of members of a Union Council and increase in some areas would affect voting strength of those residing in others.
 
(c) Sindh Local Government Ordinance (XXVII of 2001)---
 
---Ss. 6, 11 & 159---Constitution of Pakistan (1973), Art.199---Constitutional petition---Territorial limits of Union Council---Alteration---Jurisdiction of Union Council---Zila Council, role of---Zila Council, in its meeting, passed a resolution proposing creation of 3 new Union Councils---Petitioner assailed the notification of creation of new Union Councils and re-demarcation of existing Union Council on the ground that Zila Council did not have any jurisdiction to pass resolution in such respect---Validity---Proposal for alteration of territorial limits was to be made by Union Councils or Taluka Councils as the case might be---Union Council, under S.11 of Sindh Local Government Ordinance, 2001, could act on two occasions before a proposal was made to Government---In first place a change was proposed and public objections were invited---After considering such objections a resolution by 2/3rd majority was to be passed and transmitted to Government---Zila Council had no say in the matter and resolution by Zila Council in respect of alternation of territorial limits of Union Council was irrelevant for the purpose---Resolution initiated by Zila Council was ultra vires its powers and consequent Notification issued by Provincial Government was without lawful authority and of no legal effect---High Court set aside the Notification of creation of new Union Councils and directed Provincial Government to hold elections either on the basis of pre-existing Union Councils or to establish Union Councils in accordance with law---Petition was allowed in circumstances.
?
(d) Words and phrases---
 
----Alter---Meaning.
 
Black's Law Dictionary, Sixth Edition ref.
 
(e) Sindh Local Government Ordinance (XXVII of 2001)---
 
----S. 11---Territorial limits of Union Council---Alteration---Pre condition---Requirement of such alteration is that size of population in proposed Union Council should be close to the average population of existing Union Council in a district.
?
(f) Sindh Local Government Ordinance (XXVII of 2001)---
 
----S. 159---Term of office---Extension---Object and scope---To prevent a vacuum in the event of inability on the part of Government to hold elections, law authorizes a local government to remain in office for a period beyond its normal term---Such Local Government cannot presume that it continues in office despite expiry of its term and surpasses statutory limitation of its powers.
 
Federation of Pakistan v. Haji Saifullah Khan PLD 1989 SC 166 distinguished.
 
(g) Constitution of Pakistan (1973)---
 
---Art. 199---Constitutional jurisdiction of High Court---Scope---Relief, grant of---High Court may decline to accord relief, which would result in perpetuation of unconstitutionality or illegality and opted for an unlawful course to be followed in future---When it is alleged that impugned action would perpetuate an illegality in future, High Court would be required to accord appropriate relief.
 
(h) Interpretation of statute---
 
----Omission in statute---Effect---Statute has to be interpreted according to its plain ordinary meaning and Court cannot assume the functions of legislature by filling an omission unless the provisions are incapable of being understood according to their plain meaning or blatantly violate legislative intent.
 
Abdul Mujeed Pirzada, Hisamuddin and Abdul Sattar Pirzada for Petitioners.
 
Aziz A. Munshi, Abdul Fatah Malik and Anwar Mansoor Khan, A.-G., Sindh for Respondents.
 
ORDER
 
Case 3
 
2006 C L C 42
 
[Karachi]
 
Before Anwar Zaheer Jamali and Syed Zawwar Hussain Jafferi, JJ
 
JAWAID AHMED SIDDIQUI---Petitioner
 
Versus
 
DISTRICT COORDINATION OFFICER and others---Respondents
 
C. P. No.D-1170 of 2004, decided on 2nd June, 2005.
 
Press Newspapers, News Agencies and Books Registration Ordinance (XCVIII of 2002)---
 
---Ss. 4 & 10---Constitution of Pakistan (1973), Art. 199 --- Constitutional petition---Authentication of declaration---Application for---Petitioner, who was Chairman of a non-political and non-profit earning organization, had applied to District Coordination Officer for authentication of declaration---Such application was received by District Coordination Officer, but remained unattended despite several reminders from petitioner and lapse of considerable period of over one year and six months before filing the Constitutional petition---Petitioner had been harassed and made to run from pillar to post for said period for that purpose which, under law, was supposed to be done by D.C.O. within period of thirty days---District Coordination Officer could not offer any plausible explanation for said inordinate delay and not only had failed to authenticate declaration of petitioner for over one year and six months before filing the Constitutional petition as against statutory period of thirty days, but even after filing of the petition by petitioner, D.C.O. continued with his non-serious attitude in attending the issue---By virtue of subsection (5) of S.4 of Press Newspapers, News Agencies and Books Registration Ordinance, 2002, Fortnightly Journal of petitioner, sought to be authenticated, was deemed to have been authenticated by District Coordination Officer.
 
Petitioner in person.
 
Manzoor Ahmed for Respondent No. 1.
 
Abbas Ali, Addl. A.-G. Sindh for Respondents Nos.2 and 3.
 
ORDER
 
Case 4
2006 C L C 65
 
[Karachi]
 
Before Anwar Zaheer Jamali and Syed Zawwar Hussain Jaffery, JJ
 
ABDUL RUB SIDDIQUI---Petitioner
 
versus
 
GOVERNMENT OF SINDH, through Secretary, Government of Sindh and 4 others---Respondents
 
Constitutional Petition No.D-988 of 2004, decided on 30th August, 2005.
 
Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Jurisdiction---Scope---Auction of plot---Petitioner had claimed that he was highest bidder in auction of plot in question and as per terms of auction he had deposited twenty five per cent. of bid money and also deposited second instalment, but despite that his highest bid in respect of plot in question was not approved by the competent Authority---Stand of authorities was that bid offered by petitioner was never approved by the competent Authority and that documents relating to intimation to petitioner about acceptance of his bid seemed to be managed through fraudulent means in connivance with the staff of the Development Authority---From the assertions made in petition and its reply submitted on behalf of authorities, which was also accompanied with certain documents, it was evident that adjudication of claim of petitioner in respect of plot in question would require thorough investigation into serious factual controversies involved in the matter---Constitutional jurisdiction of High Court was not the proper forum for said purpose---Petitioner was permitted to withdraw constitutional petition and to approach Civil Court to seek necessary reliefs against authorities in respect of plot in question.
 
1968 SCMR 729; 2000 SCMR 718; 2001 SCMR 1493 and 2001 SCMR 1569 ref.
Abdul Hameed Shaikh for Petitioner.
Ahmed Pirzada, A.A.-G. Sindh for Respondent No. 1.
Manzoor Ahmed for Respondents Nos.2 to 5.
 
ORDER
 
Case 5
2006CLC71
 
[Karachi]
 
Before Saiyed Saeed Ashhad, C. J. and Mushir Alam, J
 
Mst. AFSHAN and another---Petitioners
 
versus
 
IIIRD ADDITIONAL DISTRICT AND SESSIONS JUDGE, KARACHI (SOUTH) CITY COURTS, KARACHI and others---Respondents
 
Constitutional Petition No.D-2455 of 2001, decided on 24th January, 2002.
 
Civil Procedure Code (V of 1908)---
 
----O. XXII, R.3---Sindh Rented Premises Ordinance (XVII of 1979), S.21--Constitution of Pakistan, 1973, Art. 199 --- Constitutional petition---Legal representatives as party to the appeal after death of the appellant---Father of the petitioners filed an appeal before the Appellate Court and died during the pendency of the same---Subsequently an application was filed by the petitioners under O.XXII, R.3, C.P.C. as legal representatives before the Appellate Court ---Such application was however, rejected and appeal was dismissed on the ground that the petitioners had not been brought on the record earlier---Validity---Appellate Court, while dismissing the appeal, had completely lost sight of the fact that after amendment in O.XXII, C.P.C. no suit or appeal or any other proceedings could be abated merely on the ground that the legal representatives of a party to the suit, appeal or proceedings were not brought on the record---Proceedings against a dead person were a nullity and could not be revived by bringing on record the heirs of such deceased person---Father of the petitioners was very much alive when he had filed the appeal and had died during the pendency of the same, therefore, on account of his death and failure of legal heirs to get themselves impleaded, the appeal could neither be dismissed nor would abate---Constitutional petition was allowed in circumstances.
 
Rashida Khatoon v. Syed Hamid Ali Naqvi 1986 SCMR 256 distinguished.
M.M. Tariq for Petitioners.
Masood Khan Ghori for Respondents.
 
ORDER
 
Case 6
 
2006 C L C 86
 
[Karachi]
 
Before Mushir Alam and Syed Zawwar Hussain Jaffery, JJ
 
Messrs PAKLAND CEMENT LIMITED---Appellant
 
versus
 
Messrs AMERICAN EXPRESS BANK N.A. and another ---Respondents
 
 
First Appeal No.75 of 2004, heard on 20ih September, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. I, R.1----Parties to suit---All persons could be joined in one suit against whom any right or relief in respect of or arising out of same act or transaction or series of acts or transactions was alleged to exist.
 
Saalim Salam Ansari and Mukhtair Ahmed Kober for Appellant. Syed Salnmuddin Nasir for Respondent No.1
Nei-no. for Respondent No.2.
 
Date of hearing; 20th September, 2005.
 
ORDER
 
Case 7
 
2006 C L C 99
 
[Karachi]
 
Before Zia Perwaz, J
 
SULTAN AHMAD---Petitioner
 
Versus
 
ADDITIONAL DISTRICT JUDGE-I, KARACHI SOUTH---Respondent
 
C.P. No.S-773 of 2002, decided on 2nd June, 2005.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
----S.15---Constitution of Pakistan (1973), Art.199---Constitutional petition---Ejectment of tenant---Bona fide personal need of landlord---Failure to specify nature of business---Selection of premises---Rent Controller dismissed ejectment application on the ground that landlords failed to disclose type of business they intended to establish and they had one shop available with them which could be used for their business---Order of Rent Controller was maintained by Lower Appellate Court---Plea raised by landlords was that it was their choice to select the premises---Validity---If landlords possessed more than one house / shop in same area, the choice as to the house / shop which they would like to possess was a matter within their prerogative and discretion---Tenant or Rent Controller did not have the power to determine which premises landlords should personally use/reside in---Question as to which portion / shop of building would suit landlords better, must be left to the discretion of landlords and there was nothing unreasonable if landlords were insisting that a particular portion of building should be made available to them---No legal requirement existed to the effect that landlords in seeking ejectment of tenant from a shop on the ground of personal and bona fide requirement must disclose the nature of business which they intended to start in the premises---Both the Courts below had erred in arriving at conclusion that landlords failed to prove their bona fide requirement of the premises in question---High Court in exercise of Constitutional jurisdiction set aside the concurrent orders passed by both the Courts below and eviction order was passed against tenant---Petition was allowed in circumstances.
 
Akhtar Qureshi v. Nisar Ahmed 2000 SCMR 1292 ref.
 
Haroon Kassam and another v. Azam Suleman Madha PLD 1990 SC 394 fol.
 
Mian Mushtaq Ahmed for Petitioner.
 
Irfanullah G. Ali for the Respondent.
 
Date of hearing: 12th May, 2005.
 
JUDGMENT
 
Case 8
2006 C L C 110
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
MUHAMMAD RAHIM and another---Petitioners
 
Versus
 
KARACHI METROPOLITAN CORPORATION through Administrator and 11 others---Respondents
 
C.P. No. 1007/D of 1994, heard on 21st December, 2004.
 
Transfer of Property Act (IV of 1882)---
 
----S. 6---Transfer of property, extent of--Owner could not transfer a better title to a transferee than he himself possessed.
 
Muhammad Saleem v. Administrator, Karachi Metropolitan Corporation, K.B.C.A. (K.M.C.), Karachi and 5 others 2000 SCMR 1748 ref.
 
M. Farooq Hashim for Petitioners.
 
Manzoor Ahmed for Respondent No. 1.
 
Abdul Majeed Ashrafi for Respondent No.2.
 
Ms. Rehana Perveen for Respondents Nos.3, 6, 7 and 11.
 
Nemo for other Respondents.
 
Date of hearing: 21st December, 2004.
 
JUDGMENT
 
Case 9
 
2006 C L C 119
 
[Karachi]
 
Before Muhammad Afzal Soomro, J
 
BIRCH CLUB---Petitioner
 
Versus
 
GOVERNMENT Of SINDH and others---Respondents
 
C.P. No.262 of 2005, decided on 3rd June, 2005.
 
Constitution of Pakistan (1973)---
 
----Art. 199---Criminal Procedure Code (V of 1898), S.22-A---Constitutional petition---Misuse of authority and harassment---Petitioner club was registered under S.21 of Societies Registration Act, 1860, and was being run in lieu of payment of Government fee---Petitioner club had its own bye-laws and was providing indoor recreational facilities such as billiard, snooker, skittle, carom board, cards and lido etc.---Management of the petitioner club, in the year, 2001, refused membership to certain persons, on account of its decision to stop any fresh membership, thus litigation started between the parties---Refusal from membership led to grudge by high officials in Government functionaries/Police Department and obstructions were started to be created for one or the other reason---Validity---Case of the petitioner club was not that of simple harassment where the petitioner could have approached Sessions Judge under S.22-A Cr.P.C.---Deputing of police force in shape of picket at the door of petitioner club, in view of background of litigation was mala fide on the part of Police authorities, 'which amounted to deprive citizens/members of the club from their fundamental right of entering into club---High Court directed police authorities to remove picket and restrained the authorities from causing harassment in future---Petition was allowed accordingly.
Muhammad Junaid Farooqi for Petitioner.
 
Date of hearing: 1st June, 2005.
 
JUDGMENT
 
Case 10
 
2006 C L C 235
 
[Karachi]
 
Before Ata-ur-Rehman and Zia Perwaz, JJ
 
MUHAMMAD HAJRA KHAN----Petitioner
 
Versus
 
GOVERNMENT OF SINDH through Chief Secretary and 5 others----Respondents
 
Constitutional Petition No.D-774 of 2003, decided on 28th January, 2005.
 
Contempt of Court Act (LXIV of 1976)---
 
----Ss. 3 & 4---Constitution of Pakistan (1973), Art.199---Constitutional petition---Contempt of Court---Constitutional petition was disposed of and petitioner had filed application under Contempt of Court Act, 1976 on the ground that order passed by High Court in constitutional petition had not been complied with---On the day, petition was disposed of counsel for respondents had made certain statements to compensate petitioner and in pursuance thereof, petitioner was informed about terms of compensation---Petitioner had filed objection to such decision---Petitioner had no right and title to property in question as he failed to deposit transfer fee as directed by Board of Revenue, but despite that he was being adequately compensated by the respondents---Question of any contempt did not arise; it was up to petitioner to accept the offer or otherwise---Petitioner had submitted that said amount be ordered to be paid to the Trust directly---Said proposition having been agreed to, application was disposed of accordingly.
 
M. Amin Memon for Petitioner.
 
Ahmed Pirzada, A.A.-G.
 
Manzoor Ahmed for K.B.C.A.
 
ORDER
 
Case 11
 
2006 C L C 240
 
[Karachi]
 
Before Faisal Arab, J
 
PAKISTAN HERALD PUBLICATIONS (PRIVATE) LTD.----Plaintiff
 
Versus
 
PAKISTAN TELECOMMUNICATION CORPORATION----Defendant
 
Suit No.309 of 1996, decided on 14th December, 2005.
 
Pakistan Telecommunication Corporation Act (XVIII of 1991)---
 
----S. 16---Specific Relief Act (I of 1877), Ss.39, 42 & 54--- Suit for cancellation, declaration and permanent injunction---Controversy in the suit was whether defendant was entitled to the revised rates of rent of machine with retrospective effect--Defendant had failed to lead any evidence, though burden was on it to establish revision in the rates---Plaintiff had every right to oppose belated introduction of documents by defendant at the argument stage---No party could be permitted to take the other side by surprise, nor could be permitted to introduce documents at belated stage without any lawful excuse---Even if High Court for the time being had ignored such legal infirmity and considered such documents, revision of rates which were claimed to have been made in February 1993, should have been notified to subscribers either through gazette notification or through publication in the newspapers, but neither of the two modes was resorted to---Plaintiff was not even billed at the revised rates in the relevant years and defendant continued to bill the plaintiff at original rates---Defendant for two long years did not demand enhanced rates from plaintiff and it was only after plaintiff sought discontinuation of service vide letter dated 30-1-1995 that defendant for the first time issued revised bill dated 28-2-1995 demanding difference of revised rates from 1993---No doubt S.16 of Pakistan Telecommunication Corporation Act, 1991, had empowered defendant to revise rates, but such revision had to be notified to the consumers so that they may or may not opt to continue with the facility, but revision in rates was not notified in any manner whatsoever---No lawful justification existed for defendant to demand revised rates from plaintiff and plaintiff was not liable to pay point to point charges at excess rate---Suit was decreed accordingly.
 
Ealhi Cotton Mills Ltd. v. Federation of Pakistan PLD 1997 SC 582 and Army Welfare Sugar Mills Ltd. v. Federation of Pakistan 1992 SCMR 1652 ref.
 
Makhdoom Zia-ul-Haque for Plaintiff.
 
Sakhiullah Chandio for Defendant.
 
Date of hearing: 9th December, 2005.
 
JUDGMENT
 
Case 12
 
2006 C L C 246
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
Haji MUNIRUDDIN KHAN through Legal Heirs----Petitioners
 
Versus
 
PROVINCE OF SINDH through Secretary, Local Bodies, Sindh and 8 others----Respondents
 
Constitutional Petition No.D-676 of 1997, decided on 2nd March, 2005.
 
Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Open place in question was reserved for amenity purpose, but subsequently layout plan was modified and said open place was carved out as a commercial and subsequently as an industrial plot---Petitioner earlier had filed a suit claiming that he had right to be allotted said plot which suit was dismissed and his appeal against judgment and decree was also dismissed---Petitioner, thereafter filed present constitutional petition praying that amenity plot could not be converted into one for residential/commercial purposes---Validity---Petitioner was perfectly reconciled with the conversion of plot in question, more than two decades before filing present constitutional petition and wanted the same to be allotted to himself---Only after failing to establish his claim before a competent Court he chose to file constitutional petition---Such petition having not been moved in public interest and bona fides of petitioner being questionable, constitutional petition was dismissed.
Muhammad Ali Jan for Petitioners.
 
Chaudhary Muhammad Rafique, Addl. 'A.-G. Sindh, Manzoor Ahmed and Arshad Mubeen Khan for Respondents.
 
ORDER
 
Case 13
2006 C L C 250
 
[Karachi]
 
Before Ata-ur-Rehman and Zia Perwaz, JJ
 
MUHAMMAD WARIS and another----Petitioners
 
Versus
 
CHIEF MINISTER, SINDH and 5 others----Respondents
 
Constitutional Petition No.D-668 of 1998 and C.M.A. No.8578 of 2004, decided on 13th January, 2005.
 
Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, (III of 2001)-----
 
----S. 3---Contempt of Court Ordinance (IV of 2003), Ss.3 & 4---Constitution of Pakistan (1973), Art.199 --Constitutional petition--Contempt of Court---Applicants/petitioners in their application for contempt of Court had sought action against alleged contemners for violation of order whereby their constitutional petition was allowed---Authority by its letter, referred the matter to Committee constituted under Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001 and Committee exercising powers under said Ordinance, decided case of petitioners pertaining to plot and allowed petitioner to get it regularized subject to payment of amount mentioned in the decision---After the matter was referred to the Committee, petitioners were represented and heard before decision was taken by Committee---Petitioners had neither challenged action of Authority of referring matter to Committee nor challenged order of Committee before any forum for want of jurisdiction---Alleged contemners did not commit any Contempt of the Court in circumstances.
M. Imtiaz Agha for Petitioners.
 
ORDER
 
Case 14
 
2006 C L C 254
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
OWNERS' ASSOCIATION OF UZMA ARCADE through Secretary and 2 others----Petitioners
 
Versus
 
GOVERNMENT OF SINDH through Secretary, Local Government
Housing Town Planning, Local Government Public Health Engineering
and K.A. Department and 3 others----Respondents
 
Constitutional Petitions Nos.977 and 1415 of 2002, decided on 9th February, 2005.
 
Constitution of Pakistan (1973)--
 
----Art. 199---Constitutional petition--Levy of charged parking fee---Petitioners had questioned the levy of charged parking fee by Authority---Resolution of council of Authority, had directed, inter alia, that charged parking should be stopped forthwith and such resolution had been given effect to---Both counsel for petitioners agreed that without prejudice to question of validity of levy, petition had become infructuous, and they would not press the' same---Petition was disposed of accordingly.
 
Petitioners in person (in C.P. No.1415 of 2002).
 
Rafiq Rajori, A.A.-G. for Respondent No.1.
 
Manzoor Ahmad for Respondent No.2.
 
ORDER
 
Case 15
 
2006 C L C 257
 
[Karachi]
 
Before Sarmad Jalal Osmany and Muhammad Mujeebullah Siddiqui, JJ
 
COLLECTIVE BARGAINING AGENT (LABOUR UNION) through General Secretary----Appellant
 
Versus
 
GOVERNMENT OF SINDH through Secretary, Housing and Town Planning Department and 2 others----Respondents
 
Constitutional Petition No.D-1083 of 2002, decided on 31st January, 2005.
 
Constitution of Pakistan (1973)---
 
----Arts. 199 & 204---Constitutional petition---Contempt of Court---Controversy whether petitioner's dues had been paid or not, could not be decided through contempt application, as it raised disputed questions of fact---Since on the one hand counsel for petitioners insisted that dues had not been paid in accordance with law, counsel for Authority (respondent) had stated that it had so been done, contempt application was dismissed with direction to the petitioners to resort to any other legal remedy available to them for the redress of their grievance.
 
Rizwan Ahmed Siddiqui for Petitioner.
 
Manzoor Ahmed for City District Government, Karachi.
 
Muhammad Sarwar Khan, Addl. A.-G.
 
ORDER
 
Case 16
 
2006 C L C 260
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
GUL MUHAMMAD HAJANO----Petitioner
 
Versus
 
PROVINCE OF SINDH through Chief Secretary, Sindh and others----Respondents
 
Constitutional Petition No.D-1219 of 2004, decided on 13th January, 2005.
 
Constitution of Pakistan (1973)---
 
----Art. 199(1)(b)(ii)---Sindh Local Government Ordinance (XXVII of 2001), S.18(ii)---Writ of quo warranto---Petitioner by way of writ of quo warranto had called in question appointment of Adviser to City Nazim relying upon S.18(ii) of Sindh Local Government Ordinance, 2001 which had explicitly stipulated that Zila Nazim, would not employ any adviser, special Assistant or Political Secretary---Counsel for City Nazim, had very fairly conceded that no such appointment could be made by Nazim and had stated that no formal appointment of any such nature had been made and that no official responsibility on behalf of City Government had been conferred upon the alleged adviser---Held, adviser in question had not been duly appointed to any position whatsoever in the City District Government nor was he entitled to exercise any functions as adviser or otherwise---Constitutional petition was disposed of accordingly.
 
Petitioner in person.
 
Manzoor Ahmed for Respondent No.3.
 
ORDER
 
Case 17
 
2006 C L C 272
 
[Karachi]
 
Before Mrs. Qaiser Iqbal, J
 
QUEENS ROAD LANE----Plaintiff
 
Versus
 
CITY DISTRICT GOVERNMENT and others----Defendants
 
Suit No.270 and C.M. No.1378 of 2005, decided on 6th December, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXIX, Rr.1 & 2---Karachi Building and Town Planning Regulation, 2002, Reglns. 19.2 & 2.7---Pakistan Environmental Protection Act (XXXIV of 1997), S.12---Constitution of Pakistan (1973), Art.9---Application under O.XXXIX, Rr.1 & 2, C.P.C. praying that the defendants,, their servants, employees, assignees, successors, legal heirs, attorneys, representatives or any other person or persons for or on behalf of the defendants be restrained from demolishing the Park, subject-matter in question and constructing illegal shops in the Park and creating third party interest---Plaintiff was a registered Welfare Association of shopkeepers of a Market carrying on business in the said market over last four and half decades with all amenities provided by the Government and had been paying taxes regularly on the demand of the City District Government--Said Market was constructed in the year 1960 and the Park was constructed by the defunct City Municipal Corporation for maintaining good atmosphere and providing entertainment to the shopkeepers including the residents of the locality and general public---Shops of the plaintiffs were constructed around the Park in question and due to demolition of Park and construction of illegal shops proposed to be raised by City District Government, all the plaintiffs (shopkeepers) of the Market were to suffer as their shops would be in back lane and the business of plaintiffs shall be ruined who were carrying on business there for last many decades---Plaintiffs, in circumstances prayed that the defendants be restrained from raising illegal construction in the Park as the action of the defendants was discriminatory and in violation of the Constitution and was aimed at harassing the plaintiffs for their illegal enrichment on the behest of the mighty persons to humiliate and ruin the business of the plaintiffs---Validity---Layout plan pertaining to the area in question reflected that there existed a park on the layout plan of the defunct City Municipal Corporation which was being utilized for the purpose of constructing shops for affectees of the widening of the road on account of construction of the bridge---Nazir of the Court who was appointed by Court to inspect the site and submit the report stated that park was found completely demolished, that its marks were available, that the fountain which was fixed in the centre of the park area was also removed, that foot-path was available in the Park area, that water pump machine was also fixed and that new shops were near completion--Fact that space now bearing shops for defendants/affectees of the bridge was earmarked as park thus, could not be lost sight of---Documents on record also established prima facie case of the plaintiffs that without any public notice or without any other action in this behalf the status of the Park and/or amenity plot was being changed by City District Government or defunct City Municipal Corporation---Contention of defendants that the construction of the shops having been completed, no action was called for, was negated from the other side on the premise that it was a public interest litigation and human rights were involved---Held, subject plot being an amenity plot used as Park as was established from the record, City District Government was bound by the law to safeguard the interest of the public, but instead they had acted ignoring all the norms of public administration and the rule of law---Contention of defendants (affectees of bridge) that they would undertake that in case they lose the case on final trial they would vacate the shops if the possession and permission to complete the remaining construction and occupy the same was granted by the Court, could not be accepted, for balance of inconvenience lay in favour of the plaintiffs coupled with irreparable loss likely to be caused to them---Such concession could not be granted to the defendants for enjoying the fruits of the property in violation of guaranteed rights enjoyed by public---Plaintiffs, in circumstances, being entitled to relief claimed, status quo order passed earlier, was confirmed by the High Court.
 
D.D. Vyas and others v. Ghaziabad Development Authority Ghaziabad AIR 1993 Allah. 57; Sindh Institute of Urology and Transplantation and others v. Nestle Milkpak Limited and others SBLR 2005 Sindh 116; S.N. Gupta v. Sadananda Ghosh PLD 1960 Dacca 153; Ms. Shehla Zia v. WAPDA PLD 1994 SC 693; Funfair (Pvt.) Ltd. v. Karachi Development Authority PLD 2004 Kar. 170; Al-Jamiaul Arabia Ahasanul Uloorn and Jamia Masjid v. Sibte Hasan 1999 YLR 1634; 1999 SCMR 2089 and PLD 1956 Kar. 521 and 1990 CLC 448 ref.
 
Aminullah Siddiqui and Farogh Naseem for Plaintiff.
 
Ali Azam for K.B.C.A. Defendant No.2.
 
Raja Qureshi for Defendants Nos.5 to 6.
 
Date of hearing: 2nd December, 2005.
 
ORDER
 
Case 18
2006 C L C 286
 
[Karachi]
 
Before Syed Zawwar Hussain Jaffery, J
 
ABDUL HAQUE and 3 others----Applicants
 
Versus
 
SUKHIAL and 2 others----Respondents
 
Civil Revision No.13 of 1999 and C.M.A. No.184 of 2001, decided on 10th September, 2001.
 
(a) Civil Procedure Code (V of 1908)---
 
----Ss. 115 & 12(2)---West Pakistan Civil Courts Ordinance (II of 1962), Ss.18 & 2(h)---Court Fees Act (VII of 1870), Art.12---Revision---Scope---Order passed on application under S.12(2), C.P.C.---Payment of court fee---Both the High Courts and the District Courts, can exercise revisional jurisdiction, there is, however, a limitation on the exercise of such jurisdiction by the latter which can exercise revisional jurisdiction only in those cases wherein the value of the subject-matter, does not exceed its appellate jurisdiction---Jurisdiction---Meaning---No court-fee is payable on the order passed on the application under S.12(2), C.P.C. and challenged before the High Court by way of revision---Principles.
 
Munir Ahmed Khan and others v. Samiullah Khan and others 1982 CLC 525; Province of Punjab through Secretary, Government of Punjab Housing and Physical Planning Department, Lahore and another v. District Judge, Lahore and 3 others PLD 1984 Lah. 515; Mst. Ghulam Sakina and 4 others v. Nishan and 2 others 1992 CLC 87; Fazar Ali Khan and 3 others v. Ghulam Ali Khan and 9 others 1995 CLC 1850 and Civil Revision No.1618 of 1981 ref.
 
(b) Jurisdiction---
 
----Connotation---Jurisdiction means the power of administering justice according to the means which law provides, and subject to the limitations imposed by law and such limitations may be territorial or pecuniary or that may relate to the nature of litigations.
 
(c) Civil Procedure Code (V of 1908)---
 
----S. 115---Revisional jurisdiction---Scope---Section 115, C.P.C. confers an exceptional and necessary power intended to secure effective exercise of the High Court's superintending and revisional powers of correction unhindered by technicalities.
 
(d) Civil Procedure Code (V of 1908)---
 
----S. 115---Revisional jurisdiction---Scope---Jurisdiction under S.115, C.P.C. is discretionary in nature---Court cannot arbitrarily refuse to exercise its discretionary power and must act according to law and the principles enunciated by superior Courts.
 
Shaikh Abdul Qadir for Applicants.
 
David Lawrence for Respondents.
 
ORDER
 
Case 19
 
2006 C L C 289
 
[Karachi]
 
Before Faisal Arab, J
 
NAZIM ALI----Plaintiff
 
Versus
 
RASHID QAMAR and 2 others----Defendants
 
Civil Suit No.926 of 1996, decided on 2nd November, 2005.
 
(a) Civil Procedure Code (V of 1908)-
 
--O. XIV, R.1---Abandonment of issue---Counsel, as a rule is competent to abandon an issue during the conduct of a suit if he in his discretion bona fide thinks appropriate, but there are exceptions to such rule; where the concession amounts to erroneously giving up an issue on a question of law or such concession cannot be justified for proper conduct of a case, then the Court would still give its finding on such issue.
 
Ali Bahadur Khan v. Hussain Khan PLD 1979 SC (AJ&K) 47 ref.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 129(g)---Adverse inference---Where a party withholds evidence of vital importance, such an act is fatal to his case---Court always draws an adverse inference against a person where he, in a given situation, is bound to react in a particular manner but fails to do so.
 
Sughran Bibi v. Aziz Begum 1996 SCMR 137 ref.
 
(c) Administration of justice-
 
----Findings of a Criminal Court are neither binding nor relevant for adjudicating a civil dispute in a civil Court---Civil disputes are decided on the basis of preponderance of probabilities and the test of proof is not the proof of a fact beyond reasonable doubt but is the preponderance of evidence.
 
Ghulam Rasool v. M. Waris Bismil 1995 SCMR 500 ref.
 
M. Ikram Siddiqui for Plaintiff.
 
Malik A.R. Arshad for Defendant No.2.
 
Nemo for Defendants Nos.1 and 3.
 
Date of hearing: 26th October, 2005.
 
JUDGMENT
 
Case 20
2006 C L C 303
 
[Karachi]
 
Before Gulzar Ahmed, J
 
PORT SERVICES COMPANY LTD.----Applicants
 
Versus
 
PORT SERVICES (PVT.) LTD. Through Chief Executive and others----Respondents
 
C.M.A. No.2050 of 2005 in Suit No.2 of 2005, decided on 4th October, 2005.
 
(a) Civil Procedure. Code (V of 1908)---
 
---O. VII, R.11---Rejection of plaint---Requirements---While considering an application under O.VII, R.11, C.P.C. for rejection of the plaint, not only the plaint has to be examined but the Court can also look at and examine the undisputed and admitted material that may be made available by the parties on the record---Averments made in the plaint are considered to be correct unless they be absurd or in contradiction of themselves.
S.M. Shafi v. Hassan Ali Khan 2002 SCMR 338 ref.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. VII, R.13, O.II, R.2 & S.11---Arbitration Act (X of 1940), S.17---When the earlier suit of the plaintiff which went into arbitration and was rejected by an award which was made rule of the Court and no appeal having been filed, as a matter of fact and law it became final and conclusive between the parties and the plaintiff was barred from reopening-the same matter by subsequent suit which on all fours was the same matter as the earlier suit in terms of O.VII, R.13, C.P.C.---Plaintiff, to maintain subsequent suit, had to show that not only the subsequent suit was in time but it would also have to be shown that earlier suit was not barred by limitation---Order II, R.2, C.P.C. in such a situation had no relevance as the claim of the plaintiff in the subsequent suit, in substance, was the same as in the earlier suit---Plaintiff's suit, in circumstances, was barred by rule of res judicata.
 
Abdul Latif v. Manzoor Ahmed 1993 MLD 177; S.M. Shafi v. Hassan Ali Khan 2002 SCMR 338; Fazal Rahim v. Al-Wajid Town 1994 MLD 126; Al-Riaz Agencies v. Chambers of Commerce 2001 CLC 1966; Trustees v. Gujranwala Steel 1990 CLC 197; Abdul Majid v. Muhammad Afzal Khokhar 1993 SCMR 1686; Asghar Ali v. P.K. Shahani 1992 CLC 2282; Hashim Khan v. National Bank PLD 2001 SC 325; Mona Batool v. Sindh Government 1992 MLD 777; Muhammad Tufail v. Atta Shabir and others PLD 1977 SC 200; Muhammad Anwar v. Messrs Associated Trading Co. 1989 MLD 4750; Muhammad Anwar v. Messrs Associated Trading Co. PLD 1995 Kar. 214; Abdul Majeed v. Abdul Ghafoor PLD 1982 SC 146; Mukhtar Ali Khan v. Goverurnent of Pakistan 1993 CLC 1239; Haji Allah Bukhsh v. Abdul Rahman 1995 SCMR 459; Jewan v. Federation of Pakistan 1994 SCMR 826; Messrs Haji Muhammad Sharif Ata Muhammad v. Messrs Khoja Mithabhai Nathoo PLD 1960 (W.P.) Kar. 10; Sakhi Muhammad v. Munshi Khan PLD 1992 SC 256; Messrs Pakistan Telecommunication Corporation v. Abdul Sattar 1995 MLD 1563; Mst. Kaneez Fatima v. Member (Revenue), Board of Revenue Punjab, Lahore PLD 1973 Lah. 459; Abdul Majeed v. Khyber Vegetable Ghee Mills 1984 CLC 2392; Sharifullah v. Mumtaz PLD 1980 Pesh. 87; Mian Khan v. Auorangzeb 1989 SCMR 58; Mrs. Zubeda v. City District Government Karachi PLD 2004 Kar. 304; Mst. Asmat Ara Begum v. Mst. Hajira Bibi PLD 1964 Pesh. 283; 'Raja Ramnad v. Velusami Tevar AIR 1921 PC 23; and Shah Harichand Nanji v. Shah Damji Hemchand AIR 1956 Kutch 13 ref.
 
Muhammad Sharif for Applicant.
 
Ms. Sana Akram Minhas for Respondent No.1.
 
Zahid F. Ibrahim for RespondentNo.2.
 
Date of hearing: 4th October, 2005.
 
ORDER
 
Case 21
 
2006 C L C 316
 
[Karachi]
 
Before Azizullah M. Memon and Ghulam Rabbani, JJ
 
LIBRA ENTERPRISES----Appellant\
 
Versus
 
Messrs MACTER PHARMACEUTICALS (PVT.) LTD.----Respondent
 
High Court Appeal No.189 of 2003, decided on 7th October, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. VII, R.2---Law Reforms Ordinance (XII of 1972), S.3---High Court appeal---Suit for recovery of outstanding amount---Respondent, in its suit claimed recovery of amount remaining outstanding against appellant towards supplies made to defendant---Appellant had argued that by mutual consent, distributorship in question was cancelled and respondent had issued certificate stating therein that outstanding amount was actually paid to respondent by appellant and that nothing was outstanding against appellant which was further confirmed by the proprietor of respondent who issued certificate certifying therein that respondent had received all outstanding dues from appellant and nothing remained to be paid to respondent---Suit was decreed by Single Judge with observation that appellants were served in the suit and their Advocate, despite filing his Vakalatnama on behalf of appellants, absented himself on various dates---Single Judge decreed suit tiled by respondents taking into consideration affidavit in evidence filed by respondents in proof of their claim---Held, cases between parties should be decided on merits and the rules and procedure which were framed to foster cause of justice, should sparingly come in the way of dispensation of justice on merits---Appellants had made out a case to allow them leave to defend themselves in suit in order that it could be heard and decided on merits---Allowing the appeal, impugned judgment and decree passed in suit were recalled and appellants were afforded with an opportunity to file written statement within specified period.
 
Wak Orient Power and Light Limited v. Westinghouse Electric Corporation and others 2002 SCMR 1954 and Syeda Tahira Begum and another v. Syed Akram Ali and another 2003 SCMR 29 ref.
 
Asim Mansoor for Appellants.
 
Ghulam Ghous for Respondents.
 
Date of hearing: 12th September, 2005.
 
JUDGMENT
 
Case 22
2006 C L C 342
 
[Karachi]
 
Before Faisal Arab, J
 
Dr. AFTAB SHAH----Plaintiff
 
Versus
 
PAKISTAN EMPLOYEES COOPERATIVE HOUSING SOCIETY LIMITED and 5 others----Defendants
 
Suit No.1228 of 1980, decided on 8th December, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 12---Suit for specific performance of contract in relation to a residential plot which the plaintiff claimed to have purchased from the Housing Society---Plaintiff, who was not a Federal Government employee and member of the Society was not entitled to allotment of the plot, claimed that the then Administration of the Society offered the said plot to him, which he accepted and paid the entire sale consideration; that possession was delivered to him and even a sub-licence was registered in his favour and that letter of allotment was issued to him---Validity---To seek a lawful allotment of a residential plot in the Society, Licence Agreement clearly stipulated that a person must possess two basic qualifications i.e. he must be an employee of Federal Government and must be a member/shareholder of the Society which qualifications the plaintiff admittedly lacked---Administrator, who was head of the Society at the relevant time, was not expected to be ignorant of the fact that the plaintiff was not a member of the Society nor he was ignorant of the scope of his authority to make allotments of residential plots---Administrator, thus abused his power---When powers of a public functionary were circumscribed by a written document then such powers were to be exercised strictly within the four corners of the prescribed limits---No public functionary, who was entrusted with the duty of dealing with Government property, should consider himself to be possessed with unfettered or unregulated powers to be used or abused in disregard of the prescribed limits---Administrator, in the present case,. had travelled beyond the scope of his authority and misconducted himself while allotting the plot to the plaintiff and it was a clear case of dishonesty and abuse of power on his part---Plaintiff, in circumstances, was not qualified to seek allotment of the plot of land in the Society---Entire process of allotment and execution of sub-licence in favour of plaintiff was invalid being violative of Licence Agreement and Bye-laws of the Society---Suit was dismissed---Principles.
 
(b) Cause of action---
 
----Presumption---When one stand is taken at one point of time and different stand at another, and both stands do not reconcile with each other, then such act by itself leads to the presumption that the person does not have a genuine cause of action.
 
(c) Public functionary---
 
----Scope of powers---When powers of a public functionary were circumscribed by a written document then such powers were to be exercised strictly within the four corners of the prescribed limits---No public functionary, who was entrusted with the duty of dealing with Government property should consider himself to be possessed with unfettered or unregulated powers to be used or abused in disregard of the prescribed limits.
 
Muhammad Inayatullah for Plaintiff.
 
Abdul Sattar, Abdul Latif A. Shakoor, Abdul Raul' and Akram Zubari for Defendants.
 
Dates of hearing: 10th, 11th, 15th and 16th November, 2005.
 
JUDGMENT
 
Case 23
 
2006 C L C 352
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
ABDUL RAUF----Petitioner
 
Versus
 
MEHRAN HEALTH AND WELFARE CENTRE through General Secretary and 2 others----Respondents
 
Constitutional Petition No.D-3492 of 1993, decided on 25th February, 2005.
 
Transfer of Property Act (IV of 1882)---
 
----S. 105---Constitution of Pakistan (1973), Art.199---Constitutional petition---Lease of plot---Petitioner had called in question fresh lease executed in favour of respondent in a civil suit on the original side of High Court which was still pending---Questions were whether said lease was valid and was sub judice in that suit---Present petition had not been pursued with diligence and events appeared to have overtaken the reliefs claimed---Constitutional petition was dismissed as infructuous with clarification that Building Control Authority would be under obligation to take appropriate action, if any violation of approved plan was brought to its notice---Said observation, however, would not affect questions raised in the suit pending adjudication.
 
Muhammad Yasin Azad for Petitioner.
 
Surayya Rahim for Respondent No.1.
 
Manzoor Ahmad along with Syed Shariq Ilyas, Project Director for Respondent No.2.
 
Shahid Jamiluddin Khan along with Muhammad Sami, Deputy Controller of Building for Respondent No.3.
 
ORDER
 
Case 24
 
2006 C L C 356
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
PAKISTAN INDUSTRIAL CREDIT AND INVESTMENT CORPORATION LTD. KARACHI----Plaintiff
 
Versus
 
KARACHI DEVELOPMENT AUTHORITY through Managing Director----Defendant
 
Suit No.1231 of 2000, decided on 24th January, 2005.
 
Specific Relief Act (I of 1877)---
 
----Ss. 42 & 54---Suit for declaration and permanent injunction---Plot in dispute was duly allotted to plaintiff for construction of its office building---Plaintiff paid fixed price, allotment/possession order was issued in its favour and then possession of plot was physically delivered to plaintiff---Under terms of allotment, plaintiff had to complete construction of its office building on said plot within two years from date of possession order---Such period of two years later on was extended---Before expiry of said extended period allowed to plaintiff for construction, Authority issued notice to plaintiff requiring it to explain the reason as to why allotment of plot in question should not be cancelled for not raising construction .upon it---Plaintiff replied said notice expressing therein that extended period of construction had not yet expired---After silence of more than ten months of reply of plaintiff, the governing body of authority vide its resolution cancelled allotment of plot of plaintiff on the ground that due to a policy decision, no building would be constructed between the road and the water line of boating basin---Validity---Cancellation of plot duly allotted to plaintiff, without giving it notice was in violation of principles of natural justice, especially when plaintiff had acquired vested rights on allotment of plot and delivery of possession thereof With right to raise construction---Cancellation order was not lawful---Plaintiff had right to raise construction upon plot in question after approval of construction plan by Authority---Prayer of plaintiff for permanent injunction, was also granted against disturbance of possession, enjoyment and use of plot by plaintiff so long it was legally entitled to possess and use of same under allotment in its favour.
 
Mushtaq A. Memon for Plaintiff.
 
S. Muzaffar Imam for Defendant.
 
Date of hearing: 26th November, 2004.
 
JUDGMENT
 
Case 25
 
2006 C L C 362
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui, J
 
In re: Mst. NAGHMA SIDDIQUI HILLFRAM, KARACHI
 
S.M.A.No.104 of 1995, decided on 19th December, 2005.
 
(a) Islamic law---
 
----Succession---Merely by marrying a non-Muslim, a female does not become non-Muslim and shall not be deprived of her right of inheritance in respect of the properties left by her parents.
 
(b) Islamic law---
 
----Faith---Conversion---If a person says that he is a Muslim and it is not shown that he still believes in something against the articles of faith, then no body has any right to dispute his claim---If, however, a person claims himself to be a Muslim but believes in something which is against the basic articles of faith such as, is the case of Ahmedis/Qadianis, he shall be treated as non-Muslim---If even no document is available the mere assertion of a person that he embraced Islam on a particular date, his statement is to be accepted and he shall not be called upon to produce any other evidence to establish his conversion to Islam---Principles.
 
(c) Succession Act (XXXIX of 1925)---
 
----S. 5--- Merely by marrying a non-Muslim, a female does not become non-Muslim and shall not be deprived of her right of inheritance in respect of the properties left by her parents---Application for revocation of the Letter of Administration on the ground that the said female had no right of inheritance in respect of the properties left by her father was without substance.
 
Ms. Rukhsana Ahmed for Petitioner.
 
Shamdas B. Changani for Applicant.
 
Mst. Shakeela Khanum widow of deceased Zubair Hussain Siddiqui.
 
Date of hearing: 21st November, 2005.
 
ORDER
 
Case 26
 
2006 C L C 366
 
[Karachi]
 
Before Anwar Zaheer Jamali and Maqbool Baqar, JJ
 
FAQIR MUHAMMAD and 9 others----Petitioners
 
Versus
 
SECRETARY, GOVERNMENT OF SINDH, BOARD OF REVENUE, KARACHI and 4 others----Respondents
 
Constitutional Petition No.D-356 of 2004, decided on 14th September, 2004.
 
Sindh Goathabad (Housing Scheme) Act (VII of 1987)---
 
----S. 6---Constitution of Pakistan (1973), Art.199---Constitutional petition---Allotment of plot---Cancellation of allotment---Petitioners, who claimed themselves to be allottees/occupants of plots in respective Goath/village, had challenged the cancellation of allotment of the plots---Claim of petitioners was that they were in possession of Sanads, Form-II and Site plan of their respective plots issued by Authorities in their favour which had confirmed lawful title, in their favour, but Authorities had treated petitioners as encroachers and had threatened to demolish existing construction over their plots, which action of Authorities was illegal and without jurisdiction---Submission of Authorities was that allotment in the Goath/village concerned which was sanctioned earlier, was subsequently cancelled by defunct Deputy Commissioner under S.6 of Sindh Goathabad (Housing Scheme) Act, 1987 after fulfilling all legal formalities and consequently land in dispute was restored to Government and out of said land some area was--earmarked and proposed for bus terminal and possession thereof was handed over to the concerned-Authority---Petitioners conceded passing of order whereby grant of village concerned was withdrawn/cancelled, but had contended that said fact was not within the knowledge of petitioners---Validity---Impugned order had been passed after detailed enquiry which could not remain secret for a period of over five years, especially when its copies were also dispatched to all concerned officers including office of Mukhtiarkar concerned---Petitioners, in circumstances had not approached High Court with clean hands and were not entitled for any equitable relief in their constitutional petition---Petition being frivolous was dismissed with special costs, in circumstances.
 
Ghulam Abbas Soomro for Petitioners.
 
Ahmed Pirzada, A.A.-G. Sindh.
 
Manzoor Ahmed for City District Government, Karachi.
 
ORDER
 
Case 27

2006 C L C 373
 
[Karachi]
 
Before Sabihuddin Ahmed and Khilji Arif Hussain, JJ
 
Messrs AL-MEHRAN BUILDERS through Attorney----Petitioner
 
Versus
 
CITY DISTRICT GOVERNMENT, KARACHI through District Coordinating Officer----Respondent
 
Constitutional Petition No.1762 of 1995, heard on 26th January, 2005.
 
Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance (III of 2001)-----
 
----S. 3---Constitution of Pakistan (1973), Art.199---Constitutional petition---Allotments of property, cancellation of---Contention of petitioner was that vested right to allotment of property had matured in his favour and non-payment of balance price of 50% was not on account of any fault on his part---Authorities urged that property had been allotted to petitioner at a price below the market rate and his right stood cancelled under Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001---Validity---Cancellation of allotment under the Ordinance, could have effect only upon a finding of the Committee to the effect that property was allotted to petitioner below the market rate---Section 3 of Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001 provided that allotment at rates lower than market value or in violation of a ban with effect from, 1-1-1985, would stand cancelled, cancellation would not lead to the conclusion that allottee retained no right or interest with respect to property---Petitioner was still entitled to acquire title to property upon payment of price determined by Committee within time specified by it---If petitioner would deposit amount required by Committee, respondent would execute' an appropriate lease in his favour.
 
Abdul Hafeez Pirzada along with Abdul Sattar Pirzada, Rana Ikramullah, Hisamuddin Qazi for Petitioner.
 
Manzoor Ahmed for Respondent.
 
Date of hearing: 26th January, 2005.
 
JUDGMENT
 
Case 28
 
2006 C L C 379
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui, J
 
ALI MUZAFFAR through L.Rs.----Petitioners
 
Versus
 
Syed MUHAMMAD ALI ABEDI through L.Rs. and others----Respondents
 
Constitution Petition No.1091 of 2002, decided on 19th December, 2005.
 
(a) Sindh Rented Premises Ordinance (XVII of 1979)---
 
----Ss. 15 & 21---Constitution of Pakistan (1973), Art.199---Constitutional jurisdiction of High Court---Scope and extent---Application for ejectment by landlord against tenant---Question pertaining to appreciation of facts cannot be resorted to, in exercise of constitutional jurisdiction by High Court, for the simple reason that in doing so constitutional petition shall be converted into a revision or second appeal and the very purpose of abolishing the second appeal and restricting the finality pertaining to the matters under Sindh Rented Premises Ordinance, 1979 to first appeal shall stand frustrated---Constitutional petition is not substitute either for revision or the second appeal and constitutional petition shall be entertained if a case is made out to the effect that the Rent Controller and First Appellate Authority have made an order palpably without jurisdiction or there is case of lack of jurisdiction or the finding is so perverse, that it is not sustainable on the established principles of the appreciation of evidence, or any specific provision of law has been violated---No constitutional petition in rent matters and in all such cases in which no second appeal or revision is provided in law, shall be entertained, until and unless there is a jurisdictional error committed by the Courts below---Exercise of jurisdiction in a perverse or arbitrary manner or ignoring the material available on record or violation of any provision of law, substantive or procedural, causing miscarriage of justice or violation of established principles of administration of justice shall bring the case within the purview of jurisdictional error---Inbuilt presumption is that the constitutional petition shall not be entertained if there is concurrent finding of facts, otherwise the petition shall be maintainable even if there is no concurrent finding of facts and the finding of the appellate Court does not suffer from any jurisdictional error or an illegality, the appellate order shall not be open to challenge in constitutional petition on the ground that there is no concurrent finding of fact---Both the Courts below, in the present case, had examined each and every aspect of the evidence available on record and had passed very lengthy and elaborate orders and not a single sentence of the evidence had remained unattended or unexamined---No illegality or jurisdictional error or instance of violating any provision of law in arriving at the finding had been pointed out---High Court declined to re-examine and reappraise the evidence with observations that such course was not to be adopted even in exercise of revisional jurisdiction and question of adopting such course in exercise of constitutional jurisdiction was totally unwarranted.
 
Saifullah v. Muhammad Bux 2003 MLD 480 fol.
 
(b) Sindh Rented Premises Ordinance (XVII of 1979)---
 
---S. 15---Bona fide personal need of landlord---Once landlord has established the personal bona tide need at the time of filing of ejectment application, then the subsequent events, in case tenant succeeds in procrastinating the matter for ten to fifteen years, would not obliterate the personal bona tide need, of the landlord.
 
(c) Sindh Rented Premises Ordinance (XVII of 1979)---
 
---Ss. 15 & 10---Default in payment of rent---If a tenant without offering the rent to the landlord in the first instance starts depositing rent with Rent Controller, then it would be treated as default in payment of rent on the part of tenant.
 
(d) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional jurisdiction of High Court---Scope and extent.
 
The extraordinary constitutional jurisdiction under Article 199 of the Constitution has been conferred on the High Court for exercise of discretionary powers in order to come in aid to justice and not for perpetration of injustice. The delay in dispensation of justice for years together itself amounts to negation of justice and perpetration of injustice. High Court shall always be slow in exercise of constitutional jurisdiction where the statute has provided appeal and a person has, either availed the remedy or has declined to avail such remedy until and unless it is shown that the action taken, or order passed or intended to be passed is palpably without jurisdiction and is violative of the principles of justice.
 
Munir A. Malik and Adnan Iqbal Choudhry for Petitioner No.1.
 
Iqbal Haider and Malik M. Eijaz for Respondent No.2.
 
Khalid Jawaid for Respondents Nos.1(i), (ii), (iii) and (iv).
 
Nemo for Respondents Nos.2 and 3.
 
Dates of hearing: 22nd, 29th August and 19th December, 2005.
 
JUDGMENT
 
Case 29
 
2006 C L C 401
 
[Karachi]
 
Before Gulzar Ahmed, J
 
Mrs. SAADIA MUZAFFAR through her Attroney----Plaintiff
 
Versus
 
Mrs. KHADIJA MANZUR and another----Defendants
 
Suit No.585 of 1996, decided on 20th January, 2006.
 
(a) Partition Act (IX of 1893)---
 
----S. 2---Civil Procedure Code (V of 1908), O.XX, R.18---Suit for partition---Title in property derived by parties through gift in equal shares---Defendant denied joint status of property by alleging that before gift, donor had constructed two units identical in area, one of them was facing main road, while other having only access to main road; and that donor had gifted to defendant the unit facing main road---Proof---Wasiat Nama and Declaration of Gift made by donor showing transfer of property together with a house built thereon as a whole one unit to both parties, but not in portions---Record of Residential Society not showing gift of property in portions to both parties---Oral evidence of defendant to contrary, could not displace such admitted documentary evidence---Mere allowing occupation by deceased donor of front portion to defendant would not negate actual gift of property as a whole one unit to both parties---Occupation of a portion of joint property either by plaintiff or defendant would be merely a matter of incident or convenience, which would have nothing to do with actual gift and could not be taken to be partition by metes and bounds---No regular partition of property had ever been effected between parties or their predecessors---Parties being co-owners and co-sharers in property would have interest in each and every part thereof---Report of Nazir showing property incapable of division from its frontage into two equal portions of equal value---Interest of both parties could be well-secured by putting up property to sale and sharing its sale proceeds equally---Court decreed suit after appointing Official Assignee for such purpose.
Muhammad Zubair v. Syed Zakir Hussain Shah 1996 CLC 275; Ali Gohar Khan v. Sher Ayaz, 1989 SCMR 130; Baqat Khan v. Mst. Dil Jan 2000 MLD 1165; Ghulam Hussain v. Mst. Hur PLD 1959 (W.P.) Kar. 408; Abdul Ghaffar v. Bashir Ahmed 2003 YLR 362; Noor Rehman v. Muhammad Yousuf 2000 CLC 1138; Muhammad Aziz v. Muhammad Arif 2001 MLD 597; Mardan Shah v. Shah Nazar Khan PLD 1970 SC 245; Malik Muhammad Abdullah v. Malik Manzoor Elahi 1993 MLD 2569; Israr Muhammad Khan v. Senior Civil Judge, Lahore 1990 SCMR 693; Muhammad Ibrahim v. Muhammad Sharif 1980 CLC 296; Maqsood Begum v. Mukhtar Ali 1999 CLC 598; Rasab Khan v. Abdul Ghani PLD 1985 SC (AJ&K) 69; Abdur Rehman v. Sheer Wadood 2001 CLC 1922; Muhammad Din v. Liaqat Ali 1991 MLD 1070; Sh. Gulzar Muhammad v. Mst. Munawar Begum 1989 ALD 323(1); Jayalakshmidevamma v. Javardhan Reddy AIR 1959 Andhra Pradesh 272; Karvidan Sarda v. Sailaja Kanta Mitra AIR 1940 Patna 683; Babulall Choukhani v. Caltex (India) Ltd. AIR 1967 Cal. 205; Badr Zaman v. Sultan 1996 CLC 202; Musheer Ahmed Pesh Imam v. Dr. Razia Omer 1991 CLC 678; Humera Rehman v. Ghazala Rehman Suit No.1057 of 1999; Kalusingh v. Gulabchand AIR 1957 Nagpur 12; Khyam Films v. Bank of Bahawalpur 1982 CLC 1275; T.S. Swaminath, Odayar v. Official Receiver of West Tanjore AIR 1957 SC 577; Parvati Amma v. Makki Amma AIR 1962 Kerala 85; Shahebzada Mahomed Kazir Shah v. R.S. Hills (1907) 35 Cal. 388; Noor Rehman v. Muhammad Yousuf 2000 CLC 1138 and Dr. Miss Gulshan Naheed v. The N.-W.F.P. 1989 CLC 1301 ref.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
----Arts. 70 & 72---Oral evidence contrary to admitted documentary evidence---Effect---Oral evidence could not displace admitted documentary evidence.
 
(c) Partition Act (IV of 1893)---
 
----S. 2---Civil Procedure Code (V of 1908), O.XX, R.18---Suit for partition and recovery of mesne profits---Plaintiff enjoying rent of rear portion of property claimed mesne profit from defendant occupying front portion thereof---Validity---Each co-owner would continue to have right of ownership in each and every part of property, until a regular partition was made---Defendant in his right of a co-owner in property would be equally entitled to the benefit of its use also---Nothing on record to show as to what rent income was generated from property and whether same was shared by plaintiff with defendant---Plaintiff in such circumstances was not entitled to any mesne profits from defendant.
 
(d) Partition Act (IV of 1893)---
 
---S. 2--Civil Procedure Code (V of 1908), O.XX, R.18---Suit for partition---Owelty of partition concept of---Applicability---Defendant claiming right over more valuable portion of joint property in his occupation---Validity---Co-owners would have equal right in every part of property until a regular partition was effected---Merely because defendant was in occupation of front portion of property purporting to be of higher value would not give him right to more benefit than what was possessed by plaintiff---Concept of owelty was not applicable to such case.
 
Blacks Law Dictionary Revised Fourth Edition p.1258 ref.
 
Qazi Faiz Isa for Plaintiff.
 
Danish Shah for Defendants.
 
Date of hearing: 23rd December, 2005.
 
 
JUDGMENT
 
Case 30
 
2006 C L C 415
 
[Karachi]
 
Before Mushir Alam, J
 
STATE LIFE INSURANCE CORPORATION OF PAKISTAN----Petitioner
 
Versus
 
HUSSAIN MUMTAZ----Respondent
 
Execution Nos.55 of 1997, 50 of 1985, 20 of 1991, 86 of 1987, 65 of 1986, 45 of 1985 and 93 of 1991, decided on 9th August, 2005.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 73 & O. XXXIV, R.13---Proceeds of execution sale---Distribution---Principle---On sale of mortgaged or charged property, foremost amount that can be appropriated before settling any other claim is towards payment of all expenses incidental to the sale of properly incurred in any attempted sale---Such claims include Nazir's Fee, expenses incurred in inviting bids of sealed tender, publication of sale proclamation or handbills, expenses incurred in protecting and preserving the property including Chowkidar's salary, or charges for security guards, if any, payment of rental or lease money, if any--Second head of account is towards payment of all interest due on account of mortgage in consequence whereof the sale was directed and of the cost of the suit in which the decree directing the sale was made---Followed by payment towards the principal due on account of mortgage in consequence whereof the sale was directed is third in order of priority--Fourthly in discharge of interest and principal amount due on subsequent mortgage or encumbrance, if any, in case there are more than one such persons then to such persons according to their respective interests therein in sequence of priority of mortgage or encumbrances.
 
(b) Civil Procedure Code (V of 1908)---
 
---S. 73--Expression `Government'---Meaning---Recovery of Government dues on execution sale---Principle---Statutory claim for recovery of tax, surcharge, penalty or dues have precedence over priorities amongst secured creditors like mortgagee as set out under S.73 C.P.C.---Right of Government dues is over all other claims---Word `Government' as used in S.73 (2) C.P.C., in the context appears to include local or other authorities as are by law empowered to impose or levy any tax, cess, charge or dues.
 
(c) Civil Procedure Code (V of 1908)---
 
----S. 73 & O.XXXIV, R.13---Karachi Port Trust Act (VI of 1886), S.46---Proceeds of execution sale---Distribution---Dispute was among different decree-holders with respect to distribution of sale proceeds of the property owned by judgment-debtor---Karachi Port Trust contended that it had the preferential right over the others, under S.46 of Karachi Port Trust Act, 1886---Validity---Karachi Port Trust had priority over mortgage decree holder, as such right had been conferred on them in supersession of the right of such mortgage under Karachi Port Trust Act, 1886, as well as under covenant contained in registered lease, to which mortgagee had notice.
 
(d) Civil Procedure Code (V of 1908)---
 
----S. 73 & O.XXXIV, R.13---Companies Ordinance (XLVII of 1984), S.405---Transfer of Property Act (IV of 1882), S.57---Proceeds of execution sale---Distribution---Dispute was among different decree-holders with respect to distribution of sale proceeds of the property owned by judgment-debtor---Employees union contended that it had preferential right over the others, under the provisions of S.405 of Companies Ordinance, 1984-Validity-Order of priorities as set down in S.405 of Companies Ordinance, 1984, was only applicable in cases where the amount realized was a result of winding up of the company---Where assets and property of a company were sold in a mortgage suit or against a money claim then priority was determined in accordance with O.XXXIV, R.13 C.P.C., S.73 C.P.C. and S.57 of Transfer of Property Act, 1882, as the case might be---Property of judgment-debtor, in the present case, was sold in mortgage suit and not as a result of winding up proceedings---Priority as claimed by employees union, under S.405 of Companies Ordinance, 1984, was not attracted in circumstances.
 
(e) Civil Procedure Code (V of 1908)---
 
----S. 73 & O.XXXIV, R.13---Sindh Chief Court Rules (O.S.), R.323---Proceeds of execution sale---Distribution---Dispute was among different decree-holders with respect to distribution of sale proceeds of the property owned by judgment-debtor---Validity---Only those decree holders were entitled to claim share in the proceeds of execution of sale, who had prior to the sale of the property, applied to the Court, which passed decree ordering such sale for execution of such' decrees and had not obtained satisfaction thereof---Incumbrancer, not party to suit might, at any time before the sale, apply to the Court, seized of the property to be sold, to be made a party or for the leave to join the sale---Court on such application, would pass an order as might be appropriate in protection of his rights and as to cost---Condition to approach the Court prior to sale might also be not attracted in case of statutory or governmental liability that was charge on the property---Sequential order of priority amongst various claimants could be set down as (a) all expenses incidental to the sale and preservation of mortgage property, (b) payment of all interest due on account of mortgage and of the cost of the suit in which the decree directing the sale was made, (c) principal due on account of the mortgage in consequence whereof the sale was directed, (d) interest on subsequent mortgage (e) principal amount due on subsequent mortgage or encumbrance according to respective interests therein in sequence of priority of mortgage or encumbrances, (f) residue, if any, amongst holders of money decree followed by (g) unsecured creditors and leftover, if any to the (h) judgment-debtor---Execution application was disposed of accordingly.
 
I.D.B.P. v. Maida (Pvt.) Ltd. 1994 SCMR 2248; Abu Miyan v. Abdul Ghani PLD 1974 Kar. 39; Habib Bank Ltd. v. Rudolf Donhi (1999) 80 Tax 99, Shanti v. K.T.C. 2000 CLC 595 rel.
 
Kazim Hassan, Muhammad Arif Khan, Asim Mansoor and Shoa- un-Nabi.
 
 
ORDER
 
Case 31
 
2006 C L C 430
 
[Karachi]
 
Before Mushir Alam and Syed Zawwar Hussain Jafery, JJ
 
Mrs. SHABEENA FARHAT----Appellant
 
Versus
 
HIGHWAY HOUSING PROJECT and 2 others----Respondents
 
H.C.A. No.241 of 2004, decided on 14th December, 2005.
 
Specific Relief Act (I of 1877)---
 
----Ss. 12---Limitation Act (IX of 1908), Art.113---Civil Procedure Code (V of 1908), O.VII, R.11---Suit for specific performance of agreement to sell---Limitation---Rejection of plaint---Valid agreement to sell---Prerequisites---Plaintiff did not file any agreement to sell executed between the parties and had only relied upon the receipts of instalment and acknowledgement by vendors---Grievance of plaintiff was that she had made full payment but vendors refused to execute sale-deed in her favour---Plaint was rejected by High Court, being barred by limitation---Validity---Not always necessary that contract was in conventional written form to constitute a valid agreement enforceable under law---Necessary requirement was that there must be an offer and acceptance by and between persons competent to enter into contract---Even oral contract, if proved, could be enforced---Receipt, containing an offer and acceptance was as good a contract as any other form of written contract---Receipts and acknowledgment filed in suit, prima facie, contained all necessary ingredients that constituted agreement to sell enforceable under law---Limitation to seek specific performance of contract was governed under two eventualities as contemplated by Art.113 of Limitation Act, 1908, that could set the limitation rolling in cases of specific performance of contract, one where time was essence of the contract and was fixed, secondly where no time was fixed for the. performance of the contract--Limitation of three years would commence from the date fixed in the agreement under first part of Art.113 of Limitation Act, 1908---Where no date was specified, then limitation of three years would start rolling from the date when the plaintiff had notice of refusal by the vendor---Limitation, in cases of such nature, was to be liberally construed without causing any injury to the intention of legislature, it must be in aid to advance cause of justice and to curb mischief---Plaintiff did not have any notice of refusal by vendors and there was no reason for the refusal as entire sale consideration was apparently received---Order passed by High Court was set aside---High Court appeal was allowed in circumstances.
 
Habibullah Khan v. Muhammad Ishaq PLD 1966 SC 505 and Subanullah v. Maryam 1988 CLC 890 rel.
 
Badar Alam for Appellant.
 
Muhammad Sharif for Respondents.
 
 
ORDER
 
Case 32
 
2006 C L C 440
 
[Karachi]
 
Before Nadeem Azhar Siddiqi, J
 
FARRUKH SAEED KHAN----Plaintiff
 
Versus
 
ANIS-UR-REHMAN BHATTI----Defendant
 
Civil Suit No.1062 of 1996, decided on 9th December, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----Ss. 42 & 54---Defamation---Suit for declaration, injunction and damages---Contention of the defendant was that suit was not maintainable as the prayer clause in the plaint was in the nature of negative declaration---Validity---Prayer clause in the plaint contained other prayers also and if one prayer was not admissible the suit, as a whole could not be dismissed---Prayer clause, which was an independent clause and subject to its proof, could be granted independent of the declaration.
 
Abdur Rehman Mobashir and 3 others v. Syed Amir Ali Shah Bukhari and 4 others PLD 1978 Lah. 113 ref.
 
(b) Civil Procedure Code (V of 1908)---
 
---O. VI, Rr.1 & 2---Pleadings---Party, who had filed written statement and refused to appear in the witness-box, the contents of his written statement ought to be ignored---Written statement filed by the party, who failed to appear in the witness-box is of no value.
 
Messrs Shalimar Ltd. Karachi v. Raisuddin Siddiqui and 3 others 1979 CLC 338; Messrs Society Oil Dealers, Karachi v. District Judge, Karachi and another 2003 MLD 2005; Saeedur Rehman and others v. Assistant Commissioner/Collector Acquisition, Swabi 2004 CLC 378 and State Life Insurance Corporation v. Mamoor Khan 1993 CLC 790 ref.
 
(c) Civil Procedure Code (V of 1908)---
 
----O. VI, Rr.1 & 2---Allegation of embezzlement against defendant in the plaint---Burden of proof---Scope---Plaintiff could produce evidence in the shape of documents to show the embezzlement etc.---Where the pleadings and the evidence were silent with regard to action instituted against the defendant for causing embezzlement, burden to prove the issue of embezzlement would be on the plaintiff---If the plaintiff failed to prove the issue, the same would be decided in negative---Defendant, in the present case, though had not produced any evidence in that regard but the matter was to be decided on the strength of the case of the plaintiff and not on the basis of the weakness of defendant.
 
(d) Civil Procedure Code (V of 1908)---
 
----O. VI, Rr.1 & 2---Defendant though had filed written statement, but neither cross-examined the plaintiff and his witness nor produced his evidence in rebuttal---Written statement filed by the defendant, in circumstances, was of no use.
 
(e) Defamation---
 
---Suit for damages---Burden of proof---If the evidence of the plaintiff had gone un-rebutted, there was no other option but to accept the same as true---Falsity would be presumed regarding the words used till it was proved that they were not false---Principles.
 
American Life Insurance v. M.S. Khawaja PLD 1960 (W.P.) Kar. 568 ref.
 
(f) Defamation---
 
----Slander---Suit for damages---Slander is defamation by words or in some transitory or fugitive form---Slander is actionable where the matter is calculated to disparage the plaintiff in regard to his office, profession, etc. without proof of special damage.
 
(g) Damages---
 
----General damages---Assessment---Principles.
(h) Defamation---
 
----Libel---Suit for damages---Assessment of general damages---Principles.
American Life Insurance v. M.S. Khawaja PLD 1960 (W.P.) Kar. 568; Sir Edward Senlson, K.B.E. and Secretary to the Government of Pakistan, Ministry of Law v. The Judges of the High Court of West Pakistan, Lahore and others PLD 1961 SC 237; Mrs. Zahra Zaidi v. M. Anwar Khan Ghauri 2004 CLC 223; Altaf Gauhar v. Wajid Shamsul Hasan and another PLD 1981 Kar. 515; Abdul Qadir v. S.K. Abbas Hussain and 2 others PLD 1997 Kar. 566 and Sufi Muhammad Ishaque v. The Metropolitan Corporation Lahore through Mayor PLD 1996 SC 737 ref.
 
(i) Constitution of Pakistan (1973)---
 
----Art. 14---Defamation---Suit for damages and injunction---Assessment of fair compensation---Factors to be kept in view---Discretion of Court---Scope---Held, usually it was difficult to assess fair compensation and in those circumstances it was the discretion of the Judge who might, on the facts of the case, determine the amount to be awarded to a person who suffered such a damage---Other factor was that conscience of the Court should be satisfied that the damage awarded, would, if not completely, satisfactorily compensate the aggrieved party---Article 14 of the Constitution provided that dignity of man was inviolable and it was legitimate right of plaintiff to defend his good name and the defendant had no right to defame him---Where the evidence available on record showed that the defendant had caused defamation, mental agony and physical discomfort to the plaintiff and defamed him in his business circle, by damaging the good name of the plaintiff the defendant exposed himself to the consequences---Plaintiff having proved that the defendant had defamed him in the family and in his business circle, he was liable to compensate the plaintiff and the plaintiff was entitled to general damages and relief of permanent injunction to the extent that the defendant had no right to damage the reputation of the plaintiff in public in general and in the circle of plaintiff's friends and relations in particular---Relief that defendant may be restrained from claiming anything in the shape and kind could not be granted and the defendant had every right to recover legal dues if he could prove the same, before a competent legal forum.
 
American Life Insurance v. M.S. Khawaja PLD 1960 (W.P.) Kar. 568; Sir Edward Senlson, K.B.E. and Secretary to the Government of Pakistan, Ministry of Law v. The Judges of the High Court of West Pakistan, Lahore and others PLD 1961 SC 237; Mrs. Zahra Zaidi v. M. Anwar Khan Ghauri 2004 CLC 223; Altaf Gauhar v. Wajid Shamsul Hasan and another PLD 1981 Kar. 515; Abdul Qadir v. S.K. Abbas Hussain and 2 others PLD 1997 Kar. 566 and Safi Muhammad Ishaque v. The Metropolitan Corporation Lahore through Mayor PLD 1996 SC 737 ref.
 
Mahmood A. H. Baloch for Plaintiff.
 
M. Zafar Iqbal for Defendant.
 
Date of hearing: 1st November, 2005.
 
 
JUDGMENT
 
Case 33
2006 C L C 454
 
[Karachi]
 
Before Mushir Alam and Syed Zawwar Hussain Jafery, JJ
 
ABDUL WAHID----Petitioner
 
Versus
 
PROVINCIAL ELECTION COMMISSIONER and others----Respondents
 
C.P. No.D-1314 of 2005, decided on 30th December, 2005.
 
Sindh Local Government Elections Rules, 2005---
 
----Rr. 35, 36, 37 & 38---Constitution of Pakistan (1973), Art.199---Constitutional petition---Tabulation of result by Returning Officer---Error, correction of---While tabulating and preparing consolidation of votes count in Forms XV and XVI, the Returning Officer had mistakenly noted 28 votes against the symbol of respondents who had actually secured 224 votes, which count was erroneously shown against the symbol of petitioner candidate---Such error crept in the Forms XV, and XVI which was corrected by Returning Officer and respondents were declared as returned candidates---Plea raised by petitioner was that Returning Officer could not revise the result---Validity---Petitioner could not be allowed to take advantage of bona fide error committed by Returning Officer, who noted incorrect count against the symbol of respondents---Petitioner had not filed copy of Form XIII, that contained the original vote count of each polling station---If Form XIII, would have been filed, the same could have exposed the fallacy of the claim of petitioner---Copy of vote counts of each polling station contained in Form XIII, was placed on record by Returning Officer, which was not questioned by petitioner nor he doubted the veracity of vote counts contained therein---Form XIII was the primary document on which consolidated vote count in Forms XV and XVI was dependent---Even the notification declaring the respondents as successful candidates had been issued---Typographical error could be corrected by Returning Officer, such act was in furtherance to hold free and impartial election as mandated under Sindh Local Government Election Rule, 2005---Another unsuccessful candidate had already challenged the election results, as revised by the Returning Officer and that election petition was pending adjudication---High Court in exercise of constitutional jurisdiction, declined to exercise discretion---No person could be made to suffer on account of official acts done in good faith and constitutional jurisdiction of High Court could not be invoked in aid of injustice---Petition was dismissed in circumstances.
 
Muhammad Hands and others v. Election Commission of Pakistan and others C.P. No.116 of 2005 distinguished.
 
Abdul Waheed Zaman Qureshi v. The Election Authority 1999 CLC 112 rel.
 
Ziaul Haq Makhdoom and Shakeel Ahmed for Petitioner.
 
Ahmed Pirzada, Addl. A.-G.
 
Miss Saify Ali Khan for Respondents Nos.3 and 4.
 
Mrs. Sabra Qaiser, Advocate/Intervenor in person.
 
Date of hearing: 12th October, 2005.
 
 
JUDGMENT
 
Case 34
 
2006 C L C 466
 
[Karachi]
 
Before Anwar Zaheer Jamali and Mrs. Yasmin Abbasey, JJ
 
GHULAM RASOOL LASHARI and 32 others----Petitioners
 
Versus
 
GOVERNMENT OF SINDH through The Secretary, Ministry of Agriculture, Karachi and 2 others----Respondents
 
C.Ps. Nos.392, 82, 1182, 1188, 1250, 1288, 1306, 1416, 1953 and Miscellaneous No.942 of 2002, 475 of 2003 and D-82 of 2004, decided on 20th December, 2005.
 
(a) Maxim---
 
----Audi alteram partem---Applicability---Party guilty of fraud, manipulation or malpractices---Such party cannot be allowed to avail benefit of principles of administration of justice for protection of ill-gotten gains---Application of principle of audi alteram partem or otherwise entirely depends upon careful examination of facts and circumstances of each case---Unless it is found that petitioners have approached the Court with clean hands and are not guilty of any such fraud or mal-practices, no benefit of principle of audi alteram partem can be extended to them.
 
Mst. Noor Jahan v. Government of Sindh 2000 CLC 1005; Abdul Haq and others v. Province of Sindh and others PLD 2000 Kar. 224 and Abdul Haq Indhar and others v. Province of Sindh 2000 SCMR 907 rel.
 
(b) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Publication of news item---Effect---Mere publication of some news item does not furnish any valid cause for a person to invoke extraordinary jurisdiction of High Court under Art.199 of the Constitution, unless substantiated by any further action against the petitioner.
 
(c) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Qabza malia---Factual controversy---Grievance of petitioners was that they were allottees in possession of shops in New Sabzi Mandi and authorities on the allegations of fraudulent and manipulated allotment of shops intended to dispossess them---Such grievance of petitioners was based upon a news item---Validity---Constitutional jurisdiction of High Court under Art.199 of the Constitution was meant to ensure/foster proper dispensation of justice and not to patronize `Qabza mafia' or the parties for protection of their illegal business---Dispute agitated by the petitioners having a long chequered history could not be resolved without detailed investigation into the factual controversies emerging from the divergent stands taken by the parties---High Court directed the authorities to act strictly in accordance with law, in case they intended to take any action against petitioners---Petition was dismissed with such directions.
 
Mrs. Anisa Rehman v. PIAC and another 1994 SCMR 2232 and Hazara (Hill Tract) Improvement Trust v. Mst. Qaisra Elahi and others 2005 SCMR 678 ref.
 
Muhammad Javed and others v. Officer Incharge, Market Committee Government of Sindh, Karachi and another 2000 SCMR 1615 fol.
 
Wali Muhammad and others v. Sakhi Muhammad and others PLD 1974 SC 107; Khiali Khan v. Haji Nazir and 4 others PLD 1997 SC 304 and Abdul Haq Indhar and others v. Province of Sindh 2000 SCMR 907 rel.
 
Abdul Mujeeb Pirzada.
 
Muhammad Saleem Sammo.
 
S. Khalid Shah.
 
Ahmed Pirzada, Addl. A.-G., Sindh.
 
ORDER
 
Case 35
 
2006 C L C 482
 
[Karachi]
 
Before Faisal Arab, J
 
Messrs KASHMIRIAN PVT. LTD. through Shomaila Loan Marker and 6 others----Plaintiffs
 
Versus
 
GHULAM NABI GUJJAR and another----Defendants
 
Suit No.1136 of 2002, decided on 25th January, 2006.
 
(a) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 129(g)---Non-production/withholding of best evidence by a party without showing any plausible reason---Effect---Presumption would be that had such evidence been produced, same would have gone against such party---Non-appearance of a party as his own witness in support of his case would make his claim highly doubtful---Principles.
 
Sughran Bibi v. Mst. Aziz Begum 1996 SCMR 137 rel.
 
(b) Specific Relief Act (I of 1877)---
 
----Ss. 12 & 42---Civil Procedure Code (V of 1908), S.2(12)---Limitation Act (IX of 1908), Art.109---Suit of possession, declaration and recovery of mesne profits---Dispute as to ownership of flat in an apartment built by a builder---Plaintiff claimed purchase of suit flat from its builder, while defendant claimed its purchase from one' "N"---Defendant neither appeared as his own witness nor examined "N", rather examined his son/attorney, who produced sale agreement in favour of "N'I and general power of attorney executed by "N" in favour of the defendant---Failure of plaintiff to prove mesne profits at claimed rate---Admission of defendant's witness regarding current rate of rent of suit flat to be between Rs.5,000 to 5,500---Validity---Such documents did not disclose from whom executants thereof had derived title to suit flat---No buyer would derive a better title than what his seller possessed---Transfer of title to suit flat in favour of defendant by its' builder or a person who derived title from builder had not been proved---Valid title to suit flat in favour of "N" had not been established, thus, defendant could not derive a valid/lawful title from "N"---Defendant, at the time of alleged purchase from "N.", had neither asked for allotment documents issued by builder nor sought confirmation of allotment from builder nor even invited objections from public---Defendant could claim back amount paid to "N", but could not displace plaintiff's right to claim ownership of suit flat---Witness of builder was not asked during cross-examination that suit flat had not been allotted to plaintiff---Non-appearance of defendant as his own witness had made his claim highly doubtful---Plaintiff's suit was decreed with direction to defendant to hand over possession of suit flat within specified time and pay mesne profit @ Rs.5,500 per month for three years prior to filing of suit till delivery of possession and with direction to builder to execute sub-lease in favour of plaintiff within specified time, otherwise same would be executed by Nazir of the Court.
 
Sughran Bibi v. Mst. Aziz Begum 1996 SCMR 137 and 1991 SCMR 2063 rel.
 
(c) Limitation Act (IX of 1908)---
 
----S. 28 [as omitted by Limitation (Amendment) Act (II of 1995)] & Art.142 [as omitted by Limitation (Amendment) Act (II of 1995)]---Suit for possession of immovable property---Dispossession or discontinuance of possession in year 1994, but filing of suit in year 2002--Maintainability-Section 28 of Limitation Act, 1908, after having been declared to be repugnant to Injunctions of Islam by Supreme Court, was omitted on 18-10-1995 through Limitation (Amendment) Act, 1995---After such omission, no such suit would be barred from the date of judgment of Supreme Court i.e. 31-8-1991---Suit was not barred by time.
 
(d) Civil Procedure Code (V of 1908)---
 
---S. 2(12)--Limitation Act (IX of 1908), Art.109---Mesne profits, claim for---Limitation---Such profits could be claimed only for three years prior to filing of suit.
 
Yawar Faruqui for Plaintiffs:
 
Sofia Saeed for Defendant No.1.
 
Aziz Malik for Defendant No.2.
 
Date of hearing: 22nd December, 2005.
 
 
JUDGMENT
 
Case 36

[Karachi]
 
Before Nadeem Azhar Siddiqi, J
 
Messrs FARM AND FOODS INTERNATIONAL through Attorney----Plaintiff
 
Versus
 
HAMID MAHMOOD----Defendant
 
Suit No.768 of 2000, decided on 17th January, 2006.
 
(a) Limitation Act (IX of 1908)---
 
---S. 19---Application of S.19, Limitation Act, 1908---Scope---Requirement of S.19, Limitation Act, 1908 was that an acknowledgment to be valid must relate to the time when the right was still enforceable and that the acknowledgment must be in writing---When plaintiff had not produced any writing by which the defendant had acknowledged the debt, S.19 was not applicable and plaintiff could not claim protection under S.19 of the Limitation Act, 1908.
 
(b) Limitation Act (IX of 1908)---
 
----S. 20---Scope of S.20 Limitation Act, 1908---Section 20 of the Act deals with effect of payment in account of debt or of interest on legacy---Explanation of S.20 provides that debt includes money payable under a decree of Court.
 
(c) Limitation Act (IX of 1908)---
 
----Art. 117---Civil Procedure Code (V of 1908), S.13---Suit for recovery of amount on the basis of foreign judgment---Limitation---Starting point---Principles.
 
Article 117 of the Limitation Act, '1908 provides that the suit upon a foreign judgment can be filed within six years from the date of the judgment. The starting point of limitation would be from the date of appellate judgment as the original judgment merged or superseded by the appellate judgment. The judgment capable of execution, which is conclusive, is the judgment of the Appellate Court. The starting point of limitation for filing suit under section 13, C.P.C. would be the date when the appellate judgment was passed and not the date on which the car of the partner of the defendant was attached and sold. For the purpose of Article 117 the limitation will begin to run from the appellate judgment. The payment recovered by attachment and sale of car cannot be considered as the same was due to coercive measure adopted by the Court and not the voluntary act of the defendant or his partner and that the same cannot be equated with acknowledgment in writing. Payment made by the debtor towards loan before the expiration of the period of limitation can give a fresh starting point to the period of limitation provided such payment is coupled with acknowledgment in the handwriting of or in the writing signed by the person making the payment. Admittedly, in the present case there was no such acknowledgment made by the defendant or his partner. The suit was, therefore, filed beyond the period prescribed and was barred by Article 117 of the Limitation Act.
 
Muhammad Suleman v. Habib Bank Limited 1987 MLD 2757 fol.
 
Baijnath Karnani v. Vallabhdas Damani AIR 1933 Mad. 511; Mian Nazeer Ahmad v. Abdur Rasheed Qureshi 1986 CLC 1309; Grosvenor Casino Ltd. v. Abdul Malik Badruddin 1997 SCMR 323; Emirates Bank Ltd. v. Messrs Oosman Brothers 1990 MLD 1779; Mst. Amir Begum v. Lt.-Col. S. Mir Fateh Shah PLD 1968 Kar. 10 and Abdul Ghani v. Haji Saley Muhammad PLD 1960 (W.P.) Kar. 594 distinguished.
 
(d) Civil Procedure Code (V of 1908)---
 
----S. 13--Institution of suit on the basis of a foreign judgment---Requirement.
 
Section 13 of the C.P.C. gives right to the plaintiff to institute the suit in Pakistan on the basis of foreign judgment treating it as a cause of action. The suit can only be filed on the basis of such foreign judgment, which is conclusive between the parties and not falling within the exception of section 13 of C.P.C. In the present case, in the written statement legal pleas were taken but it was not stated that the judgment is covered by the exception of section 13, C.P.C. Under section 13, C.P.C. a foreign judgment is not enforceable per se but a suit on its basis has to be filed though it is conclusive with respect to a matter adjudicated upon between the parties subject to exception of section 13 of C.P.C. For filing a suit under section 13, C.P.C. the existence of a decree is essential as the basis of the action and that has to be one that is final and conclusive between the parties so as to operate as res judicata. Suit can be filed in Pakistan on the basis of foreign judgment treating it as the cause of action if the conditions prescribed in section 13, C.P.C. are fulfilled. The judgment is conclusive between the parties otherwise it is res judicata between them and the Courts in Pakistan are bound by its findings.
 
Abdul Latif A. Shakoor for Plaintiff.
 
Shafaat Hussain for Defendant.
 
Dates of hearing: 28th October and 15th December, 2005.
 
 
JUDGMENT
 
Case 37
 
2006 C L C 504
 
[Karachi]
 
Before Sabihuddin Ahmad and Khilji Arif Hussain, JJ
 
RASHEED ABDUL AZIZ-AL-HUSSAN through Attorney----Petitioner
 
Versus
 
KARACHI DEVELOPMENT AUTHORITY through Director-General, K.D.A. and 2 others----Respondents
 
Constitution Petition No.D-1195 of 1995, decided on 29th September, 2004.
 
Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Allotment of plot to the petitioner, on the basis of direction issued by the Chief Minister of the Province, for establishment of a school, possession of which was delivered to petitioner in 1992-Petitioner, according to the terms of the allotment, was required to complete the construction of building within two years from the date of possession and thereafter a lease was required to be executed in his favour---Construction on the plot could not be completed within the given time and thereafter in 1995 the allotment was cancelled on the ground that petitioner had violated certain terms of allotment---Validity---Held, order of cancellation impugned in the petition did not speak of absence of authority by the Development Authority to effect the allotment in petitioner's favour or mala fides in passing the allotment order---Order of cancellation only referred to violation of certain conditions of allotment and in all fairness violation of those conditions would not automatically entail cancellation---Petitioner was entitled to show whether the violations had occurred for reasons beyond his control or otherwise and the Authority was expected to exercise its discretion fairly and honestly in determining whether cancellation or extension of time was appropriate in the circumstances---Questions whether the plot was actually available for transfer to the petitioner or whether the allotment was otherwise bona fide, were those of fact which could also be best determined by the competent authority---High Court in circumstances allowed the constitutional petition to the extent that the impugned order was set aside and the matter would be decided afresh by appropriate officer in the Development Authority within specified time and till such time petitioner was directed not to raise any construction on the plot in question.
 
Noor Muhammad v. K.D.A. PLD 1975 Kar. 373 ref.
 
Muhammad Asharaff Kazi for Petitioner.
 
Syed Jameel Ahmad for Respondent No.1.
 
Miss Rizwana Ismail for Respondent No.2.
 
Date of hearing: 29th September, 2004.
 
 
JUDGMENT
 
Case 38

2006 C L C 511
 
[Karachi]
 
Before Ata-ur-Rehman and S. Ali Aslam Jafri, JJ
 
ABDUL QUDOOS----Petitioner
 
Versus
 
CITY DISTRICT GOVERNMENT and others----Respondents
 
C.P. No.D-1057 of 2004, decided on 29th April, 2005.
 
Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Withdrawal of approval of building plan of petitioner by the Building Authority---Respondents, who were utilizing the plot owned by the petitioner as passage had raised objections to the construction on the, plot of petitioner on the ground that they had no other passage to utilize for coming on the road which was enjoyed by the Katchi Abadi where the respondents were living---Respondents, first restrained the petitioner from raising construction and subsequently Building Authority withdrew the approved plan---Validity---Held, petitioner being owner of the plot was entitled to enjoy all rights as per metes and bounds thereof and was authorized to raise construction thereon, according to law---Petitioner was not obliged to provide any passage or space for the occupants of the plot which were effected by the Katchi Abadi; in fact it was responsibility of the Authorities to see that the Katchi Abadi was removed and the respondents and others like them were provided safe and comfortable passage---No plausible reason was available with the Authorities for taking any action against the construction being raised as per approved plan by the petitioner---High Court directed that fresh application for approval of plan of construction by the petitioner be examined and approved strictly in accordance with law by the Building Authority within specified period and no fresh cost was to be paid by the petitioner for the rectification as it was no fault on his part as the approved plan was cancelled illegally.
 
Akhtar Hussain, Anwer Ali Shah, Muhammad Safdar and Ahmed Pirzada, Addl. A.-G.
 
 
ORDER
 
Case 39
 
2006 C L C 524
 
[Karachi]
 
Before Muhammad Moosa K. Leghari, J
 
RAFIQUE AHMED----Petitioner
 
Versus
 
ANWAR ALI and 2 others----Respondents
 
Constitutional Petitions Nos.S-295 and S-296 of 2004, decided on 1st September, 2005.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
---Ss. 15(2)(ii) & 16---Constitution of Pakistan (1973), Art.199---Constitutional petition-Ejectment of tenant on ground of default in payment of rent---Non-compliance of tentative rent order---Striking off defence---Defence of tenant was struck off on sole ground that he had failed to comply with tentative rent order as he had not deposited rent for the month of July, 2002 on 10th of August, 2002 and instead he had deposited rent for the month of July and August, 2002 on 6-9-2002--Rent for the month of August 2002, in circumstances, though was deposited within due date, but rent for the month of July, 2002 was not deposited within the period specified by law---Inadvertent error, partly was on the part of office of Rent Controller and partly on the part of tenant which resulted in confusion---Merely because tenant on account of some innocent error or sheer inadvertence had failed to deposit rent for one month within stipulated time, would not be a just ground for striking off his defence---Penal provisions were to be construed very strictly as law favours adjudication on merits---Case was fit to invoke constitutional jurisdiction of High Court---High Court, allowing constitutional petition, set aside impugned orders and remanded case to Rent Controller to decide afresh expeditiously in accordance with law.
 
Hussain Bux v. Haji Yaqoob and another 1990 SCMR 1354 ref.
 
Abdul Hafeez Ghouri for Petitioner.
 
Saeeduddin Siddiqui for Respondent No.1.
 
 
ORDER
 
Case 40
 
2006 C L C 578
 
[Karachi]
 
Before Anwar Zaheer Jamali and Muhammad Ather Saeed, JJ
 
KARACHI PLAY HOUSE----Appellant
 
Versus
 
CITY DISTRICT GOVERNMENT----Respondent
 
H.C.A. No.21 of 2004, decided on 7th February, 2006.
 
(a) Administration of justice---
 
----Act of Court---Effect---No party should be made to suffer due to any mistake or act or omission of Court.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. I, R.10(2)---Appeal---Proper party, joining of---Public interest litigation---Intervener, in public interest, assailed status of plot of appellants over which they were raising construction---Grievance of intervener was that the appellants had changed the use of disputed plot for which separate proceedings were being carried out by her against them---Plea raised by the appellants was that the intervener was not a necessary party to be joined in appeal---Validity---When intervener was resisting raising of construction over plot in dispute, till the issue of change of use of the plot was resolved by government, intervener was justified in approaching Court to be joined as party to appeal---Intervener might not be a necessary party to the suit but was a proper party whose presence would enable and help the Court to adjudicate relevant questions completely, effectively and in more comprehensive manner---Intervener was arrayed as respondent in appeal---Application was allowed in circumstances.
 
Hussain v. Mansoor Ali and 5 others PLD 1977 Kar. 8; A. Razzak Adamjee and another v. Messrs Datari Construction Company (Pvt.) Limited and another 2005 SCMR 142 and Altaf Parekh v. Delments Construction Company 1992 CLC 700 ref.
 
Uzin Export Import Enterprises for Foreign Trade Karachi v. Union Bank of Middle East Ltd. Karachi and another PLD 1994 SC 95 and Pakistan Banking Council and another v. Ali Mohtaram Naqvi and others 1985 SCMR 714 fol.
 
Mushtaq A. Memon for Appellant.
 
Manzoor Ahmed for the Respondents Nos.1 and 2.
 
Ms. Rizwana Ismail for Applicant/Intervenor.
 
ORDER
 
Case 41
 
2006 C L C 597
 
[Karachi]
 
Before Faisal Arab, J
 
ABN AMRO BANK N.V.----Plaintiff
 
Versus
 
CHAIRMAN/MANAGING DIRECTOR, KARACHI WATER AND SEWERAGE BOARD----Defendant
 
Suit No.658 of 2001, decided on 7th February, 2006.
 
(a) Karachi Water and Sewerage Board Act (X of 1996)-
 
----S. 7(ii)---Charges and fee for water supply and sewerage services, levy and recovery of---Scope---Such charges and fee are levied not as tax, but for supply and services required by Board to be provided to its subscriber---In absence of supply or service, no applicable charges/fee could be billed to subscriber.
 
(b) Karachi Water and Sewerage Board Act (X of 1996)-
 
----S. 7(x)---Function of Karachi Water and Sewerage Board to regulate, control and inspect water connections, sewer/service lines an internal fittings---Object and scope stated.
 
Section 7(x) of Karachi Water and Sewerage Board Act, 1996 describes one of the most important functions of the Board i.e. the function of regulating, controlling and inspecting water connections, sewer and service lines and internal fittings. The object of entrusting the Board with such functions is to ensure that its supply and services are adequately regulated, supervised and distributed. Proper regulation and distribution enables the Board to (a) detect theft of water supply, (b) supply water to different areas as per the schedules of supply, (c) effective disposal of sewerage and (d) address genuine complaints with regard to defective or deficient supply and services.
 
(c) Karachi Water and Sewerage Board Act (X of 1996)-
 
----S. 7(x)---Non-supply of water or services to consumer---Remedy of consumer---Duty of Board to redress its consumer's grievance---Principles.
 
A consumer, who has been provided water connection, but there is no supply, has to approach the Board with a complaint, so that Board can take requisite remedial measures. It is only when a complaint is made that Board is required to take appropriate remedial steps or to demonstrate to the consumer that there was no cause of complaint at all, and the supply and services are adequate. Therefore, whenever a complaint is lodged, the Board has to act and take necessary steps to address it. The Board cannot close its eyes to the complaint on the one hand and continue billing the consumer on the other irrespective of the fact whether there is no supply or service being provided. A public institution entrusted with the function of providing basic amenity such as water has to act with necessary dispatch whenever a consumer lodges a complaint. The Board has to inspect the water connections, if there is a complaint that there is no water supply and restore the supply. These inspections become all the more necessary where there is no metered supply and the consumers are charged in lump sum for the entire year of supply.
 
Whenever a new connection is provided, it is in the interest of Board itself to inform the consumer of the date of commencement of supply. This enables the Board to start billing the consumer from such date. Whenever-there is a complaint, the Board must act on it. It is about time that Government departments and agencies get rid of the lethargy and inaction and serve for which they charge the public. With high rate of unemployment and millions jobless youth qualified enough to efficiently serve, there is no room for inefficient Government employees, whose only object is to occupy secured jobs and seldom do what is required of them.
 
(d) Karachi Water and Sewerage Board Act (X of 1996)-
 
----Ss. 7 & 8---Demand of charges by Board for disputed period---Non? filing of complaint by consumer at relevant time as to non-supply of water during disputed period---Filing of complaint after such demand raised by Board, but non-holding of joint inspection of water connection by Board to demonstrate to consumer supply of water through pipeline---Validity---In absence of such complaint at relevant time, consumer would be liable to clear the bill for water supply for disputed period---Failure to carry out such inspection would disentitle Board from billing consumer for water charges, and loss so occasioned would be the personal liability of its concerned officials---Consumer would become liable to make payment towards water charges after restoration of supply---Principles.
 
Nizar Ali v. Karachi Water and Sewerage Board 2004 CLC 578 and Seven-up Bottling Co. v. L.D.A. 2003 CLC 513 rel.
 
Khalid Shah for Plaintiff.
 
Abdul Karim Khan for Defendant.
 
Date of hearing: 23rd December, 2005.
 
JUDGMENT
 
Case 42
2006 C L C 611
 
[Karachi]
 
Before Gulzar Ahmed, J
 
MEHMOOD RANGOONWALA---Plaintiff
 
Versus
 
GOVERNMENT OF SINDH and others----Respondents
 
Suit No.273 of 2004, decided on 17th January, 2006.
 
(a) Specific Relief Act (I of 1877)--
 
---Ss. 8 & 12--Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance (III of 2001), Ss.3 & 4---Sindh Goth Abad (Housing Scheme) Ordinance (IV of 1987), S.3---Civil Procedure Code (V of 1908), O.III, R.2 & O.VII, R.1h-Transfer of Property Act (IV of 1882), S.54--Suit for specific performance and possession by general attorney of allottees--Allotment of 16 acres land in favour of 50 allottees under Sindh Goth Abad (Housing Scheme) Ordinance, 1987---Cancellation of such allotment and offering of land to allottees on payment of differential value as worked out by Committee appointed under Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001-Non-issuance of challan of such differential value by authority-Such suit by agent in his own name---Maintainability---Sindh Goth Abad (Housing Scheme) Ordinance, 1987 would apply to rural areas, while Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001 would apply to urban areas of the province--- Sindh Urban State Land (Cancellation of Allotments, Conversions and Exchanges) Ordinance, 2001 would not apply to land under Sindh Goth Abad (Housing Scheme) Ordinance, 1987---Allotment under Ordinance, 1987 to be made free of cost would not be in excess of two Ghuntas of land (approximately 220 sq. yds.)-Allotment of suit-land was, thus, contrary to Ordinance, 1987--Such offer made by authority through its letter could not be labeled as contract between parties, thus; on basis of such illegal letter, no relief could be granted--Plaint did not disclose as to how general attorney/plaintiff himself had acquired his own interest in suit-land from its allottees--Power of attorney itself was neither a document of transfer of property nor a document of conveyance nor even an agreement to sell land--Plaintiff had neither joined original allottees as plaintiffs in suit nor attached with plaint letter of allotment--Agent himself could not claim ownership right of his own in property of his Principal on basis of agency document---Plaintiff-agent had no cause of action to maintain such suit--Plaint was rejected under O.VII, R.11, C.P.C.
 
(b) Specific Relief Act (I of 1877)---
 
--S. 8---Civil Procedure Code (V of 1908), O.III, R.2---Transfer of Property Act (IV of 1882), S.54---Suit for possession by General Attorney in his own name---Maintainability---Power of attorney was a document of agency, in which donor was principal, while attorney an agent--Power of attorney itself was neither a document of transfer of property nor a document of conveyance nor even an agreement of selling property---Agent himself could not claim ownership right of his own in property of his principal merely on basis of agency document-Plaintiff ?agent could not maintain suit in his own name-Plaint was rejected under O.VII, R.11, C.P.C.
 
Khalil-ur-Rehman for Plaintiff.
 
Abbas Ali, A.A.-G. for Defendant No.1.
 
Shah Nawaz Awan for Defendant No.2.
 
ORDER
 
Case 43
 
2006 C L C 624
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
Dr. KARIM AHMED KHAWAJA----Appellant
 
Versus
 
RETURNING OFFICER FOR SENATE ELECTIONS, 2006 and another----Respondents
 
Election Appeal No.3 of 2006, decided on 20th February, 2006.
 
Constitution of Pakistan (1973)---
 
---Art. 59(1)(d)--Election on the technocrat and professional seat of the Senate--Required experience in the field---Practical experience during education---Nomination papers of the candidate for the seat of technocrat in Senate were rejected on the ground that he did not have the required experience of 20 years as a practising doctor---Plea raised by the candidate was that he regularly attended wards of hospitals from third year of M.B.,B.S. till final year and after passing the final examination he had been working in different hospitals and dispensaries etc.---Validity--Required experience was not always to be necessarily alter completion of education-An certain disciplines student's experience started during education also--Copy of Medium of Instruction and certificates issued by Principal and Chairman Academic Council of the Medical College, showed that clinical postings in different disciplines of medicines were the mandatory requirement for medical student of M.B.,B.S. programme--Such posting was nothing but practical performance in the field which amounted to be an experience--Since the candidate was holder of M.B.,B.S. degree, the natural inference would be that he had performed at the clinical postings since third year M.B.,B.S. course--Certificates issued by other institutions and organizations confirmed him to be practically in the medical field and his performance against different assignments-Evidence produced showed the candidate to have an experience in the medical field, which was more than 20 years---Requirement of 20 years' experience in the field, by the candidate was thus, satisfied---Order passed by Returning Officer was set aside and nomination papers of the candidate were accepted---Appeal was allowed accordingly.
 
Aijaz Khawaja and Samullah Soomro for Appellant.
 
Date of hearing: 20th February, 2006.
 
JUDGMENT
 
Case 44
 
2006 C L C 629
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
Syed MEHBOOB HUSSAIN----Petitioner
 
Versus
 
RAZA SHAH and 2 others----Respondents
 
C.P. No.714 of 2004, decided on 1st February, 2006.
 
(a) Sindh Rented Premises Ordinance (XVII of 1979)---
 
---S. 15--Constitution of Pakistan (1973), Art.199--Constitutional petition-Ejectment of tenant--Landlord and tenant, relationship of--Onus to prove---Both the Courts below concurrently dismissed ejectment application and appeal filed by the landlord, on the ground that there did not exist any relationship of landlord and tenant between the parties---Validity---Since petitioner claimed the respondent to be tenant, it was for the petitioner to establish relationship of landlord and tenant between him and the respondent---Petitioner produced oral evidence, which was denied by the respondent orally---No such evidence was produced which could prove entry of respondent in the premises as tenant or payment of rent by respondent at some latter stage-Courts below had rightly found that entry of respondent in disputed premises as tenant or his acknowledgement to the petitioner/owner as his landlord was not established through evidence---Relationship of tenant and landlord had not been established and the decisions of two Courts below did not call for interference by High Court in exercise of constitutional jurisdiction--Petition was dismissed in circumstances.
 
(b) Sindh Rented Premises Ordinance (XVII of 1979)---
 
---S. 2(h)--"Premises"--Connotation--Premises, which has not been let out on rent do not come within the purview of Sindh Rented Premises Ordinance, 1979---Occupant of such premises does not acquire status of tenant by implication of law---Merely for being the occupant without any legal claim, such person cannot become tenant of the owners in respect of the premises in his occupation--By recognizing such occupant as tenant all legal rights and protections given by law to tenant will stand automatically conferred upon him--Such is not the scheme of Sindh Rented Premises Ordinance, 1979.
 
(c) Sindh Rented Premises Ordinance (XVII of 1979)---
 
---S. 15---Ejectment of tenant---Landlord and tenant, relationship---Proof---Prerequisites--Such relationship is combination of three components namely premises, landlord and tenant--Unless such three components as defined in Sindh Rented Premises Ordinance, 1979, are present, there is no tenancy.
 
Muhammad Shabber and others v. Mst. Hamida Begum 1992 MLD 323 and Saifullah and others' case 2000 CLC 1841 ref.
 
Chaudhry Muhammad Iqbal for Petitioner.
 
Raja Muhammad Aslam Kiyani for Respondent No.1.
 
Date of hearing: 25th November, 2005.
 
JUDGMENT
 
Case 45
2006 C L C 640
 
[Karachi]
 
Before Faisal Arab, J
 
TAHIR HASSAN CHOUDHERY----Plaintiff
 
Versus
 
SHAHID AHMED KHAN-Defendant
 
Suit No.520 and C.M.A. No.5059 of 2005, decided on 21st December, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXVII, R.2-Suit for recovery of money on the basis of negotiable instrument---Grant of leave to defend suit---Object of O.XXXVIT, C.P.C.--No fair dispute existed for trial and in absence of a serious conflict, grant of leave to the defendant on the basis of untenable pleas would only facilitate defendant to prolong the litigation---Whole object of O.XXXVII, C.P.C. was to curtail defendant's ordinary right to raise a defence and seek full trial of the suit; defendant had to first establish that he was entitled to grant of leave to defend suit---Any defence, which was eyewash and intentionally fabricated just to avoid the consequence of a clear and admitted default committed on a negotiable instrument, could not be entertained in summary jurisdiction---Where there existed no fair dispute to be tried, defendant's leave to defend application was dismissed and contents of plaint were deemed to be admitted and suit was decreed accordingly.
 
Raja Muhammad Basharat for Plaintiff.
 
Ahmed Hassan Rana for Defendant.
 
Date of hearing: 9th December, 2005.
 
ORDER
 
Case 46
 
2006 C L C 679
 
[Karachi]
 
Before Khilji Arif Hussain, J
 
Messrs U.K. INTERNATIONAL PROPRIETORSHIP CONCERN through Sole Proprietor-Plaintiff
 
Versus
 
TRADING CORPORATION OF PAKISTAN---Defendant
 
Civil Suit No.2 and C.M.A. No.1116 of 2006, decided on 1st March, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
---O. XXXIX, Rr.1 & 2--Interlocutory injunction, grant of---Applicant cannot seek interlocutory injunction with regard to a matter which is not subject-matter of the suit.
 
Muhammad Jawed Iqbal v. Government of Pakistan 1974 SCMR 481 fol.
 
(b) General Clauses Act (X of 1897)---
 
----S. 24-A---Corporate body controlled by the Government has to act fairly in a transparent manner and its acts and deeds should not be tainted with malice and ulterior motives---Court can set aside any order passed by an organization or authority which, if established,. has been passed with ulterior motives and organization has not acted in a transparent manner or acted to benefit persons of their choice at the cost of government exchequer, but nonetheless burden lies upon the party who alleged malice---Organization controlled by government, has to place on record prima facie evidence showing that in discharging their duties dealing with "public money" they have acted fairly and in a transparent manner-Principles.
 
Zafar Ali Shah's case PLD 2000 SC 869 and Messrs Airport Support Services v. The Airport Manager 1998 SCMR 2268 fol.
 
Premier Mercantile Services (Pvt.) Ltd. v. Trustees of Port of Karachi 2003 MLD 1064; Rehim Khan v. Divisional Superintendent, Pakistan Railway 2003 YLR 63; Muhammad Iqbal v. Fatima Jinnah' Medical College 1989 MLD 423 and Balochistan Construction Co. v. Port Qasim Authority 2001 YLR 2716 distinguished.
 
(c) Contract Act (IX of 1872)---
 
---S. 230--Specific Relief Act (1 of 1877), S.12-Suit for specific performance of contract by agent in his own name on behalf of principal---Maintainability---Held, specific performance of the contract executed or entered into by agent on behalf of the principal cannot be enforced by the agent in his own name---Section 230, Contract Act, 1871 puts a bar on agent to personally enforce contract entered into by him on behalf of his principal.
 
(d) Civil Procedure Code (V of 1908)---
 
-- O. XXXIX, Rr.1 & 2---Interlocutory injunction, grant of-Irreparable loss to---Plaintiff, in the present case, had offered to supply goods at a specified rate whereas defendant had accepted offer of another party at a lower rate-Whatever the loss suffered by the plaintiff due to non-acceptance of its offer could be easily compensated terms of money, such loss thus could not be termed as irreparable lost.
?
(e) Civil Procedure Code (V of 1908)---
 
----O. XXXIX, Rr.1 & 2---Interlocutory injunction, grant of Convenience and inconvenience to the parties---Defendant, in the pres case, if restrained from importing goods, as prayed by the plaintiff, s was likely to have effect on agricultural production in the country defendant was purchasing the goods at the price lesser than the offered by the plaintiff--Balance of inconveniences lay in favour of defendant in circumstances.
 
Zafar Ali Shah's case PLD 2000 SC 869; Messrs Airport Support Services v. The Airport Manager 1998 SCMR 2268; (1997) 7 Supreme Court Cases 463; Bhagavan Manaji Marwadi and others v. Hiraji Premaji Marwadi AIR 1932 Rom. 516; Messrs M.A. Majeed Khan v. Karachi Water and Sewerage Board and others PLD 2002 Kar. 315; Muhammad Javaid Iqbal v. The Government of Pakistan 1974 SCMR 481; Messrs Kohinoor Trading (Pvt.) Ltd. v. Mangrani Trading Co. and others Lashkari and 4 others v. The State PLD 1981 Kar. 1; Euro Distributors Establishment, Lugano, Switzerland v. Bank of Credit and Conunerce International, London and others 1982 CLC 2369; Messrs Malik and Haq and another v. Muhammad Shamsul Islam Chowdhry and 2 others PLD 1961 SC 531; Muhammad Farooq Khan v. Sulaiman A.G. Panjwani PLD 1977 Kar. 88; The National Electric Radio, Refrigeration Co. Pakistan Ltd., Karachi v. Messrs Sachiliae Laura, Naples, Italy and 3 others PLD 1977 Kar. 264; Tauseef Corporation (Pvt.) Ltd. v. Lahore Development Authority and others 2002 SCMR 1269; Muhammad Iqbal v. Fatima Jinnah Medical College and another 1989 MLD 4237 and Rehim Khan v. Division Superintendent, Pakistan Railways, Rawalpindi an another 2003 YLR 63 ref.
 
Anwar Mansoor Khan for Plaintiff.
 
S. Mamnoon Hassan for Defendant.
 
Dates of hearing: 22nd, 23rd and 24th February, 2006.
 
ORDER
 
Case 47
 
2006 C L C 702
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui and Sajjad Ali Shah, JJ
 
Messrs CLASSIC MARBLE and another---Petitioners
 
Versus
 
KARACHI ELECTRIC SUPPLY CORPORATION LIMITED---Respondent
 
C.P. No. D-448 of 2005, heard on 24th November, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. XXIII, R.1 (3)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Maintainability---Provisions of Civil Procedure Code, 1908---Applicability---Petitioner assailed demand notices issued by authorities for recovery of outstanding electricity dues---Earlier demand notices were assailed in number of civil suits and constitutional petitions which were filed on the same cause of action and were withdrawn without seeking permission to file fresh petition---Validity---Civil proceedings were regulated by Civil Procedure Code, 1908 and nature of proceedings did not necessarily depend on the nature of jurisdiction of Court invoked---If proceedings involved enforcement of a civil right, it was a civil proceeding and the provisions of Civil Procedure Code, 1908, would apply in exercise of High Courts' jurisdiction in a civil matter, whatever might be the nature of such jurisdiction---Specific mention was made to earlier notices, in the demand notices in question, thus petition was barred under O.XXIII, R.1 (3) C.P.C.---Constitutional petition was dismissed in circumstances.
 
Salahuddin and 2 others v. Frontier Sugar Mills and Distillery Ltd. and others PLD 1975 SC 244 distinguished.
 
Syed Wajihul Hassan Zaidi v. Government of Punjab 1997 SCMR 1901 and Muhammad Waris Ali v. Deputy Commissioner Sheikhupura 1999 SCMR 2380 ref.
 
Hussain Bakhsh v. Settlement Commissioner Rawalpindi PLD 1970 SC 1 fol.
 
H.A. Rehmani, Muhammad Anwar Tariq and Muhammad Nadeem Qureshi for Petitioners.
 
Khalid Mehmood Siddiqui for Respondent.
 
Date of hearing: 24th November, 2005.
 
JUDGMENT
 
Case 48
2006 C L C 802
 
[Karachi]
 
Before Amir Hani Muslim, J
 
JAVED IQBAL and 2 others----Petitioners
 
Versus
 
ABDUL GHAFOOR and 2 others----Respondents
 
Constitutional Petition No.150 and C.M.A. No.429 of 2005, decided on 8th August; 2005.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
---Ss. 2(f)(j), 15 & 21---Constitution of Pakistan (1973), Art.199---Constitutional petition---Relationship of landlord and tenant---Agreement of sale---Petitioner/tenant had contended that premises in dispute was on tenancy initially, but subsequently landlord by virtue of sale agreement had sold the same to him---Petitioner had submitted that on the date of execution of said sale agreement, he had ceased to be a tenant and had become the owner of the premises in question---Validity---Sale agreement itself did not confer title upon petitioner/tenant and jurisdiction of Rent Controller would continue unless Civil Court would give finding in favour of petitioner---Proceedings before Rent Controller and Appellate Authority were independent of plea raised by the petitioner-No infirmity was found in the orders impugned in proceedings to warrant interference in exercise of constitutional jurisdiction.
 
2004 SCMR 53 and PLD 2004 SC 465 ref.
 
Shaikh Fazaluddin for Petitioners.
 
 
ORDER
 
Case 49
2006 C L C 802
 
[Karachi]
 
Before Amir Hani Muslim, J
 
JAVED IQBAL and 2 others----Petitioners
 
Versus
 
ABDUL GHAFOOR and 2 others----Respondents
 
Constitutional Petition No.150 and C.M.A. No.429 of 2005, decided on 8th August; 2005.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
---Ss. 2(f)(j), 15 & 21---Constitution of Pakistan (1973), Art.199---Constitutional petition---Relationship of landlord and tenant---Agreement of sale---Petitioner/tenant had contended that premises in dispute was on tenancy initially, but subsequently landlord by virtue of sale agreement had sold the same to him---Petitioner had submitted that on the date of execution of said sale agreement, he had ceased to be a tenant and had become the owner of the premises in question---Validity---Sale agreement itself did not confer title upon petitioner/tenant and jurisdiction of Rent Controller would continue unless Civil Court would give finding in favour of petitioner---Proceedings before Rent Controller and Appellate Authority were independent of plea raised by the petitioner-No infirmity was found in the orders impugned in proceedings to warrant interference in exercise of constitutional jurisdiction.
 
2004 SCMR 53 and PLD 2004 SC 465 ref.
 
Shaikh Fazaluddin for Petitioners.
 
 
ORDER
 
Case 50
 
2006 C L C 822
 
[Karachi]
 
Before Mushir Alam and Syed Zawwar Hussain Jafery, JJ
 
UNITED BANK LTD.----Appellant
 
Versus
 
Messrs AL-NOOR ENTERPRISES and another----Respondents
 
H.C.A. No.39 of 2003, decided on 20th September, 2005.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. XXI, Rr.10, 61 & 66---Execution of decree---Sale of mortgaged property---When mortgaged property was offered and sold under orders of the Court, auction-purchaser would acquire clean and unencumbered right and title to the property---Unless such charge, lien or encumbrance was notified in the sale proclamation as required under Rr.61 & 66 of O.XXI, C.P.C., auction-purchaser could challenge the validity of such charge, lien or encumbrance.
 
I.D.B.P. v. Messrs Maida Limited 1994 SCMR 2248 ref.
 
(b) Words and phrases---
 
----Phrase "as is where is basis"---Defined and explained.
 
Amjid Ali v. Official Assignee, High Court 2001 CLC 671 ref.
 
(c) Civil Procedure Code (V of 1908)---
 
----O. XXI, Rr.10, 61 & 66---Law Reforms Ordinance (XII of 1972), S.3---High Court appeal---Execution of decree---Sale of mortgaged property---Appellant had impugned order of single Judge in execution application in which he had observed that auction-purchaser acquired property free from all encumbrances and further directed that decree-holder (Bank) would clear all liabilities---Validity---No exception could be taken to observation of Single Judge that auction-purchaser acquired property free from all encumbrances, but his direction that decree-holder would clear all liabilities, was not justified---Liabilities, if any of judgment-debtor, could not be claimed or enforced against decree-holder or for that matter the auction-purchaser---Encumbrance and charges, due against judgment-debtor could only be enforced against judgment-debtor personally or against his property before it was sold in auction by the Court---After the property, was sold at the motion of any creditor, mortgagee or charge-holder, then prior charge or encumbrance-holder, could have same: right and interest in the order of priority, in the proceeds of sale as he had in the property itself.
 
Haleem Siddiqui for Appellant.
 
Amanullah Khan for Respondent No.1.
 
Nemo. for Respondent No.2.
 
Date of hearing: 20th September, 2005.
 
 
ORDER
 
Case 51
2006 C L C 833
 
[Karachi]
 
Before Anwar Zaheer Jamali and Yasmin Abbasey, JJ
 
CITY DISTRICT GOVERNMENT, KARACHI----Appellant
 
Versus
 
AMMAR HOUSING SERVICES (PVT.) LIMITED and others----Respondents
 
H.C.A. No.164 of 1995, decided on 3rd February, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 12(2)---Law Reforms Ordinance (XII of 1972), S.3---High Court appeal---Challenging decree on allegations of fraud and misrepresenta tion---Appellant challenged collusive decree or compromise decree passed in favour of respondent under S.12(2), C.P.C. on ground of fraud and misrepresentation---Said application having been dismissed, appellant had filed High Court appeal---Validity---Respondent, despite knowing that lease of disputed property earlier made in his favour was cancelled and that he had not paid lease money, was struggling to get disputed property which was nothing, but a fraud practised on the Courts as. he had concealed said fact---To agitate against the justified grievance was the fundamental right of a person, whereas term `fraud' implied intended deprivation of property by concealing the true fact---Continuous act of such misrepresentation, would manifest, rather prove the wrongful gain to one person which was apparent in the present case---Conduct of respondent in dishonestly setting up a title for himself by obtaining injunction order in suit in his favour had further established fraud played by him and his act of continuous misrepresentation before the Court of law---Respondent in pursuance of ex parte order, got executed lease deed in his favour through Nazir of the Court---Such conduct of respondent, was conclusive proof of fraud played by him on Courts---Concealment of facts before judicial forums', would amount to fraud and misrepresentation as committed by respondent---Appellant being the real owner of property in dispute, had every right to challenge impugned order as section 12(2), C.P.C. would not debar any stranger to a suit to challenge a judgment and decree obtained by fraud and misrepresentation; when his right and interest in said property was being effected by it---Intention of Legislature by using term 'Person' in S.12(2), C.P.C., was with the object not to confine the opportunity provided in it only to the extent of parties in proceeding, but to extend it to all persons whose interest and right had been adversely affected by that judgment and decree procured by practising fraud and misrepresentation on Court---In case of fraud and collusion, whole proceedings would be deemed to fibula non judicium.
 
Abdur Rauf and others v. Abdur Rahim Khan PLD 1982 Pesh. 172; 1984 SCMR 586 and 1993 SCMR 662 .ref.
 
(b) Words and phrases---
 
----Terms 'fraud' and 'collusion', defined and explained.
(c) Civil Procedure Code (V of 1908)---
 
---S. 12(2)'---Scope and application of S.12(2), C.P.C.---Use of term "person" in S.12(2), C.P.C.---Object.
 
Muhammad Anwar Tariq for Appellant.
 
Khalid Rived Khan for Respondents.
 
Date of hearing: 17th November, 2005.
 
 
JUDGMENT
 
Case 52
 
2006 C L C 847
 
[Karachi]
 
Before Sabihuddin Ahmed, C.J. and Muhammad Ather Saeed, J
 
MUHAMMAD IRFAN----Petitioner
 
Versus
 
PROVINCE OF SINDH and others----Respondents
 
C.P. No.D-1315 of 2005, decided on 13th January, 2006.
 
Societies Registration Act (XXI of 1860)---
 
----S. 16-A---Constitution of Pakistan (1973), Art.199---Constitutional petition---Maintainability---Elections of office-bearers and Executive Committee of Association---Petitioner, who was a founder member of the Association which was registered under Societies Registration Act, 1860, held office of Association for more than 20 years---Initially, election of office-bearers and Executive Committee were to be held every year, but through an amendment in the Articles of Association said term was extended to three years---Petitioner, who was elected for several three years terms after the amendment, had now challenged said amendment alleging the same to be illegal---Validity---Evidence on record had clearly shown that petitioner under his own hand addressed to the authorities, had communicated the result of election for a three years term, wherein he was elected as President---Petitioner, for seeking relief under constitutional jurisdiction of High Court, must approach the Court with clean hands---Having taken full advantage of several three years terms, petitioner could not be allowed to urge that no legal amendment was made in Articles of Association.
 
Abdul Aziz Khan for Petitioner.
 
Anwar Mansoor Khan, A.-G. for Respondents Nos.1 and 2.
 
Abdul Rasheed for Respondent No.3.
 
Date of hearing: 16th December, 2005.
 
 
JUDGMENT
 
Case 53
 
2006 C L C 888
 
[Karachi]
 
Before Mrs. Qaiser Iqbal, J
 
FALCON ENTERPRISES----Plaintiff
 
Versus
 
NATIONAL REFINERY LTD.----Defendant
 
Suit No.1436 of 2004, heard on 9th March, 2006.
 
Arbitration Act (X of 1940)---
 
----Ss. 2(a)(b), 16, 17, 20, 30 & 33--7Making award rule of Court--Object of settlement of dispute through arbitration---Power to remit award---Objections to award---Object of settlement of dispute through arbitration was to avoid lengthy procedure by invoking jurisdiction of Civil Court---Function of the Court in such cases principally was of supervisory nature and that of appellate power under Code of Civil Procedure and it was the duty of the Court to give reasonable intendment in favour of award and lean towards upholding, rather than vitiating the same---Court should not act as a Court of appeal or sit in judgment over the award, nor it should proceed to scrutinize award in order only to discover an error for purpose of setting aside the same, whether error must be apparent on face of award and not latent---Award could be remitted under S.16 of Arbitration Act, 1940---Award should be construed liberally in accordance with common sense and it should be so read that it could be given effect to and not so that it would nullify the efforts of arbitrators appointed by parties themselves---Objections relating to non-reading of evidence by arbitrators by the defendant and rejection of claim of defendant, was not sustainable in law in circumstances---Objections raised by defendant about misconduct of arbitrators, could not be sustained as they had acted in line of rule laid down by the superior Courts---No error patent on the face of record existed and documents relied upon for the purpose of investigation and inquiries into the claim of plaintiff with full reasoning and dealing with each and every item proposed by both parties to resolve a complicated dispute with reference to explanation furnished by defendants---Contention that arbitrators had exceeded their power in circumstances, was without substance---Court hearing objection to the award could not undertake reappraisal of evidence recorded by arbitrators in order to discover the error or infirmity in the award---Perversity in reasoning of arbitrators was required to be established on the basis of material considered by arbitrators in the award---Objection filed by defendant, being not maintainable in law, were dismissed and award was made rule of the Court.
 
Messrs Joint Venture KG/RIST v. Federation of Pakistan PLD 1996 SC 108; Pakistan Steel Mills Corporation, Karachi v. Messrs Mustafa Sons (Pvt.) Ltd. Karachi PLD 2003 SC 301; Waheed Brothers (Pakistan) Ltd. v. Messrs Izhar (Pvt.) Ltd., Lahore 2002 SCMR 366; Messrs Tribal Friends Co. v. Province of Balochistan 2002 SCMR 1903; Ashfaque Ali Qureshi v. Municipal Corporation, Multan 1985 SCMR 597; A. Qutubuddin Khan v. KESC 1980 CLC 1977; Premier Insurance Company (Pakistan) Ltd. Karachi v. Ijaz Ahmed Khawaja 1981 CLC 311 and Mian Corporation v. Lever Brothers of Pakistan Ltd. PLD 2006 SC 169 ref.
 
Samiuddin Sami for Plaintiff.
 
Qamar Abbas for Defendants.
 
Date of hearing: 9th March, 2006.
 
ORDER
 
Case 54
 
2006 C L C 897
 
[Karachi]
 
Before Faisal Arab, J
 
TRADING CORPORATION OF PAKISTAN----Plaintiff
 
Versus
 
Messrs MERCHANT AGENCY through Proprietor and 2 others----Defendants
 
Suit No.1072 of 1991, decided on 13th December, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. VII, R.2---Suit for recovery of amount---Defendant filed its written statement and after settlement of issues matter was fixed for recording evidence---Notice of intimation was served on defendant through substituted service, but he did not appear to defend suit against him---Service on defendant, having been held good, Court ordered to proceed against defendant ex parte and plaintiff was directed to file affidavit in ex rte proof and officer of plaintiff filed said affidavit in ex parte proof---Validity---Claim of plaintiff as stated in the affidavit, having remained unchallenged, there was no legal infirmity in the claim of plaintiff---Suit was decreed as prayed for in the plaint against defendant with costs together with 6% mark-up from the date of filing of suit till recovery of entire decreed amount.
 
Samiuddin Sami for Plaintiff.
 
Defendants called absent.
 
Date of hearing: 6th December, 2005.
 
 
JUDGMENT
 
Case 55
2006 C L C 910
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
RASOOL BUX and 2 others----Petitioners
 
Versus
 
MUHAMMAD ASLAM and 2 others----Respondents
 
C.P. No.S-133 and C.M.A. No.342 of 1996, decided on 13th December, 2005.
 
Pakistan (Administration of Evacuee Property) Act (XII of 1957)---
 
----Ss. 2(2)(3) & 3---Constitution of Pakistan (1973), Art.199---Constitutional petition---Non-evacuee nature of property and owner thereof---Determination---Assistant Custodian of Evacuee Properties on 5-4-1958 ordered that property in dispute and owner thereof were non -evacuee---Subsequently High Court also ordered on 24-2-1965 that property in dispute and owner thereof, were non-evacuee and said order had never been challenged---Status of owner of property in dispute and property itself having finally been declared as non-evacuee, same could not subsequently be challenged---Application made challenging said status of owner and property could only be proceeded with to the extent of persons and properties other than the property in dispute---Application and status quo order, if any, in circumstances would have no effect in respect of owner of property in dispute, non-evacuee nature of which had finally been determined.
 
Jagdesh R. Mulani for Petitioners.
 
M. Saleem Samoo for Respondent No. 1.
 
Naraindas C. Mottani for Respondent No.3.
 
 
ORDER
 
Case 56
 
2006 C L C 916
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
SOOMAR----Applicant
 
Versus
 
BASHIR AHMED----Respondent
 
Civil Revision Applications Nos.188 to 194 of 2004, decided on 20th March, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O. XVIII, R.17---Closing side of plaintiff---Application for opening the same---Court, after examining witnesses of plaintiff, remained vacant for some time and later on side of plaintiff was closed---No order was passed on application of plaintiff tiled by him for opening his side and defendant was allowed to produce his witnesses---Application for opening plaintiff's side filed under O.XVIII, R.17, C.P.C. remained pending and no order was passed thereon and later on same was dismissed as time barred by non-speaking order which order could not be termed as judicial---Said order was set aside and Trial Court was directed to provide an opportunity to defendant in the suit to cross-examine plaintiff's witnesses and to finalize case within specified period.
 
Noor Ahmed Memon for Applicant.
 
Ahmed Raza Siddiqui for Respondent.
 
 
ORDER
 
Case 57
 
2006 C L C 919
 
[Karachi]
 
Before Khilji Arif Hussain, J
 
TRUSTEES OF THE PORT OF KARACHI through Chairman----Plaintiff
 
Versus
 
PROJECT SHIPPING CO. LTD. Through Manager and 2 others----Respondents
 
C.M.As. Nos.5799 of 2003 and 2017 of 2004 in Suit No.1129 of 2003, decided on 27th March, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. VII, R.11---Rejection of plaint----Material essential for consideration---Averments in plaint would be deemed to be true and on their basis, one would see whether suit is barred by law or plaintiff has no cause of action.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. II, R.2---Expression "cause of action"---Meaning stated.
 
The expression "cause of action" in Order II, rule 2, C.P.C., means the cause of action for which a suit is brought. The cause of action, as it means denotes a bundle of facts, which it is necessary for the plaintiff to prove which gives rise to a right to plaintiff, which are traversed by the defendant.
 
(c) Limitation Act (IX of 1908)---
 
----S. 14---Exclusion of time spent in prosecuting another proceedings bona fide before a wrong forum---Essential conditions stated.
 
Under section 14 of Limitation Act, 1908, while computing the period of limitation prescribed for any suit, the time during which (i) plaintiff has been prosecuting another civil proceedings, (ii) with due diligence, (iii) other proceedings whether in the same Court or in any Court of appeal against the defendant, (iv) upon the same cause of action, can be excused.
 
The benefit of section 14 of the Limitation Act, 1908 can be availed only by the party, who pursue his remedy before a wrong forum bona fide with due diligence against the same defendant and on the same cause of action cannot be granted to the defendant, if he had not filed any counter-claim in the proceedings and/or not restrained from taking proceeding against the defendant in the suit filed by him.
 
Madhavdas Parmanand v. Jan Muhammad Ghulam Hyder AIR 1942 Sindh 37 and Javaid Iqbal Abbasi & Co. v. Province of Punjab and 6 others 1996 SCMR 1433 ref.
 
Arif Khan for Plaintiff.
 
Mansoor A. Shaikh and Ejaz Ahmad for Defendants Nos.1 and 3.
 
Date of hearing: 13th February, 2006.
 
 
ORDER
 
Case 58
2006 C L C 989
 
[Karachi]
 
Before Faisal Arab, J
 
RAFIQ AHMAD through General Attorney----Petitioner
 
Versus
 
RENT CONTROLLER, JACOBABAD and 3 others----Respondents
 
C.P. No.311 of 2005, decided on 4th April, 2006.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
----Ss. 2(F)(J), 15(2)(ii) & 16(1)(2)---Qanun-e-Shahadat (10 of 1984), Art.115---Constitution of Pakistan (1973), Art.199---Constitutional petition---Denial of relationship of landlord and tenant by tenant---Default in payment of rent---Application for ejectment was filed by landlord on ground of default in payment of rent---Tenant in his written statement denied relationship of landlord and tenant with regard to premises in question--Tenant admittedly had committed default in payment of rent and had failed to furnish any reasonable and cogent reason for the default---Tenant, in order to avoid consequence of default, could not be allowed to deny ownership of landlord, especially when he had himself admitted that he was inducted as tenant in the premises---Tenant who himself had admitted to be tenant under landlord, was estopped under Art.115 of Qanun-e-Shahadat, 1984 from denying title of landlord---Where tenant denied relationship of landlord and tenant and such relationship stood proved, then no other course was left for the court, but to order his ejectment---If there was contumacious denial of relationship, tenant was liable to be ejected straightaway without recording evidence on other grounds such as default, damages to premises or personal need---Both Rent Controller and Appellate Court had rightly ordered ejectment of tenant---Said concurrent order could not be interfered with in constitutional jurisdiction of High Court.
 
1997 CLC 623; 1992 SCMR 1170; 1997 SCMR 567; 1991 CLC 1310; 1992 MLD 1391 and 2005 CLC 1696 ref.
 
Nawab Syedul Mukhtiar Siddiqui for Petitioner.
 
Date of hearing: 21st March, 2006.
 
JUDGMENT
 
Case 59
2006 C L C 996
 
[Karachi]
 
Before Muhammad Moosa K. Leghari, J
 
ZULFIQAR ALI MALIK----Applicant
 
Versus
 
Mrs. ISHRAT NAZ KHAN----Respondent
 
Revision Application No.23 of 2006, decided on 2nd March, 2006.
 
Civil Procedure Code (V of 1908)---
 
----S. 115---Revisional jurisdiction---Nature---Revisional jurisdiction is a discretionary jurisdiction and is meant to be exercised for correcting the errors of law and/or jurisdictional defects of the Courts below---Nothing wrong was found in the impugned order and no perversity, impropriety or illegality had been noticed---Impugned order, in circumstances needed no interference in revision.
 
Muhammad Ibrahim Dasti for Applicant.
 
Respondent in person.
 
Date of hearing: 23rd February, 2006.
 
ORDER
 
Case 60
 
2006 C L C 1042
 
[Karachi]
 
Before Nadeem Azhar Siddiqi, J
 
DEPUTY COMMISSIONER, MALIR----Petitioner
 
Versus
 
JAN MUHAMMAD and others----Respondents
 
C.M.A. No.6889 of 2003 in Civil Reference No.3 of 1978, decided on 24th April, 2006.
 
Land Acquisition Act (I of 1894)---
 
----Ss. 4 & 28-A---Civil Procedure Code (V of 1908), Ss.151 & 152---Acquisition of land---Claim for additional compensation---Exercise of inherent powers of Court---Application for---Applicants/claimants had sought correction of judgment and had prayed that additional compensation in respect of their acquired land be allowed to them which was allowed in law---On the date when High Court had given its decision, S.28-A of Land Acquisition Act, 1894 whereunder claimants were held entitled to additional compensation of 15% per annum on amount of compensation plus interest, was in field as at that time it was added in said Act---Pendency of reference in referee Court, amounted to pending proceedings as matter of payment of compensation, was not finally adjudicated at that time---It appeared that S.28-A of Land Acquisition Act, 1894 was not brought to the notice of the Bench, resulting in loss to claimants/applicants---Allowance provided under said S.28-A of Land Acquisition Act, 1894 was mandatory in nature and being beneficial in nature, would apply to all pending proceedings---Applicants/claimants, in circumstances were entitled to said additional compensation, so fixed from the date of Notification under S.4 of Land Acquisition Act, 1894 to the date of payment of compensation---Omission to grant additional compensation as was admissible under S.28-A of Land Acquisition Act, 1894, however was not intentional, but appeared to be an accidental slip or omission which could be corrected at any time by the Court, either on its own motion or on application of any party, in exercise of powers under S.152, C.P.C. and said omission could be rectified.
 
Abdul Hamid Ali and others v. Land Acquisition Officer, Badin PLD 1998 Kar. 50 and Dilawar Hussain and others v. The Province of Sindh and others PLD 1993 Kar. 578 ref.
 
Adnan Memon, Muhammad Saleem Mangrio, Ms. Shahida Bano Kasmani and Mushtaq Ahmed Chandio for Claimants.
 
S. Amanullah Khan, for Pakistan Steel Mills.
 
Muhammad Ahmed Pirzada, Addl. A.-G. Sindh.
 
Date of hearing: 6th April, 2006.
 
ORDER
 
Case 61
2006 C L C 1060
 
[Karachi]
 
Before Anwar Zaheer Jamali and Muhammad Athar Saeed, JJ
 
KARACHI DOCK LABOUR BOARD----Appellant
 
Versus
 
Messrs QUALITY BUILDERS LIMITED----Respondent
 
High Court Appeal No.18 of 2005, decided on 16th March, 2006.
 
Arbitration Act (X of 1940)---
 
----Ss. 5, 8, 9, 11, 20, 30 & 39---High Court appeal---Reappraisal of evidence---Appellate Court, jurisdiction of---Appointment of arbitrator---Failure to raise any objection---On the basis of arbitration clause in the contract between the parties, respondent appointed his arbitrator but appellant did not appoint any arbitrator on his behalf---Arbitrator appointed by respondent issued notices but appellant challenged his jurisdiction to conduct arbitration proceedings---Sole arbitrator after deciding the point of his jurisdiction passed an award which was made rule of the Court---Validity---Appellant was not able to show that he had acted with due diligence because instead of taking steps under Ss.5 & 11 of Arbitration Act, 1940, to approach the Court to cancel the appointment of arbitrator or stay arbitration proceedings, the appellant only attended by sending letters from time to time to the arbitrator agitating the same plea---While entertaining an appeal against order making award, delivered under Arbitration Act, 1940, the rule of the Court, Appellate Court could not sit as a court of appeal against the judgment and decree passed in the suit, therefore, reappraisal of evidence forming another opinion contrary to the material placed on record before the arbitrator was not permissible---Arbitration tribunal was properly constituted and had the jurisdiction to decide the dispute between the parties---Judgment of High Court to the effect that appellant was not able to show in what manner arbitrator misconducted himself and for that matter award was improperly procured, was based on cogent reasons and was unexceptionable--- High Court declined to interfere in the award in High Court Appeal, made rule of the Court---Appeal was dismissed in circumstances.
 
Abdul Hamid V. H.M. Qureshi PLD 1957 SC 145; Sh. Saleem Ali v. Sh. Akhtar Ali and 7 others PLD 2004 Lah. 404; Muhammad Azam Muhammad Fazil & Co., Karachi v. Messrs N.A. Industries, Karachi PLD 1977 Kar. 21; Board of Trustees of Port of Karachi v. Messrs National Construction Co., (Pakistan) Ltd. and another PLD 1981 Kar. 377; Rizwan Hussain v. The State 1999 SCMR 131; Messrs Commodities Trading International Corporation v. Trading Corporation of Pakistan Ltd. and others 1987 CLC 2063; Abdul Khanum Jan and others v. Begum Khanum Jan and others 1989 MLD 1304; Messrs Joint Venture KG/Rist v. Federation of Pakistan PLD 1996 SC 108; Project Director, Balochistan Minor Irrigation and Agricultural Development Project, Quetta Cantt. v. Messrs Murad Ali & Company 1999 SCMR 121; M.Y. Corporation (Private) Ltd. v. Messrs Erum Developers and 2 others PLD 2003 Kar. 522; AIR 1964 Madhya Pradesh 268; Pakistan Steel Mills Corporation Karachi v. Mustafa Sons (Pvt.) Ltd. PLD 2003 SC 301; Waheed Brothers (Pak.) Ltd. v. Izhar (Pvt.) Ltd. Lahore 2002 SCMR 366; Messrs Tribal Friends v. Province of Balochistan 2002 SCMR 1903; The Premier Insurance Co. v. K.M.C. 1981 CLC 311 and Messrs Ibad & Co. v. Province of Sind' PLD 1980 Kar. 207 ref.
 
Arshad Tayabally for Appellant.
 
Muhammad Masood Khan for Respondent.
 
Dates of hearing: 19th January, and 16th March, 2006.
 
JUDGMENT
 
Case 62
2006 C L C 1087
 
[Karachi]
 
Before Ghulam Rabbani and Azizullah M. Memon, JJ
 
SHAFI MUHAMMAD and another----Petitioners
 
Versus
 
RETURNING OFFICER, UNION COUNCIL MOLE, DISTRICT JAMSHORO and 3 others----Respondents
 
C.P. No.D-917 of 2005, decided on 19th August, 2005.
 
Sindh Local Government Ordinance (XXVII of 2001)---
 
----S. 152(1)(g)---Election of Nazim and Naib Nazim---Eligibility of candidates to contest election---Allegation against candidates were that they had been in Government service as teachers---Candidates pleaded that after termination of their service in December, 2004 on completion of contract, they could not be said to have been in service within six months before filing of nomination papers---Validity---Certificate produced by Education Officer showed that no salary was paid to candidates after November, 2004---Pay bills produced by District Accounts Officer showed that candidates had drawn salaries for months of December, 2004, April and May, 2005---Statement of accounts of Bank showed that candidates had drawn salaries for May, 2005---Candidates were, held, to have been in 'service in May, 2005, thus, their nomination papers were rejected.
 
Syed Zaki Muhammad for Petitioners.
 
Riazat Ali Saahar and Muhammad Sarwar Khan, Addl. A.-G., Sindh for Respondents.
 
Date of hearing: 15th August, 2005.
 
JUDGMENT
 
Case 63
2006 C L C 1093
 
[Karachi]
 
Before Muhammad Moosa K. Leghari, J
 
JAVED ISHAQUE----Petitioner
 
Versus
 
MUHAMMAD ISHAQUE----Respondent
 
C.M.As. Nos.2708 and 2709 of 2004, C.M.A. No.663 of 2005 and S.M.A. No.5 of 2005, decided on 30th March, 2006.
 
Succession Act (XXXIX of 1925)---
 
----S. 278---Petition for letter of administration---Amounts left by the deceased which were received by the widow in the capacity of "nominee" of the deceased and as "joint account holder" as well as the dividends received by her, after the death of the deceased, devolved upon all legal heirs of the deceased and all the legal heirs were entitled to get their respective shares from the said assets as per Islamic law of inheritance.
 
Malik Safdar Ali and another v. Public-at-large and others 2004 SCMR 1219; AIR 2000 SC 2747 and PLD 1974 SC 185 fol.
 
R.F. Virjee for Petitioner.
 
Arshad Lodhi for Legal Heirs Nos.(a) and (c).
 
ORDER
 
Case 64
2006 C L C 1099
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui, J
 
ZUBAIR HUSSAIN SIDDIQUI----Petitioner
 
Versus
 
Mst. SHAKEELA KHANUM and others----Respondents
 
S.M.A. No.104 of 1995, decided on 19th December, 2005.
 
Islamic Law---
 
----Inheritance---Faith, determination of---Conversion to Islam---Faith was a matter between a person and Allah---If a person says that he is a muslim and it was not shown that he still believed in something against the basic articles of faith, then nobody would have any right to dispute
his claim---If a person claimed himself to be a muslim, but believed in something which was against basic articles of faith, such as is the case of Ahmadis/Qadianis, he would be treated as non-muslim---Change of name was not necessary for conversion to Islam---Even if no document was available, mere assertion of a person that he embraced Islam on a particular date, his statement was to be accepted and he would not be called upon to produce any other evidence to establish his conversion to Islam----Muslim female marrying a christian would not become non muslim merely by fact of such marriage, though it would be a sinful act, but she would not be deprived of her right of inheritance from her muslim parents.
 
Rukhsana Ahmed for Petitioner.
 
Shamdas B. Changani for Applicant.
 
Shakeela Khanum widow of deceased Zubair Hussain Siddiqui.
 
Date of hearing: 21st November, 2005.
 
ORDER
 
Case 65
 
2006 C L C 1106
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
ABDUL RAZZAK----Petitioner
 
Versus
 
Ms. RAHAT BANO----Respondent
 
Insolvency Petition No.1 of 2002 and C.M. No.647 of 2004, heard on 25th January, 2006.
 
Insolvency (Karachi Division) Act (III of 1909)---
 
---Ss. 6, 8(ii), 9(4), 10, 11-A, 14, 25, 90 & 107---Sindh Chief Court Rules (O.S.), R.624---Insolvency petition---Protection order---Revocation of protection order---Application for---Protection order was passed in favour of petitioner/insolvent/debtor, whereby it was ordered that petitioner would not be arrested in execution filed against him by his wife/decree-holder for recovery of decretal amount---Respondent/decree holder in her application made under S.25(3) of Insolvency Act, 1909 had prayed for revocation of protection order passed in favour of petitioner/insolvent/debtor---Petitioner in whose favour protection order was passed, had extensively been examined in terms of Sindh Chief Court Rules (OS) by Official Assignee by way of public examination and counsel for respondent/decree-holder, had conducted cross-examination---Nothing had been brought on record to prompt Official Assignee to submit reference contrary to order of adjudication or to protection order issued in favour of petitioner/insolvent---Order of Additional Registrar, by which petitioner was adjudged insolvent, was appealable under S.8(ii) of Insolvency Act, 1909, but no appeal had been filed against such order---Said orders could not be reviewed under S.25(3) of Insolvency Act, 1909 or under R.624 of Sindh Chief Court Rules (OS).
 
PLD 1974 Lah. 495; PLD 1976 Lah. 1466; PLD 1973 (Notes) 18 Karachi; AIR 1938 All. P.253 and Emperor v. Muhammad Hussain, Abdul Kadir Shaikh and Bhikan 1940 BLR 742 ref.
 
Ms. Mehrun Nisa for Petitioner.
 
Moazam Baig for Respondent.
 
Date of hearing: 25th January, 2006.
 
ORDER
 
Case 66
2006 C L C 1113
 
[Karachi]
 
Before Anwar Zaheer Jamali and Mrs. Yasmeen Abbasi, JJ
 
Messrs GAMA SILK MILLS (PVT.) LTD.----Appellant
 
Versus
 
ABDUS SALAM and others----Respondents
 
H.C.A. No.100 of 2005, heard on 23rd December, 2005.
 
(a) Civil Procedure Code (V of 1908)---
 
------S. 12(2)---Specific Relief Act (I of 1877), Ss.12 & 54---Suit for specific performance of agreement and injunction---Compromise decree---Where a substantial controversy is raised by some party through averments made in the application under S.12(2), C.P.C., going to the root of the decree passed in the suit, then the proper course available to the Court would be to frame issues in the matter and provide full opportunity to the parties to prove their respective cases and then to decide as to whether, on the basis of material brought on record during the proceedings of application, the decree challenged through application under S.12(2), C.P.C., on the basis of fraud and misrepresentation is liable to be set aside or not.
 
(b) Civil Procedure Code (V of 1908)---
 
----S. 12(2) & O.XXIII, R.2---Application under S.12(2), C.P.C. in a compromise decree---Party cannot go beyond its own pleadings/ averments made in the application.
(c) Civil Procedure Code (V of 1908)---
 
----S. 12(2) & O.XXIII, R.2---Compromise decree---Internal family dispute would fall beyond the limited scope of application under S.12(2), C.P.C. which would only be agitated before the proper forum but could not be the basis for setting aside the compromise decree.
 
Munirur Rehman for Appellant.
 
Arshad Tayebally, Kazi Faez Isa, S.A. Samad Khan and Naveedul Haq for Respondents.
 
Date of hearing: 23rd December, 2005.
 
ORDER
 
Case 67
2006 C L C 1126
 
[Karachi]
 
Before Mushir Alam, J
 
SHAUKAT ISMAIL CHARANIA----Plaintiff
 
Versus
 
Mrs. SHAKEELA HAYAT KHAN and others----Defendants
 
Suit No.878 of 1986, decided on 27th April, 2006.
 
(a) Civil Procedure Code (V of 1908)----
 
----S. 152 & O.XX, R.6---Specific Relief Act (I of 1877), S.12---Scope and application of S.152 & O.XX, R.6, C.P.C.---Suit for specific performance of agreement wherein plaintiff had prayed for the relief of specific performance, possession, mesne profit and all other reliefs incidental thereto---Decree drawn was only to the extent of mesne profit, leaving out or omitting the relief of execution of sale-deed and delivery of possession of the suit property---Application under Ss.151 & 152, C.P.C. read with O.XX, R.6, C.P.C. seeking correction of the decree in accordance with judgment passed in suit in accordance with O.XX, R.6, C.P.C.---Maintainability---Limitation---While drawing the decree in the suit, relief of specific performance of. the agreement and relief of possession ought to have been drawn, which had been accidentally slipped or omitted---Court, under S.152, C.P.C. was not only competent to correct clerical or arithemetical mistakes but may correct accidental slip or omission as well---No limitation would come in the way of the applicant or in the way of the Court in exercise of its suo motu jurisdiction to deprive a party of the fruit of the judgment, which otherwise he was found to be entitled to---"Accidental slip or omission" as used in S.152, C.P.C. meant "to leave out or failure to mention something unintentionally", thus, it could be safely said that it was only where the slip or omission was accidental or unintentional it could be supplemented or added in exercise of jurisdiction under S.152, C.P.C.---Such course was provided to foster cause of justice, to suppress mischief and to avoid multiplicity of proceedings---Where however, slip or omission was intentional and deliberate, it could only be remedied or corrected by way of review, if permissible or in appeal or revision as the case may be---Principles elucidated.
 
In plaint in the present suit which was a suit for specific performance of the agreement, plaintiff had prayed for the relief of specific performance, possession, mesne profit and all other relief incidental thereto.
 
The decree drawn was only to the extent of mesne profit, leaving out or omitting the relief of execution of sale-deed and delivery of possession of the suit property.
 
Application under sections 151 and 152, C.P.C. read with Order XX, rule 6, C.P.C. had been filed by the plaintiff seeking correction of the decree in accordance with judgment passed in suit in accordance with Order XX, rule 6, C.P.C.
?
Judgment is verdict or decision of the Court usually recorded after recording the evidence and hearing the contesting parties. It is a conclusive judicial determination of rights of parties in any legal proceedings. Decree, is formal expression of opinion of the Court, it follows the judgment. When conclusion of the Court is translated into executable form, it is reflected in the "decree". Decree must be drawn in consonance and in conformity with decision of the Court.
 
On reading Rule 6 of Order XX, C.P.C. it is but clear that, the decree should be in accordance and in .conformity with the judgment. Decree in fact is will of the Court, it is 'true reflection of the judicial determination of rights of the parties made by the Court. It is the decree that is executed or implemented. It is duty of the Court, while drawing the decree, to specify clearly the relief granted or other determination of rights of the parties in the suit so as to make it in conformity with the will of the Court capable of enforcement.
 
On examination of the judgment, it appears that, the Court found that, defendants Nos.1 and 2 "party to the agreement had assumed joint responsibility to complete it". Quoted expression is a clear manifestation of the Court's opinion that, the defendants Nos.1 and 2 were held liable to specifically perform the agreement of sale. Suit has been decreed in terms of the relief contained in a para. of the judgment, Said paragraph of the judgment does stipulate the responsibility of the ,defendant to do the needful i.e. to complete the transaction. Very fact that, the Court had also granted mesne profit presupposes that plaintiff was found to be entitled to the possession of suit property and that the defendants were in unauthorized possession, otherwise, there was no occasion to grant the relief of the mesne profit. However, when the decree is examined, it is evident that, it does not appear to represent the true will of the Court. While drawing decree in the suit, relief of specific performance of the agreement, and relief of possession ought to have been drawn, which has been accidentally slipped or omitted.
 
Now the question whether the omission in the decree to expressly contain directions to execute sale-deed and deliver possession could be supplemented in exercise of the authority under section 152, C.P.C.
 
Contention of the defendant that, it is the only clerical or arithmetical mistakes in judgments and decree or order that could be corrected, in the context of section 152, C.P.C. is half-truth. Whole truth appears to be that, the Court under section 152, C.P.C. is not only competent to correct clerical or arithmetical mistake but may correct accidental slip or omission as well. Section 152, C.P.C. clearly defines the power of the Court to correct clerical or arithmetical mistake in the judgment, decree or order or errors on account of accidental slip or omission arising therefrom. Section 152, C.P.C. can be conveniently divided into two parts. First half of the section provides authority to correct "clerical or arithmetical mistake in the judgment, decree or order", other half provides authority to correct error arising thereon from any accidental slip or omission. Use of word "or" indicates that, such powers to correct are not conjunctive but disjunctive and qualified. To correct clerical or arithmetical mistake, means that where some mistake either in calculation or numerical figures creeps in, which could be verified from the record, or where any party, property or fact has been incorrectly described or where some typographical error has crept in. Second half of the section 152 (ibid) contemplates "error arising thereon from any accidental slip or omission". Catchword in the phrase "accidental slip or omission" as used in section 152, C.P.C. is "accidental", it qualifies `slips' and `omissions'. "Accidental" is defined in Chambers 20th Century Dictionary as "happening by chance". In Merriam Webster on line Dictionary, it is defined as "an event occurring by chance or unintentional; happening unexpectedly or by chance or happening without intent or through carelessness" it means "not deliberate". "Omission" is derived from root word "omit", it means "to leave out to fail" (Chambers 20th Century Dictionary). In Merriam Webster on line Dictionary omission is defined to mean, "something neglected or left undone, to leave out or leave unmentioned, to fail to perform". Thus, it could be said that "accidental slip or omission" as used in section 152 C.P.C. means `to leave out or failure to mention some thing unintentionally'. Thus, it could be safely said that, it is only where, the slip or omission is accidental or unintentional it could be supplemented or added in exercise of jurisdiction conferred under section 152, C.P.C. Such course is provided to foster cause of justice, to suppress mischief and to avoid multiplicity of proceedings. However, where slip or omission is intentional and deliberate, it could only be remedied or corrected by way of review if permissible or in appeal or revision as the case may be.
 
The Court has jurisdiction to correct the clerical or arithmetical mistakes or errors caused due to accidental slip or omission in a judgment, decree or order. Depending on facts, it confers a wide discretion on the Court to correct, (i) clerical or arithmetical mistake, (ii) errors caused due to accidental slip or omission in the judgment, decree or order. Such power can be exercised at any time. Where the Court is bound to grant relief even without it being sought by a party and if unintentionally or inadvertently the Court does not grant such relief, it would be justified at any time to correct such accidental omission or error by exercising power under section 152.
 
The Court does enjoy and can exercise, at any time jurisdiction, to supply the omission or slip provided it is accidental. Court may grant relief, which party has sought or otherwise is found entitled to, the Court is bound to grant such relief. Even in cases, where a party on the facts of case is entitled to a relief, but has omitted to pray for the same, then it is the duty of the Court to grant such relief. Court would be justified, at any point of time to correct not only the clerical or arithmetical errors but also to correct accidental omission or slip that might have crept into the order, judgment or decree.
 
No limitation could come in the way of the applicant or in the way of the Court in exercise of its suo mote jurisdiction not to deprive a party of the fruit of the judgment, which otherwise he is found to be entitled to.
 
Relevant paragraphs of the judgment and the issues on the basis of which decision was rendered is clear manifestation of the Court's will and opinion that the relief of specific performance and possession was granted and the cancellation of documents as claimed in suit was declined.
 
Therefore, due to accidental slip and omission decree prepared in the present case is not the true reflection of the judgment of the Court.
 
Accordingly, application was allowed. Decree was accordingly directed to incorporate relief of specific performance in terms of prayer contained in prayer clause of the plaint.
?
Mst. Ashraf Bibi v. Barkat Ali PLD 1956 Lah. 27; Tepri Mai Bewa v. Farey Mahmud and others PLD 1970 Dacca 475; Ghulam Muhammad v. Sultan Mahmud and others PLD 1963 SC 265; Sultan Ali v. Khushi Muhammad PLD 1983 SC 243; Water and Power Development Authority v. Aurangzeb 1988 SCMR 1354; Chambers 20th Century Dictionary; Merriam Webster on line Dictionary; Bank of Credit and Commerce International (Overseas) Ltd. v. Messrs Ali Asbestos Industries Ltd. and 5 others 1990 MLD 130 and Syed Saadi Jafri Zainzabi v. Land Acquisition Collector and Assistant Commissioner PLD 1992 SC 472 ref.
 
(b) Judgment---
 
----Connotation.
 
(c) Civil Procedure Code (V of 1908)----
 
---O. XX, R.6---Contents of decree---Principles.
 
Mumtaz Ahmed Shaikh for Plaintiff.
 
Syed Mamnoon Hasan for Defendant.
 
ORDER
 
Case 68
2006 C L C 1139
 
[Karachi]
 
Before Faisal Arab, J
 
MUHAMMAD ASIF DAR----Plaintiff
 
Versus
 
UNIVERSAL LEASING CORPORATION LIMITED through Chief Executive----Defendant
 
Suit No.1352 of 2003, decided on 17th February, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O. VI, R.2---Suit for recovery of money against defendant-Company, being amount of unpaid salaries and allowances of the plaintiff as well as claim for damages---Damages---Plaintiff, who was employed as Executive Director of a company and had no concern or involvement in any alleged fraudulent transaction by the company, was arrested and since his arrest he was not paid his salary and allowances and even the company maintained car was repossessed by the Institution from which the same was obtained on lease for the plaintiff on account of failure of the company to pay monthly lease rentals to the lessor---Plaintiff had contended that his wrongful involvement in the fraud case was quite humiliating for him and his family, hence his claim for damages---Validity---Plaintiff had proved through documents that defendant-Company had not accounted for his salaries and allowances for the relevant period---Defendant had failed to refute the plaintiff's case---Plaintiff, in circumstances, was entitled to his claim with regard to unpaid salaries, allowances and tax deductions---Plaintiff's claim for damages was also reasonable considering the humiliation and embarrassment that he had to suffer on account of his arrest, detention and trial for no fault on his part---High Court decreed the suit in a sum of Rs.42,50,598 with interest at the rate of 6% per annum chargeable from the date of filing of the suit till realization of the decretal amount.
 
Nadeem Akhtar for Plaintiff.
 
Nemo for Defendant.
 
Date of hearing: 26th January, 2006.
 
JUDGMENT
 
Case 69
2006 C L C 1145
 
[Karachi]
 
Before Muhammad Moosa K. Leghari, J
 
Sheikh MUHAMMAD HUSSAIN QURESHI----Appellant
 
Versus
 
Mrs. SANJEEDA NUZHAT and 3 others----Respondents
 
Second Appeal No.42 of 2005, decided on 7th March, 2006.
 
Specific Relief Act (I of 1877)---
 
----Ss. 8, 39 & 54--Civil Procedure Code (V of 1908), S.100 & O.XLI, Rr.23 & 24---Suit for possession, cancellation of documents and permanent injunction---Second appeal---Remand of case---Suit was decreed by the Trial Court, on the basis of evidence adduced before it, but Appellate Court below, set aside judgment and decree passed by the Trial Court and instead deciding matter itself on basis of evidence on record, remanded case to the Trial Court with direction to proceed with the matter from the stage of final arguments and decide suit afresh---Trial Court had decided case on merits, after discussing entire evidence available on record and each issue was discussed and findings were recorded thereon---It was not the case of either party that evidence recorded in case was insufficient or inclusive to justify or necessitate remand of case---Since entire evidence on record was available, which was sufficient for Appellate Court below to pronounce judgment, Appellate Court was required to decide appeal on merits---Order of remand in circumstances, was contrary to law---Remand of case was not a routine matter, but a matter should be remanded only when compelling circumstances existed---Order of remand, on the face of it, was against provision of O.XLI, R.23, C.P.C. as it militated against stipulations contained in R.24 of O.XLI, C.P.C. and had been passed in flagrant violation of principles of law settled by Supreme Court---Remand order being illegal and in violation of law, was set aside, in circumstances.
 
2005 SCMR 152 and Ashiq Ali and others v. Mst. Zamir Fatima and others PLD 2004 SC 10 ref.
 
Rao M. Shakir Naqshbandi for Appellant.
 
Ghulam Rasool Mangi for Farukh Zia Shaikh for Respondents.
 
Date of hearing: 7th March, 2006.
 
ORDER
 
Case 70
  
2006 C L C 1187
 
[Karachi]
 
Before Azizullah M. Memon, J
 
MUHAMMAD YAQOOB THABO----Petitioner
 
Versus
 
VTH SENIOR CIVIL JUDGE/RENT CONTROLLER and 3 others----Respondents
 
Constitution Petition No.187 of 2006, decided on 14th April, 2006.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
---S. 15---Constitution of Pakistan (1973), Art.199---Constitutional petition---Ejectment proceedings---Tenant filed his written statement and thereafter landlord filed affidavit-in-evidence and he was cross-examined by counsel for the tenant---Tenant, during proceedings filed an application before Rent Controller with a prayer to discard/reject affidavit-in-evidence and dismiss ejectment application along with his affidavit-in-evidence---Rent Controller dismissed the application of tenant---Tenant/petitioner again filed application with a prayer to direct landlord to file fresh affidavit in evidence in order to rectify mistake, omission committed by him in order to remove irregularity from the legal proceedings for decision of the case on merits---Said application of tenant/petitioner also was dismissed by Rent Controller---Petitioner/ tenant filed constitutional petition against said two orders.---Validity---Whenever a party would state to be unaware of the contents of affidavit filed in judicial/quasi-judicial proceedings, benefit of such defect could be awarded to other party but same was to be so awarded at the appropriate stage of such proceedings of the case---Was not necessary for the Rent Controller to throttle further proceedings of ejectment application at such a stage of the case---Landlords were to be afforded due opportunity to produce other evidence in support of ejectment case, strictly in accordance with relevant provisions of law---No prejudice was caused to petitioner by impugned order as his rights in the case were yet to be adjudicated upon by Rent Controller according to law.
 
Arshad Mubin for Petitioner.
 
Nemo for Respondents.
 
Date of haring: 7th April, 2006.
 
JUDGMENT
 
Case 71
 
2006 C L C 1196
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
Messrs AKBARI STORES and others----Petitioners
 
Versus
 
ADDITIONAL DISTRICT JUDGE, KARACHI SOUTH and others----Respondents
 
Constitutional Petitions Nos.S-462, S-463 and S-464 of 2005, decided on 2nd May, 2006.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
---Ss. 2(a) & 14---Bona fide personal need---Right of co-sharer in building to seek ejectment of more than one tenant---Scope---Different tenants under separate and individual tenancies, if in possession of different parts of a building, then each part would be treated as building---Landlord/co-owner could get possession of one building involving one tenancy, even though not satisfying his requirement fully---Co-sharer-husband could get possession of jointly owned building involving several independent tenancies, where other co-sharers were his wife and children---Principles.
 
Razia Khatoon's case 1991 SCMR 840 and Shaikh Muhammad Khalid's 1992 CLC 2307 rel.
 
Muhammad v. Dilawar Khan Durrani and Dilawar Khan Durrani v. Muhammad (Civil Appeals Nos.112-K and 113-K of 1987; Bakar v. Mst. Khatoon Hajin Kala alias Kala Begum C.P.L.A No.266-K of 1987 and Mst. Khurshid Azmat Ali v. A.S. Mughal and Ayub Sultan, Civil Appeals No.9-K and 10-K of 1982 distinguished.
 
Iftikhar Javed Qazi for Petitioners (in all C.Ps.).
 
K.B. Bhutto for Respondent No.3 (in all C.Ps.).
 
ORDER
 
Case 72
2006 C L C 1213
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
HABIB-UR-REHMAN and another----Petitioners
 
Versus
 
SAMANDAR KHAN and others----Respondents
 
Civil Revision No.31 of 2004, decided on 6th February, 2006.
 
Specific Relief Act (I of 1877)-
 
---Ss. 42 & 54---Suit for declaration and permanent injunction-Plaintiffs had pleaded that plots in dispute were in their possession wherein they had installed a hand pump and that original defendants, who later on, succeeded by their legal heirs, were illegally claiming to be the owners of said plots and they were threatening plaintiffs to dispossess them---Defendants in their written statement had claimed that they were owners in possession of said plots on the basis of sale-deed executed by Hindu owners during years 1941 and 1946---Defendants had further claimed that on the basis of said sale-deeds mutation in the record of city survey was also made in their favour---Both the Trial Court and Appellate Court below, having dismissed suit, plaintiffs had filed revision against said concurrent judgments---Validity---Plaintiffs did not claim ownership over plots in dispute and no construction was made on said plots and plaintiffs themselves had admitted that no compound wall was available at the site---Plaintiffs had only stated that they had installed a hand pump therein, which itself would not prove physical possession of plaintiffs over plots in dispute as said plots were lying open and unoccupied---Presumption of possession, in circumstances, would be in favour of Government Department---Plaintiffs did not even plead in their plaint that on account of their possession, they had become legally entitled to get the plots transferred in their favour under provisions of Displaced Persons (Compensation and Rehabilitation) Act, 1958---In absence of such plea and proof, their suit for declaration against defendants, was rightly declared to be not maintainable---Defendants had claimed their title in respect of plots in dispute through their predecessor-in-interest, but evidence on record had proved that entries in favour of their predecessors, were manipulated and fraudulent---Defendants could not produce any sale-deed in respect of plots in dispute and had also not shown any right or title over plots in dispute---Neither plaintiffs nor defendants had any legal rights over said plots---Plots being evacuee property, had to be protected and dealt with by Authorities concerned in accordance with law.
 
Gulshan v. Amir Ali PLD 1997 Kar. 292; Muhammad Hamdan Shaikh v. Chairman, Board of Secondary Education PLD 1998 Kar. 59; Sultan Mahmood Shah v. Muhammad Din 2005 SCMR 1872 and Noorali Pir Muhammad v. Patricia Dinshaw PLD 1974 Kar. 235 ref.
 
Moohanlal K. Makhijani for Petitioners.
 
Gul Hassan Solangi for Respondents.
 
Nemo for Official Respondents.
 
ORDER
 
Case 73
 
2006 C L C 1231
 
[Karachi]
 
Before Sarmad Jalal Osmany and Amir Hani Muslim, JJ
 
Sheikh NAEEM AHMED and others----Petitioners
 
Versus
 
PROVINCE OF SINDH and others----Respondents
 
Constitutional Petitions Nos.D-1122, D-771 and D-936 of 2004, decided on 5th November, 2004.
 
Karachi Development Authority Order (P.O. 5 of 1957)---
 
----Arts. 40(3)(4) & 49(4)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Commercialization of plot---Petitioner approached the Provincial Government for commercialization of his plot---Earlier, the petitioner had also filed a constitutional petition seeking direction to the Provincial Government for commercialization of his plot, but, despite direction to sanction commercialization, did not accord sanction of commercialization for want of its authority from the Karachi Building Authority---Reason assigned by the Provincial Government for not according sanction for commercialization of petitioner's plot was that his plot was owned by the Karachi Development Authority and it was the said Authority only which had the power to accord sanction of commercialization---Validity---Provincial Government, in exercise of its powers under Art.40(3) of Karachi Development Authority Order, 1957 had issued Notification by which plots/land on six different roads of Karachi including the road, on which petitioner's plot was located, had been declared commercial---Once such Scheme was notified by the Provincial Government, no person could use land for a purpose other than what was laid down in the said Scheme---Clause (4) of Art.40 of Karachi Development Authority Order, 1957 had enabled the Building Authority to permit change of use after public hearing and notice to affected person in deviation of the Scheme---Once plot of petitioner had been commercialized by virtue of Notification, there was no question of seeking permission of the Authority---Petitioner was free to construct commercial building on plot in dispute subject to approval of plan and there would be no question of paying any commercialization fee etc.
 
Petitioner in person (in C.P. No.D-771 of 2004).
 
Rasheed A. Razvi for Petitioner (in C.P. No.D-936 of 2004). .
 
Raja Sikandar Khan Yasir for Petitioners (in C.P. No.D-1122 of 2004).
 
Anwer Ali Shah for K.B.C.A.
 
Ashraf Ali Butt for Cantonment Executive Officer, Faisal.
 
Manzoor Ahmad, for City District Government.
 
Ahmed Pirzada, Addl. A.-G. Sindh.
 
Date of hearing: 5th November, 2004.
 
JUDGMENT
 
Case 74
2006 C L C 1272
 
[Karachi]
 
Before Rahmat Hussain Jafferi, J
 
UNITED BANK LTD. through Corporate and Industrial Restructuring Corporation (CIRC), Karachi----Decree-holder
 
Versus
 
HERYANA ASBESTOS CEMENT INDUSTRIES (LTD.) and 20 others----Judgment-debtors
 
Execution Application No.39 of 2003, Auction Reports Nos.2, 3, 4, C.Ms. Nos.1734, 1735, 1850, 2177 and 2703 of 2004, decided on 18th May, 2005.
 
Civil Procedure Code (V of 1908)----------
 
---O. XXI, Rr.89, 92 & S.151---Limitation Act (IX of 1908), Art.166---Execution of decree---Inherent jurisdiction of High Court---Maintainability---Sale through auction, setting aside of---Limitation---Three months after the auction, judgment-debtors filed application under S.151 C.P.C. seeking permission to deposit amounts equivalent to highest bids, whereas the highest bidders sought confirmation of sales in their favour---Validity---Judgment-debtors were required under O.XXI, R.89 C.P.C. to file application for setting aside of sales on deposit of required amount---Such application could be filed within a period of 30 days under Art.166 of Limitation Act, 1908 but the application had not been filed by judgment-debtors within required period---Instead the judgment-debtors had invoked inherent jurisdiction of High Court by filing application under S.151 C.P.C.---Such inherent provision was applicable if there was no other provision available in Civil Procedure Code, 1908, to deal with the situation---Provision in shape of O.XXI, R.89 C.P.C. was available to the judgment-debtors which they had not invoked, as such the application under S.151 C.P.C. was not maintainable---Judgment-debtors did not file application under O.XXI, R.89'C.P.C. within 30 days, therefore, the request of judgment-debtors was time barred hence sales in respect of the properties could not be cancelled---High Court accepted auction reports and bids of highest bidders in auction reports were accepted---Sales were confirmed in circumstances.
 
Hudaybia Textile Mills Ltd. v. Allied Bank of Pakistan PLD 1987 SC 512 and Nenhelal and another v. Umrao Singh AIR 1931 PC 33 rel.
 
Naveed-ul-Haq for Decree-holder.
 
S.A. Ghafoor for Auction-purchaser.
 
Muhammad Muzaffar-ul-Haque for Defendant No.5.
 
Shahid Hussain Malik, Auction-purchaser.
 
ORDER
 
Case 75
2006 C L C 1287
 
[Karachi]
 
Before Faisal Arab, J
 
KISHWAR IQBAL KHAN through Attorney----Plaintiff
 
Versus
 
MUHAMMAD ALI ZAKI KHAN and others----Respondents
 
Suits Nos.696 and 554 of 1987, decided on 29th May, 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 39---Cancellation of document, suit for---When competent---Allegation that documents was a product of fraud and forgery---Effect---Principles to be kept in view in such situation elucidated.
 
It is only when a document has been admittedly executed and for certain legitimate reasons a party which is going to be affected by its existence seeks its cancellation that it is required to file suit for cancellation of document. However, when a document is claimed to be a product of fraud or forgery then mere declaration that it is product of such fraud or forgery is sufficient to nullify the legal effect of such document and there is no need to seek its cancellation. In any case, what should not be lost sight of is that form of legal proceedings cannot take precedence over legitimate considerations of substance of a case. When the parties are aware of the controversy involved in the case and have been given opportunity to lead evidence on their respective stands then it matters not whether specific relief was sought in the plaint or not or whether specific plea was raised in the proceedings. If a relief or a plea is covered by necessary implication then omission to expressly take such plea or seek such relief would not disentitle a party to seek the requisite relief provided he satisfactorily establishes his case in evidence. Where a matter is even obscurely touched in the issues involved and evidence has been led on it then any objection to it would only be technical and has to be rejected. All that a Court is required to examine is whether the parties were aware of the questions involved in a controversy and they had led evidence and on such examining it can either grant or reject the requisite relief depending upon the merits of the case.
 
(b) Suit for partition---
 
---When a party fails in establishing its claim, but one of the opposing parties has admitted such claim then the party admitting the claim has to honour its admission to the extent of his share in the property and the party claiming the share would become entitled to claim its shares in the property on the basis of admission by the other party only to the extent of the shares which it held in the property.
 
(c) Limitation Act (IX of 1908)---
 
---Art. 127---Specific Relief Act (I of 1877), S.39---Suit for partition of joint family property/cancellation of document on the basis of being a product of fraud and forgery---Limitation---Property in question being joint family property, Art.127, Limitation Act, 1908 was attracted to the case.
 
1981 CLC 503 ref.
 
(d) Evidence---
 
---When a person takes a false plea then there is every possibility that at different stages of pleadings he makes contradictory statements of suiting a particular situation.
 
(e) Transfer of Property Act (IV of 1882)---
 
---S. 54---Power of attorney---Transfer of property by attorney---Onus to prove the consent of principal and good faith of the transaction---Principles.
 
Where members of a family hold property in common and any member of such family is in occupation or management of the' joint family property then such person stands in active confidence of other co-owners. Any exercise of power either in his own favour or in favour of his close fiduciary relation, whereby the joint property is claimed to have been sold with the consent of all other members, then the onus to prove such consent as well as good faith of the transaction is upon him. Unless consent as well as good faith, both are established, any transfer of property has to be regarded as nullity. In such cases even where Power of Attorney is executed by family members in favour of one of them, what needs to be examined is whether such power was exercised as a shield to cover-up fraudulent nature of the transaction.
 
(f) Transfer of Property Act IV of 1882)---
 
----S. 54---Power of attorney---Transfer of property by attorney holding subsisting power of attorney which has not been revoked on the date of the alleged sale transaction entered into by the attorney in favour of his own or in favour of his near or dear one---Such a sale transaction can be successfully questioned in a Court of law if it is established that it was a product of fraud and deceit---Such a transaction can always be nullified, if it is proved that it was sham and based on dishonest intentions of a person who stood in active confidence of the owners of a property.
 
Maqsood Ahmad v. Salman Ali PLD 2003 SC 31 and Jamil Akhtar v. Las Baba PLD 2003 SC 494 ref.
 
Saeeduddin Nasir for Plaintiff (in Suit No.696 of 1987)
 
Saeeduddin Nasir for Defendants Nos.3 to 5 in (Suit No.554 of 1987).
 
Haleem Siddiqui for Defendant No.1 (in Suit No.696 of 1987 and 554 of 1987).
 
Defendant No.2 (in Suit No.696 of 1987) and Plaintiff (in Suit No.554 of 1987) in person.
 
Date of hearing: 14th March, 2006.
 
JUDGMENT
 
Case 76
2006 C L C 1309
 
[Karachi]
 
Before Muhammad Sadiq Leghari and Mrs. Yasmeen Abbasey, JJ
 
MANAGER, MUSLIM COMMERCIAL BANK LIMITED and another---Applicants
 
Versus
 
BABAR---Respondent
 
R.A. No.21 of 2002, decided on 21st March, 2006.
 
(a) Negotiable Instruments Act (XXVI of 1881)---
 
----S. 13---Cheque, a negotiable instrument---Scope---Term negotiable instrument as defined in Negotiable Instruments Act, 1881, means a promissory note, bill of exchange or cheque payable either to order or to bearer---Term 'cheque' has been expressed as 'bill of exchange drawn on a specified branch and not expressed to be payable otherwise than on demand.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. XXXVII, Rr.2 & 3---Recovery of amount on the basis of cheque---Conditional leave to defend the suit---Deposit of indemnity bond as bank guarantee--Validity,--Condition of furnishing surety in the form of indemnity bond as bank guarantee having a firm identity was more than what was required, because purpose of execution of indemnity bond was to oblige the indemnifier against loss sustained by him from the conduct of person for whom he stood surety---Whereas in the present case it was yet to be determined as to where the fault lay---Order of Trial Court was modified to the extent that defendant was not required to furnish surety in the form of indemnity bond---High Court allowed the defendant to defend the suit as already leave had been granted to him but without any condition---Revision was allowed accordingly.
 
Naveed-ul-Haque for Applicants.
 
ORDER
 
Case 77
 
2006 C L C 1319
 
[Karachi]
 
Before Sarmad Jalal Osmany and Amir Mani Muslim, JJ
 
SOHAIL AKHTAR ABBASI---Petitioner
 
Versus
 
Syed AMIR ALI SHAH and 9 others---Respondents
 
Constitutional Petition No. D-239 and C.M.A. No.598 of 2006, heard on 12th April, 2006.
(a) Sindh Local Government Elections Rules, 2005---
 
----R. 30(b)(ii)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Voter has to put the mark and rubber stamp on the ballot paper at the place within the space containing the symbol of contesting candidate of his choice---Rule 30(b)(ii) of the Local Government Elections Rules, 2005 does not permit the voter to mark the stamp twice in such manner that its impression appears against the name of another candidate---Such double stamped votes are spoiled votes and were rightly excluded from the count by the Election Tribunal.
 
(b) Sindh Local Government Elections Rules, 2005---
 
----R. 36---Constitution of Pakistan (1973), Art.199---Constitutional petition---Counting and recounting of the votes is confined to the ballot papers which are detached from the counterfoils and given to the voter---Provision of R.36, Local Government Elections Rules, 2005 pertains to the count of ballot papers/votes and does not include the examination and counting of counterfoils.
 
Raza Hashmi for Petitioner.
 
Imdad Ali Awan for Respondents.
 
Ghulam Dastagir Shahani, Addl. A.-G.
 
ORDER
 
Case 78
2006 C L C 1328
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
NUZHAD AQUIL NAWAB----Petitioner
 
Versus
 
REHAN NAWAB----Respondent
 
Execution Application No.64 of 1999, decided on 6th February, 2006.
 
Civil Procedure Code (V of 1908)---
 
----S. 44-A---Scope and application of S.44-A, C.P.C.---United States of America being not reciprocating territory under S.44-A, C.P.C., the decree passed by a Court in U.S.A. could not be executed in Pakistan ---Understanding between the parties could not change legal provision.
 
Abu Saeed A. Islahi v. Talat Mir and 2 others 1994 MLD 1370 and Munawar Ali Khan and others v. Marfani & Co. Ltd. SBLR 2003 Sindh 1048 ref.
 
Brijlal Ramjidas and another v. Govindaram Gordhandas Seksaria AIR (34) 1947 PC 192 distinguished.
 
Ashfaq Hussain for Decree-holder.
 
Farrukh Zia Shaikh for Judgment-debtor.
 
Date of hearing: 25th January, 2006.
 
JUDGMENT
 
Case 79
 
2006 C L C 1365
 
[Karachi]
 
Before Mrs. Qaisar Iqbal, J
 
PERVEZ IQBAL----Applicant
 
Versus
 
Mrs. RANA/NADIA IQBAL SIDDIQUI----Respondent
 
C.M.A. No.6042 of 2004 in Suit No.914 of 2004, decided on 8th March, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. I, R.10(2)---Party in suit, addition of---Scope---Such addition could be made in order to enable Court to adjudicate upon 4nd settle effectually and completely all questions involved therein.
 
(b) Special Relief Act (I of 1877)---
 
---S. 12---Civil Procedure Code (V of 1908), 0.I, R.10(2)---Suit for specific performance of agreement to sell---Denial of agreement of defendant---Application by intervenor to be impleaded as party alleging to have issued receipt for an amount partly paid by plaintiff to defendant---Validity---Plaintiff could summon intervenor as witness to prove part payment to defendant---No cause of action had been shown by plaintiff against intervenor---Intervenor was not enjoying any status out of alleged agreement---Intervenor was neither necessary nor proper party in suit.
 
Arshad Iqbal for Applicant.
 
Muhammad Aqil for Respondent.
 
ORDER
 
Case 80
 
2006 C L C 1367
 
[Peshawar]
 
Before Salim Khan and Hamid Farooq Durrani, JJ
 
KHUSH RANG KHAN, GENERAL COUNCILLOR, UNION COUNCIL BHIRKHUND DISTRICT, MANSEHRA----Petitioner
 
Versus
 
GOVERNMENT OF N.-W.F.P. through Secretary Local Government and Rural Development N.-W.F.P., Peshawar and 4 others----Respondents
 
Writ Petitions Nos.128 to 131 of 2006, decided on 14th June, 2006.
 
North-West Frontier Province Local Government Ordinance (XIV of 2001)---
 
----Ss. 85 & 136---Constitution of Pakistan (1973), Art.199---Constitutional petition---Internal recall of Union Nazim---Application/notice for---Applicants, who were elected Union Councillors submitted an application/notice to Naib Nazim concerned for convening a meeting of the union for the internal recall of Union Nazim---Applicants had alleged that in their opinion Union Nazim was acting against the public policy, against the interest of the people and had neglected work of the residents of the Union Council and in doing so he had lost the confidence of the members of the Union Council---Naib Nazim, before whom application was filed admitted that he received written application/notice of applicants, but he did not call the session as he believed that powers and functions of applicants had been suspended by the Zilla Nazim---Zilla Nazim, in his comments had denied that he had suspended the powers and functions of applicants and had contended that only notice was sent to applicants to provide them a chance of hearing in their matter---Applicants, in circumstances, were fullfledged members of concerned Union Council until a decision was finally given against them for their removal from such membership and they had all the powers and functions, as well as the rights and liabilities of such membership of the Union Council concerned---Naib Nazim had no authority to postpone calling of session of Union Council on the ground that applicants as members had no power and functions which were allegedly suspended/ held in abeyance by Zilla Nazim illegally---High Court, declared that as Zilla Nazim had already withdrawn' his illegal order of suspending/ holding in abeyance powers and function of applicants, Naib Nazim was duty bound to call session of Union Council within next three days.
 
Naz Ellahi Moghal for Petitioner.
 
D.A.-G. and Nisar Hussain Khan for Respondents.
 
Respondent No.4 in person.
 
Date of hearing: 14th June, 2006.
 
JUDGMENT
 
Case 81

2006 C L C 1372
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui and Sajjad Ali Shah, JJ
 
KARACHI PROPERTIES INVESTMENT COMPANY (PRIVATE) LIMITED----Petitioner
 
Versus
 
GOVERNMENT OF SINDH through Secretary, Ministry of Finance and Excise and Taxation Department Sindh, Karachi and another--Respondents
 
C.Ps. Nos.D-1893, of 2002, D-251 of 2003, D-514 of 2005 and D-618 of 2003, decided on 2nd June, 2006.
 
(a) West Pakistan Urban Immovable Property Tax Act (V of 1958)---
 
----S. 5-A [as added by Sindh Finance Ordinance (VII of 2001)]---Provisional Constitution Order (1 of 1999), Preamble---Provisional Constitution (Amendment) Order (9 of 1999), Preamble---Constitution of Pakistan (1973), Art.128---Sindh Finance Ordinance, 2000 [inserting S.5-A in West Pakistan Urban Immovable Property Tax Act, 1958] was promulgated during period when Provincial Assembly was not in existence; Ordinance was not a temporary legislation, but was permanent legislation protected by the Constitution---Validity of Ordinance, could not be challenged.
 
(b) West Pakistan Urban Immovable Property Tax Act (V of 1958)---
 
----Ss. 3, 5 & 5-A [as added by Sindh Finance Ordinance (VII of 2000)]---Stamp Act (II of 1899), S.27-A---Property tax, determination of---Valuation Tables to ascertain gross annual rental value of property---Validity---Valuation Tables issued by Excise and Taxation Department under S.5-A of West Pakistan Urban Immovable Property Tax Act, 1958 was entirely different from Valuation Tables issued by Sindh Board of Revenue for purpose of Stamp Act, 1899 and Registration Act, 1908---Prior to issuance of Valuation Tables under S.5-A of West Pakistan Urban Immovable Property Tax Act, 1958, wide ranging survey was conducted, data forms were distributed, information was. collected, opportunity for filing objections were provided---Valuation Tables issued by Excise and Taxation Department were not violative of Ss.3, 5 & 5-A of the Act.
 
Government of Punjab v. Jamshed Waheed Civil Petition No.1435 of 2001 ref.
 
Ameenuddin Ansari for Petitioner (in C.P. No.D-1893 of 2002).
 
Shahanshah Hussain for Petitioner (in C.P. No. D-251 of 2003 and in C.P. No.D-514 of 2005).
 
Rehman Aziz for Petitioner (in C.P. No.D-618 of 2003).
 
Ahmad Pirzada, Addl. A.-G., Sindh along with Dr. Iqbal Seehar D.D.O. Property Tax.
 
Date of hearing: 8th November, 2005.
 
JUDGMENT
 
Case 82
 
2006 C L C 1390
 
[Karachi]
 
Before Ali Sain Dino Metlo, J
 
RIASAT ALI----Applicant
 
Versus
 
MUHAMMAD YASEEN through Legal Heirs and another----Respondents
 
Civil Revision No.92 of 2002, decided on 13th January, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 151---Consolidation of suits---Principles and object---No separate statutory provision exists for consolidation of suits---Courts in exercise of their discretionary inherent powers, have been, in appropriate cases, consolidating suits for the sake of convenience and expediency so as to save time and labour and also to avoid possibility of any conflict in findings---Since consolidation is made on the principles of convenience and expediency, stage of proceedings have to be taken into consideration as an important fact---Normally consolidation should be made at initial stage of trial and the best time for doing so is the stage of framing of issues---Resort to consolidation may not be taken when the suits or any of them is at final stage and ripe for decision or when they or any of them has already been decided for that may be a cause of great inconvenience and prejudice at least to a successful party.
 
(b) Civil Procedure Code (V of 1908)---
 
---Ss. 151 & 115---Revision---Consolidation of suits---Cross-suits were filed by the parties against each other---Suit filed by the petitioner proceeded and was decreed by Trial Court, whereas respondents did not proceed with the suit filed by them---Appellate Court allowed the appeal filed by respondents and after setting aside the judgment and decree passed by Trial Court, remanded the case to Trial Court for deciding both the suits together after consolidating them---Validity---When respondents chose not to proceed with their own suit and opted only to defend the suit filed by petitioner, it would not be fair to deprive him from the decree passed in his favour after fully contesting the suit---Practice and principle of consolidating suits being discretionary and not mandatory, its non-observance could not be given the effect of invalidating the proceedings so as to set aside the decree only for such reason---Judgment and decree passed by Appellate Court was set aside and the case was remanded to Appellate Court for deciding appeal afresh on merits---Revision was allowed in circumstances.
 
Saleem Akhtar Buriro for Applicant.
 
Nemo for Respondents.
 
Date of hearing: 13th January, 2006.
 
JUDGMENT
 
Case 83
 
2006 C L C 1401
 
[Karachi]
 
Before Ali Sain Dino Metlo, J
 
Mst. FATIMA through L.Rs.----Applicants
 
Versus
 
JAN MUHAMMAD through L.Rs.----Respondents
 
Civil Revision No.91 of 1988, decided on 13th January, 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 12---Civil Procedure Code (V of 1908), 5.115---Suit for specific performance of agreement to sell---Revisional jurisdiction---Conflicting findings/concurrent findings by Courts below---Reappraisal of evidence---Scope---Where no non-reading or misreading of evidence by the Appellate Court or any other violation of any principle of appreciation of evidence was pointed out, concurrent findings of the two Courts regarding execution of the agreement and receipt of consideration by the seller and possession of the property with the purchaser, were unexceptionable, inasmuch as, the seller, in his written statement had admitted the execution of agreement and receipt of money and the only witness examined from the side of seller admitted in his examination-in-Chief, that the purchaser was in possession of the land since the date of the execution of the agreement.
 
PLD 2000 SC 839 and PLD 2001 SC 67 ref.
 
(b) Specific Relief Act (I of 1877)---
 
----S. 12---Limitation Act (IX of 1908), Art.113---Suit for specific performance of agreement to sell---Limitation---Conditional fixation of date for performance of agreement---Effect---Seller being incapable to perform the contract, date fixed for its performance became irrelevant and could not be treated as the starting point of the period of limitation---Period of limitation, in circumstances would start "when the plaintiff had notice that performance was refused"---Contention of the seller that, owing to the time being the essence of the contract and the delay in filing the suit, the purchaser was not entitled to the discretionary relief of specific performance, was misconceived because time was not of the essence of the contract and the delay was due to the incapability of the seller to perform his part of the contract---Major part of the consideration had been paid to the seller and the property was in the possession of the purchaser, who was always ready to pay the balance and the date fixed for the performance of contract, contract was not final in the sense that it was subject to the seller's ability to perform the contract on making arrangement for the sale of his remaining land, which he had not been able to make so far---Principles.
 
According to Article 113 of the Limitation Act, 1908, suit for specific performance of a contract can be filed within three years of 'the date fixed for the performance, or, if 'no such date is fixed, when the plaintiff has notice that performance is refused'. No doubt, in the present case, the date for the performance was fixed but it was conditional on the seller's making arrangement for the sale of his remaining land in the Deh. Admittedly, the seller could not alienate the land to the purchaser on the fixed date without making arrangement for the sale of his remaining land. It was not the case of the seller that he had made the arrangement. On the contrary, the contention of the purchaser that the seller had failed to make the arrangement stood admitted by the witness who, in his cross-examination, stated that the other land of the seller was in dispute which was settled only recently. Thus, it was clear that the seller was incapable to perform the contract. Therefore; the date fixed for its performance became irrelevant and could not be treated as the starting point of the period of limitation. In the cases, like the present one, where the contract was incapable of performance on the date fixed, the period of limitation would be governed by second and not first part of Article 113 and the period of limitation would start 'when the plaintiff has notice that performance is refused'. The contention of the seller that he had notice of refusal of performance just before the filing of the suit had gone unrebutted. It was not the case of the seller that performance was refused at any earlier point of time. As a matter of fact, no. notice about the performance of contract or its refusal was given to the purchaser and the land was admittedly all along in his possession. In such circumstances, the finding of the appellate Court that the suit was not time-barred was quite correct in law as well as on facts and was, therefore, unexceptionable.
 
The contention of the seller that, owing to the time being the essence of the contract and the delay in filing the suit, the purchaser was not entitled to the discretionary relief of specific performance was also misconceived because time was not the essence of the contract and the delay was due to the incapability of the seller to perform his part of the contract. Major part of the consideration had been paid to the seller and the land was in the possession of the purchaser, who was always ready to pay the balance and the date fixed for the performance of contract was not final in the sense that it was subject to the seller's ability to perform the contract on making arrangement for the sale of his remaining land, which he had not been able to make.
 
Muhammad Bashir v. Hakim Ali 2000 YLR 368 ref.
 
2004 SCMR 436 and FLU 1988 Lah. 717 distinguished.
 
(c) Specific Relief Act (I of 1877)---
 
---S. 12--Civil Procedure Code (V of 1908), 5.115---Suit for specific performance of agreement to sell---Revision---Contention was that Appellate Court, while allowing the appeal did not specify the relief granted by it and, therefore, the judgment being, unspecific, was liable to be set aside---Validity---Only logical inference which could be drawn from the order of allowing the appeal would be that the suit, which was dismissed by the Trial Court, was decreed by the Appellate Court---Appellate Court, however, ought to have decreed the suit conditionally on payment of the balance consideration---Judgment of the Appellate Court was, therefore, modified by the High Court to the extent that the suit was decreed subject to the purchaser's depositing the balance consideration in the Trial Court within two months of the announcement of the judgment of High Court and in case the amount was not deposited within the period specified, the suit shall stand dismissed.
 
A.M. Mobeen Khan for Applicants.
 
Nemo for Respondents.
 
Date of hearing: 13th January, 2006.
 
JUDGMENT
 
Case 84
 
2006 C L C 1416
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
Syed FEROZE ALI----Petitioner
 
Versus
 
IVTH ADDITIONAL DISTRICT AND SESSIONS JUDGE, KARACHI CENTRAL and 2 others----Respondents
 
Constitution Petition No.115 of 2006, heard on 7th April, 2006.
 
(a) Sindh Rented Premises Ordinance (XVII of 1979)---
 
----S. 15(2)(ii) & 18---Default in payment of rent---Change of ownership through registered sale-deed---Notice to tenant by new landlord---Refusal of tenant to acknowledge ownership of new landlord---Deposit of rent in Court by tenant in the name of previous landlord despite service of notice---Validity---After purchase of premises by new landlord, tenant automatically became his tenant under the statute and liable to pay/tender him rent due---Tenant committed deliberate default in circumstances.
 
(b) Sindh Rented Premises Ordinance (XVII of 1979)
 
---S. 15(2)-Bona fide personal need of landlord---Proof---Landlord deposed that he was staying with his family in a rented house and required disputed premises for personal use---Such statement of landlord was not shaken in cross-examination---Tenant's simple denial of need to be bona fide, would not carry any weight as personal bona fide requirement of landlord was established in circumstances.
 
Muhammad Aquil for petitioner.
 
Ibadul Hussnain for Respondent No.2.
 
Date of hearing: 7th April, 2006.
 
JUDGMENT
 
Case 85
 
2006 C L C 1434
 
[Karachi]
 
Before Muhammad Mujeebullah Siddiqui, J
 
Messrs TEXZONE----Petitioner
 
Versus
 
THE ADDITIONAL COLLECTOR OF CUSTOMS, EXPORT COLLECTORATE, CUSTOM HOUSE, KARACHI and another----Respondents
 
Special Customs Appeal No.4 of 2005, C.M.As. Nos.175 and 176 of 2006, decided on 20th March, 2006.
 
Limitation Act (IX of 1908)---
 
----S. 5--Customs Act (IV of 1969), S.196-Application for condonation of delay and restoration of appeal dismissed in default on two dates of hearing---Contention of the appellant's counsel was that although his name was printed in the cause list but he could not appear, as no intimation notice was issued to him, and he had gone out of city, he could not see the cause list---Validity---Held, printing of the name of Advocate of parties in the cause list was sufficient notice and it was the duty of Advocates to go through the cause list and no further notice was required to be issued---No sufficient explanation having been given for non-appearance on two dates of hearing when the matter was fixed for Katcha Peshi, no case was made out either for condonation of delay or for restoration of the appeal---Application was dismissed.
 
Muhammad Aleem Khan for Appellant.
 
Raja M. Iqbal for Respondents.
 
ORDER
 
Case 86
 
2006 C L C 1574
 
[Karachi]
 
Before Gulzar Ahmed, J
 
IBRAHIM FIBRES LIMITED through General Manager----Plaintiff
 
Versus
 
COLLECTOR OF CUSTOMS (APPRAISEMENT), KARACHI and another----Defendants
 
Suit No.880 of 2001, decided on 21st June, 2006.
 
Specific Relief Act (I of 1877)---
 
----Ss. 42, 54 & 55---Civil Procedure Code (V of 1908), O.XXXIX, Rr.1, 2 & 4-A---Suit for declaration, permanent and mandatory injunction---Interim stay orders, extension of---Interim stay was granted to plaintiff on his furnishing Bank guarantee till next date---Said interim orders continued uptill the date when the matter was adjourned---By consent the matter was fixed for hearing of final arguments and plaintiff had filed application for extension of stay orders---Interim orders were extended till date of hearing---High Court observed that if suit was not proceeded on fixed date for any reason attributable to plaintiff or his counsel, interim order passed in the case would stand automatically vacated.
 
Raja Tilat Mehmood v. Ismat Ahteshamul Haq 1999 SCMR 2215 ref.
 
Farogh Nasim holding brief for Khawaja Shamsul Islam for Plaintiff.
 
Raja M. Iqbal for Custom Department.
 
Asghar Farooqui, Standing Counsel.
 
 
ORDER
 
Case 87
 
2006 C L C 1589
 
[Karachi]
 
Before Muhammad Sadiq Leghari, J
 
NASEEM AKHTAR alias LALI---Appellant
 
Versus
 
KHUDA BUX PECHOHO and others---Respondents
 
M.A. No.39 of 2004, decided on 19th June, 2006.
 
Succession Act (XXXIX of 1925)---
 
----S. 371---Federal Employees Benevolent Fund and Group Insurance Act (II of 1969), Ss.2(5), 11, 14, 17 & 19---West Pakistan Civil Services Pension Rules, 1963, Rr.4.6 & 4.8(c)---Civil Procedure Code (V of 1908), S.104---Application for grant of succession certificate in respect of legal monetary claims of deceased employee---Entitlement to monetary claims---Appeal against orders---Employee serving as Upper Divisional Clerk, died leaving behind her one son and two daughters--After death of said employee, her mother filed application for grant of succession certificate in respect of legal monetary claims to be paid by the department on death of deceased employee---Mother of deceased in her application pleaded that husband of deceased lady having divorced her in her life time, he was not entitled to get any share out of said claim---Husband of deceased claimed that he had never divorced the deceased lady and that she remained his wife till her death---Application of mother of deceased was finally dismissed holding that she could not prove that husband of deceased had divorced deceased lady and that mother of deceased lady had no right over the monetary legal claim payable on demise of said lady---Husband of deceased lady thereafter filed application for grant of succession certificate in respect of monetary claims which application was granted declaring husband of deceased alone to be entitled to receive monetary claims of deceased lady---Validity---Question of divorce allegedly pronounced by husband of deceased was considered and decided up to level of High Court in earlier round of litigation---Court below had rightly found that husband , had not divorced deceased lady---Husband was found to be entitled to certain legal monetary claims---Among said monetary claims, Benevolent Fund and Group Insurance, were to be regulated by Federal Employees Benevolent Fund and Group Insurance Act, 1969 and under provisions of Ss.14 & 19 of said Act, those two amounts were to be paid to a person or persons nominated by employee; in absence of any valid nomination made by deceased, said amount were to be paid directly to members of family of deceased for just and equitable utilization for the maintenance and benefit of all members of her family---Son and daughters of deceased who were major and married, were not living with husband of deceased---Grant from Benevolent Fund and Group Insurance Fund would be paid to the husband---General Provident Fund which would come within preview of `Tarka' of deceased would be inherited by all legal heirs of deceased---Pension and commutation was to be paid to family of deceased, under provisions of R.4.6 of West Pakistan Civil Servants Pensions Rules, 1963---Husband, one son and one unmarried daughter were entitled to said claim---Salary of 180 days of deceased would be paid to legal heirs of deceased according to Islamic Law.?
 
Ameeran Khatoon's case PLD 2005 SC 512 and Mirza Muhammad Amin v. Government of Pakistan PLD 1982 FSC 143 ref.
 
Karamat Illahi for Appellant.
 
Abbad-ul-Hassnain for Respondents.
 
Date of hearing: 5th May, 2006.
 
 
JUDGMENT
 
Case 88
 
2006 C L C 1606
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
MUMTAZ ALI----Petitioner
 
Versus
 
Mst. SALMA and others----Respondents
 
C.P. No.163 of 2005, decided on 21st March, 2006.
 
Guardians and Wards Act (VIII of 1890)---
 
----S. 25---Custody of minor---Welfare of minor was a paramount consideration and since ward was subject matter of such proceedings, the Courts exercising parental jurisdiction must keep interest and welfare of minor in mind in matter of his custody.
 
PLD 1994 (AJ&K) 1; 1985 SCMR 1367; PLD 1987 Lah. 263;PLD 1995 Lah. 441; 1998 SCMR 1593; 1995 CLC 800; 2002 CLC 1416; 2003 SCMR 1344; 1973 MLD 202 and 2002 SCMR 821 ref.
 
Muhammad Yousuf Leghari for Petitioner.
 
S.A. Shoukat Naqvi for Respondents.
 
 
ORDER
 
Case 89
 
2006 C L C 1621
 
[Karachi]
 
Before Nadeem Azhar Siddiqi, J
 
KASHIF ANWAR----Applicant
 
Versus
 
AGHA KHAN UNIVERSITY----Respondent
 
Civil Miscellaneous Application No.8246 of 2005 in Suit No.1293 of 2005, decided on 2nd June, 2006.
 
Specific Relief Act (I of 1877)---
 
----Ss. 42 & 54---Agha Khan University Disciplinary Procedure Rules, Rr. 2 & 3---Civil Procedure Code (V of 1908), O.XXXIX, Rr. 1 & 2---Interim injunction, grant of---Disciplinary action---Expulsion of student from medical college---Plaintiff was student of Agha Khan Medical University, and was expelled from college on disciplinary offences--Plaintiff sought order restraining college authorities from barring him from continuing with his medical education at the University---Contention of authorities was that grant of such interim relief would amount to grant of final relief---Validity---Relief claimed in the application was temporary in nature---Any relief granted while hearing application under O.XXXIX, Rr.1 and 2 C.P.C. was subject to final adjudication of the suit---Granting of temporary relief did not amount to grant of final relief as in case the suit was dismissed, the interim order would merge in the final order and no right could be claimed by plaintiff on the basis of interim order---As far as mandatory injunction was concerned, the plaintiff had only claimed that he might be allowed to continue with his medical studies---Such relief could be granted subject to decision in the suit and would not amount to grant of mandatory injunction at interlocutory stage---By applying the principle of moulding the relief, same could be granted by way of suspending the operation of expulsion order---Grant of mandatory injunction was permissible on showing a very strong prima facie case---Career of a student was involved and in case injunction was not granted and in the end the suit was dismissed no harm would be caused to anyone but in case the suit was decreed, the plaintiff would suffer irreparable loss, which could not be calculated in terms of money---Class fellows of the plaintiff were already one year ahead from the plaintiff and in case injunction was not granted the plaintiff would not be in a position to compete them and his career as a medical student would come to an end---High Court allowed the plaintiff to continue his classes at his own cost and risk, subject to decision of the suit---Application was allowed accordingly.?
 
Majid Malik v. Karachi Grammar School 2004 CLC 1029; Dacca University v. Zakir Ahmed PLD 1965 SC 90; Raziuddin v. PIA PLD 1992 SC 531; University of Punjab v. M. Zaheer 1985 SCMR 802; Muhammad Ilyas v. Islamia University 2000 MLD 228; M. Farukh Fayyaz v. Aitchison College Lahore 1997 MLD 928 and Shehla Rubab v. Mst. Nighat Saifullah Khan 1996 MLD 1099 ref.
 
Ferozuddin Ahmed v. TCP 1987 MLD 124; Muhammad Yousuf v. Ahmed Saeed 1999 MLD 3354; Iftikhar Siddiqi v. Clifton Cantonment Board PLD 1988 Kar. 373 and M. Ayub v. Pakistan 2001 YLR 3030 distinguished.
 
Salahuddin Ahmed for Applicant/Plaintiff.
 
Qazi Faez Isa for Respondent/Defendant.
 
 
ORDER
 
Case 90
2006 C L C 1637
 
[Karachi]
 
Before Syed Zawwar Hussain Jafery and Amir Hani Muslim, JJ
 
HASHMAT MAL----Petitioner
 
Versus
 
CHIEF ELECTION COMMISSIONER OF PAKISTAN, ISLAMABAD and 6 others----Respondents
 
C.P. No.D-113 of 2006, decided on 24th May, 2006.
 
Sindh Local Government Elections Rules, 2005---
 
----R. 65---Constitution of Pakistan (1973), Art.199---Constitutional petition---Re-counting and re-checking of votes---Petitioner, who contested Local Bodies Election for Councillor on minority seat, having been declared as (returned candidate), unsuccessful candidate filed election petition challenging election of returned candidate---Unsuccessful candidate prayed in his election petition to re-count and re-check votes of petitioner and his votes---Parties consented that election petition be disposed of on basis of results of re-count and Returning Officer undertook exercise of re-counting---On re-counting despite declaring that petitioner had secured more votes Returning Officer, instead of dismissing election petition on result of re-count, had travelled beyond prayers made in election petition---Returning Officer, without framing issues and recording evidence, had allowed election petition, holding the election nullity and declared un-success candidate as "returned candidate"---Validity--Relief granted by Returning Officer, was beyond prayers of election petition---Candidate had confined his relief in election petition to re-counting of votes which was done with consent of parties, but Returning Officer travelling beyond prayers in election petition, declared that petitioner returned candidate had secured more votes by casting bogus votes---No material was available before Returning Officer to declare the unsuccessful candidate as returned candidate who admittedly had secured less votes than returned candidate-Returning Officer did not merely commit an error of law, but had violated essential norms of judicial conduct in recording such perverse judgment---Order passed by Returning Officer did not reflect only inefficiency and ignorance of law, but, prima facie, appeared to be tainted with ulterior motive---Constitutional petition against impugned order of Returning Officer, passed in election petition, was allowed.
 
Kalandar Bux Phulpoto for Petitioner.
 
Mukesh Kumar G. Karara for Respondents No.5.
 
?A.R. Faruq Pirzada D.A.-G.
 
Date of hearing: 11th May, 2006.
 
 
JUDGMENT
 
Case 91
 
2006 C L C 1655
 
[Karachi]
 
Before Muhammad Ather Saeed, J
 
DIRECTOR, EXCISE AND TAXATION----Petitioner
 
Versus
 
MUHAMMAD AMIN WAQF----Respondent
 
Constitution Petition No.9 of 2003, head on 19th December, 2005.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
----Ss. 16(I)(2) & 21---Constitution of Pakistan (1973), Art.199---Constitutional petition---Order striking off defence---Appeal against---Application filed by landlord for striking off defence of tenant for non-compliance of tentative rent order having been dismissed by Rent Controller, landlord filed appeal against dismissal order which was allowed by impugned order whereby defence of tenant was struck off---Contention of tenant was that order striking off defence passed by Rent Controller under S.16(2) of Sindh Rented Premises Ordinance, 1979 being interim order in nature, same was not appealable under S.21 of Sindh Rented Premises Ordinance, 1979---Landlord had contended that order passed under S.16 of Sindh Rented Premises Ordinance, 1979, was not an interim order, but was a final order---Validity---Held, order passed under S.16(2) of Sindh Rented Premises Ordinance, 1979 in circumstances was appealable---Constitutional petition being devoid of merits, was dismissed.
 
Gurdasmal v. Pahlaj Ram and another 1986 CLC 43; Mrs. Zubaida Begum v. Mrs. S.T. Naqvi 1986 SCMR 261; Mst. Anwar Fatima and 5 others v. Muhammad Ali Mutlaq PLD 1986 Kar. 252; Mrs. Khairun Nisa and another v. Mrs. Mehrun Nisa 1990 CLC 661; Gatron (Industries) Limited v. Government of Pakistan 1999 SCMR 1072; Muhammad Sharif and another v. Muhammad Afzal Sohail and others PLD 1981 SC 246; Saifullah v. Muhammad Bux and 2 others 2003 MLD 480; Secretary to the Government of the Punjab Forest Department, Punjab, Lahore v. Ghulam Nabi and 3 others PLD 2001 SC 415; Messrs Mehraj (Pvt.) Ltd. Miss Laima Saeed and others 2003 MLD 1033 and Hafiz Shafatullah v. Mst. Shamim Jahan and another PLD 2004 Kar. 502 ref.
 
Muhammad Qasim Mirjat, A.A.-G. Sindh for Petitioner.
 
Iqbal Ahmed for Respondent No.1.
 
Date of hearing: 19th December, 2005.
 
 
JUDGMENT
 
Case 92
 
2006 C L C 1662
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
BABAR ISMAIL----Petitioner
 
Versus
 
Mst. SHEEBA BASHIR and another----Respondents
 
C.P.S. No.36 of 2006, decided on 24th March, 2006.
 
West Pakistan Family Courts Act (XXXV of 1964)---
 
---Ss. 5, Sched. & 10(4)---Dissolution of marriage on ground of Khula---Dower amount, if was already paid to wife, was to be restored to husband and if was unpaid, it was not to be paid to wife as she had to forego that amount in lieu of Khula---Interpretation that word dissolution mentioned in proviso to S.10(4) of West Pakistan Family Courts Act, 1964 did not include Khula, seemed to be incorrect as no other procedure had been provided for grant of Khula under the law---Khula itself ,was a kind of dissolution according to the law---Khula was to be granted when dower amount was restored or to be foregone.
 
PLD 2006 Lah. 158 ref.
 
Amjad Ali Sehto for Petitioner.
 
Naimatullah Soomro for Respondents.
 
 
ORDER
 
Case 93
 
2006 C L C 1678
 
[Karachi]
 
Before Khilji Arif Hussain, J
 
M.S. PORT SERVICES (PVT.) LIMITED----Plaintiff
 
Versus
 
PORT QASIM AUTHORITY----Defendant
 
Suit No.1156 of 2003, heard on 4th May, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----Preamble & S.9---Arbitration Act (X of 1940), Preamble---Applicability of general rule of C.P.C. to arbitration proceedings---Scope---General rule of Code of Civil Procedure though was applicable to all proceedings of civil nature, but scheme of Arbitration Act, 1940 was to curtail litigation in regular Court to get disputes settled by avoiding all types of procedural law---Technical rules of procedure contained in Code of Civil Procedure were not extended to arbitration proceedings---Provisions of C.P.C. were made available to all proceedings before the Court and not before arbitrator.
 
Messrs Haji Hasham Haji Ahmed & Bros. V. Messrs Trading Corporation of Pakistan Ltd. Karachi PLD 1977 Kar. 480 and Abdul Sattar Mandokhal v. Port Qasim Authority 2000 YLR 758 ref.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
--Arts. 1(2) & 18--Civil Procedure Code (V of 1908), O. XVI, Rr. 1 & 6---Examining witness---Restriction---Article 1 of Qanun-e-Shahadat 1984, though had excluded its applicability to proceedings before an arbitrator, but there was no provision of law under which Court could put restriction upon the right of a party to examine witnesses in support of his claim---Court/Arbitrator at the time of recording evidence was to see whether questions put to the witnesses were relevant to the dispute in the matter or not, but request to call a witness, except in exceptional circumstances, could not be denied.
 
Khalid Mahmood Siddiqui for Plaintiff.
 
Zahid F. Ebrahim for Defendant.
 
 
ORDER
 
Case 94
 
2006 C L C 1691
 
[Karachi]
 
Before Shabbir Ahmed, Ghulam Rabbani and Khilji Arif Hussain, JJ
 
Miss KHADEEJA KHAN KHANDHARI----Petitioner
 
Versus
 
PRINCIPAL AND CHAIRMAN, ACADEMIC COUNCIL, SINDH MEDICAL COLLEGE and others----Respondents
 
C.Ps. Nos.D-161, 162, 163, 183, 188, 219, 241, 279, 301, 307, 470, 473, 482 and 606 of 2003, decided on 18th May, 2004.
 
(a) Sindh Medical Colleges Act (V of 1987)---
 
----S. 3---Admission in medical college---Procedure---Candidate desirous of obtaining admission in one of the medical colleges of Karachi was required firstly to have the qualification i.e. Intermediate Science Certificate with not less than 60% marks, secondly he must be domiciled in District Karachi, Sindh---Applicant had to apply to the Centre nominated for receiving such applications i.e. Dow Medical College and there were three categories of seats, (i) on merits, District-wise, (ii) reserved seats and last (iii) reciprocal seats with medical colleges of Punjab---There was no quota for Chief Minister against Reserved Seats---No admission in medical college in Sindh was permissible except in terms of relevant prospectus, which itself had to be in consonance with the provisions of Sindh Medical Colleges Act, 1987---Selection of candidate for admission by Board, nominated by Government, in accordance with overall merits and display of list on notice board and allocation of selected candidate between Dow Medical College and Sindh Medical College based on seniority in merit and from the sessions 1998-99, such candidate had to appear in Entry Test based on Biology, Chemistry, Physics and English---Such were the requirements of the rules.
 
(b) Constitution of Pakistan (1973)---
 
----Art. 199---General Clauses Act (X of 1897), S.21---Constitutional petition---Educational institution---Admission in medical college---Principle of locus poenitentiae---Applicability---Factual controversy---Grievance of petitioners was that after they had been given admission in medical college and having paid dues and having appeared in examinations conducted by University, the authorities could not cancel their admissions--Contention of authorities was that the petitioners did not appear in entry tests, their marks were less than the merit, they were not domiciled in Sindh and were never given any admission in medical college, rather they in connivance with college staff fraudulently got themselves enrolled in the college, thus principle of locus poenitentiae, was not applicable---Validity---Principle of locus poenitentiae could not be applied in such cases where admission was claimed defecto---Mere on the basis of examination forms forwarded with connivance of the staff of the college, a vested right could not be pleaded particularly when candidates failed to demonstrate their eligibility for admission from their own statement either they were short of closing marks and/or were domiciled in Province other than Sindh---Facts contended by petitioners with regard to their claim for admission were seriously disputed by the authorities---Even the eligibility for admission had been disputed---Controversy in entirety revolved around the questions of facts and needed elaborate enquiry, such exercise could not be undertaken by High Court under Art.199 of the Constitution---Petitioners failed to demonstrate their admission in accordance with rules for admission---There was no scope of defacto admission by forged entry with the connivance of college staff and their appearance in examination---Constitutional petition was dismissed in circumstances.
Hina Jawed v. Government of N.-W.F.P. and others 1998 SCMR 1469; Sheerin Munir v. Government of Punjab PLD 1990 SC 295; Chairman Selection Committee/Principal King Edward Medical College Lahore v. Wasid Zamir 1997 SCMR 15; Shahan Aurangzeb v. Principal Liaquat Medical College 1999 CLC 509; Asif Majeed and others v. A.D.C.(C) Lahore 2000 SCMR 928; Secretary to Government Punjab v. Ghulam Nabi PLD 2001 SC 415; Lahore Cantonment Cooperative Housing Society v. Dr. Nusratullah PLD 2000 SC 1068; Pardeep Kumar v. Province of Sindh and others PLD 1998 Kar. 433; Atiya Bibi v. Federation of Pakistan 2001 SCMR 1161; State of U.P. v. Anupam Gupta AIR 1992 SC 932; Asif Hameed v. State of J&K AIR 1989 SC 1899 and Indu Kant v. State of U.P. AIR 1993 SC 1225 ref.
 
(c) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional jurisdiction of High Court---Scope---Jurisdiction of High Court under Art.199 of the Constitution is discretionary in nature---High Court declines to exercise constitutional jurisdiction in cases where such jurisdiction works in aid of injustice or protects some ill-gotten gain of a party.
 
Zameer Ahmed v. Bushir Ahmed 1998 SCMR 516; Export Promotion Bureau v. Qaiser Saifullah 1994 SCMR 859 and Province of Punjab v. S.M. Zaheer PLD 1997 SC 351 rel.
 
(d) Educational institution---
 
----Fraudulent admission in medical college---Migration to private medical college---Scope---Petitioners fraudulently got themselves admitted in medical college but authorities on coming to know about the fact cancelled their admission---Plea raised by petitioners was that they be allowed to migrate to some private medical college---Validity---No direction could be issued for such migration on the grounds that petitioners could not be permitted to reap the fruit of their own wrong and fraud---If the acts and omission of petitioners were condoned then others would also make the same as precedent, which would not be in the interest of medical institutions---Petitioners were not allowed to migrate to private medical college when their claim was seriously disputed.
 
Miss Rizwana Andleeb v. Principal Chandka Medical College, Larkana 2003 SCMR 1944 distinguished.
 
Raja Qureshi, Muhammad Nawaz, Muhammad Aqil and Muhammad Hanif for Petitioners.
 
Abbas Ali, Addl. A.-G. and M. Shoaib Ashraf for Respondents.
 
Dates of hearing: 12th, 19th and 26th April, 2004.
 
 
JUDGMENT
 
Case 95

2006 C L C 1731
 
Karachi
 
Before Mushir Alam, J
 
Syed MAHARRAM SHAH----Plaintiff
 
Versus
 
NILOFAR MINHAJ HUSSAIN----Respondent
 
C.M.As. Nos.2407 of 2003, 2645, 7832 of 2002 and 1482 of 2000 in Civil Suit No.1644 of 1998, decided on 22nd March, 2005.
 
Specific Relief Act (1 of 1877)---
 
----Ss. 12 & 19---Civil Procedure Code (V of 1908), 0.1, R.10---Suit for specific performance of agreement to sell---Impleading of party--- Application for---Application under 0.I, R.10, C.P.C. was filed by plaintiff during pendency of' suit seeking joinder of intervenors as a party to the suit on the ground that during pendency of suit, defendant having sold the property in favour of intervenors, they were necessary and proper party to the suit---Validity---Where in a suit for specific performance, it appeared that agreement was not capable of specific performance, the Court could decline same and award compensation or damage---Agreement, in the present case, having been rendered incapable of specific performance, claim for award for compensation in terms of S.19 of Specific Relief Act, 1877 Could always be entertained and suit could be treated accordingly.
 
PLD 1992 SC 80 ref.
 
Azizuddin Qureshi for Plaintiff.
 
Shaukat Hayat for Defendant.
 
ORDER
Case 96
 
2006 C L C 1736
 
Karachi
 
Before Sabihuddin Ahmed, C.J. and Qaisar Iqbal, J
 
Mrs. SHAHNAZ and others----Appellants
 
Versus
 
HAMID ALI MIRZA----Respondent
 
H.C.A. No.105 of 2006.
 
Civil Procedure Code (V of 1908)---
 
----S. 75, O.X, R.1-A, & O.XXVI, R.4--- Law Reforms Ordinance (XII Of 1972), S. 3----High Court appeal---Appointment of Commission to record evidence---Restraining appellants from raising construction on property---Grievance of appellants was two folds as they were aggrieved of two orders of Single Judge, whereby Commission had been appointed to record evidence of respondent and interim injunction restraining appellants from alienating or raising construction on the property had been granted---Contention of appellants was that evidence could not be recorded on Commission as appellants had not consented to issuance of Commission in terms of O.X, R.1-A, .C.P.C.---Validity---Respondent in the present case was Judge of Supreme Court and exigencies of his absence from the Court would impair his onerous public duties---Moreover his appearance before a Court as witness and the possibility of being cross-examined would have been a great source of embarrassment for any Court, member of the Bar and general public---Directions to record evidence on Commission were perfectly justified terms of powers available to the Court under O.XXVI, R.4, C.P.C.---So far as restrain on alienation was concerned, counsel for respondent had rightly contended that corpus of the dispute could not be allowed to be destroyed---Impugned restrain, in circumstances, was perfectly justified--Regarding construction on property in dispute, it could be said that when ostensible title had been transferred in favour of appellants, who were also in possession of disputed plot, it could not be altogether fair to deny them the benefit of its possession till such time that matter was finally resolved and respondent's claim was established---Impugned order was modified to the extent that appellants could raise construction on the plot, but entirely at their own risk and they could be required to pull it down if so required by respondents in case his suit was decreed.
 
Muhammad Shafi v. Kaniz Zohra Bibi 1983 CLC 2541 and Muhammad Akram v. Rehmat Khan PLD 1987 Lah. 68 ref.
 
Rizwan Ahmed Siddiqui for Appellants.
 
Mushtaque A. Memon for Respondent.
 
ORDER
Case 97
2006 C L C 1834
 
[Karachi]
 
Before Ghulam Rabbani, J
 
Mir GHULAM RASOOL through L.Rs.----Applicants
 
Versus
 
PROVINCE OF SINDH through Deputy Commissioner, Sukkur and others----Respondents
 
C.M.As. Nos.372 of 1994, 540 of 1998 and Civil Revisions Applications Nos.S-117 and S-127 of 1994, heard on 27th January, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---West Pakistan Land Reforms Regulation, 1959 [MLR 64 of 19591, para.24---Qanun-e-Shahadat (10 of 1984), Art.115---Title of tenant---Concurrent findings of fact recorded by the Courts below---Principle of estoppel---Applicability---Suit-land was purchased by defendants from the original owners in year, 1966 vide registered sale deed---Predecessor-in-interest of plaintiffs being tenant on the suit-land assailed the sale on the ground that it was violative of paragraph 24 of West Pakistan Land Reforms Regulation, 1959---Revenue Authorities decided the matter in favour of defendants---Plaintiffs aggrieved from such order filed civil suit which was dismissed by Trial Court---Appellate Court found that in view of Art.115 of Qanun-e-Shahadat, 1984, tenants were estopped to deny or dispute the title of landlords, therefore, plaintiffs had no cause of action so also a tenant could not challenge the title of landowner under S.42 of Specific Relief Act, 1877, hence the plaintiffs had no right and title in the suit property--Judgment and decree passed by Trial Court was maintained by Appellate Court---Validity---Plaintiffs failed to refer any law, indicating that by virtue of being Moroosi Hari (tenant by inheritance) of disputed land they could be termed to enjoy a right to challenge the ownership of the land---No other right in favour of tenants, regarding the suit-land, was brought into the notice of High Court---At no stage the original owners had challenged the registered sale-deed in favour of defendants,, nor they had challenged any entry kept on the 'basis of such sale-deed---6riginal owners also did not challenge the entries of ownership kept in favour of defendants in Revenue Record either before Revenue Authorities or by way of any civil litigation---Concurrent findings of two Courts below existed and no illegality therein had been pointed out---High Court declined to interfere in the judgments and decrees passed' by two Courts below---Revision was dismissed in circumstances.
 
Ahmed Ali A. Memos for Applicants (in C.M.A. No.540 of 1998 and Civil Revision No.S-127 of 1993).
 
Zuber Ahmed Rajput for Official Respondents (in both cases).
 
Kalandar Bux Phulpoto for Respondents Nos.5 to 7 (in C.M.A. No.540 of 1998 and Civil Revisions Nos.S-117 and S-127 of 1994).
 
Nazir Ahmed Awan for Respondents Nos.8 to 12 (in C.M.A. No.540 of 1998 and Civil Revision No.127 of 1994) and for Applicants (in C.M.A. No.372 of 1994 and Civil Revision No.S-117 of 1994).
 
Date of hearing: 27th January, 2005.
 
JUDGMENT
 
Case 98
2006 C L C 1848
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
AHMED SAEED RIZVI through L.Rs.----Petitioners
 
Versus
 
Mst. JANNAT BIBI through L.Rs.----Respondents
 
C.P. No.S-72 and M.A. No.604 of 2005, decided on 31st May, 2006.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
----S. 14---Constitution of Pakistan (1973), Art.199---Constitutional petition---Personal bona fide need of landlord--Respondent landlady, who after filing ejectment application had died, had sought ejectment of tenant on ground that she was maintaining a large family and was residing with her family in upper floor of building in question and after death of landlady, her application was not affected irrespective of the dismissal of amendment application as ejectment was sought by landlady on the ground of her children, two of whom had been examined---Both the two Courts below while ejecting tenant had taken evidence for consideration and their findings were proper.
 
PLD 2004 SC 489(c); 1990 CLC 103; 1993 MLD 1217; 1990 MLD 3088; 2001 SCMR 338 and 1988 SCMR 193 ref.
 
Raja Khan for Petitioners.
 
Rafique Ahmed for Respondents Nos.2 to 13.
 
ORDER
 
Case 99
 
2006 C L C 1853
 
[Karachi]
 
Before Munib Ahmed Khan, J
 
Mst. DILSHAD BIBI----Petitioner
 
Versus
 
RAMZAN ALI and 3 others----Respondents
 
Constitutional Petition No.S-33 of 2004, decided on 25th May, 2006.
 
Sindh Rented Premises Ordinance (XVII of 1979)---
 
----Ss. 15(2)(VII) & 15-A---Constitution of Pakistan (1973), Art.199---Constitutional petition---Bona fide personal need of landlord ---Proof---Landlady by producing evidence on record had proved that shop in question was required for personal need of her son and such claim was fully established---Apprehension of tenant that landlady would let out premises in question after obtaining same to other tenant was covered by S.15-A of Sindh Rented Premises Ordinance, 1979 which should remove said apprehension.
 
PLD 1981 SC 214; 1992 SCMR 1296; 1997 SCMR 1062; 2001 SCMR 1197; 2003 SCMR 1667; 2001 MLD 21; 2001 MLD 1219; 2000 YLR 1575; 2003 CLC 278; 1997 CLC 1085; PLD 1994 Kar. 219; 1999 CLC 470; 1989 SCMR 235; PLD 1981 SC 246; 2003 MLD 480 and 2004 YLR 3278 ref.
 
Muhammad Saleem Hashmi Qureshi for Petitioner.
 
Abdul Aziz Shaikh for Respondents.
 
Date of hearing: 25th May, 2006.
 
JUDGMENT
 
—--------------------------------------------------------
Case 1
2006 C L C 1
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
Rana ABDUL QADIR and 4 others---Petitioners
 
Versus
 
GOVERNMENT OF PAKISTAN, MINISTRY OF DEFENCE, DEFENCE PRODUCTION DIVISION, through Secretary Defence, Rawalpindi and 6 others---Respondents
 
Writ Petition No. 12178 of 1992, decided on 8th November, 2005.
 
Punjab Land Acquisition Rules, 1983---
 
----R. 14---Constitution of Pakistan (1973), Art.199---Constitutional petition---Acquired land, for which all formalities had already been completed and award announced and compensation paid, was not utilized for the purpose for which the same was acquired---Petitioners (sons of the deceased original landowner) sought direction from the High Court under Art.199 of the Constitution for release and handing over the land in question to them, thus, being the legal heirs of the original owner of the land in question, for which they (petitioners) were willing to pay the amount received at the time of award by their late father---Validity---Distinction needed to be kept in view in the case of withdrawal from acquisition and where the acquisition was complete in all respects but the erstwhile landowners sought return of the land---Rule 14, Punjab Land Acquisition Rules, 1983 made it clear that on abandonment of the land and its purpose, the same was to be handed over to the Collector who was then responsible for its disposal in accordance with the orders of the Government---No direction of absolute nature, therefore, could be issued by the High Court to the authorities to return the land to the petitioners and proper course open to them, under R.14, Punjab Land Acquisition Rules, 1983 was to approach the Government for consideration of their request---Constitutional petition was dismissed.
 
Bashir Ahmed Akhgar and others v. Collector, Land Acquisition and others 1992 MLD 2364 rel.
 
Province of Punjab through Collector, Lahore and another v. Saeed Ahmad and 4 others PLD 1993 SC 455; Yaqoob Khan v. Government of Punjab and others 1986 SCMR 1224; Bashir Ahmed Akhgar and others v. Collector, Land Acquisition and others 1992 MLD 2364, Mst. Kishwar Sultana and another v. Province of Punjab through District Officer Revenue/Notified Officer and 3 others PLJ 2005 Lahore 1113 and Bostan v. Land Acquisition Collector, Rawalpindi and 4 others PLD 2004 Lah. 47 ref.
 
Mian Dilawar Mahmood for Petitioner.
 
Ch. Yawar Ali, Deputy. A.-G. for Respondents Nos. 1, 6 and 7.
 
Ch. Aamir Rehman, Addl. A.-G. for Respondents Nos.2 to 5.
 
Date of hearing: 8th November, 2005.
 
JUDGMENT
 
Case 2
2006 C L C 11
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
ABDUL WAHEED CH. and 3 others---Petitioners
 
Versus
 
Mst. MEHBOOB SULTANA through L.Rs. and others---Respondents
 
C.M. No. 826 of 2003 in Civil Revision No. 142 of 1998, decided on 10th November, 2005.
 
Civil Procedure Code (V of 1908)---
 
----S. 147, O.XXXII, R.7 & O.XXIII, R.3---Specific Relief Act (I of 1877), Ss.8, 9, 10 & 55---Compromise---Suit for possession through partition, rendition of account, recovery of profits and permanent injunction---Request for compromise was granted by the Trial Court being fully conscious of rights and interest of plaintiffs who were then minors and were being represented by their father---Terms of compromise were partly performed by making payment in the Court and received by the plaintiff---Case was adjourned for payment of balance amount and on the adjourned date, plaintiff refused to receive that amount and applied for the cancellation and rescission of the compromise contending that since the interest of the minors was involved, the Court was under duty to take care of their interest and guard the same and that in the original suit all the properties were not included and some valuable properties had been left out and therefore, the case required to be decided on merits---Validity---Once the matter was finally resolved by making statements, plaintiff should have honoured the same instead of playing hide and seek and changing stance time and again before the Court---Plaintiff could not successfully plead that being father of the minors, he was not looking after their interest---Minors, who were now major had not alleged that their father had been siding with the other side i.e. defendants or acting contrary to their interest, rather the plaint disclosed that father had no adverse interest against his minor children---Mere omission of some properties (if at all there be any) from the suit or the compromise, would lend no justification to withdraw, resile or get out of compromise arrived at being fully conscious of the rights and interest of the minors---Compromise having been implemented and even benefit thereunder having been derived by the plaintiff by receiving the amount in the Court, the sanctity of such a compromise could not be eroded and nullified on such flimsy premises ---Factum of compromise and settlement of the matter, in the present case, was not once but twice admitted and owned before the Court---Conduct of plaintiff, not only had been inconsistent but also he had been approbating and reprobating, which could not be countenanced by the Court---Trial Court, therefore, acted illegally in allowing the plaintiff to resile from his commitment merely on the ground that he omitted to add very valuable property of the deceased, the predecessor of the parties---If there were other properties in which the minors were entitled to a share, it would be open for the plaintiff to seek and avail remedy qua the same but the compromise and settlement qua the suit properties could not be allowed to be frustrated and nullified.
 
A. R. Khan v. P.N. Boga through Legal Heirs PLD 1987 SC 107 fol.
 
Khan Baig Janjua and Raja Maqbool Hussain for Petitioners.
 
Hafiz Saeed Ahmed Sheikh for Respondents.
 
Date of hearing: 10th November, 2005.
 
JUDGMENT
 
Case 3
2006 C L C 34
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
FIDA HUSSAIN---Petitioner
 
Versus
 
DISTRICT RETURNING OFFICER, MULTAN and 2 others---Respondents
 
Writ Petition No.5776 of 2005, decided on 22nd September, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 152---Constitution. of Pakistan (1973), Art.199---Constitutional petition---Election for reserved seat---Peasant---Eligibility---Nomination papers of petitioner were rejected by Returning Officer and District Returning Officer, on the ground that he had a holding of more than 5 acres of land during the period of five years preceding the election year---Plea raised by the petitioner was that he acquired land from his father and transferred the same to his wife prior to filing of his nomination papers---Validity---Irrespective of the fact as to how and when the land was acquired by petitioner, the fact remained that he was owner of more than 5 acres of land during the five years period before the election year---Petitioner did not qualify and his nomination papers were rightly rejected by the Courts below---Petition was dismissed in circumstances.
 
Malik Altaf Hussain Rawan for Petitioner.
 
ORDER
 
Case 4
2006 C L C 40
 
[Lahore]
 
Before Syed Shabbar Raza Rizvi, J
 
Hafiz MUHAMMAD AKRAM---Petitioner
 
Versus
 
MANSOOR SARWAR KHAN, BARRISTER-AT-LAW and 3 others---Respondents
 
Review Petition No.63 of 2005, in Writ petition No.14478 of 2005, decided on 23rd August, 2005.
 
(a) Legal Practitioners and Bar Councils Act (XXXV of 1973)---
 
----S. 41---Misconduct---Counsel suppressing the fact before High Court about filing of writ petition earlier against the same person and its dismissal---Conduct of the Counsel and the petitioner was extremely condemnable and unbecoming for a lawyer; it grossly infringed upon the Code of ethics provided in the Legal Practitioners and Bar Councils Act, 1973 and constituted an offence under the Penal Code---Office was directed by the High Court to transmit certified copies of all orders on the file of the case as well as petitions and annexures to the Secretary, Punjab Bar Council to place it before the Disciplinary Committee to take an appropriate action, particularly against the Counsel and others, in the present matter---Counsel was liable to be tried and penalized for misconduct---Misconduct committed by the Counsel was also directed to be entered into his record/file.
 
(b) Constitution of Pakistan (1973)----
 
---Art. 199---Constitutional jurisdiction of High Court---Scope---Any order obtained fraudulently is not a legal order---Jurisdiction under Art.199 of the Constitution is conferred upon the High Court as a discretionary jurisdiction---Purpose of said jurisdiction is to foster justice and right a wrong and not to encourage or aid injustice, or to overlook and ignore fraud and cheating.
PLD 1989 SC 166; PLD 1973 SC 236; 1981 SCMR 231; PLD 1997 SC 351 and PLD 2001 SC 415 ref.
 
Ch. M. S. Shad for Petitioner.
 
Shahid Amin for Respondent No. 1.
 
Ch. Khurshid Anwar Bhinder, Addl. A.-G. for Respondents.
 
ORDER
Case 5
2006 C L C 46
 
[Lahore]
 
Before Syed Shabbar Raza Rizvi, J
 
LIAQAT ALI SHAHID --- Petitioner
 
Versus
 
D.R.O. and others---Respondents
 
Writ petition No. 16243 of 2005, decided on 26th September, 2005.
 
Punjab Local Council Elections Rules, 2005---
 
---Rr. 14(4) & 53---Punjab Local Government Ordinance (XIII of 2001), Ss.152, 158(1) & (2) [as added by Punjab Local Government (Amendment) Act (XXVI of 2005)] & 160---Tehsil Nazim, election of---Union Nazim and Naib Union Nazim contesting such election---Bar of dual membership---Applicability---Such candidates, if took oath of their respective offices under 5.160 of Punjab Local Government Ordinance, 2001, would be deemed to have assumed charge of their respective offices and would be disqualified to contest such election without first resigning from their respective offices---If no such oath was taken by ' such candidates, then they would not be deemed to have assumed charge of their respective offices, thus, the bar contained in S. 158(1) of Punjab Local Government Ordinance, 2001 would not apply to them---Principles explained.
 
Subsection (2) has been added vide Punjab Local Government (Amendment) Act (XXVI of 2005). Original section 158 consisted of subsection (1) only, and it included all Nazims i.e. Zila Nazim, Naib Zila Nazim, Tehsil Nazim, Naib Tehsil.Nazim, Town Nazim, Naib Town Nazim, Union Nazim and Naib Union Nazim. By new subsection (2) of section 158, Union Nazim or Naib Union Nazim have been taken out of the list given in subsection (1), and there is no bar on them becoming members of Zila Council or Tehsil Council or the members elected against reserved seats in Zila Council or Tehsil Councilor being elected as Naib Zila Nazim or Naib Tehsil Nazim, as the case may be. It means that bar contained in subsection (1) still applies to a Union Nazim or Naib Union Nazim, if he wants to contest election of Zila Nazim or Tehsil/Town Nazim. This amendment is consistent with Rule 53, which provides that "in the first meeting of Zila Council, Tehsil/Town Council presided by Returning Officer cause the conduct of poll, where the members of Zila/Tehsil/Town Council, as the case may be, shall elect from amongst themselves a Naib Zila/Tehsil/Town Nazim securing majority votes of total membership of the Council through a secret ballot".
A Nazim Union Council or Naib Nazim Union Council is not exempt from the bar mentioned in section 158(1) of the Ordinance as far as election of Zila Nazim or Tehsil Nazim is concerned. For election of " Zila Nazim or Tehsil/Town Nazim, it is not necessary that candidate should be from amongst members of the respective house. For this reason. Section 158(2) of the Punjab Local Government Ordinance, 2001 allows Union Nazim or Naib Union Nazim to contest election of Naib Zila Nazim or as the case may be, Naib Tehsil Nazim without resigning from his office, as both are members of Zila Councils and Tehsil Councils respectively by virtue of their office. But if a Union Nazim or Naib Union Nazim wants to contest the election for the office of Zila Nazim or Tehsil Nazim/Town Nazim, he is required to resign from his office to qualify for the election and the bar mentioned in subsection (1) of section 158 of Ordinance, 2001 would apply with full force.
 
A Nazim of a Union Council shall be deemed a Nazim for the purpose of performance of his functions, duties, rights etc., after his election result has been notified by the Chief Election Commissioner and he has taken oath. Under section 160 of Ordinance, 2001, a Nazim or a Naib Nazim is required to take oath before assuming the charge. Likewise unless a Nazim and Naib Nazim assumed the charge of his office, he cannot perform his functions, duties or exercise any powers etc. Thus, he will also not be deemed a Nazim qualified or disqualified as a voter or a candidate to contest any election i.e. as mentioned in Rules 53 of Punjab Local Government Election Rules, 2005. Whenever any oath is provided for any office, the incumbent can only become functional after he has been administered the oath.
All constitutional office-holders provided under the Constitution become functional only after they are given oath by the nominated persons.
 
If an elected Union Nazim (petitioner) has taken oath under section 160 of Ordinance, 2001, he shall be deemed to have assumed office of Union Nazim and therefore, he shall be disqualified to contest election of Tehsil Nazim and his case will be covered by subsection (1) of section 158 of the Ordinance, 2001, but if he has not taken such oath, he shall not be deemed to have assumed the office of Union Nazim, and in that case the bar contained in section 158(1) of the Ordinance, 2001 will not apply.
 
Muhammad Ahsan Bhoon for Petitioner.
 
ORDER
 
Case 6
2006 C L C 60
 
[Lahore]
 
Before Muhammad Akhtar Shabbir, J
 
Malik MUHAMMAD DIN and 2 others---Petitioners
 
versus
CHIEF ADMINISTRATOR AUQAF, GOVERNMENT
OF PUNJAB, LAHORE and another---Respondents
 
Writ Petition No.994 of 2004, decided on 28th June, 2005.
 
Punjab Waqf Properties Ordinance (IV of 1979)---
 
---Ss. 3, 4, 7 & 11---Punjab Auqaf Department Delegation of Powers Rules, 1960, R.4---General Clauses Act (X of 1897), S.21---Constitution of Pakistan (1973), Art. 199---Constitutional petition---Notification of taking over control of mosque---Withdrawal of Notification---Chief Administrator, Auqaf vide Notification, had taken over control of a mosque and appointed a manager to manage and maintain the same---Said Notification, later on, was withdrawn by a subsequent Notification on reference received from District Nazim and a petition from `Namazian' of said mosque---Subsequent Notification whereby earlier Notification was withdrawn, had been challenged by petitioner contending that Administrator Auqaf was not empowered to withdraw earlier Notification---Section 21 of General Clauses Act, 1897, provided that power to make, amend, vary or rescind orders, rules, or bye-laws were available to the Authority---Authority competent to snake order, in circumstances had power to undo it, but order could not be withdrawn or rescinded once it had taken legal effect and certain rights were created in favour of any individual and principle of "Locus Poenitentiae" would be available---Mosque in question was statedly run by registered Anjuman and it was alleged that petitioners were not allowing people of other sect to say their prayers in said mosque---Mosque was meant for the people to offer their prayers and it was right of every Muslim to enter into mosque and make his prayer in accordance with Injunctions of Qur'an and Sunnah according to his own religious school of thought---Mosque is for all Muslims of any sect because it was house of `Almighty Allah'---Right was vested to all muslims, not to a particular person, sect, group or particular school of thought and it was in the interest of all muslim community of area concerned---Nothing was mentioned in the impugned Notification of withdrawal that said Notification was issued under direction of any Minister---Administrator of Auqaf, while issuing impugned Notification, had applied his own mind accepting request of people of area---Administrator Auqaf, being fully empowered to withdraw Notification, petition against said Notification was dismissed and issuing of rule "nisi", was declined.
 
 
Muhammad Tufail and 2 others v. Chief Administrator of Auqaf and 2 others 1991 MLD 303 and Muhammad Zakir Khan v. Government of Sindh and others 2004 SCMR 497 ref.
 
Mujeeb-ur-Rehman Kiani for Petitioners.
Malik Muhammad Jahanzeb Khan Tamman in C. M. No.1111 of 2004.
 
ORDER
Case 7
 
2006 C L C 67
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
PROVINCE OF PUNJAB, through Secretary to Government of Punjab and 2 others---Petitioners
 
versus
 
MUHAMMAD YASIN---Respondent
 
First Appeal from Order No.205 of 2005, decided on 28th September, 2005.
 
(a) West Pakistan Requisitioning of Immovable Property (Temporary Power) Act (VII of 1956)---
 
----S. 6---Compensation, assessment of---Principles---"Payment of rent by tenant" and "payment of compensation by the Requisitioning Authority"---Distinction---Compensation could be granted at the most for a period of three years preceding the filing of petition before the Court---Mere payment of rent, which was paid prior to requisition, could not be treated as compensation after the requisition for the use and occupation of the property---Revised compensation could be ordered to be paid from the date of requisition of the property and mere fact that the owner had been receiving the amount lesser than that before filing the petition was no bar for agitating his right to have fair amount of compensation fixed, assessed and determined.
 
Ashfaq-ur-Rehman v. Chaudhri Muhammad Afzal PLD 1968 SC 230; Province of the Punjab v. Amin Jan Naeem and 4 others PLD 1994 SC 141; Government of the Punjab through Secretary, Education, Lahore v. Shahida Begum 1994 SCMR 1488; Province of Punjab v. Mst. Hanifan 1993 MLD 2430 and Sh. Muhammad Shafi v. The Province of Punjab and another 1986 CLC 593 ref.
 
(b) West Pakistan Requisitioning of Immovable Property (Temporary Power) Act (VII of 1956)---
 
----S. 6---Compensation, assessment of---Appeal to High Court---Plea in respect of delayed approach of the owner of property for determination of compensation of the requisitioned property could not be given effect to inasmuch as neither such plea was taken before the lower forum nor was any issue even claimed/framed qua the same---Question of limitation, in the context of the controversy, being a mixed question of law and fact dependant upon factual assertions, evidence and findings, same could not be countenanced for the first time in appeal.
 
(c) West Pakistan Requisitioning of Immovable Property (Temporary Power) Act (VII of 1956)---
 
---Ss. 6 & 7---Compensation, assessment of---Interest, award of---Provision of S.7, West Pakistan Requisitioning of Immovable Property (Temporary Power) Act, 1956 having been held to be repugnant to Injunctions of Islam by Shariat Appellate Bench of the Supreme Court, payment of interest could not be upheld.
 
Province of the Punjab v. Amin Jan Naeem and 4 others PLD 1994 SC 141 fol.
 
Rizwan Mushtaq, Asst. A.-G., Punjab along with Mrs. Humana Daher, District Education Officer (W.EE) for Petitioners.
Rana Pervaiz Khalid for Respondent.
 
Date of hearing: 28th September, 2005.
 
JUDGMENT
 
Case 8
 
2006 C L C 73
 
[Lahore]
 
Before Nazir Ahmad Siddiqui, J
 
MAZHAR ABBAS---Petitioner
 
versus
 
Malik GHULAM ABBAS and another---Respondents
 
Writ Petition No.4926 of 2005, decided on 10th August, 2005.
 
Punjab Local Government Elections Rules, 2005---
 
----R. 14(4)---Constitution of Pakistan (1973), Art. 199---Constitutional petition---Maintainability---Acceptance of nomination papers---Order accepting nomination papers of respondent passed by Returning Officer, had been challenged in constitutional petition without filing appeal as provided under R. 14(4) of Punjab Local Government Elections Rules, 2005---Validity---No justification was available with petitioner for not availing the statutory remedy of appeal---Constitutional petition being not maintainable, stood dismissed, in circumstances.
 
Zahoor Ahmad v. Mahmood Ali and another PLD 1977 Lah. 1377 and Alam Din and 12 others v. Administrator Auqaf, Azad Government of the State of Jammu and Kashmir, Muzaffarabad and 2 others 1989 CLC 578 ref.
 
Khadim Nadeem Malik for Petitioner.
 
M.R. Khalid Malik, Addl. A.-G. for Respondents.
 
ORDER
 
Case 9
 
2006 C L C 79
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
MOEEN AKHTAR and 2 others---Appellants
 
versus
Dr. ABDUS SATTAR through Legal Heirs---Respondents
 
Regular Second Appeal No. 190 of 1988, heard on 7th July, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 12---Contract Act (IX of 1872), Ss. 188 & 214---Qanun-e-Shahadat (10 of 1984), Arts.79 & 117---Registration Act (XVI of 1908), Ss.18 & 47---Civil Procedure Code (V of 1908), O.XV, R.1---Suit for specific performance of agreement to sell---Agreement by husband as general attorney of his second issueless wife in favour of his sons from first wife---Agreement was alleged to have been executed on 24-7-1968---Owner/wife died on 3-6-1976---Suit was filed on 18-3-1979---Attorney in written statement admitted receipt of entire sale price from plaintiffs---Plea of donee-defendant (Dar-ul-Aloom) was that suit property was partly dedicated by its owner on 11-11-1968 through a registered Waqf Deed witnessed by attorney; and that agreement had been prepared subsequent to death of owner under connivance between attorney and his sons in order to deprive donee of Waqf property---Trial Court dismissed suit to extent of Waqf property, which judgment was upheld by Appellate Court---Validity---No explanation on record as to why after receipt of entire sale price by attorney, sale-deed was not executed in favour of plaintiffs---Family circumstances/understanding among parties if were of such nature that no title document was needed for transfer of suit property in favour of plaintiffs, then why agreement was got executed---Both owner and attorney being literate persons had signed Waqf Deed---Had agreement been executed earlier to Waqf Deed, then same property would not have been included in Waqf for litigation by donee---Registered Waqf Deed carried a presumption of its execution---Donee/defendant while appearing in witness box had deposed that such property had previously been donated to "Anjuman-e-Himayat e-Islam" in March, 1962, but on its refusal to take over same was transferred to donee/defendant---Such statement would show that intention of owner was to give such property for some pious purpose---Attorney had executed agreement in favour of his own sons without concurrence of his principal, which was in fact a transfer in favour of agent himself---Plaintiffs could not succeed against donee by merely producing two marginal witnesses of agreement, who were not aware of transfer of property in the name of donee-defendant---Agreement neither being registered nor so required under law would not put owner or subsequent purchaser through whatever means at alarm---Conceding written statement of attorney was not honest and being without concurrence of owner would not furnish basis for judgment against him under O.XV, R.1, C.P.C.---High Court dismissed revision petition in circumstances.
 
Maqsood Ahmad and others v. Salman Ali PLD 2003 SC 31; Jamil Akhtar and others v. Las Baba and others PLD 2003 SC 494; Fida Muhammad v. Pir Muhammad Khan through L.Rs. and others PLD 1985 SC 341; Haji Faqir Muhammad and others v. Pir Muhammad and another 1997 SCMR 1811; Mst. Shumal Begum v. Mst. Gulzar Begum and 3 others 1994 SCMR 818; Muhammad Siddique and 2 others v. Mst. Shagufta Begum alias Shagufta Rafique 1994 CLC 1690; Haji Muhammad Din v. Malik Muhammad Abdullah PLD 1994 SC 291; Mst. Kaniz Fatima through L.Rs. v. Muhammad Salim and 27 others 2001 SCMR 1493; Abdul Hakeem v. Habib Ullah and 11 others 1997 SCMR 1139; Muhammad Sain v. Muhammad Din 1996 SCMR 1918 and Lutufur Rehman and others v. Zahoor and others PLJ 1999 SC 204 rel.
 
(b) Contract Act (IX of 1872)---
 
----Ss. 188 & 214---Registration Act (XVI of 1908), Ss.18 & 47---Agreement to sell by attorney in favour of his real sons---Non registration of agreement---Effect---Such agreement would not put owner or subsequent purchaser through whatever means at alarm.
 
(c) Specific Relief Act (I of 1877)------
 
----S. 12---Contract Act (IX of 1872), Ss.188 & 214---Civil Procedure Code (V of 1908), O.XV, R.I --- Suit for specific performance of agreement to sell---Agreement by husband as general attorney of his second wife in favour of his sons from first wife---Plaintiffs filed suit after death of owner step-mother---Attorney in written statement admitted receipt of entire sale price from plaintiffs---Effect---Such conceding written statement being not honest and without concurrence of owner-wife would not furnish basis for judgment against attorney under O.XV, R.1, C.P.C.
 
Masud Akhtar Sheikh for Appellants.
Qamar Riaz Hussain Basra for Respondents.
 
Date of hearing: 7th July, 2005.
 
JUDGMENT
 
Case 10
 
2006 C L C 87
 
[Lahore]
 
Before Abdul Shakoor Paracha, J
 
Raja MUHAMMAD SAFDAR---Petitioner
 
versus
 
DISTRICT RETURNING OFFICER, RAWALPINDI and 2 others---Respondents
 
Writ Petition No.2217 of 2005, decided on 8th August, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 152(1)(g)----Punjab Local Government Elections Rules, 2005, R.14(4)---Constitution of Pakistan, 1973, Art. 199 --- Constitutional petition---Disqualification of candidate due to bad character---Objections taken by one of the respondents against the nomination papers of the petitioner were dismissed by the Returning Officer---Appeal filed by the respondent against the said dismissal was allowed. by the District Returning Officer and the nomination papers of the petitioner were rejected on the ground that one of the earlier elections of the petitioner was declared illegal by the order of the Election Tribunal due to the fact that petitioner was discharged from the army for bearing unsatisfactory character and this discharge document was forged by him- Contention of the petitioner was that the said order of the Election Tribunal could not be made the basis for disqualification as it was not final for the matter was sub judice before the High Court---Contention of the respondent that the Election Tribunal's findings reflected upon the bad character of the petitioner and the petitioner was involved in criminal cases which were registered with the police---Validity---District Returning Officer had illegally relied on the order of the Election Tribunal and recorded a finding that the same was still in force---Order of the Election Tribunal had been suspended by the High Court under constitutional jurisdiction---Effect of suspension order of the High Court was that the order of the Election Tribunal was not in field for the time being---Mere registration of criminal cases against the petitioner would not tell upon the bad character of the petitioner and would not disqualify him to contest elections as per provisions of S.152(1)(g) of the Punjab Local Government Ordinance, 2001---Constitutional petition was allowed in circumstances.
 
Raja Muhammad Afzal v. Ch. Muhammad Altaf Hussain and others 1986, SCMR 1736 and Munir Ahmad and another v. District Returning Officer/Appellate Authority, Sargodha and others 2004 SCMR 1456 ref.
 
(b)Words and phrases---
 
----"Suspend"---Meaning of---"Suspend" means to interrupt, to cause to cease for a time; to postpone; to stay, delay, or hinder, to discontinue temporarily.
 
Black's Law Dictionary, 5th Edition, page 1297 ref.
 
(c) Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 152(1)(g)----Constitution of Pakistan (1973), Art. 199 ---Constitutional petition---Disqualification due to bad character---Requirements---Contention of the respondent was that the Election Tribunal's findings reflected upon the bad character of the petitioner and petitioner was involved in criminal cases which were registered with the police---Validity---Mere registration of criminal cases against the petitioner would not tell upon the bad character of the petitioner and would not disqualify him to contest elections as per provisions of S. 152(1)(g) of the Punjab Local Government Ordinance, 2001---Principles---Police report could not be admitted as evidence of correctness of facts, as such a report is merely an opinion of the Police Officer and the correctness of the contents of the said report could only be proved through evidence.
 
Raja Muhammad Afzal v. Ch. Muhammad Altaf Hussain and others 1986 SCMR 1736 and Munir Ahmad's case 2004 SCMR 1456 ref.
 
Sh. Zamir Hussain assisted by Raja Ikram Amin Minhas for Petitioner.
 
Saeed Yousaf for the Respondents.
 
ORDER
 
Case 11
 
2006 C L C 104
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
NADEEM SARWAR---Petitioner
 
Versus
 
DISTRICT RETURNING OFFICER, FAISALABAD and another---Respondents
 
Writ Petition No. 16244 of 2005, decided on 22nd September, 2005.
 
(a) Punjab Local Government Elections Rules, 2005---
 
----R. 12---Punjab Local Government Ordinance (XIII. of 2001), S.2(xli)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Nomination for elections of "worker" seat---Nomination papers for a "worker" seat filed by the petitioner before the Returning Officer were rejected on the ground that he did not produce any proof of being a "worker"---Appeal filed by the petitioner against the said rejection was dismissed by the District Returning Officer---Impugned orders of the election officials were challenged by placing reliance on certificate of employer of the petitioner and other documents which showed that he was a "worker" within the meaning of S.2(xli) of the Punjab Local Government Ordinance, 2001---Validity---Petitioner had fulfilled the conditions for filing of nomination papers for the seat of "workef" under R.12 of the Punjab Local Government Elections Rules, 2005---Petitioner had proved himself to be a "worker" by producing certificate of his employer showing that he was working in the establishment for the subsistence where he was undertaking physical labour---Proceedings undertaken by the election officials were summary in nature, therefore, detailed inquiry to find out whether a person was having status of any "worker" was not permissible and they were to accept/reject nomination papers on the basis of material required to be furnished by the R.12, Punjab Local Government Election Rules, 2005 or produced by any objector to challenge the nomination---No choice was left with the election officials to reject the nomination papers of the petitioner in circumstances---Constitutional petition was accepted with the direction to the Returning Officer to include the name of the petitioner in the list of candidates for the "worker seat".
(b) Punjab Local Government Elections Rules, 2005---
 
----R. 12---Rule 12 of the Punjab Local Government Elections Rules, 2005, interpretation of---Filing of nomination papers, procedure and conditions of---Rule 12 of the Punjab Local Government Elections Rules, 2005 deals with the nomination papers for the election and provides that the Returning Officer shall, after announcement of the election schedule, give public notice, inviting nomination papers, specifying time before which and the place at which nomination papers shall be received by him---Rule 12(3)(iv) of the Punjab Local Government Elections Rules, 2005 deals with nomination papers for seats reserved for women, peasants and workers, etc. which were to be filled in Form-HI(D) appended therewith and were to be signed by both the proposer and seconder along with solemn affirmation' made and signed by the candidate---Apart from the conditions provided under R. 12, Punjab Local Government Elections Rules, 2005 there is no other condition for filing of nomination papers for the seat of the worker.
 
(c) Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 2(xli)---Industrial Relations Ordinance (XCI of 2002), S.2(xxx)---Worker, definition of---Worker means a person directly engaged in work, or is dependent on his personal labour of subsistence living and would include a worker as defined in Industrial Relations Ordinance (XCI of 2002).
 
(d) Industrial Relations Ordinance (XCI of 2002)---
 
----S. 2(xxx)---Worker, definition of---Worker will be a person or group of persons who do not fall within the definition of employer or is employee in an establishment or industry, for hire or reward either directly or through a contractor but does not include any person who is employee mainly in a managerial or administrative capacity.
 
(e) Punjab Local Government Elections Rules, 2005---
 
----Rr. 73, 75 & 76---Pre-election disqualification---Annulment of the result of election, ground of---Election Tribunal, power of---If a candidate misrepresented himself as a worker at the time of filing of the nomination papers for the seat of a worker, he would be considered to be not qualified at the time of filing of the nomination papers and such pre-election disqualification could be challenged before the Election Tribunal for the annulment of the results of the election.
Muhammad Ahsan Bhone for Petitioner.
 
Ch. Muhammad Sadiq, Addl. A.-G. on Court's call.
 
ORDER
 
Case 12
 
2006 C L C 131
 
[Lahore]
 
Before Muhammad Akhtar Shabbir and Abdul Shakoor Paracha, JJ
 
S. M. ISMAIL---Appellant
 
Versus
 
CAPITAL DEVELOPMENT AUTHORITY, ISLAMABAD through Chairman and 5 others---Respondents
 
Intra-Court Appeal No. 161 of 2004, heard on 28th June, 2005.
 
(a) Transfer of Property Act (IV of 1882)---
 
----S. 116---Holding over, principle of---Applicability---After expiry of lease period, tenant continuing his possession over the site in dispute and .his status of holding over possession clearly falls within the ambit of S.116 of Transfer of Property Act, 1882.
 
AIR 1919 Oudh 124; Partap Udai Nath SAM Deo and another v. Jagannath Mahto and others AIR 1919 pat. 444; E.W.C. Moore and another v. Makhan Singh AIR 1919 Pat. 254; AIR 1981 Raj. 206; Maganlal Dulabhadas Y. Bhudar Purshottam and others AIR 1927 Bom. 192 and Banwari Lal v. Mt. Hussaini and another AIR 1940 Lah. 410 rel.
 
(b) Transfer of Property Act (IV of 1882)---
 
----Ss. 106 & 116---Islamabad Capital Territory---Possession of lessee---Provisions of Transfer of Property Act, 1882---Applicability---Though the provisions of Transfer of Property Act, 1882, are not applicable to Islamabad Capital Territory, but principles of Ss.106 & 116 of Transfer of Property Act, 1882, can be invoked as such provisions are not to be regarded as opposed to principles of equity and good conscience.
 
Messrs Airport Support Services v. The Airport Manager, Quaid-e-Azar International Airport, Karachi and others 1998 SCMR 2268 rel.
 
(c) Islamabad Rent Restriction Ordinance (IV of 2001)-
 
----S. 17---Law Reforms Ordinance (XII of 1972), S.3---Intra-Court Appeal---Ejectment of lessee---Capital Development Authority leased the disputed plot to its Staff Welfare Committee and the Committee further leased out the plot to appellant initially for thirty years---Appellant constructed petrol pump and Compressed Natural Gas station over the plot---After completion of initial period of thirty years of lease, the authorities, instead of renewing the lease, forcefully dispossessed the appellant---Plea raised by the appellant was that he could not be dispossessed without due process of law---Appellant further contended that Capital Development Authority had renewed the lease in favour of the Committee, therefore, the lease should also be renewed in his favour, who was ready to increase the rent from Rs.1000/- per month to Rs.100,000/- per month---Validity---After allotment of plot on the basis of lease agreement, Capital Development Authority during the period of lease had become functus officio and had no power or authority to act against appellant without due process of law---Action of Capital Development Authority or its Staff Welfare Committee regarding dispossession of appellant from site in dispute, was illegal, without lawful authority and based upon mala fides---Appellant was only liable to be dispossessed through a suit for possession and not illegally or forcibly, as had been done by the authorities in the case of appellant---Appellant had spent colossal amount at site in dispute for installation of petrol pump and Compressed Natural Gas station and if lease period was not extended, appellant's family would be financially ruined and doomed---Rule of equity, good conscience and fair play necessitated that period of lease of appellant be extended for further thirty years as the same benefit had been availed by Capital Development Authority Staff Welfare Committee for itself but the Committee was reluctant to extend such concession to appellant---High Court, in : Intra-Court Appeal, directed that the Committee having its upper hand as lessor should consider difficulties and hardship of appellant---High Court keeping in view the principles of equity, good conscience as well as fairness and also in order to save appellant's family from financial ruination, set aside the order passed by Single Judge of High Court in exercise of Constitutional jurisdiction and extended the lease in favour of appellant for next thirty years against a sum of Rs. 100,000 as rent per month ---Intra-Court Appeal was allowed accordingly.
 
Abdul Haq and 2 others v. The Resident Magistrate, Uch Sharif, Tehsil Ahmadpur East, Bahawalpur PLD 2000 Lah. 101; Sikandar and 2 others v. Muhammad Ayub and 5 others PLD 1991 SC 1041; Muhammad Aslam v. Station House Officer and others 1993 MLD 152; Barkat Ullah Khan v. Abdul Hamid 1981 SCMR 1200 and Messrs Wak Orient Power and Light Limited Gulberg-III, Lahore v. Government of Pakistan, Ministry of Water and Power through Secretary, Islamabad and 2 others 1998 CLC 1178 ref.
 
(d) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Dispossession without notice---Effect---If in violation of mandatory provisions of requiring prior notice, the lessee has been dispossessed, Constitutional petition before High Court is competent.
 
Suleiman Khan & Co. v. Pakistan Railways through General Manager, Railways Headquarters and 2 others 2003 SCL 331 rel.
 
(e) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional petition---Maintainability---Contractual dispute---Scope---Routine contractual disputes between private parties and public functionaries are not open to scrutiny under Constitutional jurisdiction---Breaches of such contracts, which do not entail inquiry into or examination of minute or controversial questions of fact, if committed by Government, semi-Government or local authorities or alike controversies if involving derelictions of obligations, flowing from a statute, rules or instructions, can adequately be addressed to for relief under Constitutional jurisdiction---Any contract carrying elements of public interest, concluded by functionaries of the State, has to be just, fair, transparent, reasonable and free of any taint of mala fides, all such acts remaining open for judicial review---Such rule is founded on the premises that public functionaries, deriving authority from or under law, are obligated to act justly, fairly, equitably, reasonably, without any element of discrimination and squarely within the parameters of law, as applicable in a given situation---Deviations, if of substance, can be corrected through appropriate orders under Art.199 of the Constitution.
 
Mujeeb-ur-Rehman Kiani for Appellant.
 
Malik Muhammad Nawaz and Mrs. Misbah Gulnar Sharif for Respondents.
 
Date of hearing: 28th June, 2005.
 
JUDGMENT
 
Case 13
2006 C L C 166
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
RAIZ AHMAD---Petitioner
 
Versus
 
TOGA and others---Respondents
 
Civil Revision No.638-D of 1988, heard on 17th October, 2005.
 
Punjab Pre-emption Act (I of 1913)---
 
----Ss. 3(1), 4 & 15---Punjab Alienation of Lands Act (XIII of 1900), S.2(3)(F)---Punjab Tenancy Act (XVI of 1887), Ss. 5 & 6---Colonization of Government Lands (Punjab) Act (V of 1912), S.10---Civil Procedure Code (V of 1908), S.115---Suit for pre-emption ---Transfer of tenancy right, whether could be pre-empted ---Transaction was sale, of Dakhel Kaari Rights by Muttali, in favour of respondents/ vendees---Jamabandi, showed that Provincial Government was recorded to be the owner and Muttali as one of Dekhel Kaars under S.10 of Colonization of Government Lands(Punjab) Act, 1912---Rights of occupancy referred to in S.2(3)(F) of Punjab Alienation of Lands Act, 1900, were relatable to rights mentioned in Ss.5 & 6 of Punjab Tenancy, Act, 1887---Transfer of tenancy rights not amounting to sale of land, transaction was not pre emptible.
 
Sher Bahadur v. Behram Khan 1988 SCMR 1735; Majid Ahmad v. Yousaf 1987 CLC 1891; Aziz Hussain and 2 others v. Rashid Ahmad and 3 others 1992 SCMR 1018 and Amir Din and others v. Sabir Hussain PLD 1979 Lah. 896 ref.
 
Mian Waseent Alain Ansari for Petitioners.
 
Chaudhry Muhammad Iqbal Abid for Respondents.
 
Date of hearing: 17th October, 2005.
 
JUDGMENT
 
Case 14
2006 C L C 168
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
DIN MUHAMMAD and 6 others---Petitioners
 
Versus
 
MEMBER, BOARD OF REVENUE, PUNJAB/CHIEF SETTLEMENT COMMISSIONER, LAHORE and another---Respondents
 
Writ Petition No. 112/R of 1996, decided on 30th November, 2005.
 
Constitution of Pakistan (1973)---
 
----Arts. 199 & 189---Constitutional jurisdiction of High Court---Scope---All authorities and Courts are bound by the orders passed and judgments rendered by the superior Courts, particularly the Supreme Court---Such legal position was not only because of Art. 199 of the Constitution, but also for the reason that judgment inter partis, in personam binds the parties---Attempt, had been made by the petitioner, in the present case, to attribute some inaccuracy to the judgment of the Supreme Court rendered in the earlier round of litigation---Held, it was not permissible for High Court to make any comment about the verity of judgment of the apex Court, even no such attempt could be countenanced which might have the effect of eroding the legal efficacy and finality of the previous determination made by the Courts---Principles.
 
The Chief Settlement Commissioner, Lahore v. Raja Muhammad Fazil Khan and others PLD 1975 SC 331; Ali Muhammad v. Hussain Bakhsh and others PLD 1976 SC 37; Pakistan through the Secretary, Ministry of Finance v. Muhammad Himayatullah Farukhi PLD 1969 SC 407; Zafar Iqbal Alvi and others Y. Bashir Ahmed and others 1996 SCMR 795; Pir Bakhsh through L.Rs. and others v. The Chairman Allotment Committee and others PLD 1987 SC 145 and Constitutional Limitations by Cooley at p.50 ref.
 
Jawaid Shaukat Malik for Petitioners.
 
Muhammad Iqbal Ghaznavi and Rana Muhammad Hanif for Settlement Department.
 
Date of hearing: 30th November, 2005.
 
JUDGMENT
 
Case 15
 
2006 C L C 173
 
[Lahore]
 
Before Muhammad Akhtar Shabbir, J
 
Messrs VOYAGE DE AIR, GENERAL SALES AGENT, SHAHEEN AIR INTERNATIONAL and another---Appellants
 
Versus
 
SHAHEEN AIR INTERNATIONAL PVT. LTD. and 4 others---Respondents
 
First Appeal from Order No. 132 of 2005, Civil Revisions Nos.597 and 617 of 2005, heard on 7th November, 2005.
 
(a) West Pakistan Civil Courts Ordinance (II of 1962)---
 
----S. 18---Suits Valuation Act (VII of 1887), Ss.3, 9 & 11---Civil Procedure Code (V of 1908), O.XXXIX, Rr.1, 2 & S.151---Specific Relief Act (I of 1877), Ss.42, 52 & 53---Suit for declaration with temporary injunction---Appeal, forum of---Section 18 of West Pakistan Civil Courts Ordinance, 1962 provided that forum of appeal was to be determined on basis of original value of suit and pecuniary jurisdiction of the District Judge was always to be derived from valuation in the plaint--Section 18 of the Ordinance further provided that appeal against decree or order of Civil Judge would lie to the District Judge if value of original suit in which such decree or order was made did not exceed twenty-five hundred thousand and to the High Court in any other case---Jurisdictional value of present suit fixed and determined by plaintiff was less than twenty-five hundred thousand---Neither defendants nor Trial Court or appellate Court had determined the, original jurisdictional value and the Court if had disagreed with determined jurisdictional value of suit could pass order under section 11 of Suits Valuation Act, 1887 fixing the value but that too after framing an issue and affording an opportunity to parties for production of evidence---Court having not done such exercise, had wrongly observed that it lacked the pecuniary jurisdiction to hear the appeal---Appeal was, therefore, competently filed.
 
Sadar Din v. Elahi Bakhsh and another PLD 1976 Lah. 1; Ali Muhammad and others v. Muhammad Shafi and others PLD 1996 SC 292; Ilahi Bakhsh and others v. Mst. Bilqees Begum PLD 1985 SC 393 and Munawar Hussain and 2 others v. Sultan Ahmad 2005 SCMR 1388 ref.
 
(b) Jurisdiction---
 
----Court lacking jurisdiction---Effect---When Court came to 'the conclusion that it had no jurisdiction over the subject-matter of the suit or appeal, it could not decide any question on merits and could simply decide the question of jurisdiction---Lower Appellate Court, after returning the appeal, was not competent to entertain the cross-objections filed by the defendants---Impugned order passed by the lower appellate Court returning the appeal for its presentation before proper forum was set aside by High Court and appeal would be deemed pending before the lower Appellate Court.
 
Athmanathaswami Devasthanam v. K. Gopalaswami Ayyangar AIR 1965 SC 338 (V 52 C 63); -Karachi Electric Supply Corporation Limited through Secretary v. Messrs Haji Hashim Haji Ahmad Brothers 2003 YLR 2226; Maqsood Ali Khan v. National Bank of Pakistan through. President and 3 others 2003 PLC (C.S.) 226; and Qabool Muhammad Shah v. Bibi Bushra and others 1992 MLD 833 ref.
 
Sh. Muhammad Akram and Muhammad Ilyas Sheikh for Appellants.
 
Mustafa Ramday for Respondents Nos.1 to 7.
 
Babar Ali for Respondent No.8.
 
Mian Abdul Rauf for Respondent No.9.
 
Date of hearing: 7th November, 2005.
 
JUDGMENT
 
Case 16
 
2006 C L C 180
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
Kh. MUHAMMAD RAFIQUE and others---Petitioners
 
Versus
 
HAMEED AHMAD SETHI, ADDITIONAL COMMISSIONER (REVENUE), LAHORE and 4 others---Respondents
 
Writ Petition NO.323/R of 1992, heard on 6th December, 2005.
 
Evacuee Property and Displaced Persons Law (Repeal) Act (XIV of 1975)---
 
----S. 2---Settlement Scheme No.VIII (Revised), Form RSS-VIII Constitution of Pakistan (1973), Art.199 --Constitutional petition--Whether auction purchaser of evacuee property could acquire any indefeasible right in the property without confirmation of the auction and payment of auction money---Notified Officer was to examine such aspect of the matter in the light of the material on record and by summoning the original files---When proceedings had not abated or lapsed on their own, the matter had to be disposed of as "pending proceeding" by the Notified Officer through a speaking order by judicious application of mind---Factual controversy in the present case, still remained to be resolved which exercise could be undertaken by the Notified Officer only by summoning and retrieving the files pertaining to the property in question---Order of the Notified Officer, in circumstances, could not be regarded as a lawful exercise of power which was declared as of no legal effect---High Court directed that Notified Officer was to re-examine the matter in the light of orders passed by the Settlement Authorities from time to time---Parties were directed to cause their presence/ representation before the Notified Officer on the specified date for further proceedings in the matter---Notified Officer was also to take possible steps for the service of parties who remained absent before the High Court.
 
Syed Mowahad Hussain v. Syed Karam Ali Shah through Legal Heirs and 2 others 1993 SCMR 170; Abdul Hamid and others v. Fazalur Rehman and others 1989 SCMR 120 and Muhammad Nasim Anwar and others v. Additional Deputy Commissioner, Vehari and others 2002 SCMR 226 ref.
 
Muhammad Shahzad Shaukat and Ch. Abdul Wadood for Petitioners.
 
Aish Muhammad Khan Sara for Settlement Department.
 
Ex parte for other Respondents..
 
Date of hearing: 6th December, 2005.
 
JUDGMENT
 
Case 17
 
2006 C L C 189
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
ABDUL REHMAN QURESHI and others---Appellants
 
Versus
 
NAZIR HUSSAIN SHAH and others---Respondents
 
Regular Second Appeal No.69 of 1998, decided on 7th December, 2005.
 
Transfer of Property Act (IV of 1882)---
 
---S. 41---Bona fide purchaser/purchaser in good faith---Requirements---Broad guiding principles for determination of bona fide purchaser are that the transferor is the ostensible owner; that he is so by the consent, express or implied of the real owners; that the transfer is for consideration and that the transferee has acted in good faith taking reasonable care to ascertain that the transferor has power to transfer.
 
Mst. Aimna Bi v. Mst. Bivi and others 1993 MLD 1207; Muhammad Jamil and others v. Lahore Development Authority and 3 others 1999 SCMR 2015; Muhammad Sabir Khan and 13 others v. Rahim Bakhsh and 16 others PLD 2002 SC 303 ref.
 
Sh. Naveed Shahryar and Miss Sumera Afzal for Appellants.
 
Ch. Inayat Ullah for Respondents.
 
Dates of hearing: 1st and 2nd December, 2005.
 
JUDGMENT
 
Case 18

2006 C L C 200
 
[Lahore]
 
Before Muhammad Zafar Yasin, J
 
AMIR ABDULLAH and others----Petitioners
 
Versus
 
MUHAMMAD BUKHSH----Respondent
 
Civil Revision No.207 of 2000, decided on 16th March, 2004.
 
Punjab Pre-emption Act (IX of 1991)---
 
----Ss. 6, 13 & 31---Suit for pre-emption---Superior right of pre-emption and making of Talbs---Plaintiffs had claimed that when they came to know of sale of suit-land they made Talb-e-Muwathibat there and then and that within two weeks thereafter they sent notice of Talb-e-Ishhad through registered post---Plea of defendant/vendee was that Courts below had concurrently found that plaintiffs had made Talb-e-Muwathibat after about one month and 10 days of attestation of mutation of sale in question which was in the knowledge of plaintiffs---Defendant had stated that vendee plaintiffs had relinquished their right of pre-emption and they had not made Talb-e-Ishhad within two weeks of knowledge of sale mutation and it was duty of plaintiffs to first dislodge presumption of notice of sale under S.31 of Punjab Pre-emption Act, 1991 and then assert date of knowledge---Five pre-emptors were there in the case and nothing was on record to show that plaintiffs were in any way related to each other that they all were family members and had a joint living---None of plaintiffs appeared in Court to assert that they had acquired knowledge only on date when they made Talb-e-Muwathibat immediately---Even in evidence, plaintiffs had failed to prove, the date, time and place where all of them were present---Plaintiffs having failed to rebut presumption of notice of sale under S. 31 of Punjab Pre-emption Act, 1991, it would be presumed that they had attained knowledge of attestation of sale on the date it was attested and not on the date as alleged by plaintiffs---Courts below had rightly dismissed suit---Concurrent findings of two Courts below based on legal evidence, could not be interfered with by High Court in revision in absence of any misreading or non-reading of material evidence---Plaintiffs also could not state a single word about Zarrar and Zaroorat to prove their entitlement to their right of pre-emption on basis of Zarrar and Zaroorat as claimed by them---Revision against concurrent judgments of Courts below, was dismissed, in circumstances.
 
Kanwal Nain and 3 others v. Fateh Khan and others PLD 1983 SC 53 and Haji Rana Muhammad Shabbir Ahmad's case PLD 1994 SC 1 ref.
 
Ch. Arshad Mehmood for Petitioners.
 
Zahid Hussain Khan for Respondent.
 
Date of hearing: 16th March, 2004.
 
JUDGMENT
 
Case 19
 
2006 C L C 207
 
[Lahore]
 
Before Muhammad Jehangir Arshad, J
 
Mst. JAMILA BIBI----Petitioner
 
Versus
 
SHABIR AHMAD and 2 others----Respondents
 
Writ Petition No.5134 of 2005, heard on 19th October, 2005.
 
Guardians and Wards Act (VIII of 1890)---
 
----S. 25---Constitution of Pakistan (1973), Art.199---Constitutional petition---Custody of minor boy---Welfare of minor---Mother of minor boy having died, minor remained with his maternal grandmother/ petitioner---Respondent, who was father of minor, claiming himself to be natural guardian of minor, moved application under S.25 of Guardians and Wards Act, 1890 seeking custody, of minor---Guardian Judge accepting application of respondent directed that custody of minor be delivered to respondent and judgment of Trial Court was upheld in appeal---Petitioner had filed constitutional petition against concurrent judgments of both Courts below---Despite a specific issue regarding welfare of minor, neither Guardian Judge nor Appellate Court below had bothered to record findings with reference to evidence of parties to that effect and both Courts were mainly persuaded by the principle entitling father to obtain custody of a boy over seven years of age; whereas same was not a rule of thumb---Judgments recorded by two Courts below being violative of law were not sustainable, and were set aside and matter was remitted to Guardian Judge with direction to pass a fresh judgment after hearing arguments of both parties.
 
Sardar Hussain and others v. Mst. Parveen Umar and others PLD 2004 SC 357; Mst. Nighat Firdous v. Khadim Hussain 1998 SCMR 1593 and 5h. Abdus Salam and another v. Additional District Judge, Jhang and 2 others 1988 SCMR 608 ref.
 
Mian Arshad Latif for Petitioner.
 
Ch. Khalil Asghar Sindhu for Respondents.
 
Date of hearing: 19th October, 2005.
 
JUDGMENT
 
Case 20
 
2006 C L C 212
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
SHAH MUHAMMAD----Petitioner
 
Versus
 
CHIEF ELECTION COMMISSION OF PAKISTAN through Chief Election Commissioner and 4 others----Respondents
 
Writ Petition No.6006 of 2005, heard on 22nd November, 2005.
 
Punjab Local Government Elections Rules, 2000---
 
----Rr. 39, 40 & 42---Constitution of Pakistan (1973), Art.199---Constitutional petition---Declaration of result of election---Clerical error, correction of---Petitioner, according to consolidated statement in Form-XV had polled less votes than respondent and same result was described in Part-I of Form-XVI, prepared by Returning Officer, but in Part-Il of said Form, petitioner was recorded as winning candidate due to similarity, of names of the petitioner and respondent---Respondent applied to the Provincial Election Commissioner contending that he Polled 440 votes and that he was son of Noor Khan; but because of confusion due to similarly of names, petitioner, who was son of Said Khan, had been declared elected---Matter was referred to the Returning Officer, who corrected the record and issued a revised result---Validity---Such being purely a clerical error, Provincial Election Commissioner or Returning Officer by making such correction, had not done anything which could be said to be without lawful authority-Constitutional petition against impugned order, was dismissed.
Ch. Ihsan Ahmad for Petitioner.
 
Zafarullah Khan Khakwani, A.A.-G. for Respondent.
 
Malik Muhammad Bashir and Muhammad Aslam Sumra for Respondent No.5.
 
Ghazanfar Ali, Reader to Additional District and Sessions Judge/Returning Officer, U.C. No.38, Meeran Pur, Tehsil Rojhan, District Rajanpur with record.
 
Date of hearing: 22nd November, 2005.
 
JUDGMENT
 
Case 21
2006 C L C 214
 
[Lahore]
 
Before Mian Hamid Farooq, J
 
AZHAR ABBAS----Petitioner
 
Versus
 
DISTRICT JUDGE/DISTRICT RETURNING OFFICER/APPELLATE TRIBUNAL, NAROWAL and another---Respondents
 
Writ Petition No.14395 of 2005, decided on 11th August, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 152(1)(r)---Punjab Local Government Elections Rules, 2000, R.18-Constitution of Pakistan (1973), Art.199--- Constitutional petition---Rejection of nomination papers---Returning Officer, of his own accord, rejected nomination papers of petitioner on ground that he was involved in activities prejudicial to the Society, peace and integrity of Pakistan and due to that he was not qualified. to contest elections under S.152(1)(r) of Punjab Local Government Ordinance, 2001---No prima facie evidence and material had been placed on record, either before lower forums or even before High Court in order to demonstrate that petitioner was involved in any activities alleged against him---Was not discernible from record on what basis both forums had found that petitioner was involved in activities prejudicial to integrity of Pakistan---Petitioner could not be ousted from election process and deprived of contesting elections, only on the ground that name of petitioner's brother had been mentioned in the list prepared by D.P.O., especially when said list was questionable---Both lower forums had committed grave error in passing impugned orders---Impugned orders were set aside, nomination papers of petitioner stood accepted and he was allowed to contest elections.
Pervaiz Inayat Malik for Petitioner.
 
Muhammad Nawaz Bajwa, A.A.-G. for Respondents Nos.1 and 2.
 
Nemo for other Respondents.
 
Date of hearing: 10th August, 2005.
 
ORDER
 
Case 22
 
2006 C L C 216
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
MUHAMMAD RAMZAN----Petitioner
 
Versus
 
ADDITIONAL DISTRICT JUDGE, KABIRWALA and 3 others----Respondents
 
Civil Miscellaneous Nos.1864 and 1878 of 2005 in Writ Petition No.6106 of 2005, decided on 11th November, 2005.
 
Specific Relief Act (I of 1877)---
 
---Ss. 8 & 9---Constitution of Pakistan (1973), Art.199---Application for re-hearing of constitutional petition---Applicant had sought re-hearing of constitutional petition decided by High Court in factual background---Appellate Court below had dismissed civil revision filed against a decree passed in a suit filed under S.9 of Specific Relief Act, 1877 on sole ground that a revision in such a matter lay only to the High Court---Plea of applicant was that revision was not competent at all before Appellate Court below or even before High Court because at time when Specific Relief Act, 1877 containing S.9 was promulgated, Code of Civil Procedure 1908, was not in existence and no revisional power was available to any Court and that since S.9 of Specific Relief Act, 1877 had itself provided alternate remedy by way of a suit under S. 8 of the said Act, availability of said remedy would constitute a bar to exercise of revisional jurisdiction---Validity---Specific Relief Act was promulgated in 1877 and Code of Civil Procedure initially was promulgated in 1859 and that was followed by Code of Civil Procedure, 1877, thereafter Code of Civil Procedure, 1882 was enacted and finally present Code of Civil Procedure was brought on statute book in 1908---First Civil Procedure Code of 1859, was amended in 1861, to add S.35 conferring revisional powers on High Court which provision was re-enacted in 1877 and further in 1882 finally in 1908---Revisional jurisdiction, in circumstances was very much in existence when Specific Relief Act, 1877 containing S.9 was promulgated, contention of applicant, therefore, was without any basis---Section 115, C.P.C. was to operate on its own terms---Once conditions laid down in subsection (1) of S.115, C.P.,C. were satisfied High Court and District Court could make such order in the case as it would think fit provided the amount or value of subject-matter, ,would not exceed the limits of Appellate jurisdiction---Section 9 of Specific Relief Act,' 1877 clearly provided that no appeal would lie from any order or decree passed in a suit filed under said section and no review would be allowed---Application filed by applicant/petitioner for re-hearing of constitutional petition decided by High Court, was dismissed.
 
Riasat Ali v. Muhammad Jaffar Khan and 2 others 1991 SCMR 496 ref.
 
Khizar Hayat Khan Punyan and Ch. Muhammad Anwarul Haq for Petitioner.
 
ORDER
 
Case 23
2006 C L C 220
 
[Lahore]
 
Before Nazir Ahmed Siddiqui and Muhammad Nawaz Bhatti, JJ
 
Messrs R.B. AVARI ENTERPRISES LTD.----Appellant
 
Versus
 
Ch. ASGHAR ALI----Respondent
 
Regular First Appeal No.132 of 2002, decided on 18th July, 2005.
 
Civil Procedure Code (V of 1908)---
 
----S. 96 & O.VII, R.2---Suit for recovery of amount---Trial Court dismissed suit vide its judgment and decree and said judgment and decree of Trial Court had been impugned through appeal---Trial Court had taken great pains in examining the matter in its true perspective with reference to evidence available on file and leaving no material piece of evidence unnoticed in doing so---Trial Court had passed impugned judgment and decree on a due appreciation of law and fact, calling for no interference in appeal, which stood dismissed.
 
Ch. Ghulam-ud-Din Aslam for Appellant.
 
Mazhar Kaleem Khan for Respondent.
 
Date of hearing: 13th July, 2005.
 
JUDGMENT
 
Case 24
 
2006 C L C 225
 
[Lahore]
 
Before Muhammad Sayeed Akhtar, J
 
MUHAMMAD TUFAIL and others----Petitioners
 
Versus
 
DEPUTY COMMISSIONER, FAISALABAD and others----Respondents
 
Writ Petition No.21944 of 1999, heard on 10th May, 2005.
 
Colonization of Government Lands (Punjab) Act (V of 1912)---
 
----Ss. 10 & 30--Punjab Local Councils (Property) Rules, 1981, R.19---Constitution of Pakistan (1973), Art.199---Constitutional petition---Proprietary rights in respect of land---Entitlement---Petitioners, who claimed to be in possession of land as tenants of Government since 1983 and had constructed a shop thereon, moved application for sale of said State land through private treaty, but no action was taken on their application---Petitioners thereafter requested to grant them proprietary rights, but same was declined by the Authority---Validity---No order had been produced by petitioners showing that land in question was ever allotted to them or was given to them on lease by Government, but land in question was transferred, free of cost to Municipal Corporation and petitioners had been paying the rent to Municipal Corporation---Corporation was to sell property as per provisions of R.19 of Punjab Local Councils (Property) Rules, 1981, if it wished to do so, but it could not be compelled to sell its property to petitioners--High Court, however, directed that if the Corporation intended to dispose of property in question, same would be offered first to the petitioners.
 
Tariq Ahmad Farooqi for Petitioners.
 
Ch. Ali Muhammad and Ch. Jamshed Hussain, A.A.-G. for Respondents.
 
Date of hearing: 10th May, 2005.
 
JUDGMENT
 
Case 25
 
2006 C L C 227
 
[Lahore]
 
Before Fazal-e-Miran Chauhan, J
 
TEHSIL COUNCIL TRIBAL AREA (de-excluded area), D.G. KHAN through Tehsil Nazim----Petitioner
 
Versus
 
GOVERNMENT OF PUNJAB through Secretary, Local Government and Rural Development, Civil Secretariat, Lahore and 2 others----Respondents
 
Writ Petition No.5410 of 2003, decided on 30th May, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----Ss. 54 & 116---Constitution of Pakistan (1973), Art.199---Constitutional petition---Levy of tax on cement and cement stone---Tehsil Council vide one Notification levied tax on cement and vide another Notification levied local tax on cement stone---Cement Company filed separate appeals against levy of said taxes and Provincial Government accepting said appeals, directed Tehsil Council to withdraw said Notifications and levy of taxes/fees after approval as required under 5.116 of Punjab Local Government Ordinance, 2001---Validity---Tehsil Council, after filing petition had itself informed the cement company vide letter that cement company had been exempted from taxes at category (vii); in view of said latest development which took place during pendency of constitutional petition whereby petitioner vide its letter had admitted that levy of tax of all kinds of cement stones, marble stones etc., excavation and transportation through conveyor-belt, trucks and trolly of Cement Company had been exempted from tax category (iii) impugned order was implemented in letter and spirit by Tchsil Council---Tehsil Council, while in auction notice published in newspaper, tried to resile from its letter to Cement Company---Tehsil Council had contended that only transportation through conveyor-belt was exempted and issued order by imposing tax on all kinds of cement and marble stones etc. and on its excavation and transportation---Cement Company challenged that action of Tehsil Council by filing appeal before Provincial Government, which vide its order, again set aside action taken by Tehsil Council declaring that Local Governments were not competent to levy excavation tax and its levy as well as leasing out collection rights, and set aside the said order---Order of the Provincial Government had not been challenged by Tehsil Council nor any amendment had been sought in the constitutional petition---Constitutional petition was dismissed having become infructuous in circumstances.
 
PLD 1997 Kar. 62; 1999 SCMR 1402; 1993 SCMR 1342; PLD 1971 SC 401; PLD 1975 SC 506; PLD 1958 Lah. 887; PLD 1994 Lah. 175; PLD 1963 Kar. 319 and 2000 CLD 1010(sic) ref.
 
Mian Abbas Ahmad for Petitioner.
 
Abid Aziz Sheikh for Respondent.
 
Date of hearing: 11th April, 2005.
 
JUDGMENT
 
Case 26
2006 C L C 236
 
[Lahore]
 
Before Mian Hamid Farooq, J
 
Mian NISAR AHMED----Petitioner
 
Versus
 
Syed ZAFAR ABBAS SHAH----Respondent
 
Civil Revision No.947 of 2004, heard on 11th May, 2005.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 12(2), O.V, R.17 & O.XXXVII, Rr.2, 3 & 4---Suit for recovery of amount on basis of pro note---Ex parte judgment and decree---Setting aside of---Petitioner having failed to appear despite affixing summons at the outer door of his house, `he was proceeded ex parte and ex parte judgment and decree was passed against him---Application under S.12(2), C.P.C. seeking setting aside of ex parte judgment and decree, having been dismissed vide said order, petitioner had filed revision against said order---Impugned order not suffering from any legal infirmity was maintained and revision was dismissed.
Ayub Khan and another v. Fazal Haq and others PLD 1976 SC 422; Messrs Dadabhoy Cement Industries Ltd. and 6 others v. National Development Finance Corporation, Karachi 2002 SCMR 1761; Nazir Ahmed v. Muhammad Sharif and others 2001 SCMR 46 ref.
 
(b) Civil Procedure Code (V of 1908)---
 
----S. 12(2) & O.XIV---Judgment and decree were challenged on ground of fraud and misrepresentation---Courts were not hound to frame issues in every case when an application under S.12(2), C.P.C. was brought before the Court, however, in an appropriate case, Courts were allowed to frame issues.
 
Ghulam Muhammad. v. M. Ahmad Khan and 6 others 1993 SCMR 662; Mst. Ume Kalsoom v. Zahid Bashir through Legal Heirs and another 1999 SCMR 1696; Abdul Razzaq v. Muhammad Islam and 3 others 1999 SCMR 1714 and Mrs. Amina Bibi through General Attorney v. Nasrullah and others 2000 SCMR 296 ref.
 
Ch. Ghulam Mustafa Shahzad for Petitioner.
 
Tariq Ahmed Farooqi for Respondent.
 
Date of hearing: 11th May, 2005.
 
JUDGMENT
 
Case 27
2006 C L C 243
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
GHULAM MURTAZA SHAH and another----Petitioners
 
Versus
 
CHIEF ELECTION COMMISSIONER OF PAKISTAN, ISLAMABAD and 4 others----Respondents
 
Writ Petitions Nos.5221, 5132 and 5549 of 2005, decided on 28th September, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)--------
 
---S. 152(1)(b)-Constitution of Pakistan (1973), Art.199---Constitutional petition---Election for the seat of Nazim/Naib Nazim---Disqualification of candidate being under-age---Matriculation Certificates admittedly were filed and relied upon by candidates showing the candidates as under-age, inference would be that entry of date of birth was based on informations provided by the candidates themselves in the forms filled and signed by them---Orders passed by Returning Officer accepting nomination papers of under-age candidates being without lawful authority, were set aside by High Court.
 
C.P. No.2137 of 2005 and Writ Petition No.5659 of 2005 distinguished.
 
Pir Masood-ul-Hassan Chishti for Petitioner.
 
Mehmood Ashraf Khan for Respondents Nos.4 and 5.
 
ORDER
 
Case 28
 
2006 C L C 247
 
[Lahore]
 
Before Sardar Muhammad Aslam, J
 
SHAHAMAND ALI----Appellant
 
Versus
 
MUHAMMAD ASHFAQ----Respondent
 
Regular First Appeal No.208 of 2004, heard on 8th September, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXVII, Rr.2 & 3---Suit for recovery of amount on basis of promissory note--Application for leave to defend suit---Authenticity of promissory note on basis of which suit was filed, had been challenged by defendant alleging that it was obtained by plaintiff under threat and coercion---Plaintiff by examining himself as his own witness, had proved contents of promissory note---Marginal witnesses of said promissory note, had corroborated stance of plaintiff---Defendant had admitted that he had not initiated any proceedings before any forum complaining against alleged act of obtaining thumb-mark/signature under pressure---Defendant had also admitted that he had not submitted any application to superior officer against person who allegedly made him to sign promissory note---Defendant neither lodged any report before police regarding alleged coercion and threats nor filed suit for seeking cancellation of said promissory note---Contention of defendant with regard to coercion and threat, was not believable, in circumstances---Trial Court, after examining all aspects of case rightly, decreed the suit---Judgment of Trial Court did not call for any interference.
Muhammad Sharif Chohan for Appellant.
 
Shezad Saleem Bhatti for Respondent.
 
Date of hearing: 8th September, 2005.
 
JUDGMENT
 
Case 29
 
2006 C L C 251
 
[Lahore]
 
Before Fazal-e-Miran Chauhan, J
 
Mst. SHAZIA KAUSAR----Petitioner
 
Versus
 
MUHAMMAD AHMED and another----Respondents
 
Writ Petition No.5541 of 2005, decided on 3rd October, 2005.
 
Muslim Family Laws Ordinance (VIII of 1961)---
 
---Ss. 9 & 10---Constitution of Pakistan (1973), Art.199---Constitutional petition---Suit for maintenance and recovery of prompt dower---Suit was decreed but decree was set aside in appeal---Non-payment of prompt dower---Separate living by wife---Maintenance---Entitlement---Appellate Court failed to note essential legal implications of non-payment of dower namely that wife, in such circumstances, was under no obligation to live with husband and husband was duty bound to maintain wife during period of separation---Failure of Appellate Court to consider said facts constituted non-exercise of its jurisdiction---Impugned judgment of Appellate Court was, therefore, declared without lawful authority with the result that both the appeals of petitioner were to be deemed pending for fresh decisions.
 
Mst. Chanani Begum v. Muhammad Shafiq and others 1985 MLD 310 and Tahira Begum's case PLD 1971 Lah. 866 ref.
 
Ch. Muhammad Anwar-ul-Haq for Petitioner.
 
Nemo. for Respondent No.1.
 
Respondent No.2 is pro forma respondent.
 
ORDER
 
Case 30
2006 C L C 255
 
[Lahore]
 
Before Syed Shabbar Raza Rizvi, J
 
MUHAMMAD RAZZAQ and another----Petitioners
 
Versus
 
DISTRICT RETURNING OFFICER, NAROWAL and 3 others----Respondents
 
Writ Petition No.14368 of 2005, decided on 17th August, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----Ss. 152(1)(s) & 153---Constitution of Pakistan (1973), Art.199---constitutional petition---Disqualification of candidate---Petitioner had alleged that respondent was not qualified to participate in elections as he being General Secretary of ruling party was using influence of his Party---petitioner referred newspaper clippings showing that respondent gave advertisement in daily newspaper welcoming the President of Pakistan and the Chief Minister Punjab when they visited the District concerned---No other substantial material had been produced to convince the Court that respondent was using his party's influence---Effect---Under S.152(1)(s) of Punjab Local Government Ordinance 2001, it was a disqualification if a person was using his party's flag, financial resources or other resources which could give him advantage over other contesting candidate---Something visible having not been produced or brought on record by petitioner, High Court could not disentitle a person who otherwise was a valid candidate.
Ch. Anwar-ul-Haq Pannu for Petitioner.
 
Pervaiz Inayat Malik for Respondent No.3.
 
Najeeb Faisal Chaudhary, Addl. A.-G.
 
Date of hearing: 17th August, 2005.
 
ORDER
 
Case 31
 
2006 C L C 258
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
MUNAWAR HUSSAIN----Petitioner
 
Versus
 
MEMBER (JUDICIAL-V), BOARD OF REVENUE, PUNJAB, LAHORE and 4 others----Respondents
 
Writ Petition No.313 of 2003, heard on 20th October, 2005.
 
West Pakistan Land Revenue Rules, 1968-
 
--R. 18(1)(a)-Constitution of Pakistan (1973), Art.199---Constitutional petition---Appointment of Lumberdar---Appointment of the petitioner as Lumbardar was challenged on the ground that he was convicted in a murder case and as such he was not competent to be appointed as Lumberdar---Validity---Rule 18 of West Pakistan Land Revenue Rules, 1968 provided that Lumberdar would be dismissed only if he had been convicted and sentenced for an offence involving moral turpitude but in the present case no moral turpitude was involved as it was a fight between two groups of persons and without any previous enmity whatsoever---In absence of any allegation that respondent possessed more land or better educational qualification than the petitioner or some other distinction which rendered the former more suitable candidate than latter for the job, impugned order of Executive District Officer (Revenue) remanding the case to District Officer (Revenue) was without lawful authority and was accordingly set aside by High Court.
 
Criminal Appeal No.35 of 1982 ref.
 
M. Arif Alvi for Petitioner.
 
Mian Arshad Lateef for Respondent No.3.
 
Nemo for other Respondents.
 
Date of hearing: 20th October, 2005.
 
JUDGMENT
 
Case 32
2006 C L C 265
 
[Lahore]
 
Before Sh. Abdul Rashid, J
 
FAQIR ABDUL MAJEED KHAN----Petitioner
 
Versus
 
DISTRICT RETURNING OFFICER, MIANWALI and 4 others----Respondents
 
Writ Petition No.17196 of 2005, heard on 2nd November, 2005.
 
(a) Punjab Local Government Elections Rules, 2005---
 
----R. 36(3)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Proceedings for counting of votes---Application for re-counting of votes was allowed---Examination of invalid votes before consolidating the final result---Initial count reversed---Question was as to whether direction made by District Returning Officer to the Returning Officer for looking into invalid votes was violative of Rule 36 of Punjab Local Government Elections Rules, 2005---Rule 36 sub-rule (3) of Punjab Local Government Elections Rules, 2005 had made it mandatory for the Returning Officer to examine the ballot papers excluded from the count by Presiding Officer and if he found that such ballot papers should not have been so excluded he would count said ballot papers as cast in favour of candidate for whom the votes had otherwise been cast---District Returning Officer in his direction, had only required the Returning Officer to carry out his legal duty with regard to consolidation of result under Rule 36(3) of the Rules and consequently Returning Officer had proceeded accordingly---Returning Officer had been debarred by Rule 36(6) of the Rules from re-counting only valid ballot papers unless so directed by the District Returning Officer and not from counting invalid votes---Direction of District Returning Officer, therefore, was not violative of Rule 36(3) of Punjab Local Government Elections Rules, 2005.
 
(b) Punjab Local Government Elections Rules, 2005---
 
----R. 65---Constitution of Pakistan (1973), Art.199---Constitutional petition---Maintainability---Rule 65 of Punjab Local Government Elections Rules, 2005 expressly prohibits any election to be called in question except by an election petition before Election Tribunal---Constitutional petition under Article 199 of the Constitution was not maintainable in presence of an alternate and efficacious remedy available under Rule 65 of Punjab Local Government Elections Rules, 2005.
 
Dr. Khalid Ranjha for Petitioner.
 
Malik Noor Muhammad Awan, Muhammad Ramzan Ch. and Najeeb Faisal Ch., Addl.A.-G. for Respondents.
 
Date of hearing: 2nd November, 2005.
 
JUDGMENT
 
Case 33
 
2006 C L C 321
 
[Lahore]
 
Before Muhammad Jehangir Arshad, J
 
HABIB ULLAH----Petitioner
 
Versus
 
Mst. KAUSAR and another---Respondents
 
Writ Petition No.178 of 2005/BWP, decided on 26th May, 2005.
 
West Pakistan Family Courts Act (XXXV of 1964)---
 
---Ss. 7, 9 & 11---Constitution of Pakistan (1973), Art.199---Constitutional petition---Closing of evidence by Family Court---Presiding Officer of the Court being on leave on the date fixed for recording of evidence of petitioner, case was adjourned by Reader of the Court---Evidence of petitioner being not available, on the adjourned date of hearing, Judge Family Court closed evidence of petitioner after refusing petitioner to grant any further opportunity for producing evidence---Validity--Adjournment granted by the Reader of the Court being not at the instance of petitioner, it would have been more appropriate for Trial Court to have given one more opportunity to petitioner for production of his evidence, which could be for one or two days---Reader of the Court had no authority to fix date for recording of evidence in absence of the Presiding Officer, unless so authorized by any specific order of the Chief Justice---ht absence of any expressed authority, it would be disastrous to allow Readers to fix dates of hearing---Proceedings conducted by Reader of the Court, were declared as without lawful authority and of no legal effect and in consequence thereof, impugned order of Judge Family Court closing evidence of petitioner, was set aside, with direction to allow one or two opportunities to petitioner to produce evidence and finally decide case till the specified date by not granting unnecessary adjournments to petitioner.
 
Irfan Majeed Rehmani for Petitioner.
 
Rashid Afzaal Cheema for Respondent No.1.
 
Date of hearing: 26th May, 2005.
 
JUDGMENT
 
Case 34
2006 C L C 324
 
[Lahore]
 
Before Abdul Shakoor Paracha, J
 
NAYYAR IQBAL and another----Petitioners
 
Versus
 
APPELLATE AUTHORITY and 2 others-Respondents
 
Writ Petition No.2245 of 2005, decided on 9th August, 2005.
 
(a) Punjab Local Government Ordinance (XIII of 2001)---
 
----Ss. 152(1)(i) & 152(2)(a)---Punjab Local Government Elections Rules 2005, R.14(2) & Form XIX---Constitution of Pakistan (1973), Art.199---Constitutional petition---Declaration in Form XIX, Punjab Local Government Elections Rules, 2005---Concealment of certain assets---Rejection of nomination papers by Returning Officer---Appeal against---Contention of candidate was that in absence of any declaration on the mandate of section 152(2) of Punjab Local Government Ordinance, 2001 by the Chief Election Commissioner, order of Returning Officer was not sustainable---Validity---Provisions of section 152(2) of the Ordinance had been inserted in Punjab Local Government Ordinance, 2001 to cater the post-election scenario because proceedings of disqualification under section 152(1) of the Ordinance had to be initiated on application made by any person or by Chief Election Commissioner on his own motion and Election Commission or any authority authorized by it might issue notice to show cause to a member, Nazim, as the case might be---Candidate having not disclosed his actual assets, Returning Officer, had jurisdiction to reject nomination papers of such candidate.
Qaiser Rashid Bhatti and 3 others v. Secretary, Government of the Punjab, Local Government Commission, Lahore and 3 others 2003 CLC 1936 and Abbas Khan and another v. Appellate Authority, District and Sessions Judge, Attock 2002 SCMR 398 ref.
 
(b) Punjab Local Government Ordinance (XIII of 2001)---
 
----Ss. 2(xix), 2(xxiii) & 2(xxiv)---"Member", "Naib Nazim" and "Nazim"---Meanings---Words "member", "Naib Nazim" and "Nazim" as used and defined in section 2(xix), (xxiii) & (xxiv) of Punjab Local Government Ordinance, 2001 mean the elected member, Naib Nazim and Nazim of their Council.
 
(c) Punjab Local Government Ordinance (XIII of 2001)-
 
----S. 152(1)(h)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Disqualification on the ground of having committed moral offence---Contention of candidate was that he was removed from service on disciplinary grounds, therefore, provision of section 152(1)(h) was not attracted in his case---Validity---Order of compulsory retirement of the candidate passed by competent Authority clearly expressed that candidate had been compulsorily retired from service being a corrupt official---Corruption could be said as a moral offence---Candidate, therefore, had been rightly declared as disqualified as per provisions of section 152(1)(h) of Punjab Local Government Ordinance, 2001---Concurrent findings being correct, called for no interference by High Court in exercise of its constitutional jurisdiction.
 
Ibad-ur-Rehman Lodhi for Petitioner.
 
Ch. Fawad Hussain for Respondent No.3.
 
ORDER
 
Case 35
2006 C L C 328
 
[Lahore]
 
Before Maulvi Anwarul Haq and Muhammad Jehangir Arshad, JJ
 
AHMAD ZAMAN KHAN----Appellant
 
Versus
 
MUGHIS A. SHEIKH and another----Respondents
 
R.F.A. No.122 of 1998, heard on 3rd October, 2005.
 
Pakistan Water and Power Development Authority Act (XXXI of 1958)---
 
---S. 14(2)---Civil Procedure Code (V of 1908), S.79---Constitution of Pakistan (1973), Art.174---Suit for damages---Maintainability---Appellant, who claimed to be owner of land, had filed a suit for recovery of Rs.50,00,000 as damages on ground that Electricity Supply Company, had installed electricity poles in said land without his consent, rendering his land uncultivatable and causing appellant mental torture and financial loss---Trial Court having dismissed suit, appellant had filed appeal against judgment of Trial Court---Electric Supply Company was a limited Company registered under Companies Act, 1913, Managing Director of said Company was not liable in his personal capacity for act of the company---No suit, in circumstances could be filed against the Managing Director of the Company, in his personal capacity---Trial Court had rightly found that Managing Director of the Company was not a necessary party and suit could not proceed against him in his personal capacity---Company was nationalized through Economic Reforms Order, 1972 and assets and liabilities of said Company were firstly taken over by Federal Government and later on were handed over to Water and Power Development Authority in terms of M.L.O. No.85 issued on 14-6-1981; since then WAPDA had been performing functions of defunct Electric Supply Company---Appellant neither impleaded Federation of Pakistan nor WAPDA with its correct nomenclature---Any suit filed against Federation in violation of either Art.174 of the Constitution or S.79, .C.P.C. was not maintainable---Suit was also not maintainable in view of S.14(2) of Pakistan Water and Power Development Authority Act, 1958---Suit was rightly dismissed by Trial Court, in circumstances.
1999 SCMR 16 and Malik Haji Nazar Muhammad and another v. WAPDA and another PLD 1991 SC 715 ref.
 
Muhammad Akhtar Khan for Appellant.
 
Rao Riasat Ali Khan for Respondent.
 
Date of hearing: 3rd October, 2005.
 
JUDGMENT
 
Case 36
2006 C L C 331
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
Mst. GULSHAN PARVEEN----Petitioner
 
Versus
 
MUHAMMAD TAYYAB----Respondent
 
Civil Revision No.651 of 2005, heard on 16th November, 2005.
 
Suits Valuation Act (VII of 1887) ---
 
----S. 11---Specific Relief Act (I of 1877), Ss.8 & 42---Revision petition---Suit for declaration and possession---Improper valuation of suit for the purpose of court-fee and jurisdiction---Objection against---Appellate Court set aside judgment and decree of Trial Court on ground that Trial Judge being Court of Judge-III Class, had no pecuniary jurisdiction to try and decide suit, value whereof was 6/7 lacs---Case was referred for entrustment to Civil Judge 1st Class for fresh decision---No objection had been taken in written statement to pecuniary jurisdiction of the Court as it was filed in the Court of Civil Judge 1st Class---Case was entrusted to Civil Judge-III Class in routine---Neither in first appeal nor in second appeal, any objection was taken to pecuniary jurisdiction of Trial Court---No objection was taken to jurisdiction of Civil Judge-III Class till such time that suit was decided---Section 11 of Suits Valuation Act, 1887, provided for entertaining of objection by a party to pecuniary jurisdiction of a Court in an appeal and it had provided in clear terms that such an objection would not be entertained by Appellate Court unless objection was taken in the Court of first instance---Neither any objection was taken at any stage in the Trial Court to the jurisdiction of Civil Judge-III Class nor any finding was recorded by the Court of first appeal that there had been a failure of justice on merits of the case because of said defect---Impugned order, in circumstances, was wholly without lawful authority and could not be sustained---High Court allowing revision, set aside impugned order with the result that first appeal filed by petitioner would be deemed to be pending before Appellate Court and would be decided on merit within specified period.
 
Rana Meraj Khalid for Petitioner.
 
Tariq Muhammad Iqbal for Respondent.
 
Date of hearing: 16th November, 2005.
 
JUDGMENT
 
Case 37
 
2006 C L C 334
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
HASNAIN AHMED SHAH----Petitioner
 
Versus
 
IJAZ AHMED SHAH and another----Respondents
 
Civil Revision No.2172 of 2005, decided on 20th October, 2005.
 
(a) Civil Procedure Code (V of 1908)----
 
---O. XXIII, R.3---Qanun-e-Shahadat (10 of 1984), Arts. 163 & 129---Specific Relief Act (I of 1877), S.12---Suit for specific performance of oral agreement to sell---Offer of plaintiff to decide matter on statement on oath by the defendants---Plaintiff had not denied his offer of decision of his suit on the basis of statement by the defendants which was also in, line with requirement in his two earlier applications under Article 163 of Qanun-e-Shahadat, 1984---Plaintiff did not refute his own statement before Trial Court nor he moved application resiling his offer instead he accepted the mode of statement by defendants and signed defendant's, statement in presence of his counsel---Order sheet was signed by some other Advocate just for identification purposes---Plaintiff, having done all this on losing the case, could not be permitted to turn back to say that statement of defendants was not recorded on oath of Holy Qur'an---Presumption of correctness was always attached to judicial proceedings---Plaintiff's contention that statement of defendants should have been recorded on oath of Holy Qur'an was repelled in circumstances.
 
(b) Civil Procedure Code (V of 1908)----
 
-------O. XXIII, R.3---Qanun-e-Shahadat (10 of 1984), Art.163---Specific Relief Act (I of 1877), S.12---Suit for specific performance of oral agreement to sell---Statement by defendants on oath as per offer by the plaintiff and dismissal of suit on basis thereof---Question was as to whether procedure adopted by Trial Court was not covered by O. XXIII, Rule 3, C.P.C.---Plaintiff in absence of any documentary proof out of his own free-will called upon defendants for making statement on oath of.' Holy Qur'an before Court that if the defendants stated that there was no agreement between the parties, his suit be dismissed---Such offer was not accepted by the defendants, but plaintiff's offer to make statement without oath on Holy Qur'an was accepted by the defendants---Such factual aspect made both the Courts below felt satisfied about genuineness of the compromise between the parties and procedure adopted by Trial Court was in accordance with O.XXIII, R.3, C.P.C.---No illegality or irregularity having been pointed out, revision petition was without merit and was dismissed by High Court.
 
Madan Mohan Gargh v. Murcia Lal and others AIR 1928 All. 497 and Muhammad Ijaz and 3 others v. M. Khurshid Malik and 4 others 1986 CLC 2270 ref.
 
Muhammad Zaman Qureshi for Petitioner.
 
ORDER
 
Case 38
2006 C L C 349
 
[Lahore]
 
Before Mian Hamid Farooq, J
 
ABDUL RAZAQ SALEEMI and another----Petitioners
 
Versus
 
DISTRICT RETURNING OFFICER, GUJRAT and another----Respondents
 
Writ Petition No.14484 of 2005, decided on 11th August, 2005.
 
Punjab Local Government Elections Rules, 2000---
 
----Rr. 16 & 18---Constitution of Pakistan (1973), Art.199---Constitutional petition---Rejection of Nomination papers---Respondent had raised an objection that one petitioner was not an eligible voter as he was not enlisted in the voters list---Returning Officer rejected said objection, but on appeal District Returning Officer vide impugned order set aside judgment of Returning Officer and rejected nomination papers of petitioners---Both parties had placed on record various documents in support of their respective claims, which prima facie, went counter to each other---Certified copy, issued by office of District Returning Officer, signed by Returning Officer, had shown that name of one petitioner did exist, while documents produced by one of respondents manifested that petitioner was not a registered voter---Both parties had disputed the veracity of documents produced by other party and it could not be determined and conclusively found as to which set of documents was genuine and which was forged---If documents produced by petitioners were summarily brushed aside, they would be deprived from participating in election---High Court, in exercise of constitutional jurisdiction, could not determine the genuineness of documents, which exercise could only be undertaken after recording evidence and it would be in the fitness of things if petitioners were allowed to contest election and if they succeeded, respondents could raise said question in Election petition which would be decided by Election Tribunal after recording evidence---Order passed by District Returning Officer was set aside and that of Returning Officer stood restored and petitioners were allowed to contest election accordingly.
 
Haji Arshad Ali v. Sardar Faisal Zaib and others 2003 SCMR 1848 ref.
 
Muhammad Masood Chishti for Petitioners.
 
Muhammad Nawaz Bajwa, A.A.-G. for Respondent No.1.
 
Malik Hamid Jamil Awan for Respondent No.2.
 
Date of hearing: 11th August, 2005.
 
ORDER
Case 39

2006 C L C 349
 
[Lahore]
 
Before Mian Hamid Farooq, J
 
ABDUL RAZAQ SALEEMI and another----Petitioners
 
Versus
 
DISTRICT RETURNING OFFICER, GUJRAT and another----Respondents
 
Writ Petition No.14484 of 2005, decided on 11th August, 2005.
 
Punjab Local Government Elections Rules, 2000---
 
----Rr. 16 & 18---Constitution of Pakistan (1973), Art.199---Constitutional petition---Rejection of Nomination papers---Respondent had raised an objection that one petitioner was not an eligible voter as he was not enlisted in the voters list---Returning Officer rejected said objection, but on appeal District Returning Officer vide impugned order set aside judgment of Returning Officer and rejected nomination papers of petitioners---Both parties had placed on record various documents in support of their respective claims, which prima facie, went counter to each other---Certified copy, issued by office of District Returning Officer, signed by Returning Officer, had shown that name of one petitioner did exist, while documents produced by one of respondents manifested that petitioner was not a registered voter---Both parties had disputed the veracity of documents produced by other party and it could not be determined and conclusively found as to which set of documents was genuine and which was forged---If documents produced by petitioners were summarily brushed aside, they would be deprived from participating in election---High Court, in exercise of constitutional jurisdiction, could not determine the genuineness of documents, which exercise could only be undertaken after recording evidence and it would be in the fitness of things if petitioners were allowed to contest election and if they succeeded, respondents could raise said question in Election petition which would be decided by Election Tribunal after recording evidence---Order passed by District Returning Officer was set aside and that of Returning Officer stood restored and petitioners were allowed to contest election accordingly.
 
Haji Arshad Ali v. Sardar Faisal Zaib and others 2003 SCMR 1848 ref.
 
Muhammad Masood Chishti for Petitioners.
 
Muhammad Nawaz Bajwa, A.A.-G. for Respondent No.1.
 
Malik Hamid Jamil Awan for Respondent No.2.
 
Date of hearing: 11th August, 2005.
 
ORDER
 
Case 40
 
2006 C L C 354
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
DUR MUHAMMAD----Appellant
 
Versus
 
ABDUL RAZZAQ----Respondent
 
Civil Revision 361-D of 1994, heard on 14th November, 2005.
 
Specific Relief Act (I of 1877)---
 
----Ss. 12, 42 & 54---Transfer of Property Act (IV of 1882), S.58(c)-Suit for specific performance of agreement, declaration and permanent injunction---Mortgage of property---Plaintiff had stated -that defendant had mortgaged suit-land for a period of one month to him with possession against amount' with the condition that in case mortgaged amount was not paid within said period of one month's time, suit-land would stand sold to plaintiff---Mortgaged money having not been paid within stipulated period, plaintiff had claimed to be in possession of suit-land under said agreement and he sought a decree for declaration to the effect that he was owner of suit-land on basis of said mortgage agreement which stood converted into an agreement to sell---Plaintiff also sought a permanent injunction and prayed for decree for specific performance of agreement---Suit was concurrently decreed by Trial Court and Appellate Court below---Validity---Suit-land was primarily mortgaged as per terms of agreement arrived at between the parties and nothing was available in plaint or in evidence that primary intention was to sell the suit-land---Both Courts, below were not justified to hold document of mortgage as an agreement to sell or a sale---Judgments and decrees passed by Courts below, were set aside and suit was dismissed---Defendant could get suit-land redeemed in accordance with law.
 
Abdul Sattar v. Mst. Sardar Begum and 12 others 1992 SCMR 417 and Ganu Mia v. Abdul Jammar and others PLD 1959 Dacca 293 ref.
 
M. Suleman Bhatti and Athar Rehman for Petitioner.
 
Mazhar Kaleem Khan for Respondent.
 
Date of hearing: 14th November, 2005.
 
JUDGMENT
 
Case 41
 
2006 C L C 369
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
MUHAMMAD TAHIR BAIG----Petitioner
 
Versus
 
MEMBER (CONSOLIDATION), BOARD OF REVENUE PUNJAB, LAHORE and 2 others----Respondents
 
Writ Petition No.7053 of 1995, heard on 15th April, 2005.
 
West Pakistan Consolidation of Holdings Ordinance (VI of 1960)---
 
----Ss. 9, 10 & 13---Constitution of Pakistan (1973), Art.199---Constitutional petition---Consolidation Scheme---Claim of petitioner was that entire Khasra in question was exclusively owned by him prior to consolidation, but two Kanals out of said Khasra number had been given to respondent---Petitioner had prayed that said area of two Kanals be placed in his Wanda---Revenue record showed that Khasra number in question measuring 8 Kanals was owned by petitioner and his brother in equal shares and 3 Kanals and 8 Marlas were allocated to petitioner, which would mean that out of total entitlement in Khasra in question, of 4 Kanals which fell in share of petitioner, he was allotted 3 Kanals and 8 Marlas in said Khasra number, and out of same 2 Kanals were given to respondent---Petitioner could not lay claim to 2 Kanals of land when he had already been allocated 3 Kanals and 8 Marlas leaving only balance of 12 Marlas of his original entitlement---Neither Collector nor Additional Commissioner examined the record and both of them had passed their respective orders on assumption that petitioner was original owner of said 2 Kanals of land---Scheme was confirmed with consent of petitioner and his co-sharer/his brother---Member (Consolidation) Board of Revenue, had rightly set aside unjust orders of Collector and Commissioner and impugned order passed by Member, Board of Revenue could not be interfered with by High Court in exercise of its constitutional jurisdiction.
 
Ch. Ayyaz Muhammad Khan for Petitioner.
 
Khanzada Azmat Ali with Din Muhammad Patwari for Respondent No.1
 
Sahibzada Mahboob Ali Khan for Respondent No.2.
 
Abdul Sattar Bhutto for Respondent No.3.
 
Date of hearing: 15th April, 2005.
 
JUDGMENT
 
Case 42
 
2006 C L C 375
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Mst. FATIMA BIBI and another----Petitioners
 
Versus
 
MUHAMMAD IKRAM and another----Respondents
 
Civil Revision No.2530-D of 1996, heard on 25th October, 2005.
 
Qanun-e-Shahadat (10 of 1984)---
 
----Arts. 117, 120 & 129(g)---Specific Relief Act (I of 1877), S.42---General power of attorney and sale-deed---Execution of documents by Pardanashin ladies---Plea of fraud and misrepresentation---Onus to prove---Admittedly attorney/the second defendant was son and brother of both the ladies/plaintiffs respectively and thus, was close member of the family---Said attorney through the same sale-deed had sold his own share of property and had never alleged any fraud practised upon him by vendee the first defendant---Mere appendage of thumb-impressions by an illiterate Pardanashin lady upon document, particularly involving her valuable property rights could not be considered to be valid execution but for the presence of the second defendant a close member of the family, coupled with the fact that documents were also read over to the ladies as had been deposed by witnesses and that power of attorney and sale deed both were executed by ladies after those were read over to them---Not the defendants but ladies and attorney, after sale of their property, had filed collusive suit to harass and blackmail a bona fide purchaser---No presumption of withholding the best evidence could be drawn against non-appearance of vendee in person in the light of Art.129(g) of Qanun-e-Shahadat, 1984---Principles governing Pardanashin ladies having been fulfilled and petition being without merit same was dismissed by High Court.
 
Ghulam Ali and 2 others v. Mst. Ghulam Sarwar Naqvi PLD 1990 SC 1 and Amirzada Khan and another v. Itbar Khan and others 2001 SCMR 609 ref.
 
Hafiz Muhammad Yousaf for Petitioners.
 
M.A. Zafar and Muhammad Shoaib Zafar for Respondents.
 
Date of hearing: 25th October, 2005.
 
JUDGMENT
 
Case 43
 
2006 C L C 375
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Mst. FATIMA BIBI and another----Petitioners
 
Versus
 
MUHAMMAD IKRAM and another----Respondents
 
Civil Revision No.2530-D of 1996, heard on 25th October, 2005.
 
Qanun-e-Shahadat (10 of 1984)---
 
----Arts. 117, 120 & 129(g)---Specific Relief Act (I of 1877), S.42---General power of attorney and sale-deed---Execution of documents by Pardanashin ladies---Plea of fraud and misrepresentation---Onus to prove---Admittedly attorney/the second defendant was son and brother of both the ladies/plaintiffs respectively and thus, was close member of the family---Said attorney through the same sale-deed had sold his own share of property and had never alleged any fraud practised upon him by vendee the first defendant---Mere appendage of thumb-impressions by an illiterate Pardanashin lady upon document, particularly involving her valuable property rights could not be considered to be valid execution but for the presence of the second defendant a close member of the family, coupled with the fact that documents were also read over to the ladies as had been deposed by witnesses and that power of attorney and sale deed both were executed by ladies after those were read over to them---Not the defendants but ladies and attorney, after sale of their property, had filed collusive suit to harass and blackmail a bona fide purchaser---No presumption of withholding the best evidence could be drawn against non-appearance of vendee in person in the light of Art.129(g) of Qanun-e-Shahadat, 1984---Principles governing Pardanashin ladies having been fulfilled and petition being without merit same was dismissed by High Court.
 
Ghulam Ali and 2 others v. Mst. Ghulam Sarwar Naqvi PLD 1990 SC 1 and Amirzada Khan and another v. Itbar Khan and others 2001 SCMR 609 ref.
 
Hafiz Muhammad Yousaf for Petitioners.
 
M.A. Zafar and Muhammad Shoaib Zafar for Respondents.
 
Date of hearing: 25th October, 2005.
 
JUDGMENT
 
Case 44
 
2006 C L C 400
 
[Lahore]
 
Before Syed Shabbar Raza Rizvi, J
 
ZULFIQAR ALI and another----Petitioners
 
Versus
 
DISTRICT RETURNING OFFICER and 7 others----Respondents
 
Writ Petition No.14346 of 2005, decided on 15th August, 2005.
 
Punjab Local Government Elections Rules, 2000---
 
----Rr. 16 & 18---Constitution of Pakistan (1973), Art.199---Constitutional petition---Nomination papers---Rejection of---Nomination papers filed by petitioners for the election of Nazim and Naib Nazim were accepted by Returning Officer and at the time of scrutiny also no objection was filed against such acceptance---Respondents, however filed appeal against acceptance of nomination papers of petitioner and Returning Officer accepted same on the ground that according to report by District Police, petitioner belonged to a banned organization---Supreme Court in another case in which candidates remained associated with a banned organization, were provisionally allowed to contest election and petitioners, therefore, were allowed to contest election provisionally in obedience of said judgment---Order of District Returning Officer was set aside in circumstances.
 
Sh. Umar Draz for Petitioners.
 
Muhammad Yousaf Phiphra for Respondent No.3.
 
 
ORDER
 
Case 45

2006 C L C 412
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
KHUSHI MUHAMMAD----Appellant
 
Versus
 
MANSOOR-UZ-ZAMAN and others----Respondents
 
Regular Second Appeal No.73 of 1997, decided on 12th May, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Suit for specific performance of agreement of sale---Claim of plaintiff was that out of total consideration of Rs.82,500, defendants/vendors had received a sum of Rs.50,000 as earnest money, whereas balance consideration amount of Rs.32,500 was payable on date when sale-deed was to be finalized and got registered-.Defendants accepted execution of agreement of sale, but they denied receipt of balance consideration amount of Rs.32,500---Trial Court decreed suit holding that payment of balance consideration had been established through witnesses produced by plaintiff---Appellate Court below set aside judgment and decree of Trial Court and had granted alternative decree for return of amount of Rs.50,000 which was received by defendants/vendors as earnest money---Plaintiff had failed to establish payment of balance amount, which had serious reflection upon his readiness and willingness to perform his part of agreement---Under equity, plaintiff could not seek specific performance of agreement, which he could not perform---Contention of plaintiff that the Court should have directed specific enforcement on payment of balance amount of Rs.32,500 if payment of same was not proved, was repelled, because no person in equity, could be permitted to take advantage and premium of his own inequitable action---As non-payment of balance consideration was the fault and violation of agreement on part of plaintiff, he could not enforce agreement of sale.
 
Ch. Muhammad Abdullah for Appellant.
 
Ch. Zafar Iqbal and Abdul Rasheed Qureshi for Respondent No.4.
 
Date of hearing: 12th May, 2005.
 
JUDGMENT
 
Case 46
 
2006 C L C 427
 
[Lahore]
 
Before Muhammad Jehangir Arshad, J
 
AESH MUHAMMAD----Petitioner
 
Versus
 
PROVINCE OF PUNJAB through Collector, Sheikhupura and 3 others----Respondents
 
Civil Revision No.1972-D of 1996, decided on 15th September, 2005.
 
West Pakistan Land Revenue Act (XVII of 1967)---
 
----S. 91---Specific Relief Act (I of 1877), Ss.42 & 54---Recovery of amount as arrears of land revenue---Suit for declaration and permanent injunction---Suit was filed seeking declaration that plaintiff was neither defaulter of any Government dues nor was liable to deposit any dues and that defendants be restrained from recovering that amount as arrears of land revenue from him through coercive measures---Trial Court dismissed the suit and appeal against judgment of Trial Court was also dismissed---No evidence had been led by defendants to establish that before raising demand against plaintiff, either any notice was given to him or he was ever afforded opportunity of hearing; or that amount in dispute was determined after adopting procedural requirements of West Pakistan Land Revenue Act, 1967---In absence of any such evidence, it could not be said that any legal amount was due and recoverable from petitioner as arrears of land revenue---No question thus arose, in circumstances for deposit of demanded amount before filing of suit in terms of S.91 of West Pakistan Land Revenue Act, 1967---Finding of both the two Courts below, were not maintainable---Impugned judgments and decrees of two Courts below were set aside and suit was decreed as prayed for.
 
PLD 1978 Lah. 859 ref.
 
Ch. Akbar Ali Shad for Petitioner.
 
Sarfraz Ali Khan, Asstt. A.-G. for Respondents.
 
Date of hearing: 15th September, 2005.
 
 
JUDGMENT
 
Case 47
 
2006 C L C 435
 
[Lahore]
 
Before Muhammad Khalid Alvi, J
 
FAQEER MUHAMMAD----Petitioner
 
Versus
 
MUHAMMAD HUSSAIN and another----Respondents
 
Civil Revision No.723 of 2001, decided on 13th September, 2005.
 
Punjab Pre-emption Act (I of 1913)---
 
----Ss. 4 & 15---Suit for pre-emption---Superior right of pre-emption--Property purchased by defendant was sought to be pre-empted by plaintiff through suit for pre-emption---Plaintiff had based his claim on two fold superior pre-emptive rights; firstly he was co-sharer in disputed Khata and secondly he was owner in the estate--Suit was decreed by Trial Court, but was dismissed on appeal---Validity---Plaintiff had successfully established on record through registered sale-deed, consequent mutation and jamanbandi that he was owner in disputed Khata before the sale---Incidentally before first pre-emption decree in favour of plaintiff, consolidation had taken place and land falling in disputed Khata had changed its physical place and had acquired different Khasra numbers---In order to maintain his superior right as a co-sharer at the final stage of decree, plaintiff was required to have established on record that he was having some share in new Khasra Nos. of property in dispute---Since there was no such evidence in that regard, plaintiff could not be held to be a co-sharer in new disputed Khatas/Khasras---Plaintiff, however, as a result of consolidation, remained an owner in estate, which status of plaintiff could not be denied---Objection raised by defendants that land owned by plaintiff after consolidation being not land revenue paying land, plaintiff on basis of such ownership was not entitled to superior pre-emptive right, was without any substance; as merely on ground that some land was not assessed to land revenue, its agricultural status would not diminish---Plaintiff, in circumstances was an owner in estate and could claim superior right of pre-emption on that basis---Defendants had themselves conceded that Shajra Nasabs tendered by them in evidence, did not connect them with vendors---Defendants, in circumstances could not be held collaterals of vendors, but Appellate Court below did not properly examine and evaluate evidence in that respect---Objection that plaintiff had not claimed his superior right on basis of being owner in estate and had abandoned same before Appellate Court below and before High Court, was without substance--Pre-emption right was even mentioned in the narration of facts of revision petition before High Court and was vehemently argued by plaintiff before High Court---Judgment and decree passed by Appellate Court were set aside and that of the Trial Court, was restored.
 
2004 SCMR 1693;- 2001 MLD 436; 1999 MLD 1723; 1991 MLD 2008; 1991 MLD 2015; 2004 CLC 555; 1990 CLC 1819 and 1991 CLC 127; Hasil and another v. Karim Hussain Shah and others 1995 SCMR 1385 and 2003 CLC 1073 ref.
 
Muhammad Yaqoob Chaudhry for Petitioner.
 
Shoukat Hussain Khan for Respondents.
 
Date of hearing: 9th September, 2005.
 
 
JUDGMENT
 
Case 48
2006 C L C 451
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
MUHAMMAD IDREES----Petitioner
 
Versus
 
MEMBER (COLONIES), BOARD OF REVENUE, PUNJAB, LAHORE----Respondent
 
Writ Petition No.6413 of 1999, heard on 1st December, 2005.
 
Punjab Local Government Act (XXXIV of 1975)---
 
----S. 8(iv)(proviso)---Colonization of Government Lands (Punjab) Act (V of 1912), S.10---Constitution of Pakistan (1973), Art.199---Constitutional petition---Conferment of proprietary rights in respect of lamberdari grants---Petitioner, who was a permanent lamberdar of Chak concerned, was allotted 100 Kanals of land as a lamberdari grant---Provincial Government vide notification having issued instructions for the disposal of grants, petitioner filed application for conferment of proprietary rights of said land, but his application was rejected after a decade by Authority-Notification provided that land was not to be sold to a lamberdar, if the same fell within prohibited zone and in case of second class municipality said prohibited zone was within a radius of three miles---Land, in question admittedly was located beyond three miles limit of municipality which was a second class municipality---Difference between a town and municipality subsequently was also done away with as prohibitory zone with reference to Town Committee was two miles---Petitioner, in circumstances could not be deprived of his admitted entitlement to obtain proprietary rights in land when he had also fulfilled other conditions of the notification, especially when proprietary rights in same square had been conferred upon other lamberdars--Allowing constitutional petition, impugned order was set aside declaring same to be without lawful authority.
Ch. Abdul Ghani for Petitioner.
 
Zafar Ullah Khan Khakwani, A.A.-G. for Respondent.
 
Date of hearing: 1st December, 2005.
 
 
JUDGMENT
 
Case 49
 
2006 C L C 463
 
[Lahore]
 
Before Muhammad Saeed Akhtar and Sardar Muhammad Aslam, JJ
 
MUHAMMAD SALMAN GHANI----Petitioner
 
Versus
 
GOVERNMENT OF PUNJAB through Secretary to Government of Punjab, Health Department, Lahore and 3 others----Respondents
 
Writ Petitions Nos.4117, 4256 and 4448 of 2005, heard on 27th June, 2005.
 
University of Health Sciences, Lahore Ordinance (LVIII of 2002)---
 
--S. 35---Constitution of Pakistan (1973), Art.199---Constitutional petition---Educational institution---Failure to clear M.B.,B.S. professional examination in four chances---Seeking education, a fundamental right-Scope-Candidates failed to clear their M.B.,B.S. professional examination in four chances-Plea raised by the candidates was that restriction to clear M.B.,B.S. professional examination in four chances, imposed by regulations framed under S.35 University of Health Sciences Lahore Ordinance, 2002, was ultra vires the Constitution---Validity---Candidate's fundamental right to seek education was subjected by statutes framed by the State to regulate the studies---Universities and institutions were meant to impart education to students who really were desirous to seek the same---Hard work and devotion in medical education, was not being exhibited by the students---Prior to promulgation of the rules, the candidates were governed by statute and regulations of Punjab University, which put embargo of clearance of examination in four chances availed or un-availed---If a student failed to clear examination in the prescribed chances, he would cease to become eligible for further medical education---Student who failed to clear the examination in prescribed four chances was not entitled to claim any further allowance---Petition was dismissed in circumstances.
 
Ahmad Abdullah and 62 others v. Government of the Punjab and 3 others PLD 2003 Lah. 752; Shafiq Ahmad and other v. Government of the Punjab and others PLD 2004 SC 168; Akhtar Ali Javaid v. Principal, Quaid-e-Azam Medical College, Bahawalpur 1994 SCMR 532; Maroof Khan v. Principal, Ayub Medical College, Abbottabad and 4 others 1996 SCMR 1101 and Munaza Habib and others v. Vice-Chancellor and others 1996 SCMR 1790 rel.
 
Muhammad Zafar Chaudhry for Petitioner.
 
Rasal Hassan Syed, Legal Adviser U.H.S., Lahore.
 
Misbah-ul-Hassan, A.A.-G. with Ijaz Farrukh, S.L.O., Health Department for Respondents.
 
Date of hearing: 27th June, 2005.
 
 
JUDGMENT
 
Case 50
2006 C L C 479
 
[Lahore]
 
Before Muhammad Khalid Alvi, J
 
WAJID ALI KHAN----Petitioner
 
Versus
 
DISTRICT OFFICER (REVENUE), D.C.O. OFFICE, LAHORE and 3 others----Respondents
 
Writ Petition No.15751 of 2005, heard on 24th January, 2005.
 
Muslim Family Laws Ordinance (VIII of 1961)---
 
----S. 9---West Pakistan Rules under the Muslim Family Laws Ordinance, 1961, R.6-A---Constitution of Pakistan (1973), Art.199---Constitutional petition---Recovery of maintenance allowance--Transfer of proceedings under S.9 of Muslim Family Laws Ordinance, 1961, from one union council to other union council---Grievance of husband was that only that union council was competent to grant maintenance, in which wife was residing and such matter could not be transferred to any other union council---Validity---District Officer Revenue, under R.6-A of Rules under Muslim Family Laws Ordinance, 1961, could only change chairman of arbitration council nominating some other member of the same union council to be Chairman of arbitration council for that particular case---District Officer Revenue had no jurisdiction to transfer application under S.9 of Muslim Family Laws Ordinance, 1961, from one union council to other union council---Decision given by union council other than the one where wife was residing, was without lawful authority having no jurisdiction and the transfer order passed by District Officer Revenue was also nullity in the eye of law---High Court in exercise of constitutional jurisdiction, set aside both the orders and remanded the matter to the union council where wife was residing---Petition was allowed accordingly.
 
Wali Muhammad Khan for Petitioner.
 
Sh. Muhammad Saber for Respondents.
 
Date of hearing: 24th January, 2005.
 
 
JUDGMENT
 
Case 51
 
2006 C L C 489
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
Hafiz Hakim MUHAMMAD FAYAZ----Petitioner
 
Versus
 
AKBAR ALI----Respondent
 
Civil Revisions Nos.1746 to 1749 of 2005, decided on 18th January, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. VII, R.11---Rejection of plaint---Malicious prosecution---Damages---Rejection---Discharge from criminal case---Plaintiff was involved in criminal case but he was discharged from the case on the ground that a civil suit on the same subject was pending between the same parties before civil Court---Plaintiff filed suit for recovery of damages on the plea of malicious prosecution---Trial Court as well as Appellate Court rejected the plaint---Validity---Discharge of plaintiff was only till the pendency of proceedings in his own suit, on the basis of agreement to sell which had also been claimed to be forged/fake---Criminal proceedings against plaintiff neither ended by his acquittal nor those were terminated by any other means---Discharge from the criminal case did not equip the plaintiff with a right to file suit for damages against the complainant and the witnesses---Criminal proceedings against plaintiff had only been suspended till the decision by civil Court which could be reactivated under the final verdict of civil Court---Suit for damages filed by plaintiff did not disclose any cause of action, thus the same was correctly rejected under O. VII, R.11 C.P.C.---Both the Courts below did not commit any illegality/irregularity amenable to revisional jurisdiction of High Court---Revision was dismissed in circumstances.
 
Ashiq Hussain v. Sessions Judge, Lodhran and 3 others PLD 2001 Lah. 271 rel.
 
(b) Acquittal---
 
----Discharge and acquittal-Distinction-Discharge of accused any of kind cannot be equated with acquittal of accused, as there is a marked difference between the two.
 
Abdul Sami Khawaja for Petitioner.
 
Tanvir Ashraf for Respondent.
 
 
ORDER
 
Case 52
2006 C L C 499
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
GHULAM through L.Rs.----Petitioners
 
Versus
 
ATTA MUHAMMAD and others----Respondents
 
Civil Revision No.496-D of 1991, heard on 6th December, 2005.
 
(a) Punjab Pre-emption Act (I of 1913)---
 
----S. 28---Civil Procedure Code (V of 1908), O.XX, R.14---Transfer of Property Act (IV of 1882), S.52---Pre-emption suits by rival pre-emptors qua the same sale---Lis pendence, doctrine of---Applicability---Passing of decree in one suit during pendency of other suit--Validity---Such decree would not have any legal effect and would also be hit by doctrine of lis pendence.
 
Mehr Allah Ditta and another v. Muhammad Ali and another PLD 1972 SC 59 ref.
 
Haji Muhammad Suleman v. Muhammad Akram Khan and others PLD 1956 FC 97 rel.
 
(b) Punjab Pre-emption Act (I of 1913)---
 
----S. 28---Civil Procedure Code (V of 1908), O.I, R.10 & O.XX, R.14---Limitation Act (IX of 1908), Arts.10 & 120---Pre-emption suits by rival pre-emptors qua the same sale--Passing of decree in one suit during pendency of other suit---Impleading of decree-holder/rival pre-emptor as defendant in pending suit---Limitation---Decree-holder by virtue of such decree would be assumed to be claimant under the original vendee---Matter of subsequent vendee would be governed by residuary Art.120 of Limitation Act, 1908 and not Art.10 thereof.
 
Mian Mushtaq Ahmad for Petitioners.
 
Tanvir Ahmad Saleemi for Respondents.
 
Date of hearing: 6th December, 2005.
 
 
JUDGMENT
 
Case 53
 
2006 C L C 506
 
[Lahore]
 
Before Sh. Javaid Sarfraz, J
 
NAILA IQBAL----Petitioner
 
Versus
 
PRINCIPAL, GOVERNMENT COLLEGE FOR WOMEN, MULTAN----Respondent
 
Writ Petition No.6538 of 2005, decided on 23rd January, 2006.
 
(a) Calendar of the Board of Intermediate and Secondary Education, Multan---
 
----Regln. 3---Constitution of Pakistan (1973), Art.l99---Constitutional petition---Prospectus of Government College for Women, Multan---Admission of petitioner to College in F.A. (first year)---Failure of petitioner in one subject in 9th class and one subject in 10th class, but having cleared same in supplementary examination---Refusal of college to admit petitioner on her such failure---Validity---Neither College in its Prospectus nor Board of Intermediate and Secondary Education had imposed such restriction on admission of students---Prospectus provided that admission to college would be according to Policy of Government, wherein no such condition had been laid down---Had such condition been made in Prospectus, then petitioner would have applied in another College---Prospectus issued by college must be followed by every one including college authorities---Valuable right had accrued to petitioner after having fulfilled all requirements for admission as laid down in the prospectus---College could not legally deprive petitioner of her such vested right---High Court accepted constitutional petition declaring impugned action as illegal with direction to Principal to admit petitioner in the college.
 
Yasir Arfat v. Vice-Chancellor, Mehran University and others 2000 CLC 393 and Hamidullah Jan v. Sports Selection Committee and 1984 CLC 149 rel.
 
(b) Educational institution---
 
----Admission to college---Conditions as laid down in Prospectus---Powers of Principal or College Council to change such conditions.
 
The Principal has to exercise his/her powers judicially and not arbitrarily. The Principal or College Council can change the conditions for regulating the admissions to college, but such changes should be made in the Prospectus before they are handed over to a student as before applying for admission, the student should know as to whether he/she is eligible for the admission or not. Arbitrary change in prospectus after its issuance is not desirable.
 
Tariq Mahmood for Petitioner.
 
Zafarullah Khan Khakwani, A.A.-G. with Muhammad Abdullah Sial, Superintendent, Government College for Women, Kutchery Road, Multan.
 
Date of hearing: 23rd December, 2005.
 
 
JUDGMENT
 
Case 54
2006 C L C 514
 
[Lahore]
 
Before Sh. Hakim Ali, J
 
TARIQ HUSSAIN and another----Petitioners
 
Versus
 
ADDITIONAL DISTRICT JUDGE, VEHARI and 2 others----Respondents
 
Writ Petition No.8455 of 1996, heard on 16th November, 2005.
 
(a) Arbitration Act (X of 1940)---
 
----S. 21---Reference of dispute to arbitration by Court at the request of parties---Non-filing of written application by parties---Effect---Written application by parties would not be essential---Such request of parties, if following by their statements before Court, which were signed by them or their pleaders, would tantamount to making a reference in writing to Court---Where parties themselves requested Court to shift its proceedings from law Court to Arbitrator, then their choice must be respected for they having felt satisfaction in such manner and method of adjudication---Technicalities of small nature should not hinder parties' choice of forum for adjudication of their dispute---Mere technical and formal defect of non-filing of application in writing would not be taken as major irregularity or illegality so as to upset appointment of Arbitrators and their decision thereafter.
 
Mahabir v. Manohar Singh AIR 1924 All. 540; Waliullah v. Bhaggan AIR 1925 Oudh 269; Jagmohan v. Suraj Narain AIR 1935 Oudh 499 and Ghisalal Sohanlal v. Ram Pershad Motilal AIR 1953 Ajmer 58 ref.
 
(b) Administration of justice---
 
----Relief not prayed for by any party to proceedings---Order of Court granting such relief would not be legally valid.
 
Ch. Ghulam-ud-Din Aslam for Petitioner.
 
Nemo for Respondent proceeded Ex parte vide order, dated 28-7-2004.
 
Date of hearing: 16th November, 2005.
 
 
JUDGMENT
 
Case 55
 
2006 C L C 527
 
[Lahore]
 
Before Muhammad Akhtar Shabbir, J
 
BARKAT ALI----Petitioner
 
Versus
 
AHMAD DIN and another----Respondents
 
Writ Petitions Nos.18630 and 18631 of 2005, decided on 17th January, 2006.
 
(a) Punjab Tenancy Act (XVI of 1887)---
 
----S. 14---Recovery of share of profits---Co-sharer, right of---Scope---Co-sharer can claim his share of profits from other co-sharer and tiller of land in a joint holding.
 
(b) Punjab Tenancy Act (XVI of 1887)---
 
----S. 77---Constitution of Pakistan (1973), Art.199---Constitutional petition---Maintainability---Factual controversy---Share of profits---Claim by co-sharer---Plaintiff sought recovery of share of profits from defendant being co-sharer---Revenue Court decreed the suit in favour of plaintiff---Judgment and decree passed by Revenue Court was set aside by Appellate Courts but Board of Revenue restored the judgment and decree passed by Revenue Courts and decreed the suit in favour of plaintiff---Plea raised by defendant was that there was no relationship of landlord and tenant between the parties, as he had been paying Hisa Batai to another co-sharer in Khata, which was in his possession, over and above his own share---Validity---Plaintiff purchased two Khasra numbers from two other persons, which Khasra numbers were in their possession, thus the possession of vendors had continued and plaintiff under the law was legally owner of that portion of land under plough of the defendant---Revenue Court on the basis of evidence rightly found that the relationship of landlord and tenant existed between the parties and thus decreed plaintiff's suit which was affirmed by Board of Revenue---Appellate Courts had not based their findings on the basis of documentary evidence---As the matter pertained to the question of facts determined by Revenue Court, as well as by Board of Revenue after evaluating the evidence of parties High Court would be reluctant to interfere with their findings---High Court declined to interfere with the judgment and decree passed by Board of Revenue---Petition was dismissed in limine.
 
Faqir Muhammad v. Bashir Ahmad and 2 others 1990 ALD 1975; Benedict F.D Souza v. Karachi Building Control Authority and 3 others 1989 SCMR 918; Federation of Pakistan and 2 others v. Major (Rtd.) Muhammad Sabir Khan PLD 1991 SC 476 and Muhammad Younas Khan v. Government of N.-W.F.P. through Secretary and others 1993 SCMR 618 rel.
 
(c) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional jurisdiction of High Court---Scope--High Court cannot sit as Court of appeal against judgment/order passed by Special Tribunal.
 
Muhammad Hussain Munir and others v. Sikandar and others PLD 1974 SC 139 and Sub. Muhammad Asghar v. Mst. Safia Begum and another PLD 1976 SC 435 rel.
 
Muhammad Azam Bhaur for Petitioner.
 
 
ORDER
 
Case 56
 
2006 C L C 531
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
GHULAM RASOOL----Petitioner
 
Versus
 
RASHEEDA BIBI and another----Respondents
 
Civil Revision No.929 of 2001, decided on 24th May, 2005.
 
Transfer of Property Act (IV of 1882)---
 
----Ss. 122 & 123---Specific Relief Act (I of 1877), Ss.42 & 54---Execution of gift in respect of land-Suit for declaration and injunction---Respondent, who was daughter of petitioner, through gift mutation got mutated land of petitioner in her favour and through another gift-deed she gifted land in dispute in favour of her son---Petitioner challenged said transactions as being fraudulent, by denying having gifted his land to respondent which she could further gift to her son---Both Trial Court and Appellate Court had concurrently found that mutation of gift had been proved by respondents-Validity-Respondent, who claimed oral gift in her favour, had not brought on record any positive evidence to establish as to when declaration of alleged gift was made by petitioner in her favour and she accepted the same---No witness at all had been examined by respondent in that behalf---Day, date, time, month, year and venue had neither been specified nor proved by respondent through any evidence---When initial onus which was on the petitioner, had been discharged by him through his own statement, adducing of positive evidence was the responsibility of respondents, in which they had failed---Lamberdar, who claimed to have identified petitioner at the time of mutation of gift before Tehsildar, was not Lamberdar of concerned village, but was of another village and it was not explained as to why the concerned Lamberdar had not been produced---No person from Revenue Department, Patwari or Tehsildar etc. had been examined---Possession of alleged gifted land was not shown to have ever changed hands on the basis of alleged gift, as neither there was any independent proof on the record nor change of possession was established on account of any overt act of petitioner---Said vital aspects of case had not at all been considered by the two Courts and their Judgments were absolutely sketchy and reflected non-application of Judicial mind---Judgments and decrees of Courts below which were suffering from infirmity of misreading and non-reading of evidence, were set aside and suit of petitioner as claimed, was allowed.
 
Ch. Arshad Mehmood for Petitioner.
 
Ch. Zubair Ahmad Farooq for Respondents.
 
Date of hearing: 24th May, 2005.
 
 
JUDGMENT
 
Case 57
 
2006 C L C 534
 
[Lahore]
 
Before Ali Nawaz Chowhan, J
 
Mst. ZAREENA BIBI----Petitioner
 
Versus
 
MUHAMMAD SHARIF and 3 others----Respondents
 
Writ Petition No.7139 of 2005, decided on 16th January, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O.XIII, Rr.1 & 2---Constitution of Pakistan (1973), Art.199---Constitutional petition--List of documents appended with pleadings---Object---Non-mentioning of a document in the list---Effect---Defendant relied upon Iqrarnama, which was not mentioned in the list of documents filed by her along with her written statement---Trial Court declined to accept that Iqrarnama as documentary evidence but Appellate Court allowed the same to be taken as documentary evidence on the ground that Iqrarnama was mentioned in written statement---Validity---Rationale behind the provisions of O.XIII, Rr.1 and 2 C.P.C. was that nobody should be taken by surprise and there should be transparency about the procedure---Iqrarnama was an essential document in the litigation and its mention was made in the written statement filed by the defendant---For not placing it in the list to be appended under the provisions of O.XIII, Rr.1 and 2, C.P.C., the defendant had already been penalized with costs---Delay in the case was enough penalty---High Court declined to interfere in the order passed by Appellate Court---Petition was dismissed in circumstances.
 
Sheikh Muhammad Hussain and another v. Fazal Iqbal and others PLD 1963 Lah. 501 and Anwar Ahmad v. Mst. Nafis Bano through Legal Heirs 2005 SCMR 152 rel.
 
1999 MLD 2160 distinguished.
 
Sarfraz Hussain for Petitioner.
 
Ch. Imtiaz Ahmad Kamboh for Respondent No.1.
 
Muhammad Younas Chaudhry for Respondent No.2.
 
 
ORDER
 
Case 58
 
2006 C L C 537
 
[Lahore]
 
Before Tanvir Bashir Ansari, J
 
ALI AHMAD----Petitioner
 
Versus
 
Rana MUHAMMAD AKRAM and others----Respondents
 
Civil Revision No.1561-D of 1999, decided on 17th March, 2005.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 115 & O.XLI, R.22---Revision petition challenging findings of Trial Court upon issues not challenged before Appellate Court in appeal or by way of cross-objections---Validity---Findings of Trial Court upon such issues would become conclusive qua petitioner and could not be challenged in revisional jurisdiction---Principles.
 
(b) Punjab Pre-emption Act (IX of 1991)---
 
---S. 5---Sale or exchange---Determination of the nature of transaction---Conversion of sale transaction into exchange deed---Admission of vendee as witness regarding such conversion---Attesting witness of agreement to sell also supported pre-emptor's plea that exchange deed had been executed merely to avoid right of pre-emption--Actual transaction, held, was that of sale.
 
Muhammad Afzal Khan and another v. Muhammad Latif and another 1995 CLC 1951; Muhammad Aslam and 2 others v. Syed Muhammad Azim Shah and 3 others 1996 SCMR 1862; Government of N.-W.F.P. through Chief Secretary and another v. Muhammad Zaman and others 1996 SCMR 1864; Muhammad Hussain and others v. Muhammad Gulzar PLD 2001 Lah. 390; Ilamuddin through Legal Heirs v. Syed Sarfraz Hussain through Legal Heirs and 5 others 1999 CLC 312; Muhammad Hassan v. Dharamdas and others 2000 YLR 637; Muhammad Munir and others v. Hafiz Muhammad Rafique and others 2004 SCMR 1551 and Muhammad Siddique and another v. Sajawal Khan and another 2001 SCMR 302 ref.
 
(c) Punjab Pre-emption Act (IX of 1991)---
 
----S. 27---Qanun-e-Shahadat (10 of 1984), Arts.102 & 103---Determination of price---Price of land finding mention in registered agreement to sell---Effect. Marginal witness though supporting transaction of sale and execution of agreement, but his statement as against sale price mentioned in agreement to sell would not be accepted.
 
Rana Nasrullah Khan for Petitioner.
 
Shaukat Hussain Khan Baluch for Respondents.
 
Date of hearing: 17th March, 2005.
 
 
JUDGMENT
 
Case 59
 
2006 C L C 543
 
[Lahore]
 
Before Muhammad Akhtar Shabbir, J
 
ABDUR RAHMAN BHATTI and another----Petitioners
 
Versus
 
MEMBER (COLONIES), BOARD OF REVENUE, PUNJAB, LAHORE and another----Respondents
 
Writ Petition No.13538 of 1998, heard on 18th January, 2006.
 
(a) Colonization of Government Lands (Punjab) Act (VI of 1912)--
 
----S. 17---Term 'tenant'-Connotation-Any person remains tenant under government till he pays full amount of purchase to the Government---After payment of full price of land such person becomes absolute owner of the same and property comes out of the ambit of Colony/Revenue hierarchy.
 
Ilam Din v. Muhammad Din PLD 1964 SC 842; Ali Muhammad v. Mst. Rabia Bibi and 3 others PLD 1971 (B.J.) 38 and Azmat Ali v. Member, Board of Revenue and others PLD 1978 Lah. 1148 ref.
 
(b) Colonization of Government Lands (Punjab) Act (VI of 1912)---
 
----S. 17---Colony Manual, Para. No. 364 of Colony instructions---Constitution of Pakistan (1973), Art.199---Constitutional petition---Exchange of colony land from one colony to other---Petitioners intended to exchange their proprietary land in one district with State land situated in other district but the authorities did not allow the exchange---Contention of the petitioners was that they had been discriminated, as the authorities allowed such exchange to influential persons---Validity---Petitioners were proprietors of land and not tenants, thus S.17 of Colonization of Government Lands (Punjab) Act, 1912, was not attracted to their case, as they had ceased to be tenant of land---Collector was empowered to allow exchange in the same colony only but the petitioners had applied for exchange of their land from one colony to another colony and only Government enjoyed such power---Request of petitioners was declined by Board of Revenue having the authority of Government---Land purchased at auction or otherwise could not be exchanged under paragraph No. 364 of Colonies Instructions provided in Colony Manual, without express order of Government, which should only be sought in exceptional cases--No application for exchange could be entertained once proprietary rights were acquired in a grant---High Court declined to interfere in the order passed by the authorities---Petition was dismissed in circumstances.
 
(c) Constitution of Pakistan (1973)---
 
----Art. 199---Constitutional jurisdiction of High Court---Discretion/jurisdiction of Government--- Interference--- Scope--- Discretion/jurisdiction of Government cannot be interfered with by High Court in exercise of constitutional jurisdiction.
 
M. Naeem Sadiq for Petitioners.
 
M. Akbar Tarar, Addl. A.-G. for Respondents.
 
Date of hearing: 18th January, 2006.
 
 
JUDGMENT
 
Case 60
 
2006 C L C 546
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
GHULAM NABI through L.Rs. and others----Appellants
 
Versus
 
TAHIR ABBAS and others----Respondents
 
Regular Second Appeal No.34 of 1996, decided on 18th May, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----Ss. 12 & 22---Suit for specific performance of agreement of sale---Defendants/vendors having failed to complete sale according to terms of agreement, plaintiffs/vendees had brought suit for specific performance of agreement---Subsequent vendees of suit property contested the suit and had denied execution of sale agreement made by vendor ladies in favour of plaintiffs---Said subsequent vendees also took-up defence that transfer in their favour by vendor ladies/defendants was genuine and that they were bona fide purchasers---Both Trial Court and Appellate Court decreed suit of plaintiffs holding that alleged subsequent sale-deeds in favour of appellants/subsequent purchasers, were result of collusion and that they were not bona fide purchasers---One of defendants ladies had filed conceding written statement and admitted claim of plaintiffs and second defendant lady was proceeded ex parte and ex parte evidence led by plaintiffs to prove agreement to sell in their favour by defendants, was concurrently found by two Courts below to be adequate and on appraisal had believed the same---Both Courts below had concurrently recorded findings of fact that appellants/subsequent vendees, were not bona fide purchasers---Appellants, who had collusively and knowingly purchased property subsequent to agreement to sell in favour of plaintiffs, could not set out S.22 of Specific Relief Act, 1877 as defence---Appeal filed by appellants/subsequent purchasers, was dismissed, in circumstances.
 
Dulhin Rajkishore Kuer v. Muhammad Qayyum and others AIR 1942 Pat. (29) 366; Saheb Dayal Singh v. Muhabir Singh and others AIR 1930 All. 166; Hahibar Rahaman v. Ali Azhar and others AIR 1926 Cal. 1237; Genda Ram and another v. Ram Chand and another AIR 1924 Lah. 163 and Mst. Hawa v. Muhammad Yousuf and others PLD 1969 Kar. 324 ref.
 
(b) Pleadings---
 
----No one should be allowed to plead the case beyond the scope of his pleadings and if any evidence had been led which was outside the purview of pleadings of a party, same should be ignored by the Court.
 
Qamar Riaz Hussain Basra for Appellants/Defendants Nos.3 and 4.
 
Malik Abdul Wahid for Respondents/plaintiffs.
 
Date of hearing: 18th May, 2005.
 
 
JUDGMENT
 
Case 61
 
2006 C L C 549
 
[Lahore]
 
Before Syed Hamid Ali Shah, J
 
MUHAMMAD ANWAR----Petitioner
 
Versus
 
BASHIR AHMAD and another----Respondents
 
Civil Revision No.482 of 2004, decided on 27th December, 2005.
 
(a) Punjab Pre-emption Act (IX of 1991)---
 
----S. 13---Right of pre.-emption---Scope---Such right extinguishes if demand of pre-emption under the provisions of Punjab Pre-emption Act, 1991, is not made.
 
(b) Punjab Pre-emption Act (IX of 1991)---
 
----S. 13---Right of pre-emption, exercise of---Notice of Talb-i-Ishhad--Format---Non-mentioning of Talb-i-Muwathibat in notice for Talb-i-Ishhad---Effect---Pre-emptor made Talb-i-Muwathibat, issued notice signed by two witnesses through registered A.D and postal receipt was produced in evidence---Trial Court decreed the suit in favour of pre-emptor but Appellate Court allowed the appeal and dismissed the suit for the reason that in the said notice there was no mention of Talb-i-
Muwathibat---Validity---Notice issued by pre-emptor was sufficient as per requirement of S.13 of Punjab Pre-emption Act, 1991, as no format was prescribed for issuing of such notice---Appellate Court non-suited the pre-emptor only on the ground of non-mention of Talb-i-Muwathibat while performing Talb-i-Ishhad---Finding of Appellate Court was erroneous both on law and facts---Pre-emptor had proved the performance of Talb-i-Ishhad and Talb-i-Muwathibat which by all means met the requirements of provisions of S.13 of Punjab Pre-emption Act, 1991---Judgment and decree passed by Appellate Court was set aside and that of Trial Court was upheld---Revision was allowed in circumstances.
 
Haji Qadir Gul v. Moebar Khan and others 1998 SCMR 2102 distinguished.
 
Muhammad Ramzan v. Lal Khan 1995 SCMR 1510; Muhammad Hassan and 2 others v. Shafi-ud-Din and 2 others PLD 1995 Quetta 29; Anwar Ali v. Shahnawaz and others PLD 1989 Kar. 246 and Muhammad Nasir Mehmood and others v. Rashida Bibi 2000 SCMR 1013 ref.
 
Muhammad Gul v. Muhammad Afzal 1999 SCMR 724; Abdul Haq and others v. Shaukat Ali and 2 others 2003 SCMR 74; Dr. Muhammad Ayub Khan v. Haji Noor Muhammad 2002 SCMR 219; 1995 SCMR 1510; 1998 SCMR 227 and 1999 SCMR 2167 rel.
 
Ijaz Ahmad Chadhar for Petitioner.
 
Ch. Hassan Ali Khan for Respondent No.1.
 
Ghulam Siddique Awan for Respondent No.2.
 
Date of hearing: 13th October, 2005.
 
 
ORDER
 
Case 62
2006 C L C 554
 
[Lahore]
 
Before Sh. Azmat Saeed, J
 
HAIBAT NAWAZ KHAN----Petitioner
 
Versus
 
Mst. NAJMA BIBI alias NAJMA PARVEEN and others----Respondents
 
Writ Petition No.9254 of 2005, decided on 4th July, 2005.
 
West Pakistan Family Courts Act (XXXV of 1964)---
 
----Ss. 5, Sched & 9--Constitution of Pakistan (1973), Art.199---Constitutional petition---Suit for recovery of maintenance amount---Documentary evidence, production of--Evidence was led by respondents, whereafter petitioner produced his oral evidence and case was adjourned for production of documentary evidence---Petitioner, on the adjourned date of hearing, attempted to produce certified copy of a certificate allegedly issued by Chairman, Union Council concerned and attempted to prove that he had divorced the respondent---Family Court, on the objection of respondent, vide impugned order declined permission to petitioner to produce said document--Petitioner had contended that the document sought to be produced was certified copy of a public document and Family Court was vested with jurisdiction and discretion to permit him to produce said document---Specific issue was framed by Family Court as to whether petitioner had divorced the respondent---Evidence of petitioner had not been closed and case was fixed for production of documentary evidence---Document sought to be produced by petitioner being relevant, impugned order of Family Court, was set aside in the interest of justice and petitioner was permitted to present said document in the Court subject to payment of costs---Family Court, however, would examine admissibility and legal effect of said document.
Mst. Faiza Firdous v. Ghulam Sabir 2002 CLC 1801 ref.
 
Hasnat Ahmad Khan for Petitioner.
 
Respondent No.1 in person.
 
Malik Zafar Iqbal Awan, Addl. A.-G. for Respondents.
 
Date of hearing: 4th July, 2005.
 
 
ORDER
 
Case 63
 
2006 C L C 556
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
MUHAMMAD SHAFI----Petitioner
 
Versus
 
MUHAMMAD AYUB and another----Respondents
 
Civil Revision No.410-D of 2000, heard on 12th December, 2005.
 
Punjab Pre-emption Act (I of 1913)---
 
----S. 15---Right of pre-emption, exercise of---Inclusion, of land in municipal limits---Only controversial point between the parties was that suit-land had been included in municipal limits and was not subject to pre-emption laws---Pre-emptor filed the suit on the basis of his being nearest collateral of vendor, co-sharer of Khata and owner in the estate---Trial Court decreed the suit in favour of pre-emptor but Appellate Court dismissed the suit on the ground that the suit-land had become urban property and was included in municipal limits---Plea raised by pre-emptor was that the suit-land was included in municipal limits after passing of decree by Trial Court in his favour---Validity---Properties though not included in municipal limits and lying in suburbs of big cities, where all facilities of urban life were available, were not subject to process of pre-emption under S.15 of Punjab Pre-emption Act, 1913---Suit-land stood included in municipal limits, which proved that suit-land was just near to the city and was purchased by vendees for residential purposes who were not owners in the estate---Suit-land measuring 2 Kanals by its area, could not be treated as agricultural, especially when the same was sold to non-proprietors of the estate---Such small piece of land could not have been brought under plough by a stranger to the village---Suit-land was located within constructed/ populated area where all facilities of life, i.e. roads, streets, electricity, shops, hotels, clinics, Sui gas, telephone and schools etc. were available and it had attained the colour of urban immovable property at the time of its sale and thus was not pre-emptible under S.15 of Punjab Pre-emption Act, 1913, even if included in municipal limits after the decree was passed in favour of pre-emptor---Judgment and decree passed by Appellate Court being just/lawful, required no interference by High Court in exercise of its revisional jurisdiction---Revision was dismissed in circumstances.
 
Mst. Bibi Jan and others v. Miss R.A. Monny and another PLD 1961 SC 69; Abdul Haq and 4 others v. Sardar Shah and others 1994 SCMR 1238; Government of N.-W.F.P. through Secretary Law Department v. Malik Said Kamal Shah 1986 PSC 1241; PLD 1978 SC 190; Salamat Rai v. Khushi Ram 45 I.C. 887; Shankar Das v. Mathra Das and another 55 I.C. 520; Diwan Chand v. Nizam Din and another AIR 1924 Lah. 662; Sheikh Abdul Rehman v. Khan Sahib Haji Rashid Ahmad AIR 1937 Lah. 182; Lal and others v. Muhammad Sharif PLD 1961 (W.P.) Lahore 47 and Nazir Abbas v. Manzoor Haider Shah PLD 1989 SC 568 ref.
 
Sardar Muhammad Ramzan for Petitioner.
 
Ch. Muhammad Baleegh-uz-Zaman for Respondents.
 
Date of hearing: 12th December, 2005.
 
 
JUDGMENT
 
Case 64
 
2006 C L C 563
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
MUHAMMAD ASHIQ----Appellant
 
Versus
 
MUHAMMAD NAZEER and 4 others----Respondents
 
Regular Second Appeal No.36 of 2000, decided on 24th May, 2005.
 
Punjab Pre-emption Act (IX of 1991)---
 
----Ss. 6, 13 & 35(2)---Suit for pre-emption---Making of Talbs---One of the witnesses produced by plaintiff in his statement had mentioned that other people were also present at the time when Talb-i-Ishhad was made by plaintiff, but said witness had not given the names of persons allegedly present there---Witness had also not mentioned about presence of second witness of plaintiff---No time, date and day after Talb-i-Ishhad had been given---Witness produced by plaintiff had stated that Talb-i-Ishhad was made one month and four days after sale, whereas his statement was busted by the statement of pre-emptor himself when he in cross-examination stated that he learnt about sale after 4/5 days thereof and made Talb-i-Ishhad, the same day---Said two statements were so contradictory that those could not sustain and co-exist---Second witness. of pre-emptor was totally ignorant about Talb-i-Ishhad --Appellate Court, in circumstances had rightly accepted appeal of defendants---Decree of Appellate Court not suffering from any vice or infirmity of misreading and non-reading of evidence and not being contrary to any law, could not be interfered with in second appeal.
 
Haji Rana Muhammad Shabbir Ahmad Khan v. Government of Punjab, Province, Lahore PLD 1994 SC 1 ref.
 
Malik Zafar Iqbal Awan for Appellant.
 
C.M. Sarwar for Respondents.
 
Date of hearing: 24th May, 2005.
 
 
JUDGMENT
 
Case 65
 
2006 C L C 566
 
[Lahore]
 
Before Muhammad Akhtar Shabbir, J
 
MUHAMMAD ALI----Petitioner
 
Versus
 
ADDITIONAL DISTRICT JUDGE, JARANWALA and 2 others----Respondents
 
Writ Petition No.16917 of 2003, heard on 19th January, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O.VIII, R.1---Term `ordinarily'---Object---Administration of justice---Period for filing of written statement---Power of Court---Such period should not ordinarily exceed 30 days---Legislature has specifically incorporated the word `ordinarily' to convey that the period of 30 days cannot be adhered to in all circumstances---Use of term `ordinarily' gives a discretion to Court to extend such period in suitable cases---Procedural laws are designed to promote the ends of justice and provision of O.VIII, R.1 C.P.C. is procedural in nature---Courts of law never take a fetish of technicalities, so as to lose intention or philosophy of administration of justice to decide lis in accordance with respective rights of parties---Non providing of more than two adjournments, under second proviso of O.VIII, R.1 C.P.C. indicates that it also is directory because direction has been followed by including the period of 30 days in the provision and it is prohibitory command conveyed by the second proviso of O.VII, R.1, C.P.C., which is primarily directed to further the cause of first proviso---If the first proviso of O.VIII, R.1, C.P.C. is a directory, then the second proviso should also be treated as such---By using word `ordinarily' in the proviso, period of 30 days cannot be adhered to in all circumstances---Use of term `ordinarily' gives discretion to Court to extend the period in suitable cases.
 
Hassan Usmani, Sole Proprietor and another v. T.F. Pipes Limited through Managing Director 2003 YLR 1075 rel.
 
(b) Interpretation of statutes---
 
---Words used in a statute---Scope---No word in a statute is redundant and has to be given the specific meaning, which it intends to convey.
 
(c) Words and phrases---
 
----"Ordinarily"---Applicability---Where doing of an act is bound by time but is qualified by term `ordinarily', it necessarily implies that such provision of law is intended to be directory and not mandatory.
 
(d) Interpretation of statutes---
 
---Different provisions of a statute---Scope---Different provisions of a statute should be construed harmoniously, so as to advance the purpose of a substantive provision of law---No provision should be pressed into service in order to defeat the real object of the main provision.
 
(e) Civil Procedure Code (V of 1908)---
 
----O. VIII, Rr.1 & 10---Constitution of Pakistan (1973), Art.199---Constitutional petition---Written statement, non-filing of---Striking off defence---Case was adjourned on two dates for filing of written statement but on failure of defendant to file written statement, Trial Court struck off his defence---Order passed by Trial Court was maintained by Appellate Court in exercise of revisional jurisdiction---Validity---Defence could only be struck off under O.VIII, R.10 C.P.C., where any party from whom written statement was so required, failed to present the same within the time fixed by the Court---Court might pronounce judgment or could take action as it thought fit and speaking order should have been passed by it---Last opportunity was granted in the first proviso of O.VIII, R.1, C.P.C. only keeping in view the time limit of 30 days and such provision was not applicable in the present case---Both the Courts below had passed the order in violation of settled law by Superior Courts---High Court, in such-like circumstances, in exercise of its constitutional jurisdiction, would have ample power to interfere with the orders passed by the revisional Court---Orders passed by Trial Court as well as by Appellate Court were passed illegally and were set aside---Petition was allowed in circumstances.
 
Mian Asif Islam v. Mian Muhammad Asif and others PLD 2001 SC 499; Niaz Muhammad Khan v. Mian Fazal Raqib PLD 1974 SC 134; Maulana Nur-ul-Haq v. Ibrahim Khalil 2000 SCMR 1305 and Muhammad Anwar Khan and 56 others v. Ch. Riaz Ahmad and 5 others PLD 2002 SC 491 ref.
 
S. Abid Imam Tirmizi for Petitioner.
 
Riaz Ahmad Kartaria for Respondent No.3.
 
Date of hearing: 19th January, 2006.
 
 
JUDGMENT
 
Case 66
2006 C L C 571
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
SHAMS-UD-DIN through L.Rs.----Petitioners
 
Versus
 
ABID HUSSAIN through L.Rs.----Respondents
 
Civil Revision No.1481 of 2000, heard on 13th December, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 12---Qanun-e-Shahadat (10 of 1984), Arts.17(2)(a), 78 & 79---Stamp Act (II of 1899), Ss.35, 40 & Sched. I, cl. 5---Suit for specific performance of agreement to sell---Agreement written on a simple/ordinary paper not carrying thumb-impression of defendant or number of his N.I.C.---Denial of execution of agreement by defendant--Examination of one marginal witness and scribe of agreement in Court---Validity---Plaintiff was under legal obligation not only to prove agreement itself, but also to establish through evidence that he really entered into a bargain of sale with defendant and sale transaction was in fact struck as per terms reflected therein---Plaintiff had not examined both attesting witnesses, thus, requirement of Arts.17 & 79 of Qanun-e-Shahadat, 1984 had not been fulfilled---Scribe having not attested agreement as a witness could not substitute other attesting witness thereof---Disputed agreement had been written by an unlicensed person not trained in the trade just to avoid its entry in register of Petition Writer, who under the Rules was obliged to enter same in his register and get signature of its executant thereon---Law required agreement to sell to be written on non-judicial stamp paper---Disputed agreement would carry no legal value, unless impounded by Collector under S.40 of Stamp Act, 1899---Signatures of defendant on written statement and those inscribed on disputed agreement did not tally with each other---Due execution of disputed agreement had not been proved in accordance with law---Suit was dismissed in circumstances.
Abdul Wali Khan through Legal Heirs and others v. Muhammad Saleh 1998 SCMR 760 ref.
 
Janat Bibi v. Sikandar Ali and others PLD 1990 SC 642; Hakim Khan v. Nazeer Ahmad Lughmani and 10 others 1992 SCMR 1832; Sana Ullah and another v. Muhammad Manzoor and another PLD 1996 SC 256; Muhammad v. Mst. Rehman through Mst. Sharifan Bibi 1998 SCMR 1354; Mst. Rasheeda Begum and 3 others v. Muhammad Yousaf and others 2002 SCMR 1089; Nazir Ahmed v. Muhammad Rafiq 1993 CLC 257; Mst. Rasheeda Begum and others v. Muhammad Yousaf and others 2002 SCMR 1089 and Messrs Wiqas Enterprises and others v. Allied Bank of Pakistan and 2 others 1999 SCMR 85 rel.
 
(b) Transfer of Property Act (IV of 1882)---
 
----S. 54---Qanun-e-Shahadat (10 of 1984), Arts.17(2)(a) & 79---Agreement to sell---Treating scribe as attesting witness of agreement---Essentials---No note given on agreement by scribe that he attested same as a witness as transaction was concluded, payment was made and parties put their hands thereon in his presence---Scribe, in circumstances, could not be given status of attesting witness.
 
Nazir Ahmed v. Muhammad Rafiq 1993 CLC 257 and Abdul Wali Khan through Legal Heirs and others v. Muhammad Saleh 1998 SCMR 760 ref.
 
(c) Stamp Act (II of 1899)---
 
----Ss. 35, 40 & Sched. I, cl.5---Agreement to sell written on simple/plain paper---Validity---Law required agreement to be written on non-judicial stamp 'paper---Such agreement would carry no legal value, unless impounded by concerned Collector under S.40 of Stamp Act.
 
Sh. Anwar-ul-Haq for Petitioner.
 
Kh. Saeed-uz-Zafar for Respondent.
 
Date of hearing: 13th December, 2005.
 
 
JUDGMENT
 
Case 67
 
2006 C L C 586
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
MUHAMMAD BIBI----Petitioner
 
Versus
 
PROVINCE OF PUNJAB through Collector, Gujranwala and others----Respondents
 
Civil Revision No.471-D of 2000, decided on 27th January, 2006.
 
(a) Displaced Persons (Compensation and Rehabilitation) Act (XXVIII of 1958)---
 
----S. 10---Allotment of land in favour of refugee from Azad Jammu and Kashmir as maintenance allowance for his and other family members---Effect---Land once allotted for such purpose would go out of compensation pool and vest' exclusively in the Ministry for Azad Jammu and Kashmir---Any allotment made by Settlement Authorities treating such land to be an evacuee property would be without jurisdiction, void and of no legal effect.
 
(b) Specific Relief Act (I of 1877)---
 
----S. 42---Displaced Persons (Compensation and Rehabilitation) Act (XXVIII of 1958), S.10---Suit for declaration---Allotment of land in favour of refugee from Azad Jammu and Kashmir as maintenance allowance for his and other family members---Subsequent transfer of such land by Settlement Authority in favour of defendant against his claim---Suit by wife of refugee challenging subsequent transfer in favour of defendant---Maintainability---Wife of refugee was not co-allottee---Such rights of refugee were not heritable---Refugee, despite being aware of subsequent allotment, had not challenged same during his life time---Wife of refugee had no locus standi and cause of action to challenge subsequent allotment in favour of defendant.
 
Ghulam Muhammad and another v. Ahmad Khan and another PLD 1991 SC 391; Jan Muhammad and others v. Sher Muhammad and another PLD 1979 SC 985; Mst. Sakina Bibi and another v. Mamla and 2 others PLD 1977 Lah. 202; Allah Rakhi v. Sughra Bibi and others 1986 CLC 2095 and Muhammad Bakhsh v. Ellahi Bukhsh and others 2003 SCMR 286 ref.
 
Allah Rakhi v. Sughra Bibi and others 1986 CLC 2095 and Abdul Haq and another v. Mst. Surrya Begum and others 2002 SCMR 1330 rel.
 
(c) Void order---
 
----Challenge to---Limitation---Duty of affected party was to bring an action within prescribed period of limitation after attaining knowledge of a void order---Affected party, despite attaining knowledge ' of a void order, if had not challenged same within prescribed period of limitation, then he could not take refuge under the principle that void order would not carry any sanction of limitation---Principles.
 
Muhammad Raz Khan v. Government of N.-W.F.P. and another PLD 1997 SC 397; Sayed Sajid Ali v. Sayed Wajid Ali PLD 1975 BJ 29; Muhammad Ismail v. Abdul Rashid and 2 others 1983 SCMR 168 and Riasat Ali and 2 others v. Mahmood Ahmad 1993 CLC 120 rel.
 
(d) Displaced Persons (Compensation and Rehabilitation) Act (XXVIII of 1958)---
 
----S. 10---Civil Procedure Code (V of 1908), S.9---Allotment of land in favour of refugee from Azad Jammu and Kashmir as maintenance allowance---Subsequent transfer of such land by Settlement Authority in favour of defendant against his claim---Suit before Civil Court to challenge subsequent transfer---Validity---Refugee had the right to challenge impugned transfer in settlement hierarchy---Impugned transfer being void in nature could always be assailed before Civil Court---Under rehabilitation and settlement laws, neither any protection had been provided to a void order or jurisdiction of Civil Courts was ousted---Civil court possessed jurisdiction to adjudicate such matter.
 
Mian Ghulam Rasool for Petitioner.
 
Rana Amir Ahmad Khan, A.A.-G. for Respondent No.1.
 
Sher Zaman Khan for Respondent No.2.
 
Sh. Umer Draz for Respondents Nos.3 to 5.
 
Date of hearing: 27th January, 2006.
 
JUDGMENT
 
Case 68
 
2006 C L C 596
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
MUHAMMAD SHARIF----Petitioner
 
Versus
 
TEHSIL COUNCIL KAHROR PAKKA, DISTRICT LODHRAN through Nazim and another----Respondents
 
W.P. No.6049 of 2004, heard on 3rd March, 2005.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----Ss. 57 & 67---Constitution of Pakistan (1973), Art. 1 99---Constitutional petition---Declaring petitioner as police tout---Powers and functions of Tehsil Council and Tehsil Nazim---Nazim of Tehsil Council concerned through a resolution declared petitioner a police tout and recommended that his entry in City Police Station be banned---Validity---No power had been vested in Tehsil Council or Tehsil Nazim to declare a citizen to be a police tout---High Court allowing constitutional petition by petitioner, set aside impugned resolution being without lawful authority and void.
 
Ms. Moona Safdar for Petitioner.
 
Malik Qasim Khan Joya for Respondent No. 1.
 
Date of hearing: 3rd March, 2005.
 
JUDGMENT
 
Case 69
2006 C L C 608
 
[Lahore]
 
Before Ch. Ijaz Ahmad, J
 
MUHAMMAD MANSHA and others----Petitioners
 
Versus
 
SHARIFAN BIBI and others----Respondents
 
Writ Petition No.8530 of 2005, decided on 18th May, 2005.
 
(a) Constitution of Pakistan (1973)---
 
---Arts. 189 & 190---Judgment of Supreme -Court---Judgment of Supreme Court was binding on each and every organ of the State by virtue of Arts.189 & 190 of Constitution.
Asif Jah Siddiqi v. Government of Sindh PLD 1983 SC 46, Abdul Majid and others v. Abdul Ghafoor Khan and others PLD 1982 SC 146; Pir Bakhsh through L.Rs. and others v. The Chairman, Allotment Committee and others PLD 1987 SC 145 and Noor Din's case PLD 1973 SC 17 ref.
 
(b) West Pakistan Land Revenue Act (XVII of 1967)---
 
---Ss. 42 & 44--Constitution of Pakistan (1973), Art.199---Constitutional petition---Maintainability---Correction of entries of Register Girdawari---Matter with regard to correction of entries of Register Girdawari, having concurrently been decided against petitioners by Authorities below including Board of Revenue, Authorities below were justified not to re-open the matter--Constitutional petition was not maintainable as High Court in exercise of its constitutional jurisdiction, could not substitute its own findings in place of findings of the Tribunals below.
Khuda Bukhsh v. Muhammad Sharif and another 1974 SCMR 279; Muhammad Sharif and another v. Muhammad Afzal Sohail and others PLD 1981 SC 246; Abdul Rehman Bajwa v. Sultan and 9 others PLD 1981 SC 522; Board of Intermediate and Secondary Education, Lahore through Chairman and another v. M. Massadaq Naseem Sindhoo PLD 1973 Lah. 600 and Syed Azmat Ali v. The Chief Settlement Rehabilitation Commissioner, Lahore and others PLD 1964 SC 260 ref.
 
Ch. Abdul Razzaq Kamboh for Petitioners.
 
Muhammad Hanif Khatana, Addl. A.-G. on Court's call.
 
ORDER
 
Case 70
 
2006 C L C 618
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
MUHAMMAD SHAREEF----Petitioner
 
Versus
 
MUHAMMAD RAMZAN and 3 others----Respondents
 
Civil Revision No.1612/D of 1998, heard on 17th January, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
---S. 115--Limitation Act (IX of 1908), S.4--Revision before High Court---Expiry of limitation during summer vacations---Impugned judgment was passed on 24-3-1998---Application for certified copies was made on 14-4-1998, which were prepared on 18-5-1998 and delivered on 21-5-1998---Petitioner, after excluding time spent in getting certified copies, could file revision on or before 25-7-1998, but he filed same on 14-9-1998---Validity-According to notification of High Court dated 14-5-1998, summer vacations started from 13th July up to 12th September, but its Registry remained open during vacations for receipt of all kinds of petitions on working days--In spite of closure of High Court for regular work during such vacations, alternate arrangements had been made for receipt of petitions involving question of limitation---High Court during vacations would be deemed to be open for institution of some Hs---Period of limitation, thus, could not be enlarged under cover of S.4 of Limitation Act, 1908---Preparation of memorandum of revision and its tiling on 14-9-1998 showed that petitioner had not made any effort to file same within prescribed time---Revision petition was barred by time.
 
Most Almay v. Hashanah 1989 MLD 3831; Fateh Ali Khan v. Subedar Muhammad Khan 1970 SCMR 238; Lehar Khan v. Moir Hamza and others 1999 SCMR 108; Khushi Muhammad v. Muhammad Sharif and others 1995 MLD 1042 and Rehana Kausar v. Faqir Muhammad and another 2004 CLC 1202 rel.
 
(b) Punjab Pre-emption Act (IX of 1991)-
 
---S. 30(b)---Pre-emptive suit---Limitation--Sale Mutation, according to plaintiff, was sanctioned on 27-8-1993, but according to defendant on 7-8-1993-Plaintiff produced copy of "Part Potwar" of mutation showing its sanction on 27-8-1993, whereas defendant produced copy of "Part Sarkar" of mutation showing its sanctioning on 7-8-1993---Validity---Copy of "Part Potwar" of mutation without signatures of Revenue Officer would carry no weight---"Rapt Rozenamcha Waqiati" maintained by Patwari showed that on 27-8-1993, no mutation was sanctioned by Revenue Officer---Statement of Revenue Officer about sanctioning of suit mutation on 7-8-1993 could not be shaken during cross-examination---Suit was, held, to be barred by limitation.
?
Shafqat Mehmood for Petitioner.
 
Syed Kaleem Ahmad Khursheed for Respondents.
 
Date of hearing: 17th January, 2006.
 
JUDGMENT
 
Case 71
 
2006 C L C 627
 
[Lahore]
 
Before Umar Ata Bandial, J
 
MUHAMMAD ZAFAR and 4 others----Appellants
 
Versus
 
SAJJAD MUNIR and others----Respondents
 
Regular Second Appeal No.56 of 2005, decided on 30th June, 2005.
 
Specific Relief Act (I of 1877)-
 
---S. 12---Specific performance of agreement to sell---Execution of alleged agreement to sell as well as receipt of any consideration therefor having been denied by defendants/alleged vendors, issue with regard to execution of agreement and receipt of consideration was framed, burden of proof of which was placed on plaintiffs--On said issue finding of appellate Court was that agreement to sell was tampered with, but plaintiffs denied allegation of tampering and to establish them point, they requested for original document to be summoned and examined against deposit of security in sum of Rs.10,000 to establish validity of their plea, which request was accepted---When document in question was examined, erasure and alteration were found therein---Finding given by appellate court, in circumstances was entirely justified---No question of law having arisen for determination, second appeal was dismissed and security deposited by plaintiffs was forfeited.
 
Kamil Hussain Naqvi for Appellants.
 
Rana Rashid Akram Khan for Respondents.
 
Date of hearing: 30th June, 2005.
 
JUDGMENT
 
Case 72
2006 C L C 634
 
[Lahore]
 
Before Muhammad Muzzammal Khan, J
 
Raja KHIZAR HAYAT---Petitioner
 
Versus
 
AHAD ZAFAR MINTO and 3 others----Respondents
 
Civil Revisions Nos.389, 390 and 391 of 2000, heard on 24th January; 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----Ss. 12, 21, 22(ii), 42 & 73---Transfer of Property Act (IV of 1882), Ss.10 & 110--Civil Procedure Code (V of 1908), O VI, R.17---Suit for declaration---Lease deed containing condition of extension of lease after lapse of initial term for all times to come with a restriction on lessor's right to alienate land and burdening him with penalty of Rs.2,50,000 for violation of any of its terms---Refusal of lessor (lady) to extend lease after expiry of initial term---Suit for declaration by lessee claiming to be entitled to remain in possession of land--Rejection of plaint by Trial Court--Appellate Court dismissed lessee's appeal and application to amend suit to one for specific performance---Validity---Option to extend lease period vested with lessor---Civil Court could not substitute such right of lessor through suit by lessee-Condition restricting alienation by lessor would be a clog on her ownership's rights, thus, specific performance of such contract might be refused--Lessee could sue for compensation for loss or damage, if caused by breach of contract, but he could not pray for conversion of suit for declaration into suit for specific performance by amendment---Lessee had made such application with mala fide intention to prolong his possession over suit-land---Lease deed had not been witnessed by any male member of lessor's family---Such unilateral and one-sided conditions without any consideration, would neither be binding nor would confer any right to maintain such suit without any just cause or reason-Lessee had no cause of action to maintain suit for declaration or specific performance against lessor-High Court dismissed revision petition in circumstances.
 
(b) Specific Relief Act (I of 1877)---
 
--Ss. 12 & 42---Transfer of Property Act (IV of 1882), S.110--Refusal of lessor to extend lease after expiry of its initial term--Suit for declaration or specific performance by lessee---Maintainability--Option to extend lease vested with lessor---Civil Court could not substitute such right through a suit.
 
Rana M. Ayub Khan Joia for Petitioner.
 
Malik Amjid Parvaiz and Zafar Iqbal Chohan for Respondents.
 
Date of hearing: 24th January, 2006.
 
JUDGMENT
 
Case 73
2006 C L C 645
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
MUHAMMAD NAWAZ----Petitioner
 
Versus
 
GHULAM FARID and others----Respondents
 
Civil Revision No.1653 of 2001, decided on 20th May, 2005.
 
Specific Relief Act (I of 1877)---
 
--S. 42---Suit for declaration---Both plaintiff and defendant were brothers and shop in dispute which was owned by Province of Punjab, its title was conveyed to defendant by the Provincial Government through a registered sale-deed and defendant after depositing price of shop was in possession of the same and defendant had also obtained proprietary rights in respect 'of the shop--Case of plaintiff was that he was entitled to transfer of suit shop because he was in possession of the same--Trial Court dismissed suit, but Appellate Court decreed the same---Validity-Considering the conveyance of title by admitted owner, namely, the Province, in favour of the defendant, no scope was left for any declaratory suit---If at all plaintiff asserted ally right under any Government Policy for the purpose of possession, he could not do so without seeking cancellation of sale-deed executed in favour of the defendant---Assertion of plaintiff that he was in possession of shop in dispute, was belied by evidence on record which had proved that plaintiff had placed his lock on disputed shop after filing of suit and said evidence had not been considered by Appellate Court--Impugned appellate decree being a result of non-reading of relevant evidence and failure to apply law. as set aside and decree of Trial Court stood restored.
 
Muhammad Rashid Chaudhry for Petitioner.
 
Nemo for Respondents.
 
Date of hearing: 20th May, 2005.
 
JUDGMENT
 
Case 74
2006 C L C 652
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
TALIB HUSSAIN SHAH through L.Rs.----Petitioners
 
Versus
 
NAAD ALI and others----Respondents
 
Civil Revision No.1854 of 1999, decided on 25th May, 2005.
 
Specific Relief Act (I of 1877)-
 
-S. 42---Qanun-e-Shahadat (10 of 1984), Art.64--Suit for declaration-On death of original owner of suit-land, inheritance mutation of his land was sanctioned in the name of petitioner who was his nephew and sole legal heir---Case of respondents was that original owner did not die issueless, but was survived by two sons who were predecessor-in-interest of respondents--One of respondents had also claimed to be daughter of original owner-Trial Court dismissed suit filed by respondents, but Appellate Court decreed the same---Validity---Respondents were required to prove their relationship with original owner of suit-land through witnesses who had special means of knowledge and who had requisite qualifications set out in Art.64 of Qanun-e-Shahadat, 1984, but they could not do so-Witnesses produced by respondents had made contradictory statements with regard to death of one of alleged sons of original owner who was alleged to be predecessor-in-interest of respondents-Contradictory testimony of said witnesses as to date of death of said son of original owner, had shown that they were not credible witnesses--Respondents who claimed to be grand-children of original owner, were not able to produce any family member to prove relationship between them and deceased original owner and it was difficult to believe that sons after death of original owner would be so oblivious of their rights in suit property as to be unaware that same was in possession of petitioner and that they would remain silent for decades without asserting their legal claim in suit property---Appellate Court had not taken into account said circumstances---Impugned appellate decree was set aside and decree of Trial Court stood restored.
 
Ch. Ehsan-ul-Haq Virk for Petitioners.
 
Irshad Ahmad Cheema for Respondents Nos.1 to 17.
 
Abdul Majeed Khan for Respondents NOs.18 and 19.
 
Date of hearing: 25th May, 2005.
 
JUDGMENT
 
Case 75
2006 C L C 659
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Mst. REHMAT BIBI and 6 others----Appellants
 
Versus
 
BAHADAR KHAN-Respondent
 
Regular Second Appeal No.131 of 1989, decided on 7th February, 2001.
 
Specific Relief Act (I of 1877)---
 
----S. 8--Suit for possession on basis of title---Courts below concurrently decreed the suit finding that plaintiff had been able to prove his title to suit property and that alleged transaction of sale as claimed by defendants in their favour on account of certain mutations had not been proved on record---Defendants had set up plea that they had purchased suit property from plaintiff by virtue of mutations in their favour, but they had failed to prove same as person who had allegedly identified the plaintiff at the time of alleged mutations, had not been examined by defendants so as to substantiate valid transaction of sale in their favour---Nothing was on record that prior to entry or attestation of said mutations, there were any sale negotiations between the parties and bargain was finalised and that defendants paid any price to plaintiff for said sale-Courts below had concurrently found that defendants had failed to establish valid sale and mutations on basis of sane-In absence of any misreading or non-reading of evidence on record, said concurrent findings could not be interfered with in second appeal.
 
Muhammad Bashir v. Mst. Sattar Bibi and another PLD 1995 Lah. 321; Hakim Khan v. Nazeer Ahmed Lughmani and 10 others 1992 SCMR 1832; Tooti Gul and 2 others v. Irfanuddin 1996 SCMR 1386 and Muhammad Igbal Khalid v. Chairman P.L.A.T. and others 1994 PLC 535 ref.
 
Ch. Arshad Mahmood for Appellants.
 
Sh. Naveed Shaharyar for Respondent.
 
Date of hearing: 7th February, 2001.
 
JUDGMENT
 
Case 76
2006 C L C 664
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Mst. HAMEEDA KHATOON and others----Petitioners
 
Versus
 
MUMMAL and others----Respondents
 
Civil Revision No.2368 of 2002, decided on 27th April, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Qanun-e-Shahadat (ID of 1984), Art.79---Suit for specific performance of agreement of sale---Plaintiffs by producing one of marginal witnesses had proved execution of agreement by predecessor in-interest of defendant and had further stated that other witnesses and predecessor-in-interest of plaintiffs had died---Trial Court, despite that, dismissed suit mainly on the ground that plaintiffs had not produced two marginal witnesses as required by Qanun-e-Shahadat, 1984---Plaintiffs had contended that agreement could have been proved by producing even one marginal witness because at relevant time Qanun-e-Shahadat, 1984 had not been promulgated and mandatory provision of Article 79 of Qanun-e-Shahadat, 1984 requiring production of two marginal witnesses, was not in force---Validity---Contentions of plaintiffs were well founded--Courts below, in dismissing suit, had proceeded in a manner not warranted by law---Impugned decrees were set aside and suit of plaintiffs was decreed.
 
Syed Muhammad Sultan v. Kabir-ud-Din and others 1997 CLC 1580 ref.
 
Tasawwar Hussain Qureshi for Petitioners.
 
Nemo. for Respondents.
 
Date of hearing: 27th April, 2005.
 
JUDGMENT
 
Case 77
 
2006 C L C 669
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
ARIF ALI alias MUHAMMAD ARIF---Appellant
 
Versus
 
MUHAMMAD ASLAM and another-Respondents
 
Regular Second Appeal No.171 of 2004, decided on 30th May, 2005.
 
Specific Relief Act (I of 1877)---
 
--S. 12---Suit for specific performance of agreement to sell---Case of respondents was that father of appellant had orally agreed to sell suit-land to them, while on following day, a written agreement to sell was executed by appellant--Appellant in his written statement denied having executed said agreement--Validity---Said agreement was proved through marginal witness and also scribe of same--Respondents also produced Part Patwar which had gone to show truthfulness of respondent's testimony-Appellate Court had examined evidence on record and concluded that appellant had indeed, executed agreement to sell in favour of respondents-Reasoning of Appellate Court below was proper and it had correctly appreciated evidence on records-Appellate decree was unexceptionable and appellant was unable to show existence of any of the grounds mentioned in S.100, C.P.C. which would justify interference in appellate decree in second appeal---Appeal was dismissed.
 
Nazir Ahmad v. Muhammad Rafique 1993 CLC 257 ref.
 
Anwar Basit for Appellant.
 
Syed M. Kaleem Ahmed Khurshid for Respondents.
 
Date of hearing: 30th May, 2005.
 
JUDGMENT
 
Case 78
 
2006 C L C 671
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
AMANAT ALI---Appellant
 
Versus
 
ASSISTANT COMMISSIONER WITH POWERS OF COLLECTOR,
NAROWAL and others----Respondents
 
Civil Revision No.1149 of 2001, decided on 14th June, 2005.
 
Specific Relief Act (I of 1877)---
 
---S. 54---Punjab Jinnah Abadies for non-proprietors in Rural Areas Act (III of 1986), S.3--Suit for permanent injunction-Plaintiff had sought permanent injunction to restrain defendants from interfering in his possession of suit-land contending that he being one of the owners in Shamlat, was in possession of suit-land in his own right--Fact that plaintiff was in possession of suit-land had not been denied by defendants, but defendants had merely asserted that they were entitled to possession under 7 Marlas Scheme for non-proprietors issued by Government under S. 3 of Punjab Jinnah Abadies for Non-Proprietors in
 
Rural Areas Act, 1986---Courts below concurrently dismissed suit on ground that suit-land had been allotted to defendants under said Scheme---Assistant Commissioner had acknowledged that plaintiff was an owner in village- -Jamabandi for relevant year had also supported submission/claim of plaintiff that he was entitled to land in Shamlat Deh in his own right---Courts below had seriously misread record and in particular had failed to consider Khasra Girdawari and Jamabandi for relevant year showing plaintiff's right in suit property-Impugned decrees of Courts, in circumstances, were not maintainable and were set aside and suit of plaintiff was decreed as prayed for.
 
Mian Muhammad Nawaz' vice Muhammad Sharif Chohan for Petitioner.
 
Kh. Muhammad Saced for Respondents Nos.1 to 3, 5, 11 and 12.
 
Other Respondents: Ex parte.
 
Date of hearing: 14th June, 2005.
 
JUDGMENT
 
Case 79
 
2006 C L C 677
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
NAZAR MUHAMMAD-Petitioner
 
Versus
 
MUHAMMAD HUSSAIN and others----Respondents
 
Civil Revision No.1041 of 1999, decided on 12th-May,2005.
 
Specific Relief Act (I of 1 877)---
 
---Ss. 39, 42 & 54-Suit for declaration, permanent injunction and cancellation of sale-deed--Dispute in the present case related to land measuring 1 Kanal, 7 Marlas which was claimed to have been purchased by petitioner---Suit by respondents against petitioner vendor was finally decreed concurrently by Courts below and said decree had attained finality---Petitioner, however was aggrieved of finding in appellate judgment that sale-deed in respect of land purchased by him was void-Petitioner had claimed that Vendor being owner in village, was entitled to proportionate ownership in Abadi Deh and respondents being not owners in the village, could not have asserted any title to said land---Petitioner, on that basis had rightly contended that findings of Appellate Court in respect of sale-deed regarding said land of 1 Kanal and 7 Marlas, was gratuitous and could not have been passed, once the suit had been dismissed--Finding of Appellate Court holding that sale-deed in respect of 1 Kanal and 7 Marlas land was illegal and void, was not Justified, in circumstances---Portion of decree in appellate judgment, was set aside-Judgment and decree of Trial Court, as a consequence, stood restored.
 
Sh. Naveed Shaharyar for Petitioner.
 
Riasat Ali Chaudhry for Respondents.
 
Date of hearing: 12th May, 2005.
 
JUDGMENT
 
Case 80
 
2006 C L C 689
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
GHULAM RASOOL and 4 others----Petitioners
 
Versus
 
ALLAH BAKHSH and 8 others----Respondents
 
Civil Revision No.817 of 2001, decided on 16th May, 2005.
 
Colonization of Government Lands (Punjab) Act (V of 1912)---
 
----S. 30---Specific Relief Act (I of 1877), S.12---Proprietary rights in land included in tenancy---Suit for specific performance of agreement---Plaintiffs had not impleaded Government as a defendant in suit and it was also not clear from the record that dues payable to Government for acquiring proprietary rights had been paid---Proprietary rights in respect of suit-land having not yet been transferred in favour of defendants, a decree for specific performance could not have been passed in favour of plaintiffs-Specific performance of agreement as per terms of said agreements, would need to await till conferment of proprietary rights on defendants, especially when parties themselves being cognizant of that limitation, had agreed that enforcement of agreements would be postponed till conferment of proprietary rights on defendants-Impugned concurrent decrees were modified accordingly.
 
Hashim Sabir Raja for Petitioners Nos.1 to 6.
 
Ms. Rizwana Naseer for Respondents Nos.1 to 4, 5-A, 5-B and 8.
 
Date of hearing; 16th May, 2005.
 
ORDER
 
Case 81
 
2006 C L C 694
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
BASHEER AHMAD-Petitioner
 
Versus
 
FAZAL DIN----Respondent
 
Civil Revision No.2574 of 2000, heard on 14th February, 2006.
 
(a) Oaths Act (X of 1873)---
 
--Ss. 8, 9, 10 & 11---Dismissal of appeal as per offer of appellant, when respondent took oath on Holy Qur'an-Plea of appellant was that respondent was a man of unsound mind, and he could not file suit in his own name without next friend-Validity--Respondent had not raised such plea/objection in written statement---Appellant himself had called upon respondent during appeal to give an oath on Holy Qur'an which would be sufficient to conclude that respondent was not a man of unsound mind---Such bald statement of appellant would not be enough for holding respondent as a man of unsound mind-High Court dismissed revision in circumstances.
 
(b) Civil Procedure Code (V of 1908)---
 
--O. II, R.2---Constructive res judicata, principles of-Applicability-Non-maintainability of earlier suit for declaration of ownership in absence of further relief of possession---Withdrawal of earlier suit after filing of subsequent suit for possession---Held: bar contained in O.II, R.2, C.P.C., would not attract as earlier suit was not maintainable.
 
Ghulam Nabi and others v. Seth Muhammad Yaqoob and others PLD 1983 SC 344; Saeed Ahmad and-3 others v. Tanveer Ahmad and another 1990 MLD 788; Ejaz Hussaina v. Abbas Ali 1993 CLC 2478 and Khaleeq Ahmad v. Tahir Saeed and others 1998 UC 740 rel.
 
Riaz Ahmad Kasuri for Petitioner.
 
Muhammad Ijaz Ahmad Lashari for Respondent.
 
Date of hearing: 14th February, 2006.
 
JUDGMENT
 
Case 82
 
2006 C L C 718
 
[Lahore]
 
Before Syed Shabbar Raza Rizvi, J
 
MUHAMMAD ZAFARULLAH KHAN and another----Petitioners
 
Versus
 
EHSAN ULLAH KHAN and 2 others----Respondents
 
Writ Petition No.1580 of 2006, decided on 23rd February, 2006.
 
Punjab Local Government Elections Rules, 2005---
 
-- Rr. 67, 71(4) & 72---Civil Procedure Code (V of 1908), O.VI, R.15--- Constitution of Pakistan (1973), Art.199--- Constitutional petition---Non-signing and non-verification of election petition---Election Tribunal allowed application for amendment---Validity---Discretionary for Election Tribunal to dismiss election petition for non-fulfilling of requirement of R.67 of Punjab Local Government Elections Rules, 2005---Not mandatory for Election Tribunal in all circumstances to dismiss election petition for such lapse---Election Tribunal had exercised its powers under R.71(4) of Rules, 2005---High Court dismissed constitutional petition in limine.
 
Zulfiqar Hassan v. Mirza Haq Nawaz 2004 MLD 1331; Sardar Zada Zafar Abbas v. Syed Hassan Murtaza PLD 2005 SC 600; 2000 SCMR 250 and Abdul Nasir v. Election Tribunal, T.T. Singh and others 2004 SCMR 602 ref.
 
Malik Abdus Sattar Chughtai for Petitioners.
 
ORDER
 
Case 83
 
2006 C L C 721
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
MUHAMMAD ASHIQ----Appellant
 
Versus
 
SAMEER ASHFAQ and 11 others----Respondents
 
Civil Revision Nos.524 and 525 of 2001, heard on 14th February, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. XLI, R.27---Additional evidence, production of---Principles---Provision of O.XLI, R.27 C.P.C. is couched in negative language prohibiting parties to adduce additional evidence whether oral or documentary, at appellate stage but with two exceptions---Firstly, that the Court from whose decree the appeal was preferred had refused to admit evidence which ought to have been admitted and secondly that the appellate Court required any document to be produced or any witness to be examined to enable it to pronounce judgment or for any other substantial cause, it may allow such evidence to be produced---Under the first part of O.XLI, R.27 C.P.C., evidence should have been refused by Trial Court and under the second, necessity of recording of evidence sought to be produced should have been felt by appellate Court itself.
 
(b) Civil Procedure Code (V of 1908)----------
 
-----O. XLI, R.27 & 5.115---Additional evidence---Deciding application for such evidence in isolation---Appellate Court did not allow petitioner to adduce additional evidence, hence his appeal was dismissed---Validity---Application for additional evidence should have been decided along with the appeal so that in case of necessity felt by Appellate Court, it might not feel itself handicapped in allowing such evidence to be brought on record---Appellate Court was in a better position to decide whether documents sought to be produced were needed for just/fair decision of the case or would be helpful for it in administration of justice to the parties, when it decided the appeal and application for additional evidence, simultaneously, at one time---Since both the appeal and application of petitioner under O.XLI, R.27 C.P.C. were decided in isolation to each other, against the spirit of law, both the judgments and decrees and orders in such behalf were not sustainable being tainted with material illegalities/irregularities, envisaged by S.115 C.P.C.---High Court in exercise of revisional jurisdiction set aside the judgments and decrees of Courts below and remanded the case to Lower Appellate Court for decision afresh---Revision was allowed accordingly.
?
Mst. Fazal Jan v. Roshan Din and 2 others PLD 1992 SC 811; Zar Wall Shah v. Yousaf Ali Shah and 9 others 1992 SCMR 1778; Abdul Haq v. Mst. Mughalani and 10 others 1999 YLR 1655; Ghulam Ahmad Chaudhry v. Akbar Hussain (deceased) through L.Rs. and another PLD 2002 SC 615; Mst. Fatima Bibi and 5 others v. Ghulam Safdar and another 2004 MLD 742 and Mst. Naziran Bibi v. Abdul Sattar and 12 others 2004 MLD 815 rel.
 
Abdul Aziz Akhgar and Khanzada Mukaram Khan for Petitioner.
 
Jahangir A. Jhoja for Respondents Nos.1 to 9.
 
Muhammad Ghani for Respondent No.10.
 
Date of hearing: 14th February, 2006.
 
JUDGMENT
 
Case 84
2006 C L C 726
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Mst. SALAMAT BIBI through L.Rs.----Appellants
 
Versus
 
YAMEEN through L.Rs. and others----Respondents
 
Regular Second Appeal No.129 of 1989, decided on 30th March, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Punjab Muslim Personal Law (Shariat Application) (Removal of Difficulties) Act (XXV of 1975), S.3---Civil Procedure Code (V of 1908), S.100---Second appeal---Limitation---Land mutated in year, 1974, was assailed in year, 1979, on the ground of sale by limited owner under custom---Trial Court dismissed the suit for being barred by limitation--Judgment and decree passed by Trial Court was maintained by Appellate Court---Validity---Special law had conferred maximum period of one year for challenging the sales, which otherwise were not earlier challenged by successor of the last male owner---Period of limitation commenced on the enforcement of law and the suit was brought after one year---Suit had been rightly held by the Courts below being barred by limitation---Second appeal was dismissed in circumstances.
 
Sher Muhammad v. The Additional Rehabilitation Commissioner, Multan and 7 others PLD 1968 Lah. 234; Additional Settlement Commissioner (Land), Sargodha v. Muhammad Shari and others PLD 1971 SC 791; Muhammad Yaqub v. Member, Board of Revenue, Lahore and 3 others PLD 1973 SC 304; Muhammad Asadullah Shaikh v. Government of Pakistan and others 2003 SCMR 392 and Saifur Rehman and another v. Sher Muhammad and others 2002 SCMR 1000 distinguished.
 
Hashmat Ali and another v. Mst. Jantan and 6 others 1993 SCMR 950 rel.
 
Muhammad Rasheed Mirza for Appellants.
 
Sheikh Abdul Aziz for Respondents.
 
Date of hearing: 22nd March, 2005.
 
JUDGMENT
 
Case 85
 
2006 C L C 730
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
SHAUKAT YAR MUHAMMAD----Petitioner
 
Versus
 
Ch. JAMAL DIN through L.Rs. and 4 others----Respondents
 
Civil Revision No.2657 of 2004, heard on 16th February, 2005.
 
Civil Procedure Code (V of 1908)---
 
----O. I, R.10 & S.151---Impleading of party---Application for--Application filed to be impleaded as party in pending appeal having been dismissed by Appellate Court, applicant challenged same in revision---Application contained some averments which were factual in nature---Proper course for Appellate Court was to receive reply from the parties who intended to oppose said application---Mere delay in making application was not enough to dismiss said application---In terms of 0. I, R.10, C.P.C. such a power could be exercised by the Court at any time if presence of a party was necessary to effectually and completely adjudicate upon and settle the question involved---There being conflicting claims of parties qua suit property, application filed by applicant had not been disposed of in accordance with law which needed to be heard and decided by Appellate Court after receiving reply thereto from those who opposed to his being impleaded as party---Revision against impugned order was accepted with the direction that application tiled by applicant for impleading him as party would be deemed to be pending before Appellate Court, which would be decided in accordance with law.
 
Khalid Ikram Khatana for Petitioner.
 
Respondents: Ex parse.
 
Date of hearing: 16th February, 2005.
 
JUDGMENT
 
Case 86
2006 C L C 732
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Syed ANSAR HUSSAIN and 2 others----Appellants
 
Versus
 
Khawaja MUHAMMAD KALEEM and 4 others----Respondents
 
Regular Second Appeal No.21 and Civil Revision No.400 of 2000, heard on 8th February, 2005.
 
(a) Specific Relief Act (I of 1877)--
 
---S. 42--Benami transaction---Onus to prove---Onus in Benami transaction is heavily upon the shoulders of the person who asserts to be the real owner.
 
(b) Specific Relief Act (I of 1877)---
 
---Ss. 8 & 42---Cross-suits---Effect---Benami transaction---Proof---Concurrent findings of fact by the Courts below---Plaintiff sought recovery of possession of house in question on the ground that the same was owned by her deceased son---Defendants claimed to be the actual owners of the disputed house and asserted that the deceased son of plaintiff was 'the only Benamidar---Contention of the defendants was that the suit house was actually purchased by a partnership firm of which the deceased was one of the partners---Possession of the suit house was with the defendants and original documents were also produced by them---Suit filed by plaintiff was dismissed and that of defendants for declaration of title was decreed by the Trial Court---Judgment and decree passed by Trial Court were maintained by Appellate Court---Plea raised by plaintiffs was that the defendants neither produced 4ny record of the firm nor any witness from where it could be established that the house was purchased by the firm---Validity---Only for the reason that being a partner of the firm, the possession of the house was taken over after the death of plaintiff's son, by a co-partner, including custody of the documents of title would not mean that the, property was purchased by the firm in the name of the deceased---Main ingredients about Benami transaction were the motive and source of money, proof whereof was missing in the case---Such aspect of the matter was overlooked by the Courts below, resultantly their judgments and decrees could not be sustained---If decree passed in the suit tiled against plaintiff was set aside, the other suit filed by the plaintiff had to be decreed---High Court set aside the judgments and decrees passed by both the Courts below and dismissed the suit filed by defendants while that of the plaintiff was decreed---Second appeal was allowed accordingly.
 
Talib H. Rizvi for Appellants.
 
Muhammad Sued Bhatti for Respondent.
 
Date of hearing: 8th February, 2005.
 
JUDGMENT
 
Case 87
 
2006 C L C 736
 
[Lahore]
 
Before Sheikh Azmat Saeed, J
 
SARGODHA IMPROVEMENT TRUST through Chairman----Appellant
 
Versus
 
ABDUL JABBAR and 2 others----Respondents
 
Regular Second Appeal No.10 of 2005, decided on 7th March, 2005.
 
Civil Procedure Code (V of 1908)---
 
----S. 100---Limitation Act (IX of 1908), S. 5---Second appeal---Limitation---Application for certified copy of impugned judgment was filed after 2 months and 21 days from passing of impugned order and its copy was prepared after 22 days of filing the application delivered to appellant after more than two months from its preparation---Appeal filed by appellant being barred by limitation, was dismissed as time-barred.
Iftikhar Ali v. Sh. Abdul Rashid and others 2003 SCMR 1560 ref.
 
Haji Ch. Haroon Akbar Cheema for Appellant.
 
Muhammad Ghani for Respondents.
 
ORDER
 
Case 88
 
2006 C L C 738
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
MUHAMMAD AMEER KHAN alias AMEER MUHAMMAD KHAN and 3 others----Appellants
 
Versus
 
MUHAMMAD KHAN and 2 others----Respondents
 
Regular Second Appeal No.93 of 1985 and C.M. No. 1 119 of 2000, heard on 10th February, 2005.
 
(a Punjab Pre-emption Act (I of 1913)---
 
----Ss. 21 & 30---Civil Procedure Code (V of 1908), 5.100 & O.XLI, R.27---Second appeal---Pre-emption suit---Limitation---Determination---Delivery of possession---Concurrent findings of fact by the Courts below---Mutation of sale was entered on 31-5-1973 and was sanctioned in favour of vendees on 18-4-1974---Pre-emptors filed suit for pre-emption on 14-2-1975---Both the Courts below considered the date of sanction of mutation as starting point of limitation and decreed the suit and appeal in favour of pre-emptors---Vendee contended that possession was taken over by him under the sale, prior to the sanction of mutation---Validity---Date of delivery of possession mentioned in mutation could not be taken to be the date of delivery of possession---Fact of taking over of possession by vendee prior to sanction of mutation or registration of sale, was to be independently proved---Statement of vendor which should be considered to be most important one was not shattered in the cross examination---On the basis of all evidence, both the Courts below had concurrently found the issue limitation against vendee---Such findings were neither shown to be the result of any misreading and non-reading of evidence not to be contrary to law---High Court declined to interfere in the judgments and decrees passed by the Courts below---Second appeal was dismissed in circumstances.
 
(b) Civil Procedure Code (V of 1908)---
 
----O. XLI, R.27---Punjab Pre-emption Act (I of 1913), S.21---pre emption suit---Delivery of possession---Proof---Additional evidence, production of---Scope---Appellate Court had rightly rejected the application of vendees under O.XLI, R.27, C.P.C. for the reason that they were conscious of the nature of the dispute between them and the pre-emptors in the Hs---At the appropriate stage of trial, no effort was made to bring such evidence on the record, despite having ample and full opportunity to produce the same.
 
Hameed Azhar Malik for Appellants.
 
Sh. Naveed Shahryar for Respondents.
 
Date of hearing: 10th February, 2005.
 
JUDGMENT
 
Case 89
 
2006 C L C 741
 
[Lahore]
 
Before Umar Ata Bandial, J
 
Ch. ABDUL HAMEED and another----Petitioners
 
Versus
 
BASHIR AHMAD SHAUQ and 3 others----Respondents
 
Civil Revision No.2574 of 2005, heard on 16th January, 2006.
 
Cooperative Societies Act (VII of 1925)---
 
----Ss. 70 & 70-A read with Bye-laws 17 & 18---Suit against Cooperative Society---Bar against institution of suit without statutory notice---Plaintiffs in suit for declaration asserted that they be declared as elected office-bearers of Society because their candidature was unopposed in elections which were to be held in its general meeting, notwithstanding that such meeting could not be held for lack of quorum---Suit was decreed and decree upheld in appeal---Validity---Suit against a Society or its officers in respect of any act touching the business of the Society was not competent under Ss.70 & 70-A of the Cooperative Societies Act, 1925, without issuance of notice prior to its institution---Objection of defendant was that Bye-laws 17 & 18 of the Society expressly required that election of office-bearers of Society was to be held in a meeting of general body---Meeting that was convened suffered from lack of quorum, therefore, no election could be held and in absence of election no person could be declared elected to an office---Such objection was well-founded on legal principles and binding instruments including the bye-laws of the Society as they dealt with the legal validity of election process and could neither be treated as directory nor were deemed to be waived by the Society and its members---Courts below had failed to apply their judicial mind to consider such crucial aspect of dispute---Impugned findings of Courts below were, therefore, set aside by High Court.
 
Lahore Cantt. Cooperative Housing Society Limited v. Messrs Builders and Developers (Pvt.) Limited and others PLD 2002 SC 660 and Messrs Sunshine Biscuits Limited v. Muhammad Hassan Lodhi and another PLD 1982 Lah. 189 ref.
 
Ch. Zafar Ullah for Petitioners.
 
Muhammad Ramzan Chaudhry for Respondents.
 
Date of hearing: 16th January, 2006.
 
 
 
JUDGMENT
 
Case 90
 
2006 C L C 743
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
MUHAMMAD HANIF KHAN----Petitioner
 
Versus
 
SHAH MUHAMMAD----Respondent
 
Civil Revision No.426 of 2004, heard on 21st February, 2006.
 
Specific Relief Act (I of 1877)-
 
----S. 12---Suit for specific performance of agreement to sell by the agent-Plaintiff asserted that he had made payment of earnest money through cheque issued by his agent but defendant contended that cheque was not encashed and same was returned---Suit was decreed and decree was upheld---Validity---No evidence was available to show that disputed cheque was ever presented to the bank from where it was alleged to have been bounced---Original cheque if not returned to agent should have been available with defendant but he, without plausible explanation, was not in possession of the same---Even it was not established that on the requisite date stipulated for encashment of cheque in question, agent had no funds in his bank account due to which payment was not received by defendant---Agreement had to be accomplished by defendant after attaining the proprietary rights which had been admittedly conferred upon him, plaintiff was justified to seek specific performance of agreement to sell against defendant---No legal infirmity in judgments of Courts below, calling for interference in revisional jurisdiction had been shown, hence petition was dismissed.
 
Ch. Rehmat Ali Dhillon for Petitioner.
 
Ch. Muhammad Chiragh Dogar for Respondent.
 
Date of hearing: 21st February, 2006.
 
JUDGMENT
 
Case 91
 
2006 C L C 745
 
[Lahore]
 
Before Ali Nawaz Chowhan, J
 
S.M. ISMAIL----Petitioner
 
Versus
 
CAPITAL DEVELOPMENT AUTHORITY, ISLAMABAD through Chairman and 4 others----Respondents
 
Writ Petitions Nos.346 and 491 of 2004, heard on 30th June, 2004.
 
Capital Development Authority Ordinance (XXIII of 1960)---
 
----S. 49(b)---Constitution of Pakistan (1973), Art.l99---Constitutional petition---Eviction of lessee---Plot given by Capital Development Authority to Staff Welfare Committee for welfare purposes---Lease of plot by Committee in favour of petitioner for a fixed term---Eviction of petitioner from plot by Authority after expiry of lease while matter of renewal of lease was under process---Petitioner alleged such eviction to be illegal as lessor of plot was Committee, which was a separate body from Authority and thus, such lease was outside purview of Capital Development Authority Ordinance, 1960---Validity---Committee was not alien to Authority, but was its component---Authority had delegated certain powers to Committee to deal with plot and use its funds for purposes of welfare of staff---Apprehension was that Authority under political influence would lease out plot surreptitiously to someone else---High Court disposed of constitutional petition with directions to Committee to decide fate of renewal of lease independently within specified time, and on its failure to do so, petitioner would be put in possession of plot till its decision.
 
Raja Hassan Ali Khan v. Additional District Judge, Islamabad and 2 others 2003 CLC 1819; Abdul Haq and 2 others v. The Resident Magistrate, Uch Sharif, Tehsil Ahmadpur East, District Bahawalpur and 6 others PLD 2000 Lah. 101; Sikandar and 2 others v. Muhammad Ayub and 5 others PLD 1991 SC 1041; Syed Mehdi Hasnain v. Muhammad Ayub and another 1970 SCMR 434; Muhammad Aslam v. Station House Officer and others 1993 MLD 152; Atta Muhammad Qureshi v. The Settlement Commissioner, Lahore Division, Lahore and 2 others PLD 1970 SC 61; Zaman Cement Company (Pvt.) Ltd. v. Central Board of Revenue and others 2002 SCMR 312; Khalid Saeed v. Shamim Rizwan and others 2003 SCMR 1505; Rahmat Khan v. Abdul Razzaq 1993 CLC 412; Nawab Syed Raunaq Ali and others v. Chief Settlement Commissioner and others PLD 1973 SC 236 and Muhammad Sharif through Legal Heirs and 4 others v. Sultan Hamayon and others 2003 SCMR 1221 ref.
 
Bad-ur-Rehman Lodhi and Mujeeb-ur-Rehman Kiani for Petitioner.
 
Muhammad Nawaz, Ch. Muhammad Tariq and Zaheer Bashir Ansari for Respondents.
 
Date of hearing: 30th June, 2004.
 
JUDGMENT
 
Case 92
 
2006 C L C 755
 
[Lahore]
 
Before Syed Hamid Ali Shah, J
 
MUHAMMAD MAALIK----Petitioner
 
Versus
 
MEMBER, BOARD OF REVENUE, PUNJAB, LAHORE and-3 others----Respondents
 
Writ Petition No.17411 of 2003, decided 14th July, 2005.
 
(a) West Pakistan Land Revenue Rules, 1968---
 
----R.l7---Lambardar, appointment of---Contest between son of former lamberdar and other candidate---Son of former lambardar was educated, retired employee and belonged to a community of village---Other candidate was Chairman Zakat and Ushr Committee of the area, had rendered unblemished services as sarbarah lambardar for over a decade, belonged to major Baradari of village and owned more land than son of former lambarar---Appointment of other candidate by Collector was, held, to be based on valid reasons.
 
Muhammad Ismail v. Member (Judicial-II), B.O.R. 1994 CLC 913; Muhammad Younas v. Member (Revenue) BOR 1997 SCMR 1115; Taj Muhammad v. M.B.R. 1994 CLC 906 and Mst. Nasreen Iqbal v. Member (Revenue) B.O.R. PLD 1993 Lah. 423 ref.
 
(b) West Pakistan Land Revenue Rules, 1968---
 
----R. 17---Lambardar, appointment of---Essential factors requiring consideration stated.
 
Authority competent to appoint lambardar is under an obligation to consider these essentials: (i) hereditary claim, (ii) extent of property in the estate, (iii) services rendered to the Government, (iv) character, ability and freedom from indebtedness, (v) strength and importance to the community to which a candidate belongs.
?
(c) West Pakistan Land Revenue Rules, 1968---
 
----R. 17---Appointment of lambardar---Choice of Collector in selection of lambardar---Validity---Such choice would not be interfered with, if Collector exercised his discretion in a reasonable manner.
 
Rao Abdul Jabbar Khan for Petitioner.
 
Muhammad Akbar Cheema for Respondent No.4.
 
ORDER
 
Case 93
 
2006 C L C 758
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
WATER AND POWER DEVELOPMENT AUTHORITY through Chairman and 2 others----Petitioners
 
Versus
 
NASIR IBRAHIM and another----Respondents
 
Civil Revision No.542 of 2001, heard on 24th March, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Suit for declaration---WAPDA had impugned concurrent decrees of Courts below whereby declaratory suit filed by respondents was decreed---Respondents sought declaration to the effect that detection bill issued by WAPDA, was illegal---One respondent did not appear as witness and the other respondent claimed that he had purchased property in respect or which disputed bill had been issued but said respondent could not produce any sale-deed or other document showing transfer of title to him---Respondent also could not bring on record any application filed by hint with WAPDA for change of name---WAPDA not only had produced detection bill, but also produced S.D.Os. as witnesses who proved that disputed bill had rightly been issued to the registered consumer/first respondent---WAPDA had fully proved by producing evidence that seals and postal orders pasted on the meter-box were broken and that first respondent was present at the time of checking of meter---Respondents had failed to discharge the onus of proof placed on them and could not prove that no tampering was made with the meter---Suit, in circumstances should have been dismissed even if WAPDA had not produced defence evidence---Courts below having exercised their jurisdiction illegally and with material irregularity, concurrent judgments and decrees of Courts below, were set aside---Suit of respondents stood dismissed, in circumstances.
 
Mian Khurshid Alam Ramay for Petitioners.
 
Respondents: Ex parte.
 
Date of hearing: 24th March, 2005.
 
JUDGMENT
 
Case 94
2006 C L C 760
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
KHALID FAROOQ----Appellant
 
Versus
 
MAZHAR IQBAL HUSSAIN----Respondent
 
Regular First Appeal No.19 of 2002, heard on 16th September, 2004.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXVII, Rr.2 & 3---Suit for recovery of amount on basis of Pro note---Application for leave to appear and defend suit---Application filed by defendant for leave to appear and defend suit was allowed by Trial Court and leave was granted subject to furnishing a surety bond in suit amount before next date of hearing---Needful was not done by defendant and instead he filed an application for extension of time on ground that defendant remained ill and could not file surety bond and written statement---No medical certificate was appended by defendant with his application for extension of time---Even with the present appeal no such certificate had been filed by defendant---Defendant did not even disclose nature of his illness--- Trial Court, in circumstances had rightly decreed suit filed by plaintiff and appeal against said order of Trial Court, was dismissed.
 
Syed Zulfiqar Ali Bokhari for Appellant.
 
Ch. Ishtiaq Ahmad for Respondent.
 
Date of hearing: 16th September, 2004.
 
JUDGMENT
 
Case 95
 
2006 C L C 762
 
[Lahore]
 
Before Muhammad Sair Ali, J
 
SECRETARY AGRICULTURE, AGRICULTURE DEPARTMENT, GOVERNMENT OF THE PUNJAB, LAHORE and 3 others----Petitioners
 
Versus
 
MUHAMMAD ABBAS & SONS----Respondent
 
Civil Revisions Nos.1670 and 1671 of 2003, heard on 17th January, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXIX, Rr.1 & 2---Specific Relief Act (I of 1877), Ss.52 & 53---Lease---Allegation of default in payment of rent---Temporary injunction, grant of---Prima facie case---Lessor was obliged to prove that lessee was defaulter and before cancellation of lease he was served with notice or heard by the competent authority---Lessee, who apparently was not a defaulter, had a prima facie case, balance of convenience was also in his favour and he was to suffer irreparable loss in case of refusal of injunction---No infirmity having been found in impugned order, petition was dismissed.
 
Rizwan Mushtaq, A.A.-G. for Petitioners.
 
Nemo for Respondent.
 
Date of hearing: 17th January, 2006.
 
JUDGMENT
 
Case 96
2006 C L C 765
 
[Lahore]
 
Before Sheikh Azmat Saeed, J
 
MUHAMMAD IQBAL and 3 others----Petitioners
 
Versus
 
ALLAH RAKHA and another----Respondents
 
Civil Revision No.2954-D of 1996, decided on 18th January, 2006.
 
Transfer of Property Act (IV of 1872)---
 
----S. 41---Qanun-e-Shahadat (10 of 1984), Art.118---Specific Relief Act (I of 1877), S.15---Bona fide purchaser---Proof---Defendant had specifically denied any knowledge of alleged prior agreement to sell therefore, burden of proof' shifted upon plaintiff to prove through cogent evidence that subsequent purchaser had specific knowledge of oral agreement---Impugned appellate judgment and decree made no reference to any cogent evidence in this behalf---Assumption of appellate Court that defendants were inhabitants of same village was disputed by them and no specific evidence in support of this conjecture was mentioned---Original contract for sale of property pertained to 1/3rd share of total property and plaintiff's suit, having been filed in respect of less area, was barred under S.15 of Specific Relief Act, 1877, but such matter was not adjudicated upon in appellate judgment---Such judgment being not sustainable, case was remanded to appellate Court for decision afresh.
 
Mst. Khair-ul-Nisa and 6 others v. Malik Muhammad Ishaque and 2 others PLD 1972 SC 25; Atta Muhammad v. Ali Sher and others 1989 MLD 4504; Din Muhammad v. Bashir Ahmad and 5 others 1979 CLC 466 and Muhammad Afzaal v. Muhammad Iqbal and another 2004 MLD 1288 ref.
 
Ch. Ras Tariq for Petitioners.
 
Ch. Muhammad Abdullah for Respondent No.2.
 
ORDER
 
Case 97
2006 C L C 767
 
[Lahore]
 
Before Jawad S. Khawaja, J
 
MUHAMMAD MUNSHI and 2 others----Petitioners
 
Versus
 
PROVINCE OF PUNJAB through District Officer (Revenue),
Sheikhupura and 3 others----Respondents
 
Civil Revision No.1972 of 2005, heard on 24th October, 2005.
 
Specific Relief Act (I of 1877)---
 
----Ss. 42 & 54---Qanun-e-Shahadat (10 of 1984), Arts.117 & 118-Suit for declaration---Dismissal of suit and appeal---Question of title---Burden of proof---No order of competent functionary for transfer of suit-land to defendants was available on record---Memo. according to which possession of suit-land was ordered to be delivered to predecessor-in interest of defendants, did not indicate the name of addressee---Report of proceedings for delivery of possession was extremely dubious in nature and could not be relied on---Attorney/witness of defendants clearly deposed that possession had never been delivered to defendants---Proceedings, if any, were taken for allotting land to predecessor-in interest of defendants, who had died many years earlier, were in respect of an area originally allotted to some other person and not in respect of suit-land---Incumbent upon defendants to prove the title through evidence and by producing the order of transfer of suit-land in their favour---Neither defendants nor their representative appeared in Court to prove their title---Decrees of Courts below being result of non-reading of evidence were not sustainable and. were set aside by High Court.
 
Padahabi alias Pat Shahi v. Lal Din 2001 CLC 742 and Pervez Alam Khan and 15 others v. Muhammad Mukhtar Khan through Legal Heirs 2001 CLC 1489 ref.
 
Sardar Muhammad Ramzan and Ghulam Rasool Chaudhry for Petitioners.
 
Ch. Muhammad Azeem for Respondents Nos. l and 2.
 
Ch. Bashir Ahmad for Respondents Nos.3 and 4.
 
Date of hearing: 24th October, 2005.
 
JUDGMENT
 
Case 98
 
2006 C L C 772
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
RAZIA BEGUM----Petitioner
 
Versus
 
ABDUL AZIZ----Respondent
 
Civil Revision No.1434 of 2005, decided on 22nd February, 2006.
 
Punjab Pre-emption Act (IX of 1991)---
 
----S. 13---Qanun-e-Shahadat (10 of 1984), Art.76---Suit for pre emption---Performance of Talbs---Proof---Plaintiff stated that she came to know about sale of suit-land at "Digar Waila" but said time did not correlate to the one mentioned in plaint, similarly the date of notice of Talb-i-Ishhad described during cross-examination was also different---Performance of Talb-i-Ishhad was proved by two witnesses but none of them was confronted with the original notice of Talb-i-Ishhad and instead photostat copy was tendered in evidence---Such a private document had to be proved by producing its original and photostat copy was not admissible in evidence---Without bringing on record, original documents and without seeking permission for secondary evidence, notice of Talb-i-Ishhad would not be considered to have been proved, in accordance with law---Defendant having denied the receipt of notice, it was the duty of plaintiff/pre-emptor to prove performance of Talbs which, in absence of proof, could not be presumed true on account of non-raising of objection by defendant to admissibility of photostat copy of notice of Talb- i-Ishhad---Neither any postal receipt regarding dispatch of notice was tendered in evidence nor the postman who distributed the notice in question was examined---In the absence of any such evidence, it could not be held that plaintiff had discharged her obligations according to the provisions of S.13 of Punjab Pre-emption Act, 1991---Courts below having not committed any illegality/irregularity amenable to revisional jurisdiction of High Court, petition was dismissed.
 
Mst. Amir v. Soini 1997 MLD 2376; Muhammad Rafique v. Ghulam Murtaza 1998 MLD 292; Fateh Muhammad and 2 others v. Gulsher 2000 CLC 409; Hadayat Ullah and others v. Jan Alam and others 2003 MLD 625 and Ghulam Abbas v. Manzoor Ahmad and another PLD 2004 Lah. 125 ref.
 
Ch. M.S. Shad for petitioner.
 
Ch. Pervaiz Ashraf and M. Zaman Chaudhry for Respondent.
 
ORDER
 
Case 99
2006 C L C 776
 
[Lahore]
 
Before Syed Sakhi Hussain Bukhari, J
 
JALAL and another----Petitioners
 
Versus
 
PROVINCE OF PUNJAB through District Collector, Gujrat and 2 others----Respondents
 
Civil Revision No.750 of 2003, decided on 6th February, 2006.
 
Civil Procedure Code (V of 1908)---
 
----S. 115---Limitation Act (X of 1908), S.5---Revision---Delay in filing of revision---Application for condonation of delay was dismissed---Validity---Petitioners in their. application asserted that they could not file revision within prescribed period due to unavoidable circumstances but they failed to give any plausible explanation in this regard for which petition deserved dismissal---Petitioners, on merits too, had no case as property in dispute was Shamlat Deh and was admittedly owned by owners of the village---School had been built on suit-land many years back and that land was reserved for residents of village---Petitioners themselves produced Jantri Taqseem Shamlat Deh which clearly showed that petitioners had already sold land which was more than their due share---Claim of petitioners being baseless was rightly dismissed by Courts below---No illegality or material irregularity having been found in impugned judgments, same did not call for any interference under revisional jurisdiction.
 
Zafar Iqbal Chohan for Petitioners.
 
Ch. Muhammad Suleman, Addl. A.-G. for Respondents.
 
 
ORDER
 
Case 100
2006 C L C 787
 
[Lahore]
 
Before Syed Hamid Ali Shah, J
 
ZULFIQAR AHMED BUTT and another----Petitioners
 
Versus
ASAD DAR and 4 others----Respondents
 
Civil Revision No.2609 of 2005, decided on 1st March, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. XXXIX, Rr. 1 & 2, O.XLIII, R.3 & S.115---Interim injunction---Registered post acknowledgment due receipt, non-filing of---Effect---Filing of fresh appeal---Scope---Trial Court declined to grant interim injunction to plaintiff---Appeal against order of Trial Court was dismissed by Appellate Court, as no registered post acknowledgment due receipt was annexed with the appeal---Validity---Before presenting appeal, notice under O.XLIII, R.3 C.P.C. to respondent or his Advocate with a copy of memorandum/grounds of appeal and copy of order appealed against, was a mandatory requirement-Plaintiff was required to the acknowledgment due, postal or other receipt with memorandum of appeal for the record of Appellate Court---Non-compliance of such requirement entailed penal consequences and no appeal could be entertained without issuance of the requisite notice---Dismissal of appeal on non-compliance of O.XLIII R.3 C.P.C. did not stop plaintiff from seeking relief on merits---Subsequent to dismissal of appeal under O.XLIII, R.3, C.P.C., plaintiff could file fresh appeal after complying with mandatory provisions and fresh appeal was no bar---High Court in exercise of revisional jurisdiction declined to interfere with the order passed by Lower Appellate Court as there was no illegality or infirmity in the order---Revision was dismissed in circumstances.
 
Messrs Nasir Metal Crafts Pvt. Ltd. through Chief Executive v. Zasha through Chief Executive and 2 others 1997 MLD 1910 distinguished.
 
Mrs. Dino Manekji Chinoy and others v. Muhammad Muteen PLD 1983 SC 693; Ghulam Rabbani v. Abdul Qayyum and 2 others 1990 MLD 1871; Noor Muhammad v. Ch. Liaqat Ali Khan 1990 CLC 929 and Haji Muhammad Naeem and another v. Malik Ghulam Nabi and 5 others PLD 1988 Quetta 9 rel.
 
(b) Interpretation of statutes---
 
----Mandatory provisions of law are to be applied with full force and vigor.
 
Rao Tajammal Abbas and Manzoor Qadir for Petitioners.
 
Mansoor-ur-Rehman Khan Afridi for Respondent No.1.
 
 
ORDER
 
Case 101
 
2006 C L C 791
 
[Lahore]
 
Before Jawad S. Khawaja, J
 
Messrs JAM'S CONSTRUCTION COMPANY (PVT.) LIMITED through Managing Director----Appellant
 
Versus
 
PROVINCE OF PUNJAB through Secretary to the Government of Punjab (Communication and Works) Department, Lahore and 3 others----Respondents
 
First Appeal from Order No.495 of 2002, heard on 8th December, 2005.
 
Arbitration Act (X of 1940)---
 
----Ss. 30, 17 & 26-A---Setting aside of award---"Personal misconduct" and "misconduct of proceedings"---Proof---Sufficient material was not available to prove that arbitrators had committed personal misconduct or that they misconducted the proceedings---Mere fact that reasoning adopted by arbitrators in support of one or more items of award, was not legally sustainable, did not, by itself, establish misconduct on their part---To prove personal misconduct of arbitrators there had to be some evidence showing wrongdoing on their part such as dishonesty or established bias---Only deliberate disregard of the law could constitute misconduct of proceedings and there was an important distinction between "intentional and deliberate disregard of law" and "faulty reasoning contrary to law"---Award in the present case was broken down into different heads and was adjudicated separately in respect of' each head and subhead of the claim---Sixteen items had been decided by the arbitrators and claim of the appellant in respect of some of items was rejected---Appellant having not filed any objection to the award, rejection of his claim had attained finality---Allegation that award was wrong and was based on dishonesty had not been substantiated by reference to any fact---Only specific reference made by respondent was to standard specification which had not been mentioned in the contract and, therefore, was not applicable to the case---Out of disputed three items of award only one item had been found unsustainable on the ground that same was contrary to law---Award for idle time could not have been allowed by arbitrators because such matter was not referred to arbitration and therefore, could not have been decided by arbitrators---Arbitrators were fully justified in awarding claim of appellant regarding cost of material used in the project which was furnished by appellant---Reason given by arbitrators for awarding the claim based on escalation in cost of fuel and labour during contract period was found to be contrary to law because appellant had himself admitted that there was no sanction by the Government permitting the escalation envisaged under one of the conditions of contract---Distinction existed between "interest payment" and "payment by way of damages"---Reasons given by the arbitrators for awarding claim in respect of turn over were on account of damages while arbitrators had disallowed the claim for interest (mark-up)---Barring two items, the award was proper and had to be upheld---Award was made separately in respect of each item of claim under directions of the Court---Court was, therefore, required to consider the reasoning of arbitrators in respect of each item of claim and to affirm those parts of award which did not suffer from any defect of reasoning---Court however proceeded on erroneous premise that it was an appellate forum and was required to render its decision, de novo, on respective pleas of parties based on evidence---Observation of Court that award lacked reasoning, quite clearly, was contrary to record because the award itself contained reasoning behind the acceptance or rejection of each item of claim---Under S.26-A of Arbitration Act, 1940, the reasoning of arbitrators given in award was subject to the scrutiny of the Court but legal defect, if any, in such reasoning could not, by itself, vitiate the award on ground of misconduct of proceedings---Appellant and the respondent (department) had, by and large, accepted the award but Trial Court set aside the same as a whole---Impugned order was, therefore, set aside by High Court---Exercise of power in respect of question of limitation being permissible under S.17 of Arbitration Act, 1940---Objections filed by respondent/department, after the prescribed period of limitation, were of no consequence.?
 
Standard Specification No.821 ref.
 
Syed Almas Haider Kazmi for Appellant.
 
Muhammad Nawaz Bajwa, A.A.-G. assisted by Ch. Muhammad Azeem for Respondent.
 
Akbar Ali, XEN and Shahid Pervez, S.D.O. Highway, Sahiwal.
 
Date of hearing: 8th December, 2005.
 
 
 
 
 
JUDGMENT
 
Case 102
2006 C L C 799
 
[Lahore]
 
Before Sardar Muhammad Aslam, J
 
ALTAF HUSSAIN----Petitioner
 
Versus
 
ALI MUHAMMAD through L.Rs.---Respondents
 
Civil Revision No.1096 of 2000, heard on 20th October, 2004.
(a) Punjab Pre-emption Act (IX of 1991)---
 
---S. 13---Talb-e-Muwathibat performance of---Proof---Version of pre-emptor in plaint and notice of Talb-e-Ishhad as to acquisition of knowledge of sale-Evidence of pre-emptor and witnesses of such-notice contradictory to each other as to date on which pre-emptor acquired knowledge of sale, issued such notice and filed suit for pre-emption---Validity---Laxity in performance of Talb-e-Muwathibat, being a jumping demand, would be seen with rigour---Performance of Talb-e-Muwathibat was not proved in circumstances---Principles.
 
(b) Punjab Pre-emption Act (IX of 1991)---
 
----S. 13---Talb-e-Muwathibat---Laxity in performance of such Talb, which being a jumping demand, would be seen with rigour.
 
S.M. Tayyab for Petitioner.
 
Kh. Basit Waheed for Respondents.
 
Date of hearing: 20th October, 2004.
 
 
JUDGMENT
 
Case 103
 
2006 C L C 803
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
SAHIBZADA alias SAHIB KHAN----Appellant
 
Versus
 
MUHAMMAD HAYAT and another----Respondents
 
Regular Second Appeal No.47 of 1999, heard on 11th January, 2005.
 
Transfer of Property Act (IV of 1882)---
 
---Ss. 54 & 118---Specific Relief Act (I of 1877), S.12---Specific performance of an agreement---Agreement of exchange---Agreement of exchange, which was akin to an agreement to sell, would not create or purport to create any right in the immovable property, and only right a person could have, was to seek specific enforcement of such agreement.
 
G.H. Khan for Appellant.
 
M.M. Hanif for Respondent No.1.
 
Zahid Hussain Khan for Respondent No.2.
 
Date of hearing: 11th January, 2005.
 
 
JUDGMENT
 
Case 104
 
2006 C L C 809
 
[Lahore]
 
Before Maulvi Anwarul Haq and Muhammad Jahangir Arshad, JJ
 
BILAL HUSSAIN----Appellant
 
Versus
 
BAHAUDDIN ZAKARIYA UNIVERSITY, MULTAN through Vice-Chancellor and 2 others----Respondents
 
I.C.A. No.197 of 2005 in Writ Petition No.4903 of 2005, decided on 5th October, 2005.
 
Bahauddin Zakariya University Act (III of 1975)---
 
----S. 11-A---Revision was competent before Chancellor of University under S.11-A of Bahauddin Zakariya University Act, 1975 against decision of University's Syndicate.
 
Malik Waqar Haider Awan for Appellant.
 
 
ORDER
 
Case 105
2006 C L C 810
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
Mst. RASHIDA BANO----Petitioner
 
Versus
 
Mst. SAMINA YOUSAF and 6 others----Respondents
 
Civil Revisions Nos.2264 to 2266 of 2003, decided on 22nd March, 2005.
 
Succession Act (XXXIX of 1925)---
 
----S. 372---Succession certificate, grant of---Commulative Deposit Certificates---Purchase of certificates in joint names of mother (respondent) and deceased son---Applicant as widow claimed that certificates were exclusively owned by deceased and respondent was a Benamidar---Respondent claimed to be exclusive owner of certificates on the ground that at the time of their purchase, deceased was a student of 20 years age having no independent source of income; that she with her income earned from abroad purchased certificates; and that she possessed the key of locker, wherein certificates were locked by deceased---Proof---Nothing was available on record to show as to who out of two contributed to what extent and proportion---Both parties had failed to establish their independent and exclusive source of such purchase---Motive of Benami had not been proved by either party---Acquisition of assets by deceased after purchase of certificates would have no retrospective nexus to prove his exclusive purchase and that respondent was a Benamidar---Money used for purchase of such certificates being family money would be deemed and assumed to have been equally contributed by mother and son---Certificates were, held, equally owned by respondent and deceased, thus, were entitled to share equally the amount with interest accrued thereon-Respondent as mother would also be entitled to 1/6th share out of 1/2 share of her deceased son, while the remaining share would go to applicant.
 
Mian Asrar-ul-Haq for Petitioner.
 
Ahmad Awais for Respondents Nos.1 to 5.
 
 
ORDER
 
Case 106
 
2006 C L C 817
 
[Lahore]
 
Before Syed Zahid Hussain, J
 
SAKHI MUHAMMAD----Petitioner
 
Versus
 
RASHIDA BIBI and 11 others----Respondents
 
Civil Revision No.940 of 2000, heard on 16th February, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Civil Procedure Code (V of 1908), S. 115---Suit for specific performance of agreement---Plaintiff, in a suit for specific performance, was to confine his claim to the extent mentioned in agreement while seeking enforcement thereof---Since the share, which was agreed to be sold by defendant in favour of plaintiff was only up to one fifth and ownership of defendant had been reduced to only 12 Kanals, plaintiff could seek proportionate performance to the extent of one fifth of 12 Kanals---Decree passed concurrently in favour of plaintiff in a suit which' was not barred by time, was modified which would be for 2 Kanals and 8 Marlas on payment of proportionate price and not for 12 Kanals as was concurrently decreed by both the Courts below.
 
Ch. Muhammad Abdullah for Petitioner.
 
Aftab Ahmad Sherazi for Respondents Nos.1-9.
 
Date of hearing: 16th February, 2005.
 
 
JUDGMENT
 
Case 107
2006 C L C 819
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
ABDUL MAJEED----Appellant
 
Versus
 
ABDUR RASHID and 3 others----Respondents
 
Regular Second Appeals Nos.84 and 100 of 1999, heard on 11th April, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
---S. 42---West Pakistan Urban Immovable Property Tax Act (V of 1958), S.3---Suit for declaration---Shop purchased by father in auction from Settlement Department---Son claimed to be real owner of shop and that father was only a Benamidar---Son's plea was that he had paid price of the shop; that he was in possession of shop and 'original P.T.O./P.T.D. thereof and that his name appeared in record of Excise and Taxation Department---Proof---Son had not shown his motive to buy shop in father's name---Son's counsel conceded that father had adjusted his compensation book towards price of shop, thus, consideration stood proved to have been paid by father---Father and son were closely related and son seemed to have been put in shop as licensee by father---Custody of original documents, which might be lying. in shop if given to for safe custody, would not have much relevance---Record did not establish as 'to how son had been shown as owner in Excise and Taxation record---Entry of ownership in Excise and Taxation record by itself would not confer any title to property---Suit was dismissed in circumstances.
 
(b) West Pakistan Urban Immovable Property Tax Act (V of 1958)---
 
---S. 3---Entry of ownership in Excise and Taxation Department's record---Effect---Such entry by itself would not confer any title to the property.
 
(c) Islamic Law---
 
--Gift---"Marz-ul-Maut"--- Gift through registered deed by father in favour of two sons excluding his third son---Death of father after two days after execution of deed---Effect---No evidence on record was available to show that father was on death bed or was of indisposed mind at the time of snaking gift or execution of deed---Such death of father by itself would not invalidate gift for reason of Marz-ul-Maut.
 
Ch. Naseer Ahmad Sindhu for Appellant.
 
Talib H. Rizvi for Respondents.
 
Date of hearing: 11th April, 2005.
 
 
JUDGMENT
 
Case 108
 
2006 C L C 829
 
[Lahore]
 
Before Sardar Muhammad Aslam, J
 
Messrs RANA WORKS ENGINEERS AND CONTRACTORS through Proprietor----Appellant
 
Versus
 
PAKISTAN through Secretary Defence, Government of Pakistan, Islamabad and 5 others----Respondents
 
Regular Second Appeal No.59 of 2004, decided on 17th February, 2005.
 
Civil Procedure Code (V of 1908)---
 
----S. 100, O.XLI, R.1(1) & O.XLII---Second. appeal---Non-filing of certified copy of judgment and decree of Trial Court in spite of objection raised by the office of High Court---Application seeking exemption from filing of such copy was filed after a period of ten (10) months---Validity---Second appeal, in absence of such copy, would not be maintainable in law---Appellant was negligent as he had not adverted to objection raised by the office on such point-High Court did not allow application and dismissed appeal--Principles.
 
Siraj Din and another v. Muhammad Ishaq 1981 CLC 1740; Kala v. Allah Dad PLD 1977 Lah. 376; Muhammad Hanif v. Faqir Muhammad PLD 1977 Lah. 1214 and Akbar Khan v. Muhammad Razzaq alias Abdul Razaq PLD 1979 SC 830 ref.
 
Mian Sarfraz-ul-Hassan for Appellant.
 
Tariq Shamim for Respondents.
 
 
ORDER
 
Case 109
2006 C L C 842
 
[Lahore]
 
Before Sardar Muhammad Aslam, J
 
Mst. FATEH BEGUM through Special Attorney----Petitioner
 
Versus
 
GHULAM SARWAR through L.Rs.----Respondent
 
Civil Revision No.252-D of 1998, heard on 21st December, 2004.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 11---Qanun-e-Shahadat (10 of 1984), Art.114---Dismissal of first suit up to Supreme Court---Second suit challenging validity of same gift on same allegation---Plaintiff's plea was that he was not bound by decision in first suit filed by another person as his next friend branding him a person of unsound mind---Validity---Plaintiff in earlier suit had stated to be of sound mind and admitted making of gift without coercion---Institution of second suit was earlier than decision of Supreme Court rendered in plaintiff's petition arising out of his first suit, but his counsel had not disclosed pendency of second suit before Supreme Court---Plaintiff could not turn round to assert such plea as he was estopped by his words and conduct---Second suit was dismissed in circumstances.
 
(b) Islamic Law---
 
----Gift of Musha in favour of an existing co-sharer---Delivery of possession---Donee co-sharer in possession would not be obliged to seek possession of gifted land---Principles.
 
According to Register Haqdaran Zamin, donor was not the sole owner of suit-land. Donee was also one of the co-sharers in suit-land even before making of gift in his favour. Donee being co-sharer in possession was not obliged to seek possession of suit-land. A co-sharer in possession of any portion of land would be deemed to be in possession of each inch of the property jointly owned by the parties.
 
(c) Islamic Law---
 
----Gift---Allegation of securing gift deed through coercion---Non appearance of donor in witness-box though living a healthy life---Effect---Onus to prove such facts would lay on donor---Inference would be drawn against donor for his non-appearance in wiriness-box---Objection was overruled in circumstances.
 
Muhammad Afzal Wahla for Petitioner.
 
Mehdi Khan Chowhan for Respondents.
 
Date of hearing: 21st December, 2004.
 
 
JUDGMENT
 
Case 110
2006 C L C 850
 
[Lahore]
 
Before Ijaz Ahmad Chaudhry, J
 
Mst. QURRAT-UL-AIN----Petitioner
 
Versus
 
SECRETARY EDUCATION, LAHORE and 3 others----Respondents
 
Writ Petition No.3034 of 2005, decided on 4th July, 2005.
 
Educational Institution---
 
----Examination---Petitioner/candidate, who appeared in Intermediate Part-I Examination of Session 2002, had failed in two subjects in which he was given compartment---Petitioner then applied for Intermediate Part-I and II examination 2004 with nominal examination fee and she appeared in examination with full subjects of both parts of Intermediate without any objection by the Examination Authorities---Result card was not issued to petitioner, despite according to her information, she had passed examination in full---Stand of Authorities was that since petitioner failed to appear in two papers of compartment of Part-I and all subjects of Part-II in Session 2003, she was declared failed in examination as a whole and she was required to appear in all subjects of both parts of Intermediate examination in Session 2004, but she only appeared in one paper of Part-I along with all subjects of Part-II through concealment of fact and that was why result card could not be issued to her---Validity---Rule 25 of Rules Regarding Part-I and Part-II (Part System) Examination at Intermediate Level, issued by Notification dated 29-12-1997, had provided that two chances had to be given to candidate to clear subjects of compartment---Petitioner, in circumstances could appear in two coming examinations to clear said papers---If petitioner did. not appear in Session 2003 to clear said papers of compartment with papers of Part-II, it could not be said that petitioner had lost her second chance as well to clear said papers of compartment, which she had availed in Session 2004 and it could not be said that petitioner having not appeared in said papers in Session 2003, had failed as a whole---High Court accepting constitutional petition directed the Authorities to issue Result Card for Intermediate Examination Session 2004 in favour of petitioner.
 
Ijaz Ahmad Toor for Petitioner.
 
M.R. Khalid Malik, Addl. A.-G.
 
Haji Muhammad Aslam Malik for Respondents.
 
Malik Manzoor Ahmad, Senior Superintendent (Inter) and Tariq Mahmood, Assistant (Legal Cell).
 
 
ORDER
 
Case 111
 
2006 C L C 852
 
[Lahore]
 
Before Muhammad Nawaz Bhatti, J
 
Mst. SHAMIM AKHTAR SAMINA----Petitioner
 
Versus
 
JAFFAR HUSSAIN and 2 others----Respondents
 
Writ Petition No.9767-F of 2002, heard on 8th December, 2005.
 
West Pakistan Family Courts Act (XXXV of 1964)---
 
----Ss. 5, Sched, 9 & 14---Constitution of Pakistan (1973), Art.199---Constitutional petition---Suit for recovery of dowry articles---Filing of written statement---Family Court and appellate Court having dismissed suit, constitutional petition had been filed against concurrent judgments of courts below---Written statement to the suit filed by petitioner, was not filed by respondent himself, but was filed by his special attorney---Validity---Under provisions of S.9 of West Pakistan Family Courts Act, 1964, defendant was bound to appear before Family Court himself for the purpose of filing a written statement and his attendance could not be dispensed with---Written statement filed by special attorney of respondent did not deserve consideration in the eye of law---Judgment passed without written statement of respondent himself was void and illegal---Impugned judgments were set aside and case was remanded to pass fresh order after hearing parties.
 
Mazhar Iqbal v. Falak Naz and 2 others PLD 2001 Lah. 495 and Mushtajab Hasan and others v. Director Trade Organisations and others 1996 CLC 1725 ref.
 
Sardar Muhammad Akram Khan Pitafi for petitioner. Respondent No. 1: Ex parte.
 
Date of hearing: 8th December, 2005.
 
 
JUDGMENT
 
Case 112
 
2006 C L C 855
 
[Lahore]
 
Before Mian Saqib Nisar, J
 
KHALIL AHMAD through Special Attorney----Appellant
 
Versus
 
KAMRAN SHARIF and another----Respondents
 
Regular Second Appeal No.69 of 2000, heard on 18th January, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 12---Contract Act (IX of 1872), Ss.2(e) & 24---Suit for specific performance of agreement to sell---Plaintiff not party to agreement---Absence of offer by plaintiff to purchase property, which could be accepted by vendor---Terms and conditions of agreement were absolutely vague---Non-mentioning of amount of consideration in agreement for which plaintiff would purchase property---Such agreement was not enforceable in law.
 
Muhammad Zofigan v. Muhammad Khan and others PLD 2004 Lah. 255 and Sher Baz Khan and others v. Mst. Malkani Sahibzadi Tiwana and others PLD 1996 Lah. 483 ref.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 31---Admission of co-defendant---Not binding upon other defendant.
 
(c) Specific Relief Act (I of 1877)---
 
----S. 12---Transfer of Property Act (IV of 1882), Ss.41 & 52---Civil Procedure Code (V of 1908), O.XXIII, R.3---Suit for specific performance of agreement to sell---Pendente lite sale of suit property by defendant-vendor in favour of second purchaser---Compromise between plaintiff and defendant-vendor for settlement of dispute through opinion of a Referee---Validity---Defendant-vendor, after sale of suit property, was left with no authority to enter into compromise with plaintiff---Real dispute after such sale, would be between plaintiff and second purchaser (also party to suit) as assignee of defendant-vendor and would have every right to independently contest matter on merits to protect his rights as lawful purchaser.
 
Yamin Khan and others v. Rais Jhangli Khan and others 1999 CLC 1755; Muhammad Murasleen v. Syed Noor Muhammad Hussani PLD 1968 Kar. 163 and Nisar Ahmed Sheikh v. Secretary to Government of Punjab PLD 1982 SC 457 ref.
 
Mian Suba Sadiq Klasson for Appellant.
 
Ch. Zafar Iqbal for Respondents.
 
Date of hearing: 18th January, 2005.
 
 
JUDGMENT
 
Case 113
 
2006 C L C 860
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
MUHAMMAD ASLAM alias BHOOLA----Petitioner
 
Versus
 
MUMTAZ HUSSAIN BABOO and another----Respondents
 
Civil Revision No.300 of 2000, heard on 13th December, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 9-Civil Procedure Code (V of 1908), O.II, R.2---Suit for possession---Maintainability---Suit having been concurrently decreed by two Courts below, defendant had filed revision against said concurrent decrees---Contention of defendant was that matter in dispute having been determined in earlier suit filed by plaintiff, present suit was barred under O.II, R.2, C.P.C.---Present suit in which possession of suit property was sought, being based on cause of action different to earlier suit, present suit was not barred by O.II, R.2, C.P.C.---Such aspect of case had been duly considered by Courts below holding that present suit was maintainable---Impugned decrees were consistent with record---Defendant being unable to advert to any jurisdictional error or other infirmity in impugned judgments, same could not be interfered with by High Court in exercise of its revisional jurisdiction.
 
Ch. Muhammad Sarwar for Petitioner.
 
Ch. Javed Rasool for Respondents.
 
Date of hearing: 13th December, 2005.
 
 
JUDGMENT
 
Case 114
 
2006 C L C 862
 
[Lahore]
 
Before Sardar Muhammad Aslam, J
 
Mst. BILQEES BEGUM alias JIMMI----Petitioner
 
Versus
 
MUHAMMAD IBRAHIM through L.Rs.----Respondents
 
Civil Revision No.1944 of 2000, heard on 8th February, 2005.
 
Punjab Pre-emption Act (IX of 1991)---
 
----Ss. 6 & 13---Suit for pre-emption---Making of Talbs, proof of---Witnesses produced by plaintiff had stated that plaintiff had performed Talb-i-Muwathibat by declaring that she would pre-empt suit property---Statements of said witnesses were not even questioned through a bare suggestion that plaintiff did not perform Talb-i-Muwathibat---Defendant did not state anywhere about non-performance of Talb-i-Muwathibat by plaintiff---Trial Court had recorded finding that plaintiff had failed to prove Talb-i-Muwathibat and Talb-i-Ishhad, whereas Appellate Court below in its impugned judgment had observed that plaintiff had succeeded in performance of Talb-i-Ishhad, but had failed to prove Talb i-Muwathibat--Findings of Appellate Court below in rejecting statement of husband of plaintiff, was not maintainable in law as his statement was supported by all other witnesses---Findings of Courts below though concurrent, were not maintainable in law as statements of witnesses of plaintiff were misconstrued and were not considered at all by Courts below---Concurrent judgments and decrees of Courts below were set aside and suit for possession by way of pre-emption filed by plaintiff was decreed in favour of plaintiff.
 
Muhammad Hanif v. Mst. Munawar Bi alias Munawar Noor 1999 SCMR 2230 ref.
 
Muhammad Sharif Khokhar for Petitioner.
 
Ch. Shafqat Qadeer for Respondent.
 
Date of hearing: 8th February, 2005.
 
 
JUDGMENT
 
Case 115
 
2006 C L C 864
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
TALIB HUSSAIN----Petitioner
 
Versus
 
SIRAJ----Respondent
 
Civil Revision No.1013 of 2004, heard on 7th June, 2004.
 
Specific Relief Act (I of 1877)---
 
----S. 39---Qanun-e-Shahadat (10 of 1984), Art.17---Suit for cancellation of alleged agreement to sell--Suit was decreed but decree was set aside in appeal---Incorrect recording of evidence---Effect---Plaintiff's entire evidence was to the effect that alleged agreement had been fraudulently prepared and that plaintiff had never agreed to sell the disputed property to defendant therefore, the concluding sentence of plaintiff's testimony i.e. "it is right that an amount of Rs.20,000 have been received and property has been sold" could only be taken as an incorrect recording of plaintiff's evidence---Defendant failed to produce marginal witnesses to the agreement---Prima facie, case having been proved in favour of plaintiff impugned appellate decree was set aside and that of Trial Court was restored by High Court.
 
Ch. Imtiaz Ahmad Kamboh for Petitioner.
 
Syed Zahid Hussain Shah for Respondent.
 
Date of hearing: 7th June, 2004.
 
 
JUDGMENT
 
Case 116
 
2006 C L C 867
 
[Lahore]
 
Before Muhammad Jehangir Arshad, J
 
MUHAMMAD ARSHAD----Petitioner
 
Versus
 
CIVIL Judge, 1ST CLASS and 3 others----Respondents
 
Writ Petition No.1183 of 2005/BWP, decided on 18th April, 2005.
 
Constitution of Pakistan (1973)---
 
----Arts. 199 & 203---Constitutional petition---Petitioner had sought direction to the Civil Judge for accelerated hearing of the suit---Record had shown that the Trial Court was not being allowed by counsel for the parties to proceed with the suit---After framing issues, suit was listed for petitioner's evidence and thereafter it was being adjourned due to non-co-operation of counsel for respondent---Examination-in-chief of one witness of petitioner was recorded, but he was not cross-examined by counsel for respondent for want of preparation and cross-examination of said witness had to be adjourned on payment of heavy costs---Thereafter case remained adjourned for one reason or the other---Said resume of proceedings of the Trial Court depicted a dismal state of affairs and uncalled for attitude of respondent/defendant who for one reason or the other did not allow the Trial Court to proceed with the suit---If counsel was busy in contesting election, he should not have filed power of attorney nor the Court should have allowed adjournment just for the pleasure of counsel who was a, prospective candidate for Punjab Bar Council Election---High Court, while exercising supervisory jurisdiction under Art.203 of the Constitution, directed Additional Registrar of High Court to place the matter before Inspection Judge for his perusal and issuance of necessary direction on administrative side---Trial Court, however, was directed to expedite the trial of the case.
 
Ch. Muhammad Ashraf Mahandra for Petitioner.
 
 
ORDER
 
Case 117
2006 C L C 869
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
NAZIR BEGUM and 6 others----Petitioners
 
Versus
 
AURANG ZEB through L.Rs. and 7 others----Respondents
 
Civil Revision No.1531 of 2001, heard on 2nd November, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 8---Registration Act (XVI of 1908), S.17---Suit for possession---Suit was dismissed but decreed in appeal---Oral sale by co-sharer--Question of title---Determination---Although in the earlier suit, declaration sought by defendant, was declined because they had not produced any registered sale-deed in their favour in respect of the suit-land valued at more than Rs.100 but mere fact that they were not owners of disputed land did not automatically mean that the same was owned by plaintiffs---Plaintiffs who were co-sharers of suit-land could only have succeeded if they had established either that vendor/co-sharer had sold his entire entitlement and therefore, could not convey title in disputed land or in the alternate, if they had brought proof on record to show that their entitlement in the Khasra could only be satisfied if the disputed land was included in their share---Plaintiffs were to establish their own title through evidence but they failed to prove their case---Appellate Court proceeded on wrong premises by holding that question of title had been settled in earlier litigation---Appellate judgment and decree being not sustainable, were set aside and findings of Trial Court were affirmed by High Court.
 
Nisar Ahmad Baig for Petitioners.
 
Ch. Arshad Mehmood for Respondents.
 
Date of haring: 2nd November, 2005.
 
 
JUDGMENT
 
Case 118
 
2006 C L C 873
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
ABDUL RASHID KHAN----Petitioner
 
Versus
 
ABDUL HAMEED KHAN through L.Rs.----Respondents
 
Civil Revision No.1220 of 2004, heard on 4th April, 2005.
 
(a) Islamic Law---
 
---Inheritance---Title to property would come to vest in legal heir(s) upon death of its owner regardless of any mutation of inheritance.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
---Arts. 17(2)(a), 79 & 117---Agreement to sell---Proof---Non -production of original agreement and its marginal witnesses in evidence by vendee without any reason---Production of extracts from register of scribe to show existence of agreement between parties---Validity---Such extracts could be considered in evidence in absence of original agreement---Scribe could not identify vendor and vendee present in Court as the persons on whose behest such entries were made in his register---Receipt of money had not been proved through such extracts---Burden was on vendee to prove his case, but he failed---Agreement was not proved on record.
 
Abdul Ghaffar Khan for Petitioner.
 
Muhammad Jameel Rana for Respondents.
 
Date of hearing: 4th April, 2005.
 
 
JUDGMENT
 
Case 119
 
2006 C L C 876
 
[Lahore]
 
Before Sh. Abdur Rashid, J
 
ANJUM MAHMOOD and 5 others----Petitioners
 
Versus
 
RIZWAN AHMAD and 7 others----Respondents
 
Civil Revision No.1999 of 2004, decided on 23rd February, 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 42---West Pakistan Land Revenue Act (XVII of 1967), S.172---Suit for declaration relating to inheritance mutation---Questions of facts and law---Bar of Civil Court Jurisdiction in terms of S.172 of West Pakistan Land Revenue Act, 1967---Validity---General jurisdiction of Civil Court was not barred rather would be more appropriately attracted in cases involving complicated questions of facts and law and complete transactions.
 
(b) Specific Relief Act (I of 1877)---
 
----S. 42---Civil Procedure Code (V of 1908), O.VII, R.11---Limitation Act (IX of 1908), Arts.120 & 144---Suit for declaration relating to inheritance mutation---Application for rejection of plaint on ground that suit was time-barred, was dismissed---Validity---Land in question was originally inherited by predecessors of plaintiffs---Assertion that inheritance mutation was outcome of fraud, was raised after more than half a century by legal heirs (plaintiffs) of such predecessors who lived long after the said mutation was sanctioned and impugned sale-deed was registered but they never raised any objection during their lifetime---Such assertion, therefore, had little evidentiary value---Long delay of many decades was not only inexplicable but unconscionable also---Contention of plaintiffs that question of limitation did not arise in case of joint possession as co-sharers, had no force as the matter in question was not a case of inheritance simplicitor---Right to sue having accrued to plaintiff's predecessors with regard to impugned mutation 63 years back, had indisputedly expired when predecessors were still alive---Suit should have been brought within 6 years of a cause of action---Plaintiffs were seeking declaration of ownership, claiming possession as consequential relief and also seeking rectification of Record of Rights and it was well-settled that such a suit was covered by Art.120 of Limitation Act, 1908 for which period of limitation was 6 years---Plaintiffs, in a suit for possession, had to show that they had been dispossessed within a period of 6 years prior to the institution of suit---Even under the residuary Art.144 of Limitation Act, 1908 the maximum period prescribed was 12 years---Suit brought more than 6 decades after cause of action was clearly time-barred and trial Court had committed a patent illegality in not rejecting the plaint.
 
Moolchand v. Muhammad Yousaf (Udhamdas) PLD 1994 SC 462; Ali Bahadur v. Nazir Begum PLD 2005 Lah. 218; Muhammad Rafiq v. Muhammad Ali 2004 SCMR 704; Mst. Reshman Bibi v. Amir 2004 SCMR 392; Mst. Saabran Bibi v. Muhammad Ibrahim 2005 CLC 1160; Munir Ahmad v. Muhammad Siddique 2005 MLD 364; Rehman v. Yara 2004 SCMR 1502; Mst. Sharam v. Taj Muhammad 2002 CLC 2001; Nawab Din v. Muhammad Ishaque PLD 2004 (AJ&K) 49 and Muhammad Ali and 25 others v. Hassan Muhammad and 6 others PLD 1994 SC 245 ref.
 
(c) Qanun-e-Shahadat (10 of 1984)---
 
---Art. 114---Specific Relief Act (I of 1877), S.42---Limitation Act (IX of 1908), Art.91---Estoppel---Acquiescence---Plaintiffs in their suit sought declaration that inheritance mutation was result of fraud and admitted that entire suit property had been sold vide sale-deed---Such was essentially a suit for cancellation of registered sale-deed for which period of limitation was three years under Art.91 of Limitation Act, 1908---Where predecessors of plaintiffs, original owner of suit property, who lived for twenty years after the impugned mutation was sanctioned having not taken steps for cancellation of wrong entry in mutation register would be deemed to have acquiesced in such entries---Predecessors had certainly failed on ground of limitation as well as for reason of estoppel---Plaintiffs .claiming under their said predecessors must fail for same reason.
 
(d) Transfer of Property Act (IV of 1872)---
 
----S. 41---Sales by bona fide purchasers during period of interregnum---Validity---Admittedly property in dispute neither was challenged by original owners nor by their legal heirs for a considerable period of time---Such transactions and consequent mutations could not be held nullified as it would be wholly unjust to uproot the successors of bona fide purchaser for valuable consideration on basis of public record.
 
Sharif Ahmad Hashmi v. Chairman Screening Committee, Lahore 1978 SCMR 376 ref.
 
(e) Civil Procedure Code (V of 1908)---
 
---S. 12(2)---Separate suit to challenge validity of a decree on plea of fraud had been barred---Such decrees could be challenged by having recourse to S.12(2), C.P.C.
 
(f) Civil Procedure Code (V of 1908)---
 
---O. I, R.10---Non-joining of necessary parties---Effect---Undeniably all those persons in whom any right, title or interest stood vested were necessary parties in whose absence no effectual decree could be passed---Non-impleadment of beneficiaries of impugned mutation rendered the suit of plaintiffs not entertainable.
 
Muhammad Ghani for Petitioners.
 
Talib Hussain Azad for Respondents.
 
Date of hearing: 31st January, 2006.
 
 
JUDGMENT
 
Case 120
 
2006 C L C 893
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
AHMED BAKHSH alias AHMAD----Petitioner
 
Versus
 
SALABAT KHAN and another----Respondents
 
Civil Revision No.1742 of 2003, heard on 14th February, 2006.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Qanun-e-Shahadat (10 of 1984), Art.79---Suit for specific performance of agreement to sell---Suit dismissed but appeal against dismissal was allowed---Validity---Disputed documents which showed an unexplained and significant gap between end of agreement and signature of defendant had lent credence to the stance taken by defendant that he had signed three blank papers with object to give his land on lease to plaintiffs but plaintiffs utilized said papers for fabricating agreement to sell and two receipts---Marginal witness of document was nephew of Advocate in whose office disputed documents were prepared and he was not a resident of locality where disputed land was located---Said witness had stated his address different from the one he had mentioned on the receipt of agreement which had affected his veracity---Endorsement on agreement simply noted that stamp was to be used for an Iqrarnama without indicating whether it was for sale of land or its lease, also supported the case of defendant---Receipts had not been proved as marginal witness of receipts deposed that amount was not paid in his presence---Contents of agreement revealed that possession of suit property was to be delivered at time of execution of said agreement against receipt of total amount but nothing was on record to explain reason for delivering possession when a substantial part of agreed consideration had yet to be paid---Plaintiffs were unable to explain why a sale-deed had not been obtained by them when they allegedly paid the balance amount mentioned in receipts---Appellate decree being a result of irregularity in exercise of appellate jurisdiction, same was set aside.
 
Khalid Ikram Khatan for Petitioner.
 
Manzoor Hussain Khan for Respondents.
 
Date of hearing: 14th February, 2006.
 
 
JUDGMENT
 
Case 121
2006 C L C 899
 
[Lahore]
 
Before Sheikh Azmat Saeed, J
 
MUHAMMAD SHAFI and 3 others----Appellants
 
Versus
 
MUHAMMAD HUSSAIN and another----Respondents
 
Regular Second Appeal No.182 of 1987, decided on 17th February, 2005.
 
(a) Punjab Pre-emption Act (I of 1913)---
 
----Ss. 15 & 21---Right of pre-emption---Pre-emption suit was filed by brothers of vendor as his son did not opt to pre-empt the sale---Trial Court and Appellate Court concurrently decreed the suit and dismissed the appeal respectively---Plea raised by vendees was that as pre-emptors could not inherit from vendor, therefore, they did not have right of pre emption---Validity---Superior right of pre-emption in terms of S.15 of Punjab Pre-emption Act, 1913, was to be determined in order of succession between the contesting parties---If there was a successor who was higher in order of succession but did not pre-empt the sale, status of such person was irrelevant and did not debar or exclude any other person from agitating his right of pre-emption even if he was lower in the order of succession---Both the Courts below had rightly decided the matter in favour of pre-emptors in circumstances.
 
(b) Punjab Pre-emption Act (I of 1913)---
 
----S. 15---`Order of succession'---Connotation---Term `order of succession' under S.15 of Punjab Pre-emption Act, 1913 means an order under which persons inter se would be entitled to inherit and if a person nearer in order of succession does not seek to, pre-empt the sale, the person next in order of succession is entitled to do so if such person has superior right of pre-emption as opposed to an utter stranger.
 
Jalal Din v. Saeed Ahmed and others PLD 1979 SC 879 and Muhammad and another v. Muhammad Yar and another PLD 1986 SC 231 rel.
 
(c) Punjab Pre-emption Act (I of 1913)---
 
----S.21---Qanun-e-Shahadat (10 of 1984), Art.114---Pre-emption suit---Maintainability---Principle of estoppel---Applicability---Mere presence of a party at the time of transaction subsequently pre-empted by him does not bar the suit under Punjab Pre-emption Act, 1913.
 
Jam Pari v. Muhammad Abdullah 1992 SCMR 786 rel.
 
Muhammad Anwar Bhaur for Appellants.
 
Malik Noor Muhammad Awan for Respondents.
 
 
ORDER
 
Case 122
 
2006 C L C 907
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
MUHAMMAD and 19 others----Petitioners
 
Versus
 
MUHAMMAD HAYAT and 8 others----Respondents
 
Civil Revision No.767 of 2001, heard on 25th October, 2005.
 
(a) West Pakistan Land Revenue Act (XVII of 1967)---
 
---S. 42---Civil Procedure Code (V of 1908), S. 9---Mutation---Consolidation proceedings were challenged on dispute related to title---Jurisdiction---Validity---Civil Court alone had jurisdiction to adjudicate the matter related to title---Appellate Court wrongly observed that matter to challenge consolidation proceedings could only be adjudicated by a Revenue Court.
 
(b) West Pakistan Land Revenue Act (XVII of 1967)---
 
---S. 42---Limitation Act (IX of 1908), Art.120---Specific Relief Act (I of 1877), S.42---Mutation---Decree of entitlement---Non-reflection in Revenue Record---Legal effect of inaccurate mutation on title to property---Decree which determined entitlement of a party would be legally operative whether the same was reflected in Revenue Record or not---Revenue Record would not create or extinguish title, it was merely meant to reflect title which otherwise had been acquired by a person---Any inaccuracy in Revenue Record would not, by itself affect the title of owner---Entitlement of plaintiffs to suit-land was admitted, Appellate Court, therefore, proceeded on wrong premise that plaintiffs head not challenged the inaccurate mutation within time prescribed by Art.120 of Limitation Act, 1908---Appellate decree being unsustainable was set aside and that of Trial Court stood restored.
 
Muzamil Akhtar Shabbir for Petitioners.
 
Mian M. Ashraf Tanveer for Respondents.
 
Date of hearing: 25th October, 2005.
 
 
JUDGMENT
 
Case 123
 
2006 C L C 913
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Mst. ZEENAT BIBI----Petitioner
 
Versus
 
BASHIR AHMAD and. another-Respondents
 
Civil Revision No.571 of 2001, heard on 8th February, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Declaration of title---Proof of ownership---Suit property was stated to be owned by grandfather of plaintiff who being daughter of brother of defendants, claimed 1/8th share in that property---Defendants denied ownership of their father and claimed the' same to be owned by one of the contesting defendants---Trial Court decreed the suit in favour of plaintiff---Contesting defendant filed appeal which was allowed by Appellate Court on the ground that plaintiff failed to prove ownership of her grandfather through any document---Validity---Being refugee from Jammu and Kashmir, grandfather of plaintiff did not have any document of title in respect of the suit property and the defendants also did not have any title document---Title of grandfather of plaintiff and after his death of his sons was based on their occupation and possessory interest in the suit property---Contesting 'defendant stated in his evidence that brothers, rather he himself alone, was entitled to the property in dispute---Validity---Judgment and decree passed by Appellate Court in circumstances, was not valid and was set aside and that of the Trial Court was restored.
 
Muhammad Nawaz Sulehria for Petitioner.
 
Muhammad Saleem Chichi for Respondents.
 
Date of hearing: 8th February, 2005.
 
 
JUDGMENT
 
Case 124
 
2006 C L C 917
 
[Lahore]
 
Before Muhammad Sayeed Akhtar and Sheikh Azmat Saeed, JJ
 
Mst. SHAMIM AKHTAR and 16 others----Appellants
 
Versus
 
Mst. KANIZ FATIMA and 73 others----Respondents
 
Regular First Appeal No.152 of 2001, decided on 30th May, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 8---Suit for possession---Ex parte proceedings against defendant---Plaintiff produced in evidence copies of Jamabandies, Khasra Girdawari and report of Local Commission appointed by Court---One plaintiff's witness categorically stated that defendant had encroached upon the suit land---Trial Court dismissed suit on the ground that plaintiff had not produced cogent evidence to show encroachment upon suit-land by defendant---Validity---Impugned judgment was sketchy, wherein such evidence had not been considered or discussed---High Court accepted appeal, set aside impugned judgment/decree and remanded case to Trial Court for its decision afresh after taking into consideration entire evidence on record.
 
Mirza Hafeez-ur-Rehman for Appellant.
 
 
ORDER
 
Case 125
2006 C L C 924
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
GHULAM YASIN----Petitioner
 
Versus
 
ABDUL KARIM----Respondent
 
Civil Revision No.1238 of 2001, heard on 24th March, 2005.
 
Punjab Pre-emption Act (IX of 1991)---
 
----Ss. 6 & 13---Suit for pre-emption---Making of Talbs---Trial Court found that Talb-i-Ishhad had not been proved by plaintiff because neither the scribe of said notice nor two witnesses were questioned with reference to the notice---Trial Court was fully justified in concluding that plaintiff had failed to prove requirements of S.13 of Punjab Pre-emption Act, 1991 in respect of Talb-i-Ishhad---Appellate Court below which had reversed finding of Trial Court, had not adverted to material aspect of the case---Reasoning of Trial Court, had been ignored entirely in appellate judgment and decree---Said judgment and decree of Appellate Court below being result of illegal exercise of jurisdiction were set aside and judgment and decree of Trial Court stood restored.
 
Qazi Khurshid Alam for Petitioner.
 
Malik Ijaz Hussain Gorecha for Respondent.
 
Date of hearing: 24th March, 2005.
 
 
JUDGMENT
 
Case 126
2006 C L C 926
 
[Lahore]
 
Before Nazir Ahmad Siddiqui, J
 
BABU DIN----Petitioner
 
Versus
 
CIVIL JUDGE/RENT CONTROLLER, MULTAN and 6 others----Respondents
 
Writ Petition No.2088 of 2005, decided on 12th May, 2005.
 
West Pakistan Urban Rent Restriction Ordinance (VI of 1959)---
 
----Ss. 2(c)(i), 13 & 13(6)---Constitution of Pakistan (1973), Art. 199---Constitutional petition---Ejectment application---Relationship of landlord and tenant---Determination of---Tentative rent order---Petitioner had denied relationship of landlord and tenant between the parties---Rent Controller, however had passed tentative rent order directing petitioner to deposit arrears of rent---Relationship of landlord and tenant, being yet to be determined, impugned order directing petitioner to deposit rent, suffered from material irregularity/illegality and jurisdictional defect---Said order was declared to be without lawful authority and of no legal effect by High Court in exercise of constitutional jurisdiction.
Sarwar Khalil Samdani for Petitioner.
 
Ch. Khalil Asghar Sindhu for Respondent No.2.
 
 
ORDER
 
Case 127
 
2006 C L C 927
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
RIAZ AHMAD BUTT and 6 others----Petitioners
 
Versus
 
PROVINCE OF PUNJAB through Collector, Sheikhupura and another----Respondents
 
Civil Revision No.755 of 2000, heard on 1st November, 2005.
 
West Pakistan Land Revenue Act (XVII of 1967)---
 
----S. 42---Specific Relief Act (I of 1877), S.42---Mutation---Legal effect of mutation on title to property---Mutation would not create rights of title in respect of property, it was, at best, a record of some title which allegedly had been acquired by defendants through notification--Defendants were to prove the manner in which title came to vest in them---Neither notification of acquisition of land in question by the Provincial Government was produced nor the only witness examined by the Provincial Government had asserted the right of Province on the basis of acquisition---Plaintiffs had fully established their title in suit-land by sale-deed and through their continuous possession over suit-land whereas Provincial Government had failed to prove its claim---Courts below proceeded on conjectural premise and fell in error by non-suiting the plaintiffs simply on ground of mutation---Impugned decrees were, therefore, set aside and suit of plaintiffs was decreed by High Court.
 
M.A. Zafar for Petitioners.
 
Muhammad Nawaz Bajwa, A.A.-G. with Ch. Muhammad Azam for Respondents.
 
Date of hearing: 1st November, 2005.
 
 
JUDGMENT
 
Case 128
2006 C L C 929
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
NABI BAKHSH KHAN GHAURI and 11 others----Appellants
 
Versus
 
Mst. SAKINA BEGUM----Respondent
 
Regular Second Appeal No.552 of 1978, heard on 5th July, 2005.
 
(a) Qanun-e-Shahadat (10 of 1984)---
 
--Arts. 117 & 120---Gift---Onus to prove---Principles---Onus lies upon donee to prove a valid gift in his favour by donor.
 
(b) Specific Relief Act (I of 1877)---
 
----S. 39---Civil Procedure Code (V of 1908), S.115---Document cancellation of---Pardahnashin and illiterate lady---Donor was an illiterate and Pardahnashin lady who denied execution of any gift deed in favour of donees and sought cancellation of gift deed---Trial Court dismissed the suit but Appellate Court allowed the appeal and decreed the suit on the ground that the donees failed to prove execution of valid gift in their favour---Validity---No relative of the donor lady was present when the gift was stated to have been executed---Donor did not have independent advice and was old Pardahnashin lady and simpleton who had not given the suit house to donees---Appellate Court had correctly followed the dictum laid down by the superior Courts---No ground was made out for interference in the judgment and decree passed by Appellate Court---Revision was dismissed in circumstances.
 
Muhammad Nazir v. Khurshid Begum 2005 SCMR 941; Baja and 8 others v. Mst. Bakhan and 3 others 2004 YLR 3047; Muhammad Rasheed v. Mst. Saleema Bibi 2004 CLC 1026 and Suleman Khan v. Makhmal Jan and another PLD 1974 AJ&K 106 rel.
 
Sarfraz Ahmad Zia for Appellants.
 
Sahibzada Mehboob Ali Khan for Respondent.
 
Date of hearing: 5th July, 2005.
 
 
JUDGMENT
 
Case 129
2006 C L C 933
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Mst. ALLAH RAKHI and 26 others----Petitioners
 
Versus
 
ASHIQ HUSSAIN and 5 others----Respondents
 
Civil Revision No.925 of 2001, heard on 15th February, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Suit for declaration---Plaintiffs had claimed in their suit that they were owners in possession of suit-land which was part of Shamlat Deh and appeared in Jamabandi for the years 1915-1916---Defendants resisted suit contending that they were owners of suit-land by judgment of Tehsildar and decree of Civil Court---Jamabandi for the years 1915-1916 showed that predecessor-in-interest of plaintiffs was in cultivating possession of suit-land, whereas predecessor-in-interest of defendants was in cultivating possession of different Khasra Number---Suit was concurrently dismissed by Courts below---Conclusion of Courts below was quite contrary to relevant Jamabandi and constituted misreading of said document---In view of said misreading of evidence and unjustified reliance, it was clear that Courts below had misdirected themselves and had .exercised their jurisdiction with material irregularities---Impugned decrees of Courts were set aside and on basis of available evidence, plaintiffs were declared to be owners in possession of suit-land.
 
Ch. Manzoor Hussain Basra for Petitioners.
 
Zafar Iqbal Chaudhry for Respondents.
 
Date of hearing: 15th February, 2005.
 
 
JUDGMENT
 
Case 130
 
2006 C L C 935
 
[Lahore]
 
Before Parvez Ahmad, J
 
Mst. ALLAH RAKHI and 14 others----Petitioners
 
Versus
 
MUHAMMAD SIAN and 4 others----Respondents
 
Civil Revision No.1137 of 2002, heard on 6th January, 2003.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Transfer of Property Act (IV of 1882), Ss.122 & 123---Suit for declaration---Execution of gift---Claim of plaintiff was that she was owner of suit property and was in possession of property as a co-sharer along with defendants who were her brothers and defendants being in cultivation possession, had been making payment of share of produce to her till 1977 and later on they refused to make payment of share of produce to her---Defendants had alleged that suit property stood gifted in their favour---Plaintiff had totally denied making of any gift in favour of defendants and insisted that she was owner and was in possession of property in dispute as a co-sharer---Trial Court dismissed suit on the ground that it was barred by time, but Appellate Court below set aside judgment and decree of Trial Court and decreed suit of plaintiff--Defendants could not produce in evidence any person who had attested mutation of alleged gift in their favour, whereas plaintiff, apart from herself, produced two independent witnesses, who in very clear terms, had stated that defendants had been paying share of produce of land to her and thereafter they stopped making payment of share of produce to plaintiff---Plaintiff had clearly submitted that she along with defendants/her brothers was owner of property in dispute and that defendants had throughout been making payment of share of produce to her---Defendants could not prove execution of gift of suit property in their favour by whatever evidence-Judgment and decree passed by Appellate Court was in consonance with law---In absence of any misreading, non-reading, illegality, jurisdictional defect and material irregularity, judgment and decree of Appellate Court could not be interfered with by High Court in exercise of its revisional jurisdiction.
 
Ch. Bashir Ahmad for Petitioners.
 
Ch. Muhammad Abdullah for Respondents Nos.1 and 2.
 
Siddique Ahmad Ch. for Respondents Nos.3 to 5.
 
Date of hearing: 6th January, 2003.
 
 
JUDGMENT
 
Case 131
 
2006 C L C 939
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Hafiz MUHAMMAD ISHFAQ----Petitioner
 
Versus
 
Hakeem SAEED AHMAD and 17 others----Respondents
 
Civil Revision No.946 of 2001, heard on 18th October, 2005.
 
Civil Procedure Code (V of 1908)---
 
---O. XXXIX, Rr.1, 2 and O.XXVI, Rr.9, 10, 16 & S.75(b)---Qanun-e-Shahadat (10 of 1984), Art.117---Specific Relief Act (I of 1877), Ss.42, 52, 53 & 55---Encroachment---Suit for permanent and mandatory injunction---Appointment for Local Commission for demarcating land in dispute---Suit was decreed on the report of Local Commission and decree was affirmed in appeal---Report of Local Commission on record wherein some error in demarcating Khasra was pointed out with suggestion that if such error was rectified, the defendant's encroachment would have been established, clearly showed that Local Commission had travelled beyond the matter referred to him---Local Commission was not supposed to suggest rectification of Revenue Record because this was not disputed between the parties---Parties had based their respective pleas on basis of existed record and, therefore, the encroachment, if any, also had to be determined on the basis of current record---Plaintiff was supposed to prove that defendant had made an encroachment on his property but he failed to prove his case---Concurrent decree having been based on unwarranted observation of Local Commission, was not sustainable, therefore, was set aside by High Court.
 
Shaukat Hussain Khan Baloch for Petitioner.
 
M. Baleegh-uz-Zaman Ch. for Respondents.
 
Date of hearing: 18th October, 2005.
 
 
JUDGMENT
 
Case 132
 
2006 C L C 942
 
[Lahore]
 
Before Syed Zahid Hussain and Syed Sakhi Hussain Bukhari, JJ
 
Sheikh ABDUL RAZZAQ----Appellant
 
Versus
 
UMER KHAN----Respondent
 
Regular First Appeal No.278 of 2000, heard on 15th February, 2005.
 
Civil Procedure Code (V of 1908)---
 
--- O. XXXVII, Rr. 2 & 3---Suit for recovery of amount on basis of promissory note---Promissory note bore stamps and it had signatures as well as thumb-impression of defendant and was witnessed by two persons who had been produced and examined as witnesses by plaintiff and plaintiff had himself appeared as a witness-Taking of loan and execution of promissory note by defendant having fully been established, Trial Court had rightly decreed the suit---Original loan was Rs.2,00,000, but promissory note was showing Rs.2,20,000 in which amount of Rs.20,000, as profit was included, which was not justified---Decree, however, was modified by the High Court and amount was reduced to original loan/Rs.2,00,000 (two lacs) instead of Rs. two lacs and twenty thousands.
 
Mian Maqsood Ahmad for Appellant.
 
Zafar Ali Raja for Respondent.
 
Date of hearing: 15th February, 2005.
 
 
JUDGMENT
 
Case 133
 
2006 C L C 944
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Chaudhry ALLAH RAKHA and 3 others----Petitioners
 
Versus
 
NOOR DIN and others----Respondents
 
Civil Revision No.74 of 2002, heard on 17th January, 2006.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Civil Procedure Code (V. of 1908), O.XIV, R.5, O.XXII, R.4(4) & O.XLI, R.25---Qanun-e-Shahadat (10 of 1984), Arts.117 & 118---Suit for declaration to the effect that decree obtained by defendants was fraudulent and inoperative against the rights of plaintiff---Framing of an additional issue at appellate stage---Validity---Defendants could not assert any prejudice on framing an additional issue at appellate stage in view of judgment passed in civil revision whereby Appellate Court was directed to decide additional issue relating to the genuineness of power of attorney allegedly executed by plaintiff in favour of defendants---Defendants were unable to deny that said additional issue encapsulated the factual controversy between parties---After the testimony of plaintiffs, who denied the execution of any power of attorney onus of proving the issue shifted upon defendants but neither they summoned the alleged attorney as witness through Court nor did they avail any such independent means as comparison of handwriting/thumb-impression through which they could have proved alleged power of attorney---Appellate Court rightly noted that there was no necessity to substitute legal representatives of such defendants who had been proceeded against ex parte---Courts below were justified in granting the decree for possession to plaintiffs after conclusion that there was no decree in favour of defendants and no title vested in them whereunder defendants could have conveyed the suit property to the vendee---Vendee, who derived title from such defendants during pendency of lis could not have asserted any 'right to suit property better than that asserted by defendants---Concurrent decrees were upheld subject to the modification that suit to the extent of one of the plaintiffs whose legal representatives had compromised .the matter with defendants, was dismissed.
 
Khushi Muhammad v. Mst. Aziz Bibi PLD 1988 SC 259 ref.
 
Mushtaq Mehdi Akhtar for Petitioners.
 
Syed Raza Hussain Naqvi for Respondents.
 
Date of hearing: 17th January, 2006.
 
 
JUDGMENT
 
Case 134
2006 C L C 948
 
[Lahore]
 
Before Fazal-e-Miran Chauhan, J
 
MUHAMMAD MUSHTAQ and another----Petitioners
 
Versus
 
MUHAMMAD JEHANGIR----Respondent
 
Civil Revision No.2865 of 2004, decided on 20th December, 2004.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Suit for specific performance of agreement---Plaintiff claimed that he had entered into an agreement to sell suit property with defendant who was father of minor, for consideration---Plaintiff had further claimed that he had paid earnest money and agreement was to be executed by mother of minor with his consent---On serving legal notice by, plaintiff, defendant informed plaintiff that mother of minor being not ready to execute sale-deed in favour of plaintiff, plaintiff could take back earnest money paid by him---Plaintiff, instead of receiving earnest money, filed suit for specific performance of agreement , which was dismissed by Trial Court, but was decreed by Appellate Court---Validity---Plaintiff knowingly that defendant (father) was not authorized to act on behalf of minor son, had acted mala fide to usurp property of the minor---Conduct of plaintiff who had not acted bona fide was dubious---Plaintiff was not entitled to receive double of earnest money paid by him to defendant, but was entitled to receive what he had actually paid to him.
 
Haji Dildar Khan for Petitioners.
 
 
ORDER
 Case 135
 
2006 C L C 951
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
FALAK SHER through L.Rs. and 11 others----Petitioners
 
Versus
 
Mst. FIRDOUS AKHTAR and 4 others----Respondents
 
Civil Revision No.696 of 2000, heard on 29th November, 2005.
 
(a) Specific Relief Act (I of 1877)---
 
----Ss. 12, 42, 52 & 53---Limitation Act (IX of 1908), S.5---Suit for declaration and injunction with specific performance of agreement of sale---Suit was deceased but decree was set aside in appeal---Question of title---Limitation---Title in land vested in the Province and the Province through revenue functionaries had decided to abide by any decision, which might be rendered by civil Court---Suit of plaintiffs which was filed within two months of said order, was within time.
 
(b) Specific Relief Act (I of 1877)---
 
---Ss. 12, 42, 52 & 53---Qanun-e-Shahadat (10 of 1984), Art.59---Agreement to sell---Proof---Affidavit sworn by promisor/predecessor-in- interest of defendants, attested by two witnesses along with application moved by promisor to the Development Authority for permission to transfer the land to the plaintiffs had proved the case of plaintiffs---In earlier declaratory suit filed by present defendants and which was withdrawn when the suit was mature for decision, plaintiffs had produced witnesses who confirmed the attestation of documents in question---One of the witnesses, in the present suit, could not be produced because he had died but his statement in earlier suit had conclusively proved the sale transaction---Lamaberdar, who in the earlier suit had identified the promisor/predecessor-in-interest of defendants before the Naib Tehsildar, in the present suit, was declared hostile by Court, however, his signatures were proved through the statement of Handwriting Expert, and his denial of signatures on affidavit was, held, incredible---Promisor, who was employee of Board of Revenue and was well-versed with transactions relating to land could not explain as to why he signed any blank paper on the asking of a person who featured nowhere in the litigation---Sale transaction by predecessor-in-interest of defendants/promisor in favour of plaintiffs was duly proved and one of the legal representatives of promisor had acknowledged that the sale had been made by the promisor---Appellate decree being the result of illegality in the exercise of jurisdiction by Appellate Court was not sustainable which was set aside and the decree of Trial Court was upheld and affirmed.
 
Muhammad Farooq Qureshi Chishti for Petitioners.
 
Zia Ullah Khan Niazi for the Remaining Respondents.
 
Malik Muhammad Azam Awan for Respondent No.4.
 
Date of hearing: 29th November, 2005.
 
 
JUDGMENT
 
Case 136
 
2006 C L C 955
 
[Lahore]
 
Before Ali Nawaz Chowhan, J
 
MUHAMMAD SAIFULLAH KHAN and others----Petitioners
 
Versus
 
GULLU and others----Respondents
 
Civil Revision No.845 of 1994, heard on 16th February, 2006.
 
Specific Relief Act (I of 1877)---
 
----S. 42---West Pakistan Land Reforms Regulation, 1959 [Martial Law Regulation No.64], para. No.22---Civil Procedure Code (V of 1908), O.XLI, R.31---Declaration of title---Adna Malkiat, claim of---Failure to give issue-wise finding---Effect---Plaintiffs assailed disputed mutations attested in favour of defendants, on the ground that they were Adna Malikan and had become owner of suit-land due to operation of para. No.22 of Land Reforms Regulation, 1959---Trial Court dismissed their suit as the plaintiffs had failed to establish themselves as Adna Malikan---Appellate Court without giving any findings on the main issue set aside the judgment and decree passed by Trial Court---Validity---Appellate Court in appeal did not dilate upon the main issue as it should have done as it seemed to be impressed by the fact that disputed mutations had been declared to be illegal, therefore, even if the defendants claimed themselves to be Ala Malik, they had no right left, which was an erroneous conclusion as disputed mutations were not declared illegal---Appellate Court ought to have decided the status of plaintiffs and defendants while giving its views whether it was upholding the findings of Trial Court or not and in case, Appellate Court was not agreeing with the views of Trial Court, the basis of such disagreement should have been given---Since present was a peculiar case pertaining to the rights bestowed by law Appellate Court ought to have given reasons for not agreeing with Trial Court, instead of merely stating that he was upsetting the finding on the main issue---High Court in exercise of revisional jurisdiction, set aside the judgment and decree and the case was remanded to Appellate Court for decision afresh---High Court directed the Appellate Court to follow the principle as laid down by High Court in case titled Ghulam Haider v. Ghulam Raza Shah and 12 'others, reported as PLD 1979, Lah. 481---Revision was allowed accordingly.
 
Ghulam Haider v. Ghulam Raza Shah PLD 1979 Lah. 481 ref.
 
Malik Allah Wasaya for Petitioners.
 
Gohar Razzaq Awan for Respondents.
 
Date of hearing: 16th February, 2006.
 
 
JUDGMENT
 
Case 137
 
2006 C L C 965
 
[Lahore]
 
Before Muhammad Sair Ali, J
 
MUHAMMAD NAWAZ----Appellant
 
Versus
 
MUHAMMAD ASIM and another----Respondents
 
Regular Second Appeal No.77 of 2004, decided on 16th December, 2004.
 
Punjab Pre-emption Act (IX of 1991)---
 
----Ss. 6 & 13---Suit for pre-emption---Making of Talbs---Courts below through concurrent findings, had arrived at the conclusion that plaintiff, despite having knowledge through registered sale-deed of suit property, had failed to make timely `Talbs' in accordance with S.13 of Pre-emption Act, 1991---Courts below through due, proper and threadbare analysis of oral and documentary evidence, had recorded that plaintiff's story of knowledge after about four months of registration of sale-deed, was not only unbelievable, but also totally false---Courts below also came to the conclusion that construction over the suit property was raised immediately after registration of sale-deed and disbelieved plaintiff that he had no knowledge of construction made on suit-land which adjoined that of plaintiff who took about four months to claim knowledge of transaction in question---In absence of any misreading or non-reading of evidence, no justification was found to interfere in concurrent findings of fact recorded by Court below.
 
Ch. Muhammad Bashir Goraya, Advocate.
 
ORDER
 
Case 138
 2006 C L C 967
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Hafiz KHAN MUHAMMAD----Petitioner
 
Versus
 
MUHAMMAD AZIZ and another----Respondents
 
Civil Revision No.1724 of 2005, heard on 24th November, 2005.
 
Specific Relief Act (I of 1877)---
 
----Ss. 9 & 42---Civil Procedure Code (V of 1908), O.II, R.2---Plaintiff, without the withdrawal of earlier suit for declaration, filed suit for possession---Consolidation of suits---Dismissal of suits---First suit was decreed in appeal but dismissal of second suit was upheld on technical ground that second suit was barred under O.II, R.2, C.P.C.---Validity---Second suit, for good order's sake and in order to ensure consistency with the provisions of C.P.C. was treated as an application for seeking amendment of plaint in earlier suit with the object of incorporating therein the prayer of possession---After declaring plaintiff as the owner of suit property Appellate Court proceeded on wrong premises by holding that second suit was barred under O.II, R.2, C.P.C.---Appellate decree in the second suit was thus set aside by High Court.
 
Shaikh Naveed Shaharyar for Petitioner.
 
Respondents proceeded against ex parte.
 
Date of hearing: 24th November, 2005.
 
JUDGMENT
 
Case 139
 
2006 C L C 970
 
[Lahore]
 
Before Syed Zahid Hussain and Syed Sakhi Hussain Bokhari, JJ
 
EXECUTIVE ENGINEER, HIGHWAY DEPARTMENT LAHORE and 3 others----Appellants
 
Versus
 
MEHRAJ BEGUM and others----Respondents
 
R.F.A. No.215 of 1999 and R.F.A. No.86 of 2005, heard on 8th March, 2005.
 
(a) Land Acquisition Act (I of 1894)---
 
----Ss. 4 & 23---Acquisition of land---Determination of compensation---Matters to be considered---While determining amount of compensation of acquired land instances of sale of adjacent lands, made shortly before and after notification, were to be taken into consideration; an area could be Banjar Qadeem or Barrani, but its market value could be tremendously high because of its location, neighbourhood, potentiality or other benefits; consideration should be had to all the advantages, present or future, which land possessed in hands of owners; in determining the quantum of fair compensation, the main criterion was the price which a buyer would pay to a seller for the property, if they voluntarily entered into the transaction and only the "past sales" should not be taken into account, but value of land with all its potentialities should also be determined by examining local property dealers or other persons who were likely to know the price that the property in question was likely to fetch in open market---Adoption of such criteria could furnish a just basis for fair determination of compensation---Formula of past sales in the area and average price could not be made as the sole basis.
 
Province of Punjab through Collector, Attock v. Engineer Jamil Ahmad Malik and others 2000 SCMR 870 ref.
 
(b) Land Acquisition Act (I of 1894)---
 
---Ss. 4, 11, 18, 23 & 54---Acquisition of land---Determination of compensation---Reference to Referee Court---Acquired land was of much higher value as it had characteristics of urbanization due to its location and commercial utility---Value of land in vicinity was Rs.10,000 to Rs.15,000 per Marla---Landowners, in circumstances could not be deprived of fair compensation of their land which was being acquired from them compulsorily---All said aspects were not kept in view by Referee Court---Neither compensation as claimed by landowners (Rs.50,000 per Marla) was reasonable nor value (Rs.4,000 per Marla) as given in the award---Even determination made by Referee Court (Rs.8,796 per Marla) was not just and fair---Assessment made by Collector (Rs.10,000 per Marla) should have been allowed to the landowners.
 
Fawad Malik, Asstt. A.-G. for Appellants.
 
Taki Ahmad Khan, and Wali Muhammad Ch. for Respondents.
 
Date of hearing: 8th March, 2005.
 
JUDGMENT
 
Case 140
2006 C L C 973
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
MUHAMMAD YAQUB----Petitioner
 
Versus
 
Mirza SHAHID MAHMOOD----Respondent
 
Civil Revision No.1741 of 2001, heard on 8th March, 2005.
 
Specific Relief Act (1 of 1877)---
 
----S. 8---Suit for possession of roof of shops---Plaintiff had claimed possession of roof of two shops which were conveyed to him through sale-deed executed in his favour by the Reader of the Court in execution of a decree for specific performance---Defence set up by defendant was that he was a tenant in the adjacent property for many years and thereafter had purchased same---Defendant, however, had conceded in his testimony that the roof on top of shops purchased by plaintiff was not included in conveyance in his favour---Defendant had acquired title subsequent to conveyance in favour of plaintiff---Evidence on record had shown that title which was conveyed to plaintiff, included the roof top claimed by plaintiff---Trial Court decreed suit for possession of plaintiff, but Appellate Court while dismissing suit of plaintiff neither had taken into consideration circumstances of case nor had addressed reasoning of Trial Court---Appellate Court having exercised its jurisdiction with material irregularity and ignoring material aspects of the case, appellate judgment and decree, legally were not maintainable and were set aside and decree passed by Trial Court stood restored.
 
S.M. Masood for Petitioner.
 
Nemo for Respondent: Ex parte.
 
Date of hearing: 8th March, 2005.
 
JUDGMENT
 
Case 141
 
2006 C L C 976
 
[Lahore]
 
Before Sheikh Azmat Saeed, J
 
MUHAMMAD AKBAR----Petitioner
 
Versus
 
SECRETARY HOUSING, URBAN DEVELOPMENT AND PUBLIC HEATH ENGINEERING DEPARTMENT (HUD AND PHED) GOVERNMENT OF THE PUNJAB----Respondent
 
Writ Petition No.18073 of 2004 and C.M. No.534 of 2005, decided on 28th March, 2005.
 
Constitution of Pakistan (1973)---
 
----Arts. 18 & 199---Constitutional petition---Freedom of trade---Suspension of registration of firm---Petitioner had not at all been found to have indulged in "corrupt or fraudulent practices" and basic disqualification specified for annulment of petitioner's registration was palpably lacking in the case---Petitioner had been penalized unilaterally on erroneous assumption and in violation of Art.18 of the Constitution, that had safeguarded freedom of trade, business and profession---Case, in circumstances, was fit one for interference by High Court in exercise of its Constitutional jurisdiction---High Court accepting Constitutional petition, set aside impugned suspension letter, declaring the same to have been issued without any lawful justification and legal effect.
 
Muhammad Arif Saeed and Faisal Islam for Petitioner.
 
Ali Zafar for Applicant (in C.M. No.534 of 2005).
 
M. Sohail Dar. A.A.-G.
 
ORDER
 


Case 142
 
2006 C L C 978
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
ABDUS SAMI BUTT----Petitioner
 
Versus
 
DEPUTY COMMISSIONER/COLLECTOR, LAHORE and another----Respondents
 
Civil Revision No.743-D of 1997, heard on 1st March, 2005.
 
Land Reforms Act (II of 1977)---------
 
------S. 16(2)-Land Reforms Regulation, 1972 [M.L.R.115], para.13---Specific Relief Act (I of 1877), S. 42---Transfer of Property Act (IV of 1882), S.41---Cancellation of grant of land---Suit for declaration---Suit land which was resumed under Martial Law Regulation No.115 from its original owner was granted to a person under Land Reforms Act, 1977---Grantee of land sold the same to another person and finally it was purchased by the petitioner by means of a registered sale-deed and mutation of said sale was also sanctioned in his favour---Subsequently Deputy Commissioner and then Additional Commissioner cancelled said grant from the name of original grantee without affording opportunity of hearing to petitioner/vendee---Section 16(2) of Land Reforms Act, 1977, did not in any manner, dispense with provisions of natural justice where grantee had actually transferred land to bona fide purchaser for value---Appellate Court, in circumstances had misdirected itself and exercised its jurisdiction illegally by holding that it was not necessary to give a notice to petitioner/vendee from original grantee before resuming land---Land Commission and Board of Revenue, were responsible for ensuring that restrictive covenants, if any, attaching to grant of land under Land Reforms Act, 1977, were duly noted in Revenue Record, but that was not done in the present case---Successive transferees of land, in circumstances could not have had any notice of restrictions imposed on grant made in favour of grantee/vendor---Authorities, in circumstances, were themselves responsible for creating circumstances which would mislead a bona fide purchaser/petitioner---Authorities therefore, were estopped from resuming land---Last vendor of land in dispute was quite clearly ostensible owner of said land and mutation did not include any indication that land was granted to grantee subject to restrictive covenants and could not be sold---Four essential ingredients of S.41 of Transfer of Property Act, 1882, stood fulfilled in the case---Courts below having acted illegally in exercise of their jurisdiction, their judgments and decrees, legally were not maintainable and were set aside---Petitioner having produced sufficient evidence on record to prove his case, was entitled to declaratory decree prayed for by him; his suit was decreed as prayed for.
 
Mian Nisar Ahmad for Petitioner.
 
Kh. Muhammad Saeed for Respondents.
 
Date of hearing: 1st March, 2005.
 
JUDGMENT
 
Case 143
2006 C L C 982
 
[Lahore]
 
Before Mian Hamid Farooq, J
 
Prof. (R) Dr. MUHAMMAD JAMIL BHUTTA----Petitioner
 
Versus
 
ABDULLAH FAROOQ----Respondent
 
Civil Revision No.2344 of 2005, decided on 21st February, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. XXXVII, R.3(2)---Suit for recovery of money---Conditional leave to appear and defend suit---Legality---Plea of defendant was that he was entitled to unconditional leave to appear and defend the suit and a conditional leave granted to him by the Trial Court was not sustainable under the law---Validity---Under O.XXXVII, R.3(2), C.P.C. discretion had been conferred upon a Court to grant leave to defend the suit, either unconditionally or subject to such terms as to payment into Court or giving security---Trial Court, in exercise of its discretionary powers, had tagged the condition for the defendant of submitting bank security with leave to appear and defend the suit, and the same could not be termed as illegal---Defendant having failed to furnish the requisite bank guarantee, Trial Court was justified in closing defendant's right to appear and defend the suit.
 
Mian Rafique Saigal and another v. Bank of Credit and Commerce International (Overseas) Ltd. and another PLD 1996 SC 749; Zubair Ahmad and another v. Shahid Mirza and 2 others 2004 MLD 1010; Niaz Ahmad and 2 others v. Habib Bank Ltd. and others 1991 SCMR 75; Messrs Ark Industrial Management Ltd. v. Messrs Habib Bank Limited PLD 1991 SC 976 and Shahzada Muhammad Umar Beg v. Sultan Mahmood Khan and another PLD 1970 SC 139 ref.
 
(b) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 114---Civil Procedure Code (V of 1908), O.XXXVII, R.3(2)---Estoppel---Acquiescence---Application by defendant to appear and defend the suit was granted subject to furnishing bank guarantee---Defendant sought adjournment for filing the bank guarantee which showed his acquiescence over impugned order and subsequently, he was not in position to challenge said conditional order because principle of estoppel operated very harshly against him and he could not be allowed to blow hot and cold in same breath.
 
Irfan Masood Sheikh for Petitioner.
 
Rana Mushtaq Ahmad for Respondent.
 
ORDER
 
Case 144
2006 C L C 987
 
[Lahore]
 
Before Jawwad S. Khawaja, J
 
Mst. ZEENAT KHATOON and 2 others----Petitioners
 
Versus
 
KHALIQDAD KHAN and 4 others----Respondents
 
Civil Revision No.893 of 2005, heard on 20th February, 2006.
 
Islamic Law---
 
----Gift---Validity---Gifts in question were made by father in favour of his four sons excluding the three daughters---Daughters, in their suit for declaration impugned the gift mutations on ground that their father being old and infirm had not made any gift---Suit was decreed but appellate Court reversed the finding disregarding the material fact that one of brothers who was also a beneficiary of gift mutations, had testified the desire of his deceased father to distribute entire land to all children in accordance with Islamic law---Said brother deposed that impugned mutation was entered in his absence and such testimony belied the report appearing in mutation which showed his presence at the time impugned mutation was sanctioned---Concerned Patwari was not produced and report of Patwari did not indicate as to when donor gave intimation of oral gifts to Patwari---Witness of mutation confirmed the old age and infirmity of donor but he showed his lack of knowledge about deprivation of donor's daughters from their share inheritance---Absence of such explanation as to why such brother received less than his other brothers lent credence to contention of daughters that gifts were not recorded in accordance with any declaration made by their father---Appellate decree being result of non-reading and misreading of evidence same was set aside by High Court.
 
Rabnawaz Khan Niazi for Petitioners.
 
Allah Wasaya Malik for Respondents Nos.1 to 3.
 
Hashim Niazi for Respondent No.4.
 
Date of hearing: 20th February, 2006.
 
JUDGMENT
 
Case 145
2006 C L C 994
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
Mst. SURAYIA BEGUM and another----Petitioners
 
Versus
 
Sardar SAEED ULLAH through L.Rs.----Respondents
 
Civil Revision No.368-D of 1984, heard on 27th March, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O. XVII, R.3---Qanun-e-Shahadat (10 of 1984), Art.118---Islamic Law---Faith---Inheritance---Suit regarding inheritance of deceased who, as per plaintiff's claim (his brother) was Sunni, while defendants (his daughters) alleged deceased to be Shia by faith---Onus was on defendants to prove, whether deceased was Shia Muslim by faith---Non-production of evidence by defendants in spite of having availed sufficient opportunities---Trial Court decreed suit---Validity---Presumption in the Sub-Continent was that a Muslim is Sunni, unless proved to the contrary---Trial Court had correctly called upon defendants to prove such issue on merits---In absence of any evidence to rebut such presumption, suit was, correctly decreed.
 
Abdul Shakoor v. Abdul Rasul PLD 1963 (W.P.) Kar. 356 and Aziz Ullah Khan and others v. Gul Muhammad Khan 2000 SCMR 1647 ref.
 
M. Ghazanfar Ali Sheikh for Petitioners.
 
Maqbool Elahi Malik, Ch. Munir Alam and Muhammad Arif Alvi for Respondents.
 
Date of hearing: 27th March, 2006.
 
JUDGMENT
 
Case 146
2006 C L C 999
 
[Lahore]
 
Before Fazal-a-Miran Chauhan, J
 
Rana NISAR AHMAD----Petitioner
 
Versus
 
SHER BAHADUR KHAN and others----Respondents
 
Writ Petition No.113 of 2006, heard on 20th February, 2006.
 
(a) Specific Relief Act (I of 1877)---
 
----S. 11---Civil Procedure Code (V of 1908), O.XXIII, R.3 & S.12(2)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Suit for specific performance of contract of sale---Compromise agreement executed by person having special power of attorney on behalf of the defendant---Order passed by Court on basis of compromise agreement had been characterized as fraudulent on the sole ground that attorney was not given power to compromise the suit---Application under S.12(2), C.P.C. was allowed by revisional Court---Validity---Defendant, in his written statement had specifically denied the execution of agreement and thereafter he had appointed special attorney to appear and defend the suit on his behalf---General words used in the instrument did not confer general power to concede the suit---Disputed special power of attorney, admittedly having been executed by defendant, did not contain authority to compromise the suit---Act of attorney compromising the suit on behalf of defendant and making statement in the Court to that effect was without lawful authority---No jurisdictional defect or illegality, in circumstances, was committed by Appellate Court by accepting the application under S.12(2), C.P.C.
 
(b) Interpretation of document-----
 
--Rule of construction---Power of attorney---Rule of construction of a
document containing special powers followed by general words are to be construed as limited to what is necessary for the proper exercise of special powers and where the authority was given to do a particular act followed by general words the authority was deemed to he restricted to what was necessary for the purpose of doing that particular act---Before an act purported to be done under the powers, it is necessary to show that the authority exercised was within the four corners of the instrument.
 
Ch. Muhammad Iqbal Abid for Petitioner.
 
Sahibzada Mehboob Ali Khan, Ghazanfar Ali Khan and Muhammad Arif Sargana for Respondents.
 
Date of hearing: 20th February, 2006.
 
JUDGMENT
 
Case 147
2006 C L C 1006
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
SALEEM KHAN and 9 others----Petitioners
 
Versus
 
KARIM KHAN----Respondent
 
Civil Revision No.333-D of 2004, heard on 29th March, 2006.
 
(a) Islamic Law---
 
----Gift---Son in acknowledgment of providing auction price of land to father alleged to have been gifted land by father---Other legal heirs claimed to be co-owner of land as gift mutation was void---Proof---Donee in examination-in-chief did not refer to his said plea, but when confronted with the same during cross-examination, he deposed that he was of 14 years age at the time of purchase of land in auction by father, who paid its price in instalments--Donee-son, thus, completely belied his said plea---Gift was void in circumstances.
 
Barkat Ali through Legal Heirs v. Muhammad Ismail through Legal Heirs 2002 SCMR 1938 rel.
 
(b) Islamic law---
 
----Gift of land through mutation---Proof---Remarks column of gift mutation showing its entry on basis of a report, but its number and date was left blank---Such report or its copy was not produced in evidence---Pedigree-table drawn up on gift mutation showing mother of donee to be dead, but donee (son) admitted same to be a false statement---Mutation showing two witnesses to have identified donor, but one of them was stated to be dead, while other witness being Patwari deposed not to know donor personally---Retired Patwari who had compared entries of gift mutation deposed that none of the parties appeared before him---Held, as to declaration of gift by donor or its acceptance by donee or delivery of possession under gift, there was no evidence on record---Gift mutation was set aside in circumstances.
 
Mirza Aziz Akbar Baig for Petitioners.
 
Anwar Mubeen Ansari for Respondent.
 
Date of hearing: 29th March, 2006.
 
JUDGMENT
 
Case 148
2006 C L C 1009
 
[Lahore]
 
Before Sh. Hakim Ali, J
 
MUHAMMAD HUSSAIN and another----Petitioners
 
Versus
 
TAFHEEM-UL-HUDA and another----Respondents
 
Civil Revision No.58-D of 2006/BWP, decided on 6th February, 2006.
 
Islamic Law-
 
--Gift---Proof---Grandfather making gift in favour of minor granddaughter who was residing in the house of grandfather---Burden of proof, was not on the beneficiary but upon the donor to prove the alleged fictitious and forged nature of transaction---In case of father and minor daughter, grandfather qua the minor granddaughter, the intention to make the gift had to play the pivotal role---Delivery of possession had been proved by copy of record of rights---Alienation from donor in favour of his another son of the remaining lands without any objection repelled the contention that ability and capacity of donor was affected by any infirmity of illiteracy and deafness preventive in matter of alienation---Non-production of the Revenue Officer, recorder of impugned gift statement, relevant Patwari and two alleged identifiers of the concerned village had clearly showed that petitioner had failed to disprove the factum of gift---Non-filing of appeal and revision against mutation in revenue hierarchy and against decree passed in favour of vendee/granddaughter, with regard to gift mutation before District Court and in the High Court was also fatal for acceptance of case of donor---Qanun-e-Shahadat (10 of 1984), Arts.117 & 118.
 
Mst. Naseeban and others L.Rs. of Abdullah v. Maqbool Ahmad PLD 1987 Lah. 654 and Samo and 5 others v. The Officer on Special Duty, Federal Land Commission, Rawalpindi and 4 others 1981 CLC 1308 ref.
 
Sardar Muhammad Hussain Khan for Petitioners.
 
ORDER
 
Case 149
2006 C L C 1015
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
JAN MUHAMMAD through L.Rs. and others----Appellants
 
Versus
 
NOOR MUHAMMAD through L.Rs. and others----Respondents
 
Regular Second Appeal No.40 of 1972, heard on 4th April, 2006.
 
Custom (Punjab)---
 
--Balouch Tribes---Custom excluding females from right of inheritance, prevalence of---Proof---Burden of proof would be upon the person setting up such custom---Judicial trend in Punjab had throughout been that few instances would be sufficient to rebut initial presumption in favour of Riwaj-i-Aam, wherein such custom was recorded---Principles.
Eada Khan v. Mst. Ghanwar and others 2004 SCMR 1524 and Ghulam Rasool and 7 others v. Rashid and 4 others 2005 MLD 1782 ref.
 
Mian Arshad Latif, Syed Izhar-ul-Haq Gillani and Shahid Tasawar Rao for Appellants.
 
Muhammad Amir Bhatti for Respondents.
 
Date of hearing: 4th April, 2006.
 
JUDGMENT
 
Case 150
2006 C L C 1018
 
[Lahore]
 
Before Maulvi Anwarul Haq and Fazal-e-Miran Chauhan, JJ
 
Miss SHAZIA ASHRAF----Appellant
 
Versus
 
MUNICIPAL COMMITTEE, SAHIWAL through Administrator and another----Respondents
 
C.Ms. Nos.581 and 5822 of 2005 in Intra-Court Appeal No.122 of 2001, decided on 2nd February, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----S. 12(2)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Provisions of S.12(2), C.P.C., applicability of---Scope---Petitioner applied for post of P.T.C. Teacher and was selected after interview but due to imposition of ban on recruitment her appointment letter was withheld by the department---Constitutional petition was dismissed on ground that letter of recommendation was not duly signed by the competent authority---Intra-Court appeal was also not allowed--Petitioner, after a period of three years, filed application under S.12(2), C.P.C. and sought recall of judgment and decree passed against her asserting that in order to get decision in their favour department malafidely served petitioner with the copy of deficient recommendation letter and that said letter, later on was duly signed by the competent authority---Validity---Provisions of S.12(2), C.P.C. could only be pressed into service where fraud was played or misrepresentation was made during the proceedings of the suit in Court and not if done outside the Court---Petitioner having not stated that department obtained order by practising fraud upon the Court nor any fraud or misrepresentation was alleged in connection with the proceedings of the Court, power under S.12(2) could not be invoked---Photocopy of duly signed recommendation letter on record was not certified---Petitioner, in circumstances, had failed to give particulars of alleged fraud and misrepresentation in his petition as per requirement of S.12(2), C.P.C.
 
Lal Din and another v. Muhammad Ibrahim 1993 SCMR 710; Rehmat Ullah v. Ali Muhammad and another 1983 SCMR 1064; Hyesons Sugar Mills (Pvt.) Ltd. v. Consolidated Sugar Mills Ltd. and others 2003 CLD 996 and WAPDA through Chairman and 5 others v. Messrs Sea Gold Traders 2002 MLD 19 ref.
 
(b) Civil Procedure Cod (V of 1908)---
 
----S. 12(2)---Term "fraud and misrepresentation" as occurring in S.12(2), C.P.C.---Connotation and distinction---Difference between "fraud" and "misrepresentation" is one of knowledge and intention---"Fraud" proceeds on the basis of a fact or assertion or omission to assert such fact with knowledge to its falsity, whereas in the context of "misrepresentation" assertion or its omission may lack both.
 
Salma Begum v. Collector, Land Acquisition and others 2003 CLC 1355 and Mobina Begum v. The Joint Secretary, Ministry of Religious and Minority Affairs, Government of Pakistan, Islamabad and 2 others 1994 MLD 1441 ref.
 
(c) Civil Procedure Code (V of 1908)---
 
----S. 12(2)---Setting aside of decree---Limitation---Decree sought to be .set aside was passed three years back---Limitation for setting aside an order obtained through fraud and misrepresentation would start from the date of knowledge---Applicant. having not disclosed the date on which she came to know about the alleged fraud or misrepresentation, application filed after three years from passing the impugned decree, was time-barred.
 
Sh. Muhammad Rafiq Goreja for Appellant.
 
Ch. Muhammad Rafiq for Respondents.
 
Zafar Ullah Khan Khakwani, A.A.-G.
 
ORDER
 
Case 151
2006 C L C 1023
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
Mst. KHURSHID BIBI and others----Petitioners
 
Versus
 
RAMZAN and others----Respondents
 
Civil Revision No.442 of 1995, heard on 3rd April, 2006.
 
(a) Islamic Law---
 
----Gift---Absence of reasons for making gift---Effect---Sisters having their own children and husbands alleged to have gifted land to mother and ultimately to brother---Denial of gift by sisters---Absence of plea and evidence as to why sisters made such gift---Effect---Such fact made doubtful genuineness of transaction, which on ifs face was void.
 
Ghulam Ali and 2 others v. Mst. Ghulam Sarwar Naqvi PLD 1990 SC 1 and Barkat Ali through Legal Heirs and others v. Muhammad Ismail through Legal Heirs and others 2002 SCMR 1938 rel.
 
Abdul Mateen and others v. Mst. Mustakhia 2006 SCMR 50; Mst. Phaphan through L.Rs. v. Muhammad Bakhsh and others 2005 SCMR 1278 and Khalil Ahmad v. Abdul Jabbar Khan and others 2005 SCMR 911 distinguished.
 
(b) West Pakistan Land Revenue Act (XVII of 1967)----
 
---S. 42---Qanun-e-Shahadat (10 of 1984), Arts.119 & 129(e)---Gift---Mutation of gift incorporated in Jamabandi---Presumption of genuineness---Evidentiary value---In case of denial of gift, despite such presumption, burden would lie upon beneficiary to prove validity of transaction.
 
Abdul Majeed and 6 others v. Muhammad Subhan and 2 others 1999 SCMR 1245 and Fida Hussain through Legal Heirs Muhammad Taqi Khan and others v. Murid Sakina 2004 SCMR 1043 rel.
 
(c) Co-sharer---
 
----Suit by co-sharer/co-heir---Limitation---When parties are co-heirs, then limitation would not run against co-heir.
 
Syed Mohtasham-ul-Haq Pirzada for Petitioners.
 
Ch. Abdul Ghani and Ch. Muhammad Hafeez Ahmad for Respondents.
 
Date of hearing: 3rd April, 2006.
 
JUDGMENT
 
Case 152
2006 C L C 1028
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
KHIZAR HAYAT and another----Petitioners
 
Versus
 
PAKISTAN RAILWAY through Chairman, Pakistan Railway, Lahore and 2 others----Respondents
 
Civil Revisions Nos.2047, 2048 and 2049 of 2004, heard on 24th March, 2006.
 
West Pakistan Land Revenue Act (XVII of 1967)---
 
----S. 3---Specific Relief Act (I of 1877), S.42---Civil Procedure Code (V of 1908), O.XXVI, R.9---Demarcation of land occupied and used as a building site---Jurisdiction of Revenue Authorities---Scope---Section 3, West Pakistan Land Revenue Act, 1967 provided that except for certain restricted physical purposes nothing in the said Act would apply to land which was kept/used as a building site---Undisputedly suit properties were no more agricultural land and were building sites, located within the municipal limits hence demarcation reports of such properties by the officials working in revenue hierarchy under West Pakistan Land Revenue Act, 1967, were prepared unauthorizedly---Said reports produced by parties did not resolve the controversy as to whether the suit properties were owned by plaintiffs according to their claim or had been encroached upon by plaintiffs as per assertions of defendants---Reports of Local Commissioner relied upon by Trial Court prepared about nine years earlier to the institution of suit without associating the adversaries on the day of demarcation, had no legal sanctity and could not be based for settlement of dispute inter parties in just manner---Court should have deputed Local Commissioner for demarcating land in dispute but same was neither adverted to nor was resorted by any of the two Courts below---Impugned judgments and decrees passed by Courts below having tainted with material illegalities and irregularities were set aside and case was remanded with direction to decide the suits afresh after having fresh demarcation through some senior revenue experts in accordance with law.
 
Ghulam Rasul v. Ikram Ullah and another PLD 1965 (W.P.) Lah. 429; Tahir Hanif v. Member, Board of Revenue and others 1982 CLC 1732; Syed Aslam Shah and 3 others v. Mst. Sakina and another 1988 MLD 1596 and Pervez Ahmed Khan Burki and 3 others v. Assistant Commissioner, Lahore Cantt. and 2 others PLD 1999 Lah. 31 ref.
 
Sh. Naveed Shaharyar for Petitioners.
 
Irfan Masood Sheikh for Respondents Nos.1 and 2.
 
Muhammad Ilyas Khan and Abdul Rauf Patwaris, Khushab for Respondent No.3.
 
Date of hearing: 24th March, 2006.
 
JUDGMENT
 
Case 153
 
2006 C L C 1036
 
[Lahore]
 
Before Syed Sajjad Hussain Shah, J
 
MUHAMMAD NAWAZ----Petitioner
 
Versus
 
ADDITIONAL SESSIONS JUDGE/JUSTICE OF PEACE, JHANG and 12 others----Respondents
 
Writ Petition No.2185 of 2006, decided on 4th April, 2006.
 
Dissolution of Muslim Marriages Act (VIII of 1939)---
 
----S. 2(vii)---Dissolution of marriage on ground of Khayar-ul-Baloogh---Law did not prescribe any particular form of the procedure for repudiation of marriage; it could be by oral or even by conduct seeking rejection of marriage and if the minor entered into second marriage on attaining the age of puberty, it would be sufficient proof of repudiating her earlier marriage and subsequent marriage would be valid.
 
Zafar Iqbal Chowhan for Petitioner.
 
Faisal Ali Qazi, A.A.-G. for Respondents.
 
ORDER
 
Case 154
 
2006 C L C 1046
 
[Lahore]
 
Before Sh. Hakim Ali, J
 
ARSHAD MEHMOOD and others----Appellants
 
Versus
 
MAKHDOOM AHMAD GHAUS----Respondent
 
Regular Second Appeal No.8 of 1994/BWP, decided on 5th December, 2005.
 
Punjab Pre-emption Act (I of 1913)---
 
----S. 15---Evidence Act (I of 1872), S.50---Civil Procedure Code (V of 1908), O.VIII, R.1---Suit for pre-emption---Superior right of pre-emption on basis of Yakjaddi and Shareek Khata---Pedigree-table, proof of relationship---Words "it is incorrect" used iii written statement---Significance---Insufficiency of concept of positive denial, in such words highlighted---Contention of defendant was that pedigree-table without any other corroborative evidence satisfying the requirement of S.50 of Evidence Act, 1872 was not sufficient to prove that pre-emptor was collateral of vendor---Plaintiff's claim of superior pre-emption right was not specifically refuted by defendant/vendee in written statement---Words "that it is incorrect" were not sufficient to constitute the denial of relationship---Plaintiff's deposition on oath with respect of relationship having not been crossexamined by defendant, it was deemed to be admitted---Statement of witness that before impugned sale an offer was made to plaintiff for purchase of land but same was refused by plaintiff showed that superior right of plaintiff did exist---Waiver under Punjab Pre-emption Act, 1913 had to be proved through cogent evidence and by a mere advertisement in newspaper same could not be established---No objection was raised at the time when pedigree-table was brought on record into evidence and relationship of plaintiff with. vendors was not contested by vendee, therefore, objection of proof in consonance with provision of S.50 of Evidence Act, 1872 had no significance---Display of minor legal heirs of deceased vendee as major was merely an irregularity which was curable and caused no prejudice to the other party.
 
Mian Khan v. Abdul Aziz PLD 2002 Lah. 159 and Rchman v. Noora through his Legal Heirs 1996 SCMR 300 ref.
 
Sh. Karimuddin for Appellant.
 
Sajjad Hussain Khan Kanju for Respondent.
 
Date of hearing: 5th December, 2005.
 
JUDGMENT
 
Case 155
2006 C L C 1050
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
ABDUL HAMID and 6 others----Appellants
 
Versus
 
Mst. HAJRAN BIBI and 6 others----Respondents
 
Regular Second Appeal No. 15 of 2004, heard on 15h March, 2006.
 
Specific Relief Act (I of 1877)---
 
----Ss. 8 & 12---Suit for possession and specific performance on the ground that defendants, who were relatives of plaintiffs were permitted to reside in suit house, but they had refused to vacate the same---Defendants had filed a suit for specific performance of agreement of sale allegedly executed between the parties---Both suit were consolidated and issues were framed---Vide consolidated judgment and decree, suit of plaintiffs, was decreed by the Trial Court---First appeal by defendants against judgment and decree of the Trial Court, was dismissed---Validity---No error of law or fact having been found in concurrent judgments and decrees of Courts below, second appeal was dismissed with costs.
 
Mian Habib-ur-Rehman Ansari for Appellants.
 
Muhammad Tariq for Respondents.
 
Date of hearing: 15th March, 2006.
 
JUDGMENT
 
Case 156
2006 C L C 1056
 
[Lahore]
 
Before Syed Hamid Ali Shah, J
 
MUNICIPAL COMMITTEE, MANDI BAHAUDDIN, TEHSIL PHALIA through Chairman----Petitioner
 
Versus
 
PROVINCE OF PUNJAB through District Collector, Gujrat and others ----Respondents
 
Civil Revision No.810 of 2000, heard on 28th July, 2005.
 
Specific Relief Act (I of 1877)---
 
----S. 42---Suit for declaration to the effect that plaintiff was exclusive owner of the property being transferee from the Settlement Department and that order of its subsequent transfer to defendant, if any, was void, ultra vires and of no effect on the rights of plaintiff---Plaintiff had proved the allotment of land through documents---Defendant claimed himself to be the owner, on the basis of his purchase of the property through open auction---Record had proved that defendant had not purchased the property in question and the record was prepared by defendant, in connivance with staff of the department---Defendant had failed to bring on record any agreement, sale certificate, order of Settlement Department regarding the confirmation of sale through .auction in his favour and receipt of payment of auction price---Mere mention of the property in the auction list and entry in the Register CSC-V would not prove the purchase of property by the defendant---Allotment, once made to the plaintiff could not be cancelled for non-deposit of balance amount, since authorities could recover the same amount from the plaintiff as arrears of land revenue---Suit property not being the part of the compensation pool, sale thereof through auction was illegal---Suit of the petitioner, in circumstances, was decreed.
 
Sultan Khan and 3 others v. Sultan Khan 2004 MLD 918; Nawab Din and another v. Mst. Haseeb-un-Nisa and others 1980 SCMR 798; Mst. Majeeda Begum v. Deputy Settlement Commissioner-II and others 1980 SCMR 827; Mst. Roshan Jahan and others v. Settlement Commissioner and others 1988 SCMR 346 and Israr Ahmad and others v. Member, Board of Revenue/Chief Settlement Commissioner, Lahore and another 1997 SCMR 1559 ref.
 
Dr. Mohy-ud-Din Qazi for Petitioner.
 
Kh. Muhammad Saeed for Respondent No. 1.
 
Mushtaq Masood for Respondent No.2.,
 
Nazir Ahmad Qureshi and Muhammad Adeel Aqil Mirza for Respondent No.3.
 
Date of hearing: 28th July, 2005.
 
JUDGMENT
 
Case 157
2006 C L C 1076
 
[Lahore]
 
Before Syed Hamid Ali Shah, J
 
Mst. LATIFA BIBI and 8 others----Appellants
 
Versus
 
MUHAMMAD BASHIR and 10 others----Respondents
 
Regular Second Appeal No.92 of 1989, heard on 19th April, 2006.
 
(a) Islamic Law---
 
----Inheritance---Faith of Muslim deceased, whether Sunni or Shia---Presumption---Burden of proof---Every Muslim in Pakistan would be presumed to be Sunni, unless proved otherwise---Burden of proof would lie on person claiming deceased to be Shia by faith---Performance of "Janaza Prayer" not determining factor of one's faith--Determining factors for ascertaining one's faith stated.
 
Pakistan being in abundance of Sunni Muslims, the initial presumption is that every Muslim citizen is a Sunni, unless otherwise proved. The duty is cast upon the person, who claims that a person is Shia, to prove it through cogent and consistent evidence. The majority of Muslims in Pakistan being Sunnis, it cannot therefore, be ascertained that a person belongs to Sunni School of Thought, from the surrounding circumstances i.e. offering of "Janaza Prayer" or funeral ceremonies of deceased by Sunni Aalim or his birth and life style. A person is not required to give his consent as to where he has to take birth and by whom his "Janaza Prayer" is to be performed. Janaza Prayer is thus not a determining factor of one's belief, being an act done after the death of a person and without his permission.
 
The expressions and conduct of deceased is relevant for determination of his faith. Opinion of the parties and the faith of close relatives is not a determining factor.
 
The sect of a person cannot be determined by opinion of the parties, but can be inferred from prevalent circumstances.
 
No hard and fast test can be laid to ascertain one's belief or faith. It cannot be ascertained on the basis of one or more events. The faith of a person has to be determined either by what he professed during his life time or by what he confessed verbally or otherwise in his daily course of life or by conduct that is to say by performance of his religious rites in a particular manner. In the event these elements are silent, faith of deceased can be determined by birth i.e. faith of his parents; by family i.e. faith of his brother, sister or Kiths and kins; by nationality i.e. faith of majority of a country of which he was national.
 
A person knows about his faith more than the others, no matter how close are others with that person.
 
Syed Lal Hussain Shah v. Mst. Robina Shaheen and another PLD 2000 SC (AJ&K) 25; Sardar Muhammad v. Muhammad Akram and others 2000 YLR 1824; Amir Ali v. Gul Shaker and 10 others PLD 1985 Kar. 365; Sabir Hussain and others v. Afrasayyab and others 1989 CLC 1591; Ahmad Khan and 4 others v. Sikandar 1999 YLR 2692; Zohran Mai v. Mst. Siftan and others 1983 CLC 2559 and Mt. Iqbal Begum v. Mt. Syed Begum and others AIR 1933 Lah. 80 ref.
 
(b) Islamic Law---
 
----Inheritance---Faith of deceased, determination of---Deceased belonged to a Sunni Family and was resident of a village, where predominantly population was followers of Sunni Fiqa---Deceased as Patwari remained posted for 25 years in a village, where people followed Shia School of faith---"Wassiyat Nama" by deceased in favour of his widow and sister, affidavit sworn by deceased and statement of widow recorded before Revenue Authorities at the time of attestation of inheritance mutation showing deceased to be Shia by faith---Plaintiff being collaterals of deceased claimed him to be Sunni by faith---Proof---Witnesses of plaintiff did not state with corroboration about faith of deceased---Wassiyat Nama and affidavit of deceased were proved by their marginal witnesses---Widow did not deny factum of her statement recorded before Revenue Authorities prior to litigation---Such statement of widow would carry much weight for she having spent most of the time with deceased was aware of her husband's faith more than anyone else---Affidavit of deceased had more evidentiary value than a person, who claimed to be his relative or friend---Statements made by deceased in Wassiyat Nama and affidavit, being related to his family affairs, would fall within ambit of Art.46(5)(6) of Qanun-e-Shahadat, 1984---Faith of deceased was held to be Shia---Qanun-e-Shahadat (10 of 1984), Art.46(5) & (6).
 
Riaz Hussain and others v. Board of Revenue and others 1991 SCMR 2307; Mst. Sahib Bibi and others v. Lal 1992 CLC 807; Nazir Ahmad and others v. Abdullah and others 1997 SCMR 281; Mst. Nur Jehan Begum through Legal Representatives v. Syed Mujtaba Ali Naqvi 1991 SCMR 2300; Mst. Manzoor Mai v. Abdul Aziz 1992 CLC 235; Fazal Haq and others v. Mt. Said Nur and others AIR (35) 1948 Lah. 113; Syed Lal Hussain Shah v. Mst. Robina Shaheen and another PLD 2000 SC (AJ&K) 25; Sher Zaman v. Mst. Nawab Khatoon and 7 others 1998 SCMR 133; Mst. Rasheeda Begum and others v. Muhammad Yousaf and others 2002 SCMR 1089; Habib Bux v. Zahoor-ul-Hassan 1986 CLC 1119; Zafar Mirza v. Mst. Naushina Amir Ali PLD 1993 Kar. 775; Barkat Ali v. Muhammad Nawaz PLD 2004 SC 489 and Abdul Rahim and others v. Muhammad Hayat and others 2004 SCMR 1723 ref.
 
Patinharkuru Vallaban Chattan Rajah Amergal v. Raman Varma and others AIR 1915 Mad. 217; Ram Bharose and others v. Diwan Rameshwar Prasad Singh AIR 1938 Oudh 26; Hira Lal Jawala Sahai v. Sitla Kahna and another AIR (38) 1951 Pepsu 82 and S. Veeraraghava Lyer v. J.D. Mu;;ha Sait AIR 1950 Mad. 486 rel.
 
(c) Pleadings---
 
----Evidence beyond the scope of pleadings could not be considered.
 
(d) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 70---Oral evidence, appreciation of---Where parties to lis stand to gain .or lose valuable property, then oral evidence would be approached with caution---Safer would be to rely on evidence, which is in accord with admitted circumstances.
 
Mst: Sardar Bibi v.. Muhammad Bakhsh PLD 1954 Lah. 480 rel.
 
(d) Qanun-e-Shahadat (10 of 1984)---
 
----Art. 46---Statements of persons, who cannot be called as witnesses---Exception to general rule of evidence that all evidence must be direct; and that statement of witness on oath could be tested through cross ?examination---Article 46 of Qanun-e-Shahadat, 1984 related only to relevancy of evidence and not to manner of its proof---Maker of statement in cases detailed in Art.46 would not be examined as a witness at all.
 
Taqi Ahmad Khan for Appellants.
 
Malik Noor Muhammad Awan for Respondents.
 
Date of hearing: 19th April, 2006.
 
JUDGMENT
 
Case 158
2006 C L C 1090
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
BASHIR AHMAD and another----Petitioners
 
Versus
 
TEHSIL MUNICIPAL ADMINISTRATION through Tehsil Nazim, Faisalabad and 3 others----Respondents
 
Writ Petition No.171-A of 2000, heard on 25th April, 2006.
 
Punjab Local Government Ordinance (XIII of 2001)---
 
----S. 180---Constitution of Pakistan (1973), Art.199---Constitutional petition---Structure of the petitioners' shops was pulled down and portion of the land beneath those shops was included in expanded road by the Municipal Authorities---Award of compensation etc.---By introduction of District Governments through Punjab Local Government Ordinance, 2001, Municipal Authorities had been taken over by the Town Municipal Administration and by virtue of S.180 of the Punjab Local Government Ordinance, 2001 all the properties, assets and liabilities of local councils, were to be succeeded by the bodies nominated therein and by virtue of S.180(a) of the Ordinance City Government was to take over Municipal Corporations in the concerned City District, thus all the liabilities which were previously to be discharged by Tehsil Municipal Administration had now to be fulfilled by the City District Government---Rights of petitioners to compensation and their entitlement stood already determined by the High Court, which shall be read as part of the present judgment---Authorities had not denied ownership of the petitioners over their shops in question, which were pulled down and land beneath was included in the expanded area of abutting road, thus, there appeared to be no lawful excuse for the Authorities in .not providing compensation---High Court directed the City District Government to allot/allocate alternate land/plots to the petitioners in lieu of their properties utilized for expansion of the Road, besides awarding them compensation for the structure pulled down by the Nazim concerned, after hearing the petitioners, within a period of four months, in accordance with law and compliance report to be submitted to the Deputy Registrar (Judicial) of the High Court.
 
Bashir Ahmed Chaudhry for Petitioners.
 
Nemo for Respondents.
 
Date of hearing: 25th April, 2006.
 
JUDGMENT
 
Case 159
2006 C L C 1097
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
INAYAT MASIH----Petitioner
 
Versus
 
MEMBER (REVENUE), BOARD OF REVENUE, PUNJAB, LAHORE and another----Respondents
 
Writ Petition No.3919 of 2006, decided on 26th April, 2006.
 
Qanun-e-Shahadat (10 of 1984)---
 
----Arts. 87 & 90---Constitution of Pakistan (1973), Art.199---Certified copy of any Court order issued with authentication as required by Art.87, Qanun-e-Shahadat, 1984 carried a presumption of correctness as per its Art.90 and no further verification thereof was needed under law---Authority, in the present case, neither had any business to certify any judicial order nor it was conferred any such power by law applicable, thus Authority was justified in refusing to verify the order---Constitutional petition rested on disputed factual controversy, requiring determination through detailed enquiry/recording of evidence but such exercise could not be undertaken while discharging jurisdiction under Art.199 of the Constitution---Constitutional petition was dismissed.
 
The Province of East Pakistan v. Kshiti Dhar Roy and others PLD 1964 SC 636 and Muhammad Younas Khan and others v. Government of N.-W.F.P. through Secretary Forest and others 1993 SCMR 618 fol.
 
Ch. Inayat Ullah for Petitioner.
 
ORDER
 
Case 160
2006 C L C 1103
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
GHULAM QADIR----Petitioner
 
Versus
 
MUHAMMAD BAKHSH and 2 others----Respondents
 
Civil Revision No.2419 of 2005, decided on 20th April, 2006.
 
(a) Civil Procedure Code (V of 1908)---
 
----O. XLI, R.27---Production of additional evidence at appellate stage---Application under O.XLI, R.27, C.P.C. could be dismissed in isolation from the appeal as such course would be opposed to the spirit of provisions of O.XLI, R.27, C.P.C. whereunder appellate Court while hearing appeal might need/feel necessity of documents sought to be produced for just/fair decision of the case---Order passed by the District Judge being tainted with illegalities/irregularities was not sustainable at law which was set aside by the High Court with the result that application under O.XLI, R.27, C.P.C. shall be deemed to be pending and shall be decided afresh along with his appeal by the District Judge.
 
(b) Civil Procedure Code (V of 1908)------
 
---O. XLI, R.27---Production of additional evidence at appellate stage---First appellate Court incorrectly dismissed the application under O.XLI, R.27, C.P.C. on the ground that order of Trial Court was maintained on revision, thus, the same could not be reopened, being oblivious of the provisions of S.105, C.P.C. and the fact that applicant's revision petition was not decided on merits and was dismissed on technical ground---Order passed by the District Judge being tainted with illegalities/irregularities was not sustainable at law which was set aside by the High Court with the result that application under O.XLI, R.27, C.P.C. shall be deemed to be pending and shall be decided afresh along with his appeal by the District Judge.
 
Ata-ul-Mohsan Lak for Petitioner.
 
G.M. Sarwar for Respondents Nos.2 and 3.
 
ORDER
 
Case 161
2006 C L C 1110
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
Chaudhary MUHAMMAD SARWAR through L.Rs.----Petitioners
 
Versus
 
Mst. AIMNA BIBI and 2 others----Respondents
 
Civil Revisions Nos.621 to 626 of 2006, decided on 18th April, 2006.
 
Contract Act (IX of 1872)---
 
----S. 56---Specific Relief Act (I of 1877), S.12---Suit for specific performance of agreement to sell---Agreement, in circumstances of the case, had become void---Effect---Law to this effect was enacted in S.56, Contract Act, 1872, which provided that agreement to sell which afterwards became impossible of performance or unlawful, would become void---Agreements, the performance of which was prayed in suit having become void i.e. impossible of performance, the only course open for the plaintiffs was to sue the defendants for loss, if any, sustained by them on account of their non-performance and for return of their advanced money.
 
Masood Abid Naqvi for Petitioners.
 
ORDER
 
Case 162
2006 C L C 1123
 
[Lahore]
 
Before Muhammad Muzammal Khan, J
 
ABDUL MAJEED----Appellant
 
Versus
 
MUHAMMAD NAEEM and 3 others----Respondents
 
First Appeal from Order No.43 of 2005, decided on 20th April, 2006.
 
Civil Procedure Code (V of 1908)---
 
----O. XXXIX, Rr.1 & 2--Specific Relief Act (I of 1877), S.12---Suit for specific performance of agreement to sell with the averments that defendant had failed to perform his part of contract and possession of the land was not handed over to plaintiff as per agreement, after receipt of huge amount of earnest money---Plaintiff also filed an application under O.XXXIX, Rr.1 & 2, C.P.C. with the plaint, praying for issue of restraint order against the defendant preventing him from alienating the suit property by any means whatsoever---Defendant aggrieved of acceptance of stay application filed appeal with the claim that he being owner, could not be restricted to alienate the land and that without requiring the plaintiffs/applicants to deposit the agreed balance sale price, the injunction prayed could not have been issued---Validity---Defendant, in spite of urging interpolation and incomplete nature of the agreement to sell admitted its execution and receipt of earnest money of Rs.27,50,000 in place of Rs.50,00,000---Terms of the agreement on the basis of which the plaintiffs had filed the suit for specific performance, were also not refuted by the defendant whereunder it was agreed that actual physical possession of the land had been handed over to the plaintiffs and they would pay another amount of Rs.1,00,00,000 as per agreement---Defendant, during the course of proceedings offered to deliver possession of the suit-land forthwith, in case plaintiffs paid him the settled amount of Rs.1,00,00,000---Record revealed that plaintiffs entered into agreement for development of the land by laying some housing scheme and were to pay part of the sale consideration by a specified date after developing the land, possession of which was not handed over to them---Claim of defendant regarding payment of Rs.1,00,00,000 without handing over possession and without giving crucial period of one year and three months to the plaintiffs, was opposed to the terms settled between the parties---Plaintiffs, in circumstances, had made out a prima facie/arguable case in their favour and they could not be further burdened to pay/deposit another amount of Rs.1,00,00,000 without giving them possession of the suit-land, contrary to the agreement---Held, restraint on alienation of the suit property would not result in any irreparable loss/injury to the defendant whereas the . same might occur to the plaintiffs who would face further complications and multiplicity of proceedings; balance of convenience also leaned in favour of the plaintiffs and the defendant would not suffer any inconvenience in case the injunction issued was allowed to continue; plaintiffs' suit had already reached at the stage of evidence which could not be recorded on account of stay of proceedings by the High Court, hence recall of injunctive order issued by the Trial Court which was granted after due consideration of respective cases of the parties and according to the settled principles governing issuance/refusal of prohibitory orders, at the present stage, appeared to be not just/fair---Record and the impugned order, revealed that restraint order was not arbitrary/fanciful and same being within four corners of law, admitted no exception---High Court, however, made it clear that all the findings by High Court and those by the Trial Court were only confined to disposal of stay matter and would not influence the Trial Court while deciding the suit on merits according to the law and evidence of the parties, which ultimately they might produce---Trial Court having committed no error of law and its impugned order being lawful was maintained by the High Court.
 
Muhammad Kazim Khan for Appellant.
 
Ch. Abdul Majeed for Respondents.
 
ORDER
 
Case 163
2006 C L C 1141
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
NOORA and 3 others----Petitioners
 
Versus
 
PROVINCE OF PUNJAB through District Collector, Vehari and others----Respondents
 
Civil Revision No.156-D of 1992, heard on 6th April, 2006.
 
Colonization of Government Lands (Punjab) Act (V of 1912)---
 
----S. 30---Cooperative Farming Act (LII of 1976), S.21---State land---Cooperative Farming Scheme, allotment under---Death of original member-allottee---Claim of son of deceased allottee as independent allottee---Validity---Original Register containing resolution regarding permanent allotment in favour of deceased allottee showed interpolation---Subsequent resolution passed after death of original allottee narrated that his son had filed application that suit-land stood allotted to his father, and after his death, he was cultivating land, thus, son was resolved to be made a member of the Society---Record showed that suit-land had never been allotted to son or any other child of the deceased---Rights, interest and liabilities of deceased member would devolve upon his legal heirs under S.21 of Cooperative Farming Act, 1976, who would become member of the Society in place of deceased member---Suit-land therefore, would devolve upon all legal heirs of the deceased allottee.
 
Manzoor Ahmad v. Mst. Salaman Bibi and others 1998 SCMR 388 and Fazal Shah v. Muhammad Din and others 1990 SCMR 868 ref.
 
Ch. Muhammad Hussain Jahania for Petitioners.
 
Azmat Ali Khanzada for Respondents Nos.1 to 3.
 
Ch. Abdul Ghani and Mian Mushtaq Ahmad for Respondents Nos.4 to 12.
 
Date of hearing: 6th April, 2006.
 
JUDGMENT
 
Case 164
 
2006 C L C 1149
 
[Lahore]
 
Before Sh. Hakim Ali, J
 
Hafiz MUHAMMAD RAMZAN----Petitioner
 
Versus
 
DEPUTY DISTRICT OFFICER (REVENUE), TEHSIL BAHAWALPUR and another----Respondents
 
Writ Petition No.3756 of 2005IBWP, decided on 6th March, 2006.
 
Punjab Pre-emption Act (IX of 1991)---
 
----S. 13---Registration Act (XVI of 1908), S.17(2)(6)---Civil Procedure Code (V of 1908), O.XX, R.14(b)---Constitution of Pakistan (1973), Art.199---Constitutional petition---Suit for pre-emption---Decree passed on compromise---Application for incorporation of decree in Revenue Record was refused by Revenue Officer on the basis of non-registration of decree---Validity---Right of pre-emption was a right of substitution, as in the sale transaction, vendee was substituted by entry of pre-emptor after the decree was passed, hence pre-emption decree which did not create any fresh transaction of sale or give birth to new alienation need not be registered---Pre-emptors' right under O.XX, R.14 of C.P.C. accrued from date of deposit and registered document was not necessary for passing of title to pre-emptor---Section 17(2)(6) of Registration Act, 1908 had also exempted the pre-emption decree from registration, therefore, impugned order whereby implementation of pre-emption decree was refused for non-registration, was declared illegal and unlawful.
Shahra and others v. Member, Board of Revenue, Punjab and others 2004 SCMR 117; Rain Lal v. Harpal and another AIR 1929 All. 237; Bajirao Samaji Salewar v. Abdul Ghaffar son of Sheikh Rahman AIR 1949 Nag. 338 ref.
 
Muhammad Yousuf Sarni Khan for Petitioner.
 
Ch. Shafi Muhammad Tariq, A.A.-G. along with Tariq Javed, Naib Tehsildar and Munawar Hussain Patwari.
 
ORDER
 
Case 165
2006 C L C 1152
 
[Lahore]
 
Before Maulvi Anwarul Haq, J
 
ALLAH DITTA----Petitioner
 
Versus
 
ABDUL KHALIQUE----Respondent
 
Civil Revision No.1092-D of 2003, heard on 21st February, 2006.
 
Specific Relief Act (I of 1877)---
 
----S. 12---Contract Act (IX of` 1872), S.74---Suit for specific performance of penalty clause of agreement---Plaintiff forgoing performance of agreements to sell land and residential property by executing fresh agreement on the terms that sum of Rs.66,400 received under previous agreements would be repaid to him in instalments and on defendant's failure to pay instalments, he would be liable to transfer land to plaintiff @ Rs.40,000 per acre---Plaintiff filed suit on defendant's failure to pay instalments---Trial Court decreed suit by directing defendant to transfer land as promised---Appeal filed there against was dismissed---Validity---Such penal clause was not enforceable---Courts below had acted without jurisdiction by enforcing such penal clause---Plaintiff was entitled to reasonable compensation---Possession of land was with defendant and sum of Rs.66,400 was lying with him since 13-4-1985---High Court accepted revision petition and modified decree by passing a decree for recovery of Rs.66,400 with profits to be paid @ 12% per annum w.e.f. 13-4-1985 in favour of plaintiff and against defendant with costs throughout.
 
Province of West Pakistan v. Messrs Mistri Patel & Co. another PLD 1969 SC 80 fol.
 
Messrs Nigah-e-Karimee Enterprises through Proprietor and another v. Trust Investment Bank Limited 2005 CLC 912 and Abdullah v. Karim Haider PLD 1975 Kar. 385 ref.
 
M. Waseem Shahab for Petitioner.
 
Mian Faiz Rasul for Respondent.
 
Date of hearing: 21st February, 2006.
 
JUDGMENT
 


Brief facts leading to this writ petition are that the petitioner filed three suits, (1) suit for maintenance allowance, (2) suit for recovery of dower and (3) suit for recovery dowry articles, against respondent No.1 before the learned Family Judge, Muzaffargarh, who decreed two suits, one for recovery of maintenance allowance and the other for recovery of dower but dismissed the suit for recovery of dowry articles vide his judgment, dated 17-4-2004. The petitioner challenged the vires of the judgment dated 17-4-2001 passed by the learned Judge, Family Court, Muzaffargarh, whereby a suit for recovery of dowry articles was dismissed. The appeal was also dismissed by the learned District Judge, Muzaffargarh, vide his judgment dated 1-6-2002. Against the said judgment, the petitioner has filed this writ petition.
 
2. Learned counsel for the petitioner has contended that the written statement to the suit for recovery of dowry articles was not filed by the respondent/defendant Jaffar Hussain himself but was filed by the special attorney of the respondent, as such the same did not deserve consideration and reliance in this behalf is placed on Mazhar Iqbal v. Falak Naz and 2 others PLD 2001 Lah. 495 and that the appeal before the learned District Judge, Muzaffargarh was within time as the copies of the decree sheets of the judgment and decrees were delivered to the petitioner on 4-7-2001 but if it is admitted for the time being that the appeal was barred by time, even otherwise limitation would not run against void order and in this behalf reliance is placed on Mustajab Hassan and others v. Director Trade Organisations and others 1996 CLC 1725 and, therefore, the impugned judgment, dated 17-4-2001 passed by the learned Judge, Family Court, Muzaffargarh and the judgment, dated 1-6-2002 passed by the learned District Judge, Muzaffargarh are illegal, void ab initio and against well-settled principles of equity and law.
 
3. Arguments heard. Record perused.
 
4. Perusal of the written statement to the suit for recovery of dowry articles filed by the respondent itself shows that it was filed by Jam Ghulam Rasool special attorney of the respondent/defendant Jaffar Hussain and not filed by the respondent himself. Under section 9 of the West Pakistan Family Courts Act, 1964, a defendant is bound to appear in the Family Court himself for the purpose of filing a written statement and his attendance cannot be dispensed with. Therefore, the written statement filed by the special attorney of the respondent/defendant Jaffar Hussain did not deserve consideration in the eye of law. On this proposition, I am supported by the authority cited by learned counsel for the petitioner i.e. Mazhar Iqbal v. Falak Naz and 2 others PLD 2001 Lah. 495.
 
4-A. As far as the limitation is concerned, learned counsel for the petitioner has stated that as the decree-sheet of the decree, dated 17-4-2001 was not prepared well in time, the Copying Agency did not deliver the copy to the petitioner on 18-6-2001 and the copy of the decree-sheet of the decree, dated 17-4-2001 was delivered to the petitioner on 4-7-2001 when it was prepared. If it is admitted that the appeal before the learned District Judge, Muzaffargarh was barred by time, even though limitation would not run against the void order. Reliance in this behalf is placed on Mustajab Hasan and others v. Director Trade Organisations and others 1996 CLC 1725. The judgment dated 17-4-2001 was passed by the learned Judge Family Court, Muzaffargarh without the written statement of the respondent/defendant Jaffar Hussain, therefore, it was void and illegal. As the judgment dated 17-4-2001 was illegal and void, limitation would not run against the same order.
5. In view of the above circumstances, this writ petition is accepted, the judgment, dated 17-4-2001 passed by the learned Judge Family Court, Muzaffargarh and the judgment, dated 1-6-2002 passed by the learned District Judge, Muzaffargarh are set aside and the case is remanded back to the learned District Judge, Muzaffargarh to pass a fresh order after hearing both the parties and considering the observations made above.



"""

# Process the input text
df_case_data = process_cases(input_text)

# Change output path to a valid directory on your local machine
output_file = "C:/Users/xiHawks 1002/Documents/legal_judgments_summary_output.csv"

# Save the results to a CSV file
df_case_data.to_csv(output_file, index=False)

output_file  # This will return the path to your CSV file
