from utils import Utils
from typing import Mapping, Union
from user_model import User_Model
from bcrypt import gensalt, hashpw
from data_io import Transaction_IO
from getpass_asterisk.getpass_asterisk import getpass_asterisk


class User:
    def __init__(self, bank) -> None:
        self.bank = bank
        self.model = User_Model()
        self.data: Mapping[str, list[Mapping[str, Union[str, int, float]]]] = {
            'transactions': list()
        }
        self.transaction_io = None
        self.retrieve()
        
    def get_encoded_data(self) -> None:
        print(f"Pin {self.model.pin}")
        print(f"Pin-Salt {self.model.pin_salt}")
        print(f"Password {self.model.password}")
        print(f"Password-Salt {self.model.password_salt}")
    
    def retrieve(self) -> None:
        if input('Login T/F? ').casefold() in ['t', 'true']:
            acc_num: str = input('Account Number: ').strip()

            if acc_num.isdigit():
                self.transaction_io = Transaction_IO(f'./db/{acc_num}.csv')
                self.transaction_io.import_data(self.data)
                model: Mapping[str, Union[str, int]] | None = self.bank.get_model(acc_num)

                if model:
                    temp_trans: list[Mapping[str, Union[str, int]]] = list()

                    for transaction in self.data['transactions']:
                        if acc_num in transaction.values():
                            temp_trans.append(transaction)

                    latest: Mapping[str, Union[str, int, float]] = temp_trans[-1]
                    self.model.pin = model['Pin']
                    self.model.bvn = model['BVN']
                    self.model.email = model['Email']
                    self.model.account_name = model['Name']
                    self.model.password = model['Password']
                    self.model.pin_salt = model['Pin-Salt']
                    self.model.account_number = model['Account']
                    self.model.password_salt = model['Password-Salt']
                    self.model.balance = float(latest['Available Balance'])
                    print(self.model.get_details())
                else:
                    print("Account Doesn't Exist!")
                    self.setup()
            else:
                print("Invalid Account Number! Creating new account...")
                self.setup()
        else:
            self.setup()
        
    def auth(self) -> bool: return self.model.is_connected
    
    def get_account_name(self) -> str: return self.model.account_name
    
    def get_account_number(self) -> str: return self.model.account_number
    
    def setup(self) -> None:
        print('\nCreating New User Instance!')
        account_name: str = input('Account Name: ').strip()
        bvn: str = input('BVN: ').strip()
        passwd_input: str = getpass_asterisk('6-Digit Account Password: ').strip()[:6]
        pin_input: str = getpass_asterisk('4-Digit Transaction Pin: ').strip()[:4]

        if account_name.isalpha() and bvn.isdigit() and passwd_input.isdigit() and pin_input.isdigit():
            self.model.account_name = account_name
            self.model.bvn = bvn
            self.model.email: str = input('Email: ').strip()

            passwd_salt: bytes = gensalt()
            hashed_passwd: str = hashpw(passwd_input.encode(), passwd_salt).decode()
            self.model.password = hashed_passwd

            pin_salt: bytes = gensalt()
            hashed_pin: str = hashpw(pin_input.encode(), pin_salt).decode()
            self.model.pin = hashed_pin

            self.bank.new_model(
                self.model.account_name,
                self.model.bvn,
                self.model.email,
                self.model.account_number,
                self.model.pin,
                self.model.password,
                pin_salt,
                passwd_salt
            )

            self.transaction_io = Transaction_IO(f'./db/{self.model.account_number}.csv')
        else: raise ValueError("Verify either of these: Account Name, BVN, Password, Pin!")
        
    def validate(self) -> bool: return self.bank.validate(self)
    
    def login(self) -> None:
        print(f'\nLogging in {self.model.account_name}...')
        password_input = getpass_asterisk('Account Password: ').strip()[:6]
        if password_input.isdigit():
            if hashpw(password_input.encode(), self.model.password_salt) == self.model.password:
                self.model.is_connected = True
        else: raise ValueError("Verify Account Password!")
        
    def logout(self) -> None:
        print(f'\nLogging out {self.model.account_name}...')
        self.model.is_connected = False
        self.bank.validate(self)

    def transfer(self, amount: float, callback: bool = False) -> None:
        if self.validate() and amount >= 100:
            print('\nProcessing Bank Transfer...')

            # Processing Transfer Details
            description: str = 'Bank Transfer CR' if callback else 'Bank Transfer DR'
            self.model.balance = amount if callback else -amount
            amt: str = f'{self.bank.get_currency()}{amount} CR' if callback else f'{self.bank.get_currency()}{amount} DR'
            date_time = Utils.get_datetime()

            transaction: Mapping[str, Union[str, int, float]] = dict(zip(
                Utils.transaction_headers(),
                [
                    self.model.account_number,
                    amt,
                    description,
                    self.model.balance,
                    date_time
                ]
            ))

            self.data['transactions'].append(transaction)
            self.model.trans_msg = [amt, description, date_time]
            print(self.model.trans_msg)
            self.transaction_io.export_data(self.data)

    def deposit(self) -> None:
        if self.validate():
            print(f'\nProcessing Deposit - Minimum of {self.bank.get_currency()}100.00 should be deposited!')
            amount: str = input('Deposit Amount: ').strip()

            if amount.split('.')[0].isdigit() and amount.split('.')[1].isdigit():
                amount: float = float(amount)
                pin_input = getpass_asterisk('Transaction Pin: ').strip()[:4]
                if hashpw(pin_input.encode(), self.model.pin_salt) == self.model.pin:
                    if amount >= 100:
                        self.model.balance = amount
                        description: str = 'Bank Deposit'
                        date_time = Utils.get_datetime()

                        transaction: Mapping[str, Union[str, int, float]] = dict(zip(
                            Utils.transaction_headers(),
                            [
                                self.model.account_number,
                                f'{self.bank.get_currency()}{amount} CR',
                                description,
                                self.model.balance,
                                date_time
                            ]
                        ))

                        self.data['transactions'].append(transaction)
                        self.model.trans_msg = [amount, description, date_time]
                        print(self.model.trans_msg)
                        self.transaction_io.export_data(self.data)
                else:
                    print('Invalid Pin!')
            else: raise ValueError("Invalid Deposit Amount Format!")
            
    def withdraw(self) -> None:
        if self.validate():
            print(f'\nProcessing Withdrawal - Minimum of {self.bank.get_currency()}100.00 should be left!')
            amount: str = input('Withdrawal Amount: ').strip()

            if amount.split('.')[0].isdigit() and amount.split('.')[1].isdigit():
                amount: float = float(amount)
                pin_input = getpass_asterisk('Transaction Pin: ').strip()[:4]
                if hashpw(pin_input.encode(), self.model.pin_salt) == self.model.pin:
                    if self.model.balance - amount >= 100:
                        self.model.balance = -amount
                        description: str = 'Bank Withdrawal'
                        date_time = Utils.get_datetime()

                        transaction: Mapping[str, Union[str, int, float]] = dict(zip(
                            Utils.transaction_headers(),
                            [
                                self.model.account_number,
                                f'{self.bank.get_currency()}{amount} DR',
                                description,
                                self.model.balance,
                                date_time
                            ]
                        ))

                        self.data['transactions'].append(transaction)
                        self.model.trans_msg = [amount, description, date_time]
                        print(self.model.trans_msg)
                        self.transaction_io.export_data(self.data)
                else:
                    print('Invalid Pin!')
            else: raise ValueError("Invalid Withdrawal Amount Format!")
