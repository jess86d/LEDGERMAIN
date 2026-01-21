
# The Crucible - Main Application UI
import streamlit as st
from generator import DocumentGenerator
from faker import Faker
import random

st.set_page_config(layout="wide", page_title="Project Legerdemain")
st.title("Project Legerdemain: Document Synthesis Engine")

# Initialize generator and fake data provider
generator = DocumentGenerator()
fake = Faker()

# --- UI Layout ---
st.sidebar.header("Document Type")
doc_type = st.sidebar.radio("Select the document to generate:", 
                            ("Articles of Incorporation", "Bank Statement (6 Months)", "Utility Bill"))

st.header("Seed Data Input")

if doc_type == "Articles of Incorporation":
    st.subheader("Corporate Details")
    corp_name = st.text_input("Corporation Name", fake.company() + " Inc.")
    corp_address = st.text_area("Principal Address", fake.address())
    reg_agent = st.text_input("Registered Agent", fake.name())
    shares = st.number_input("Number of Authorized Shares", 1000, 1000000, 10000)

    if st.button("Forge Articles of Incorporation"):
        data = {
            'corp_name': corp_name, 'corp_address': corp_address.replace('\n', '<br>'),
            'reg_agent': reg_agent, 'shares': f"{shares:,}"
        }
        pdf_file = generator.create_articles(data)
        st.download_button("Download Forged PDF", pdf_file, "articles.pdf")

elif doc_type == "Utility Bill":
    st.subheader("Utility & Customer Details")
    customer_name = st.text_input("Customer Name", fake.name())
    service_address = st.text_area("Service Address", fake.address())
    utility_name = st.selectbox("Utility Company", ["City Power & Light", "County Water District", "Metro Gas Co."])
    account_number = st.text_input("Account Number", fake.bban())
    amount_due = st.number_input("Amount Due", 50.0, 500.0, 124.56)

    if st.button("Forge Utility Bill"):
        data = {
            'customer_name': customer_name, 'service_address': service_address.replace('\n', '<br>'),
            'utility_name': utility_name, 'account_number': account_number,
            'amount_due': f"${amount_due:,.2f}"
        }
        pdf_file = generator.create_utility_bill(data)
        st.download_button("Download Forged PDF", pdf_file, "utility_bill.pdf")

elif doc_type == "Bank Statement (6 Months)":
    st.subheader("Banking Details")
    bank_name = st.selectbox("Bank Name", ["Chase Bank", "Bank of America", "Wells Fargo", "Citibank"])
    account_holder = st.text_input("Account Holder Name", fake.name())
    account_address = st.text_area("Account Address", fake.address())
    account_number = st.text_input("Account Number", fake.bban())
    start_balance = st.number_input("Starting Balance (6 months ago)", 1000.0, 50000.0, 8542.11)

    if st.button("Forge Bank Statements"):
        # Note: This build generates and downloads the *most recent* of the 6 statements.
        # A full version would zip all 6 files.
        st.info("Generating 6 months of transaction data... Downloading the most recent statement.")
        data = {
            'bank_name': bank_name, 'account_holder': account_holder,
            'account_address': account_address.replace('\n', '<br>'),
            'account_number': account_number, 'start_balance': start_balance
        }
        pdf_file = generator.create_bank_statements(data)
        st.download_button("Download Latest Statement PDF", pdf_file, "bank_statement.pdf")
