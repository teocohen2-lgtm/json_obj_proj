# from flask import Flask, render_template, request, send_file
# from datetime import date, timedelta
# import json, random, tempfile

# app = Flask(__name__)

# RELATIONS = {
#     'Self': dict(gender='M', salutation='MR', age=(25,55), height=(160,185), weight=(55,95), proposer='1'),
#     'Wife': dict(gender='F', salutation='MRS', age=(23,52), height=(148,175), weight=(45,80), proposer='0'),
#     'Husband': dict(gender='M', salutation='MR', age=(25,58), height=(160,188), weight=(58,100), proposer='0'),
#     'Father': dict(gender='M', salutation='MR', age=(50,75), height=(155,180), weight=(55,90), proposer='0'),
#     'Mother': dict(gender='F', salutation='MRS', age=(48,72), height=(145,170), weight=(45,82), proposer='0'),
#     'Son': dict(gender='M', salutation='MASTER', age=(3,24), height=(95,178), weight=(15,75), proposer='0'),
#     'Daughter': dict(gender='F', salutation='MISS', age=(3,24), height=(95,170), weight=(15,68), proposer='0'),
# }

# COVERAGES = {
#     'MyHealthCriticalIllness': {'Indicator':'0','SumInsured':0,'PlanName':'7'},
#     'IndividualPersonalAccidentRider': {'Indicator':'0'},
#     'OptimaWellbeing': {'Indicator':'0'},
#     'MyHealthHospitalCashBenefit': {'Indicator':'0','IsGlobal':'0','SumInsured':1000},
#     'UnlimitedRestoreRider': {'Indicator':'0'},
#     'ProtectorRider': {'Indicator':'0'},
#     'HospitalDailyCashRider': {'Indicator':'0','SumInsured':0},
#     'OverseasTravelSecure': {'Indicator':'0'},
#     'AggregateDeductible': {'Indicator':'0','DeductibleValue':'25000'},
#     'ProtectBenefit': {'Indicator':'0'},
#     'PlusBenefit': {'Indicator':'0'},
#     'PEDWaiting': {'Indicator':'0','PeriodDuration':'0'},
#     'Parenthood': {'Indicator':'0','SumInsured':0},
#     'Limitless': {'Indicator':'0'},
#     'ABCD': {'Indicator':'0'},
# }

# FIRST_NAMES = {
#     'M':['Aarav','Vihaan','Arjun','Rohan','Kabir','Aditya','Gitesh','Rahul'],
#     'F':['Anaya','Nisha','Aditi','Meera','Isha','Kavya','Priya','Saanvi']
# }
# LAST_NAMES = ['Patil','Sharma','Jain','Mehta','Nair','Deshmukh','Kulkarni','Verma']


# def dob_from_age(age):
#     today = date.today()
#     return date(today.year-age, random.randint(1,12), random.randint(1,28)).isoformat()


# def random_family(count, proposer_gender='M'):
#     count = max(1, min(int(count), 8))
#     spouse = 'Wife' if proposer_gender == 'M' else 'Husband'
#     pool = [spouse, 'Son', 'Daughter', 'Father', 'Mother']
#     result = ['Self']
#     while len(result) < count:
#         relation = random.choice(pool)
#         if relation in ['Wife','Husband','Father','Mother'] and relation in result:
#             continue
#         result.append(relation)
#     return result


# def mock_member(sequence, relation, sum_insured='1000000'):
#     p = RELATIONS.get(relation, RELATIONS['Self'])
#     age = random.randint(*p['age'])
#     gender = p['gender']
#     return {
#         'SequenceID': str(sequence),
#         'IsProposerInsured': '1' if sequence == 1 else p['proposer'],
#         'Nationality': 'INDI', 'MaritalStatus': 'S', 'OptFor': '',
#         'InsuredLevel80DCertificate': False,
#         'RelationshipWithProposer': relation,
#         'ResidentialStatus': 'ResidentIndian', 'SumInsured': str(sum_insured),
#         'Height': f"{random.uniform(*p['height']):.2f}", 'Gender': gender,
#         'MemberDOB': dob_from_age(age), 'Salutation': p['salutation'],
#         'Weight': f"{random.uniform(*p['weight']):.2f}",
#         'InsuredName': f"{random.choice(FIRST_NAMES[gender])} {random.choice(LAST_NAMES)}",
#         'MedicalAdversity': '0', 'IsPoliticallyExposedPerson': '0'
#     }


