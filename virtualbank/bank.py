from user import User
from os import listdir
from utils import Utils
from data_io import Model_IO
from bank_model import Bank_Model
from typing import Mapping, Union


class Bank:
    def __init__(self, name: str) -> None:
        if name.isalpha() and name not in self.model_db():
            self.model = Bank_Model()
            self.model.name = name
        else:
            raise NameError("Bank name exists or must be alphabetical only!")

        self.data: Mapping[str, list[Mapping[str, Union[str, int]]]] = {
            'models': list()
        }
        self.model_io = Model_IO(f'./db/{self.model.name}.csv')
        self.model_io.import_data(self.data)
        self.sort_models()

    def model_db(self) -> list[str]:
        return [file for file in listdir('./db/') if file.split('.')[0].isalpha()]

    def sort_models(self) -> None:
        self.data['models'] = sorted(self.data['models'], key=lambda model: model['Name'])
        
    def get_model(self, acc_num: str) -> Mapping[str, Union[str, int]]:
        if acc_num.isdigit():
            if self.data['models']:
                for model in self.data['models']:
                    if acc_num in model.values():
                        return model
            
    def new_model(self, name: str, bvn: str, email: str, acc_num: str, pin: int, password: int, pin_salt: str, password_salt: str) -> None:
        model: Mapping[str, Union[str, int]] = dict(zip(
            Utils.model_headers(),
            [
                name,
                bvn,
                email,
                acc_num,
                pin,
                password,
                pin_salt.decode(),
                password_salt.decode()
            ]
        ))
        self.data['models'].append(model)
        self.sort_models()
        self.model_io.export_data(self.data)
        
    def get_currency(self) -> str: return self.model.currency
        
    def register(self, user: User) -> None:
        print(f'\nRegistering {user.get_account_name()} in {self.model.name}...')
        self.model.users = user
        
    def login(self, user: User) -> None:
        if user.auth():
            print(f'\nLogging {user.get_account_name()} in {self.model.name}...')
            self.model.auth_users = user
            
    def get_users(self) -> None: self.model.users
        
    def get_auth_users(self) -> None: self.model.auth_users
            
    def validate(self, user: User) -> bool:
        return self.model.validate(user)

    def transfer(self, sender: User, receiver: User) -> None:
        print(f'\nTransfer amount must exceed {self.get_currency()}100.00')
        amount: str = input('Amount: ').strip()

        if amount.split('.')[0].isdigit() and amount.split('.')[1].isdigit():
            amount: float = float(amount)
            if amount >= 100:
                if isinstance(sender, User) and isinstance(receiver, User):
                    sender.transfer(amount=amount, callback=False)
                    receiver.transfer(amount=amount, callback=True)
            else:
                print(f'Transfer amount must exceed {self.get_currency()}100.00')
        else: raise ValueError("Verify Amount!")
    