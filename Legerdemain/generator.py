# The Forge - Document Generation Engine
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import datetime
from dateutil.relativedelta import relativedelta
from data_logic import generate_transactions
import random
import io

class DocumentGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates/'))

    def _render_to_pdf(self, html_content):
        result = io.BytesIO()
        pisa.CreatePDF(html_content, dest=result)
        return result.getvalue()

    def create_articles(self, data):
        template = self.env.get_template('articles.html')
        html_out = template.render(data)
        return self._render_to_pdf(html_out)

    def create_utility_bill(self, data):
        template = self.env.get_template('utility_bill.html')
        html_out = template.render(data)
        return self._render_to_pdf(html_out)

    def create_bank_statements(self, data):
        statement_period_end = datetime.datetime.now()
        start_balance = data['start_balance']
        
        # We'll just generate the most recent one for the demo
        statement_period_start = statement_period_end - relativedelta(months=1)
        transactions, end_balance = generate_transactions(
            start_date=statement_period_start,
            end_date=statement_period_end,
            start_balance=start_balance,
            num_transactions=random.randint(15, 40)
        )
        
        statement_data = {
            **data,
            'statement_date': statement_period_end.strftime('%B %d, %Y'),
            'period_start': statement_period_start.strftime('%m/%d/%Y'),
            'period_end': statement_period_end.strftime('%m/%d/%Y'),
            'start_balance': f"${start_balance:,.2f}",
            'end_balance': f"${end_balance:,.2f}",
            'transactions': transactions
        }
        
        template = self.env.get_template('statement.html')
        html_out = template.render(statement_data)
        return self._render_to_pdf(html_out)