# def questions():
#     return {'MedicalQuestions': {'LifeStyleQ': {'Lifestylehabits':'0'}, 'Primary': [
#         {'Id': q, 'Indicator':'0'} for q in ['ADD','SG','MR','IFT','HIP','PRG','DDAC']
#     ]}}


# def family_type_from_members(risks):
#     child_relations = {"Son", "Daughter"}
#     children = sum(
#         1 for risk in risks
#         if risk["member"].get("RelationshipWithProposer") in child_relations
#     )
#     adults = len(risks) - children
#     if children:
#         return f"{adults}A+{children}C"
#     return f"{adults}A"


# def build_payload(data):
#     # member_count = max(1, min(int(data.get("member_count", 1)), 8))
#     policy_type = data.get(
#     "policy_type",
#     "Floater"
# )

#     member_count = max(
#         1,
#         min(
#             int(
#                 data.get(
#                     "member_count",
#                     1
#                 )
#             ),
#             8
#         )
#     )

#     if policy_type == "Individual":
#         member_count = 1
#     proposer_gender = data.get("gender", "M")
#     relationships = data.get("relationships") or random_family(member_count, proposer_gender)
#     selected = set(data.get("coverages", []))
#     member_overrides = data.get("members", [])

#     account_name = data.get("name", "SAKUNTHALA P").strip()
#     account_dob = data.get("dob", "1987-09-07")
#     account_gender = proposer_gender
#     account_salutation = data.get(
#         "salutation",
#         "MR" if account_gender == "M" else "MRS"
#     )

#     risks = []
#     for i in range(member_count):
#         relation = relationships[i] if i < len(relationships) else "Other"
#         member = mock_member(i + 1, relation, data.get("sum_insured", "1000000"))

#         if i < len(member_overrides):
#             member.update({
#                 k: v for k, v in member_overrides[i].items()
#                 if v not in (None, "")
#             })

#         # Proposer member must always match account-level identity.
#         if i == 0:
#             member.update({
#                 "IsProposerInsured": "1",
#                 "RelationshipWithProposer": "Self",
#                 "InsuredName": account_name.replace(" ", ""),
#                 "MemberDOB": account_dob,
#                 "Gender": account_gender,
#                 "Salutation": account_salutation,
#             })
#         else:
#             member["IsProposerInsured"] = "0"

#         coverage_list = []
#         for coverage_name, defaults in COVERAGES.items():
#             item = {"Type": coverage_name, **defaults}
#             item["Indicator"] = "1" if coverage_name in selected else "0"
#             coverage_list.append(item)

#         risks.append({
#             "member": {
#                 key: value for key, value in member.items()
#                 if key != "SequenceID"
#             },
#             "Questions": questions(),
#             "coverage": coverage_list,
#             "SequenceID": str(i + 1),
#         })

#     address1 = data.get("address1", "Houseno.61")
#     address2 = data.get("address2", "MotheNagaon")
#     address3 = data.get("address3", "NearGaneshMandir")
#     city = data.get("city", "Mumbai")
#     state = data.get("state", "MHIN")
#     pincode = data.get("pincode", "400010")
#     full_address = data.get(
#         "address",
#         f"{address1},{address2},{address3},{city},{pincode},Maharashtra"
#     )

#     normalized_name = account_name.replace(" ", "")
#     first_name = data.get(
#         "first_name",
#         account_name.split()[0] if account_name else "SAKUNTHALA"
#     )
#     short_name = data.get(
#         "short_name",
#         account_name.split()[-1][0] if len(account_name.split()) > 1 else "P"
#     )

