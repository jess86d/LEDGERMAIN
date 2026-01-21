
# The Alchemist - AI Data Logic Module
import random
import datetime
from faker import Faker
import numpy as np

fake = Faker()

def generate_transactions(start_date, end_date, start_balance, num_transactions):
    transactions = []
    current_balance = start_balance

    # Generate random dates for transactions
    days_in_period = (end_date - start_date).days
    if days_in_period <= 0: days_in_period = 1 # Avoid error on same day
    transaction_dates = sorted([start_date + datetime.timedelta(days=random.randint(0, days_in_period-1)) for _ in range(num_transactions)])

    # Define transaction archetypes
    transaction_types = {
        'debit': ['POS DEBIT - {merchant}', 'ONLINE PAYMENT TO {company}', 'ATM WITHDRAWAL'],
        'credit': ['DIRECT DEPOSIT - {company}', 'INBOUND TRANSFER FROM {person}', 'ZELLE PAYMENT FROM {person}']
    }
    merchants = ['AMAZON', 'WALMART', 'STARBUCKS', 'UBER', 'DOORDASH', 'TARGET', 'CHEVRON']

    for date in transaction_dates:
        trans_type_key = random.choices(['debit', 'credit'], weights=[0.75, 0.25], k=1)[0]

        if trans_type_key == 'debit':
            amount = round(random.uniform(5.50, 450.00), 2)
            description_template = random.choice(transaction_types['debit'])
            description = description_template.format(merchant=random.choice(merchants), company=fake.company())
            current_balance -= amount
        else: # credit
            amount = round(random.uniform(100.00, 3500.00), 2)
            description_template = random.choice(transaction_types['credit'])
            description = description_template.format(company=fake.company(), person=fake.name())
            current_balance += amount

        transactions.append({
            'date': date.strftime('%m/%d/%Y'),
            'description': description,
            'debit': f"${amount:,.2f}" if trans_type_key == 'debit' else '',
            'credit': f"${amount:,.2f}" if trans_type_key == 'credit' else '',
            'balance': f"${current_balance:,.2f}"
        })

    return transactions, current_balance
