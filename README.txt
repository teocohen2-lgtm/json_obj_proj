FULL QUOTE → PAYMENT → ISSUE POLICY → RENEWAL PROJECT

NO FILE REPLACEMENT IS REQUIRED.

PROJECT CONTENTS
- app.py
- templates/index.html
- requirements.txt
- .env.example
- run_local.sh
- run_local.bat
- Procfile
- render.yaml
- .gitignore

UBUNTU / LINUX LOCAL RUN

1. Extract this ZIP.
2. Open terminal inside the extracted folder.
3. Run:

   chmod +x run_local.sh
   ./run_local.sh

4. The first run creates .env.
5. Open .env and enter:

   API_CLIENT_ID=...
   API_CLIENT_SECRET=...

6. Run again:

   ./run_local.sh

7. Open:

   http://127.0.0.1:5000


MANUAL LOCAL RUN

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

Add credentials to .env, then:

python app.py


WINDOWS LOCAL RUN

Double-click:

run_local.bat

Then edit the created .env and run run_local.bat again.


EXACT CREATE QUOTE → CREATE PAYMENT MAPPING

QuoteID:
response.session["@id"]

ClientID:
response.session["@clientId"]

QuoteNumber:
response.session.data.policy.QuoteNumber

PremiumAmount:
response.session.data.policy.line.Premium

InstrumentDate:
response.session.data.policy.EffectiveDate


CREATE PAYMENT BODY

PayorPartyId = ClientID
QuoteId = QuoteID
QuoteNumber = QuoteNumber
Remarks = QuoteNumber
Instrumentamount = PremiumAmount
InstrumentDate = InstrumentDate


CREATE PAYMENT → ISSUE POLICY

SuspenseID:
createPaymentResponse[0].session.data.CreatePaymentResponse
.PaymentDetail.PaymentAllocations.PaymentAllocation.DestinationId

Issue Policy:
ProposalId = QuoteID
SuspenseId = SuspenseID


ISSUE POLICY → RENEWAL

PolicyNumber:
response.session.data.policy.PolicyNumber

Renewal policyNumber:
PolicyNumber + "00"


DEBUG FILES CREATED AUTOMATICALLY

actual_create_quote_request.json
actual_create_quote_response.json
actual_create_payment_request.json
actual_create_payment_response.json


BUTTON FIX

The Run Complete Policy Flow button previously failed because index.html
still referenced deleted elements:

- paymentDate
- paymentAmount

Those references have now been removed.

Create Payment now uses:
- InstrumentDate from Create Quote response policy.EffectiveDate
- Instrumentamount from Create Quote response policy.line.Premium
- InstrumentNumber from the existing UI input
- MandateId from the existing UI input

No manual Payment Date or Payment Amount fields are required.

If a frontend JavaScript error occurs, it will now appear directly inside
the workflow output panel instead of silently doing nothing.