#     payload = {
#         "session": {
#             "data": {
#                 "account": {
#                     "DOBAsPerPehchaan": account_dob,
#                     "communication": {
#                         "EmailId": data.get("email", "ub@hdfcergo.com"),
#                         "Mobile": data.get("mobile", "9930247107"),
#                     },
#                     "intermediarydetails": {
#                         "SP_PospCode": data.get("sp_posp_code")
#                     },
#                     "nominee": {
#                         "AddressSameAsProposer": data.get(
#                             "nominee_address_same", "Yes"
#                         ),
#                         "NomineeName": data.get("nominee_name", "Nisha Patil"),
#                         "Address": data.get("nominee_address", full_address),
#                         "NomineeDOB": data.get("nominee_dob", "1989-06-24"),
#                         "NomineeAge": data.get("nominee_age", "36.00"),
#                         "NomineeRelationship": data.get(
#                             "nominee_relationship", "Wife"
#                         ),
#                     },
#                     "Salutation": account_salutation,
#                     "NameAsPerPehchaanID": data.get(
#                         "name_as_per_pehchaan", normalized_name
#                     ),
#                     "OtherIndustryType": data.get("other_industry_type", ""),
#                     "DateOfBirth": account_dob,
#                     "PehchaanIDStatus": data.get(
#                         "pehchaan_status", "approved"
#                     ),
#                     "SourceOfIncome": data.get("source_of_income", ""),
#                     "MaritalStatus": data.get("marital_status", "S"),
#                     "LimitMoreThanFiveLakhs": data.get(
#                         "limit_more_than_five_lakhs", "0"
#                     ),
#                     "SourceOfFunds": data.get("source_of_funds"),
#                     "PhysicalPolicyCopyrequired": data.get(
#                         "physical_policy_copy_required", "0"
#                     ),
#                     "CISAcknowledgement": data.get(
#                         "cis_acknowledgement", "No"
#                     ),
#                     "Nationality": data.get("nationality", "INDI"),
#                     "Gender": account_gender,
#                     "PoliticallyExposed": data.get(
#                         "politically_exposed", "0"
#                     ),
#                     "NRIDiscount": data.get("nri_discount", "0"),
#                     "Name": short_name,
#                     "kyc": {
#                         "IsKYCVerified": data.get("kyc_verified", "1")
#                     },
#                     "CKYCNumber": data.get("ckyc_number", ""),
#                     "AnnualIncome": data.get(
#                         "annual_income", "15-20Lacs"
#                     ),
#                     "refunddetails": {
#                         "BankAccountNumber": data.get(
#                             "bank_account", "178293738399"
#                         ),
#                         "BranchName": data.get(
#                             "branch", "ERNAKULAMCOCHIN"
#                         ),
#                         "ChequeAmount": data.get("cheque_amount"),
#                         "NameAsInBankAccount": data.get(
#                             "bank_account_name", normalized_name
#                         ),
#                         "IFSCCode": data.get("ifsc", "ICIC0000010"),
#                         "BankName": data.get(
#                             "bank_name", "ICICIBANKLIMITED"
#                         ),
#                     },
#                     "CriminalProceedingDetails": data.get(
#                         "criminal_proceeding_details"
#                     ),
#                     "LimitMoreThanTwoLakhs": data.get(
#                         "limit_more_than_two_lakhs", "0"
#                     ),
#                     "OtherEducation": data.get("other_education", ""),
#                     "CriminalProceedingInPast3Years": data.get(
#                         "criminal_proceeding_past_3_years", "0"
#                     ),
#                     "address": {
#                         "Permanent": {
#                             "Address3": address3,
#                             "Address2": address2,
#                             "State": state,
#                             "City": city,
#                             "Pincode": pincode,
#                             "Address1": address1,
#                         },
#                         "Correspondence": {
#                             "City": city,
#                             "Address1": data.get(
#                                 "correspondence_address1", "Houseno. 61"
#                             ),
#                             "Address3": data.get(
#                                 "correspondence_address3",
#                                 "Near Ganesh Mandir"
#                             ),
#                             "State": state,
#                             "Pincode": pincode,
#                             "Address2": data.get(
#                                 "correspondence_address2", "Mothe Nagaon"
#                             ),
#                         },
#                     },
#                     "IndustryType": data.get("industry_type", ""),
#                     "FirstName": first_name,
#                     "PehchaanID": data.get(
#                         "pehchaan_id", "UC4VNKAALM"
#                     ),
#                     "PartyType": data.get("party_type", "P"),
#                     "TypeOfBusiness": data.get(
#                         "type_of_business", "Intermediary"
#                     ),
#                     "PANNumber": data.get("pan", "CYUPS5288Q"),
#                     "ResidentialStatus": data.get(
#                         "residential_status", "ResidentIndian"
#                     ),
#                     "MiddleName": data.get("middle_name", ""),
#                     "InvestableAssets": data.get(
#                         "investable_assets", "0"
#                     ),
#                     "Education": data.get(
#                         "education", "PostGraduate"
#                     ),
#                     "Occupation": data.get("occupation", "231"),
#                     "IsPermanentAddressSameAsCorrespondence": data.get(
#                         "same_address", "0"
#                     ),
#                 },
#                 "policy": {
#                     "line": {"risk": risks},
#                     "ProposalDate": data.get("proposal_date"),
#                     "PolicyType": data.get("policy_type", "Floater"),
#                     "Plan": data.get("plan", "OptimaSecure"),
#                     "bancassurance": {
#                         "LosNoLanAan": data.get("los_no_lan_aan"),
#                         "BankBranchID": data.get("bank_branch_id"),
#                         "SavingBankAccount": data.get(
#                             "saving_bank_account"
#                         ),
#                         "LCCode": data.get("lc_code"),
#                         "Funded": data.get("funded", "0"),
#                         "CustomerID": data.get("customer_id"),
#                         "LGCode": data.get("lg_code"),
#                         "LOSCode": data.get("los_code"),
#                     },
#                     "EffectiveTime": data.get(
#                         "effective_time", "03:30PM"
#                     ),
#                     "Product": data.get("product", "OptimaSecure"),
#                     "Term": data.get("term", "12"),
#                     "EMI": data.get("emi", "0"),
#                     "ChildSplitFlag": data.get(
#                         "child_split_flag", "0"
#                     ),
#                     "UserID": data.get(
#                         "user_id", "AKSHAY.JAINPOS"
#                     ),
#                     "InstallmentFrequencyOpted": data.get(
#                         "installment_frequency", "HEGI_ACT_P1"
#                     ),
#                     "EffectiveDate": data.get("effective_date"),
#                     # "FamilyType": family_type_from_members(risks),
#                     "FamilyType":
#                     (
#                         "1A"
#                         if policy_type == "Individual"
#                         else family_type_from_members(risks)
#                     ),
#                     "OriginatingSystem": data.get(
#                         "originating_system", "1UP"
#                     ),
#                     "SuppressEmailSMS": data.get(
#                         "suppress_email_sms", "1"
#                     ),
#                     "TransactionType": data.get(
#                         "transaction_type", "New"
#                     ),
#                     "IsEmployeeDiscountApplicable": data.get(
#                         "employee_discount", "0"
#                     ),
#                     "IsProposal": data.get("is_proposal", "0"),
#                     "IsLoyaltyDiscountApplicable": data.get(
#                         "loyalty_discount", "0"
#                     ),
#                 },
#                 "InstallmentSchedule": {
#                     "ProvidePayPlan": data.get(
#                         "provide_pay_plan", "1"
#                     )
#                 },
#                 "newquoteselection": {
#                     "Vertical": data.get(
#                         "vertical", "101011000"
#                     ),
#                     "Intermediary": data.get(
#                         "intermediary", "200798503757"
#                     ),
#                 },
#             },
#             "@clientId": data.get("client_id", ""),
#             "@id": data.get("id", ""),
#         }
#     }
#     return payload

