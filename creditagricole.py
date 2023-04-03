from datetime import datetime, timedelta

from creditagricole_particuliers import Authenticator, Accounts
from constant import *

class CreditAgricoleClient:
    def __init__(self, logger):
        self.logger = logger
        self.department = BANK_DEPARTMENT_DEFAULT
        self.account_id = BANK_ACCOUNT_ID_DEFAULT
        self.password = BANK_PASSWORD_DEFAULT
        self.enabled_accounts = IMPORT_ACCOUNT_ID_LIST_DEFAULT
        self.get_transactions_period = GET_TRANSACTIONS_PERIOD_DAYS_DEFAULT
        self.max_transactions = MAX_TRANSACTIONS_PER_GET_DEFAULT
        self.session = None

    def validate(self):
        if self.department == BANK_DEPARTMENT_DEFAULT:
            self.logger.error("Please set your bank account department.")
        if (
            not self.account_id.isdigit()
            or len(self.account_id) != len(BANK_ACCOUNT_ID_DEFAULT)
            or self.account_id == BANK_ACCOUNT_ID_DEFAULT
        ):
            self.logger.error("Your bank account ID must be a 11 long digit.")
        if (
            not self.password.isdigit()
            or len(self.password) != len(BANK_PASSWORD_DEFAULT)
            or self.password == BANK_PASSWORD_DEFAULT
        ):
            self.logger.error("Your bank password must be a 6 long digit.")
        if self.enabled_accounts == IMPORT_ACCOUNT_ID_LIST_DEFAULT:
            self.logger.error("Please set your account ID list to import.")
        if (
            not self.get_transactions_period.isdigit()
            or int(self.get_transactions_period) < 0
        ):
            self.logger.error(
                "Your transactions's get period must be a positive number."
            )
        if not self.max_transactions.isdigit() or int(self.max_transactions) < 0:
            self.logger.error(
                "The maximum number of transactions to get must be a positive number."
            )

    def init_session(self):
        password_list = []
        for i in range(len(self.password)):
            password_list.append(int(self.password[i]))
        self.session = Authenticator(
            username=self.account_id, password=password_list, department=self.department
        )

    def get_accounts(self):
        accounts = []
        for account in Accounts(session=self.session):
            if account.numeroCompte in [
                x.strip() for x in self.enabled_accounts.split(",")
            ]:
                accounts.append(account)
        return accounts

    def get_transactions(self, account_id):
        account = Accounts(session=self.session).search(num=account_id)

        current_date = datetime.today()
        previous_date = current_date - timedelta(days=int(self.get_transactions_period))
        date_stop_ = current_date.strftime("%Y-%m-%d")
        date_start_ = previous_date.strftime("%Y-%m-%d")

        return [
            op.descr
            for op in account.get_operations(
                count=int(self.max_transactions),
                date_start=date_start_,
                date_stop=date_stop_,
            )
        ]