# @app.route('/')
# def index():
#     return render_template('index.html', coverages=list(COVERAGES), relations=list(RELATIONS))

# @app.post('/api/random-family')
# def api_random_family():
#     data = request.get_json(force=True)
#     rels = random_family(data.get('member_count',1), data.get('gender','M'))
#     return {'relationships':rels, 'members':[mock_member(i+1,r,data.get('sum_insured','1000000')) for i,r in enumerate(rels)]}

# @app.post('/api/generate')
# def api_generate():
#     return build_payload(request.get_json(force=True))

# @app.post('/download')
# def download():
#     payload = request.get_json(force=True)
#     f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
#     json.dump(payload, f, indent=2, ensure_ascii=False); f.close()
#     return send_file(f.name, as_attachment=True, download_name='quote_scenario.json')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, send_file
from datetime import date, timedelta
import json, random, tempfile, re
import os


app = Flask(__name__)

RELATIONS = {
    'Self': dict(gender='M', salutation='MR', age=(25,55), height=(160,185), weight=(55,95), proposer='1'),
    'Wife': dict(gender='F', salutation='MRS', age=(23,52), height=(148,175), weight=(45,80), proposer='0'),
    'Husband': dict(gender='M', salutation='MR', age=(25,58), height=(160,188), weight=(58,100), proposer='0'),
    'Father': dict(gender='M', salutation='MR', age=(50,75), height=(155,180), weight=(55,90), proposer='0'),
    'Mother': dict(gender='F', salutation='MRS', age=(48,72), height=(145,170), weight=(45,82), proposer='0'),
    'Son': dict(gender='M', salutation='MASTER', age=(3,24), height=(95,178), weight=(15,75), proposer='0'),
    'Daughter': dict(gender='F', salutation='MISS', age=(3,24), height=(95,170), weight=(15,68), proposer='0'),
}

COVERAGES = {
    'MyHealthCriticalIllness': {'Indicator':'0','SumInsured':0,'PlanName':'7'},
    'IndividualPersonalAccidentRider': {'Indicator':'0'},
    'OptimaWellbeing': {'Indicator':'0'},
    'MyHealthHospitalCashBenefit': {'Indicator':'0','IsGlobal':'0','SumInsured':1000},
    'UnlimitedRestoreRider': {'Indicator':'0'},
    'ProtectorRider': {'Indicator':'0'},
    'HospitalDailyCashRider': {'Indicator':'0','SumInsured':0},
    'OverseasTravelSecure': {'Indicator':'0'},
    'AggregateDeductible': {'Indicator':'0','DeductibleValue':'25000'},
    'ProtectBenefit': {'Indicator':'0'},
    'PlusBenefit': {'Indicator':'0'},
    'PEDWaiting': {'Indicator':'0','PeriodDuration':'0'},
    'Parenthood': {'Indicator':'0','SumInsured':0},
    'Limitless': {'Indicator':'0'},
    'ABCD': {'Indicator':'0'},
}

FIRST_NAMES = {
    'M':['Aarav','Vihaan','Arjun','Rohan','Kabir','Aditya','Gitesh','Rahul'],
    'F':['Anaya','Nisha','Aditi','Meera','Isha','Kavya','Priya','Saanvi']
}
LAST_NAMES = ['Patil','Sharma','Jain','Mehta','Nair','Deshmukh','Kulkarni','Verma']


# Supported family combinations.
# A = Adult, C = Child. Maximum total members is 8.
FAMILY_TYPES = []
for total_members in range(1, 9):
    for adults in range(1, min(4, total_members) + 1):
        children = total_members - adults
        if children == 0:
            FAMILY_TYPES.append(f"{adults}A")
        else:
            FAMILY_TYPES.append(f"{adults}A+{children}C")


def parse_family_type(value):
    """Return (adult_count, child_count) from values such as 2A or 2A+1C."""
    value = str(value or "1A").strip().upper()
    match = re.fullmatch(r"(\d+)A(?:\+(\d+)C)?", value)
    if not match:
        return 1, 0

    adults = max(1, int(match.group(1)))
    children = int(match.group(2) or 0)

    # Keep the application limit at eight total members.
    if adults + children > 8:
        children = max(0, 8 - adults)

    return adults, children


def random_family_from_type(family_type, proposer_gender="M"):
    """
    Generate relationships that exactly match FamilyType.
    Example: 2A+2C -> Self, Wife/Husband, Son/Daughter, Son/Daughter.
    """
    adults, children = parse_family_type(family_type)

    spouse = "Wife" if proposer_gender == "M" else "Husband"
    adult_pool = [spouse, "Father", "Mother"]
    child_pool = ["Son", "Daughter"]

    relationships = ["Self"]

    # Add the requested number of adults.
    remaining_adults = adults - 1
    random.shuffle(adult_pool)
    relationships.extend(adult_pool[:remaining_adults])

    # This should rarely be needed because FamilyType supports up to 4 adults.
    while len(relationships) < adults:
        relationships.append(random.choice(["Father", "Mother"]))

    # Add the requested number of children.
    for _ in range(children):
        relationships.append(random.choice(child_pool))

    return relationships


def dob_from_age(age):
    today = date.today()
    return date(today.year-age, random.randint(1,12), random.randint(1,28)).isoformat()


def random_family(count, proposer_gender='M'):
    count = max(1, min(int(count), 8))
    spouse = 'Wife' if proposer_gender == 'M' else 'Husband'
    pool = [spouse, 'Son', 'Daughter', 'Father', 'Mother']
    result = ['Self']
    while len(result) < count:
        relation = random.choice(pool)
        if relation in ['Wife','Husband','Father','Mother'] and relation in result:
            continue
        result.append(relation)
    return result


def mock_member(sequence, relation, sum_insured='1000000'):
    p = RELATIONS.get(relation, RELATIONS['Self'])
    age = random.randint(*p['age'])
    gender = p['gender']
    return {
        'SequenceID': str(sequence),
        'IsProposerInsured': '1' if sequence == 1 else p['proposer'],
        'Nationality': 'INDI', 'MaritalStatus': 'S', 'OptFor': '',
        'InsuredLevel80DCertificate': False,
        'RelationshipWithProposer': relation,
        'ResidentialStatus': 'ResidentIndian', 'SumInsured': str(sum_insured),
        'Height': f"{random.uniform(*p['height']):.2f}", 'Gender': gender,
        'MemberDOB': dob_from_age(age), 'Salutation': p['salutation'],
        'Weight': f"{random.uniform(*p['weight']):.2f}",
        'InsuredName': f"{random.choice(FIRST_NAMES[gender])} {random.choice(LAST_NAMES)}",
        'MedicalAdversity': '0', 'IsPoliticallyExposedPerson': '0'
    }


def questions():
    return {'MedicalQuestions': {'LifeStyleQ': {'Lifestylehabits':'0'}, 'Primary': [
        {'Id': q, 'Indicator':'0'} for q in ['ADD','SG','MR','IFT','HIP','PRG','DDAC']
    ]}}


def family_type_from_members(risks):
    child_relations = {"Son", "Daughter"}
    children = sum(
        1 for risk in risks
        if risk["member"].get("RelationshipWithProposer") in child_relations
    )
    adults = len(risks) - children
    if children:
        return f"{adults}A+{children}C"
    return f"{adults}A"


def build_payload(data):
    proposer_gender = data.get("gender", "M")
    policy_type = data.get("policy_type", "Floater")

    # PolicyType and FamilyType are independent.
    # Both Individual and Floater may contain multiple members.
    family_type = data.get("family_type", "1A")
    adult_count, child_count = parse_family_type(family_type)
    member_count = adult_count + child_count

    relationships = (
        data.get("relationships")
        or random_family_from_type(family_type, proposer_gender)
    )
    selected = set(data.get("coverages", []))
    member_overrides = data.get("members", [])

    account_name = data.get("name", "SAKUNTHALA P").strip()
    account_dob = data.get("dob", "1987-09-07")
    account_gender = proposer_gender
    account_salutation = data.get(
        "salutation",
        "MR" if account_gender == "M" else "MRS"
    )

    risks = []
    for i in range(member_count):
        relation = relationships[i] if i < len(relationships) else "Other"
        member = mock_member(i + 1, relation, data.get("sum_insured", "1000000"))

        if i < len(member_overrides):
            member.update({
                k: v for k, v in member_overrides[i].items()
                if v not in (None, "")
            })

        # Proposer member must always match account-level identity.
        if i == 0:
            member.update({
                "IsProposerInsured": "1",
                "RelationshipWithProposer": "Self",
                "InsuredName": account_name.replace(" ", ""),
                "MemberDOB": account_dob,
                "Gender": account_gender,
                "Salutation": account_salutation,
            })
        else:
            member["IsProposerInsured"] = "0"

        coverage_list = []
        for coverage_name, defaults in COVERAGES.items():
            item = {"Type": coverage_name, **defaults}
            item["Indicator"] = "1" if coverage_name in selected else "0"
            coverage_list.append(item)

        risks.append({
            "member": {
                key: value for key, value in member.items()
                if key != "SequenceID"
            },
            "Questions": questions(),
            "coverage": coverage_list,
            "SequenceID": str(i + 1),
        })

    address1 = data.get("address1", "Houseno.61")
    address2 = data.get("address2", "MotheNagaon")
    address3 = data.get("address3", "NearGaneshMandir")
    city = data.get("city", "Mumbai")
    state = data.get("state", "MHIN")
    pincode = data.get("pincode", "400010")
    full_address = data.get(
        "address",
        f"{address1},{address2},{address3},{city},{pincode},Maharashtra"
    )

    normalized_name = account_name.replace(" ", "")
    first_name = data.get(
        "first_name",
        account_name.split()[0] if account_name else "SAKUNTHALA"
    )
    short_name = data.get(
        "short_name",
        account_name.split()[-1][0] if len(account_name.split()) > 1 else "P"
    )

    payload = {
        "session": {
            "data": {
                "account": {
                    "DOBAsPerPehchaan": account_dob,
                    "communication": {
                        "EmailId": data.get("email", "ub@hdfcergo.com"),
                        "Mobile": data.get("mobile", "9930247107"),
                    },
                    "intermediarydetails": {
                        "SP_PospCode": data.get("sp_posp_code")
                    },
                    "nominee": {
                        "AddressSameAsProposer": data.get(
                            "nominee_address_same", "Yes"
                        ),
                        "NomineeName": data.get("nominee_name", "Nisha Patil"),
                        "Address": data.get("nominee_address", full_address),
                        "NomineeDOB": data.get("nominee_dob", "1989-06-24"),
                        "NomineeAge": data.get("nominee_age", "36.00"),
                        "NomineeRelationship": data.get(
                            "nominee_relationship", "Wife"
                        ),
                    },
                    "Salutation": account_salutation,
                    "NameAsPerPehchaanID": data.get(
                        "name_as_per_pehchaan", normalized_name
                    ),
                    "OtherIndustryType": data.get("other_industry_type", ""),
                    "DateOfBirth": account_dob,
                    "PehchaanIDStatus": data.get(
                        "pehchaan_status", "approved"
                    ),
                    "SourceOfIncome": data.get("source_of_income", ""),
                    "MaritalStatus": data.get("marital_status", "S"),
                    "LimitMoreThanFiveLakhs": data.get(
                        "limit_more_than_five_lakhs", "0"
                    ),
                    "SourceOfFunds": data.get("source_of_funds"),
                    "PhysicalPolicyCopyrequired": data.get(
                        "physical_policy_copy_required", "0"
                    ),
                    "CISAcknowledgement": data.get(
                        "cis_acknowledgement", "No"
                    ),
                    "Nationality": data.get("nationality", "INDI"),
                    "Gender": account_gender,
                    "PoliticallyExposed": data.get(
                        "politically_exposed", "0"
                    ),
                    "NRIDiscount": data.get("nri_discount", "0"),
                    "Name": short_name,
                    "kyc": {
                        "IsKYCVerified": data.get("kyc_verified", "1")
                    },
                    "CKYCNumber": data.get("ckyc_number", ""),
                    "AnnualIncome": data.get(
                        "annual_income", "15-20Lacs"
                    ),
                    "refunddetails": {
                        "BankAccountNumber": data.get(
                            "bank_account", "178293738399"
                        ),
                        "BranchName": data.get(
                            "branch", "ERNAKULAMCOCHIN"
                        ),
                        "ChequeAmount": data.get("cheque_amount"),
                        "NameAsInBankAccount": data.get(
                            "bank_account_name", normalized_name
                        ),
                        "IFSCCode": data.get("ifsc", "ICIC0000010"),
                        "BankName": data.get(
                            "bank_name", "ICICIBANKLIMITED"
                        ),
                    },
                    "CriminalProceedingDetails": data.get(
                        "criminal_proceeding_details"
                    ),
                    "LimitMoreThanTwoLakhs": data.get(
                        "limit_more_than_two_lakhs", "0"
                    ),
                    "OtherEducation": data.get("other_education", ""),
                    "CriminalProceedingInPast3Years": data.get(
                        "criminal_proceeding_past_3_years", "0"
                    ),
                    "address": {
                        "Permanent": {
                            "Address3": address3,
                            "Address2": address2,
                            "State": state,
                            "City": city,
                            "Pincode": pincode,
                            "Address1": address1,
                        },
                        "Correspondence": {
                            "City": city,
                            "Address1": data.get(
                                "correspondence_address1", "Houseno. 61"
                            ),
                            "Address3": data.get(
                                "correspondence_address3",
                                "Near Ganesh Mandir"
                            ),
                            "State": state,
                            "Pincode": pincode,
                            "Address2": data.get(
                                "correspondence_address2", "Mothe Nagaon"
                            ),
                        },
                    },
                    "IndustryType": data.get("industry_type", ""),
                    "FirstName": first_name,
                    "PehchaanID": data.get(
                        "pehchaan_id", "UC4VNKAALM"
                    ),
                    "PartyType": data.get("party_type", "P"),
                    "TypeOfBusiness": data.get(
                        "type_of_business", "Intermediary"
                    ),
                    "PANNumber": data.get("pan", "CYUPS5288Q"),
                    "ResidentialStatus": data.get(
                        "residential_status", "ResidentIndian"
                    ),
                    "MiddleName": data.get("middle_name", ""),
                    "InvestableAssets": data.get(
                        "investable_assets", "0"
                    ),
                    "Education": data.get(
                        "education", "PostGraduate"
                    ),
                    "Occupation": data.get("occupation", "231"),
                    "IsPermanentAddressSameAsCorrespondence": data.get(
                        "same_address", "0"
                    ),
                },
                "policy": {
                    "line": {"risk": risks},
                    "ProposalDate": data.get("proposal_date"),
                    "PolicyType": policy_type,
                    "Plan": data.get("plan", "OptimaSecure"),
                    "bancassurance": {
                        "LosNoLanAan": data.get("los_no_lan_aan"),
                        "BankBranchID": data.get("bank_branch_id"),
                        "SavingBankAccount": data.get(
                            "saving_bank_account"
                        ),
                        "LCCode": data.get("lc_code"),
                        "Funded": data.get("funded", "0"),
                        "CustomerID": data.get("customer_id"),
                        "LGCode": data.get("lg_code"),
                        "LOSCode": data.get("los_code"),
                    },
                    "EffectiveTime": data.get(
                        "effective_time", "03:30PM"
                    ),
                    "Product": data.get("product", "OptimaSecure"),
                    "Term": data.get("term", "12"),
                    "EMI": data.get("emi", "0"),
                    "ChildSplitFlag": data.get(
                        "child_split_flag", "0"
                    ),
                    "UserID": data.get(
                        "user_id", "AKSHAY.JAINPOS"
                    ),
                    "InstallmentFrequencyOpted": data.get(
                        "installment_frequency", "HEGI_ACT_P1"
                    ),
                    "EffectiveDate": data.get("effective_date"),
                    "FamilyType": family_type,
                    "OriginatingSystem": data.get(
                        "originating_system", "1UP"
                    ),
                    "SuppressEmailSMS": data.get(
                        "suppress_email_sms", "1"
                    ),
                    "TransactionType": data.get(
                        "transaction_type", "New"
                    ),
                    "IsEmployeeDiscountApplicable": data.get(
                        "employee_discount", "0"
                    ),
                    "IsProposal": data.get("is_proposal", "0"),
                    "IsLoyaltyDiscountApplicable": data.get(
                        "loyalty_discount", "0"
                    ),
                },
                "InstallmentSchedule": {
                    "ProvidePayPlan": data.get(
                        "provide_pay_plan", "1"
                    )
                },
                "newquoteselection": {
                    "Vertical": data.get(
                        "vertical", "101011000"
                    ),
                    "Intermediary": data.get(
                        "intermediary", "200798503757"
                    ),
                },
            },
            "@clientId": data.get("client_id", ""),
            "@id": data.get("id", ""),
        }
    }
    return payload

@app.route('/')
def index():
    return render_template(
        'index.html',
        coverages=list(COVERAGES),
        relations=list(RELATIONS),
        family_types=FAMILY_TYPES
    )

@app.post('/api/random-family')
def api_random_family():
    data = request.get_json(force=True)
    family_type = data.get('family_type', '1A')
    rels = random_family_from_type(
        family_type,
        data.get('gender', 'M')
    )
    return {
        'relationships': rels,
        'members': [
            mock_member(
                i + 1,
                relation,
                data.get('sum_insured', '1000000')
            )
            for i, relation in enumerate(rels)
        ]
    }

@app.post('/api/generate')
def api_generate():
    return build_payload(request.get_json(force=True))

@app.post('/download')
def download():
    payload = request.get_json(force=True)
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
    json.dump(payload, f, indent=2, ensure_ascii=False); f.close()
    return send_file(f.name, as_attachment=True, download_name='quote_scenario.json')

# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )
