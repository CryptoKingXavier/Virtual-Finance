from os import listdir
from typing import Union
from random import randint


class User_Model:
    def __init__(self) -> None:
        self.__balance: float = float()
        self.__is_connected: bool = False
        self.__bvn: Union[str, None] = None
        self.__email: Union[str, None] = None
        self.__pin: Union[bytes, None] = None
        self.__password: Union[bytes, None] = None
        self.__account_name: Union[str, None] = None
        self.__pin_salt: Union[bytes, str, None] = None
        self.__trans_msg: Union[list[str], None] = None
        self.__passwd_salt: Union[bytes, str, None] = None

        self.__account_number: str = f'07{randint(11_111_111, 99_999_999)}'
        while self.__account_number in self.transaction_db():
            self.__account_number: str = f'07{randint(11_111_111, 99_999_999)}'
            if self.__account_number not in self.transaction_db():
                break

    def transaction_db(self) -> list[str]:
        return [file for file in listdir('./db/') if file.split('.')[0].isdigit()]

    # Bank Verification Number (BVN) getter and setter
    @property
    def bvn(self) -> Union[str, None]: return self.__bvn

    @bvn.setter
    def bvn(self, bvn: str) -> None: self.__bvn = bvn

    # Email getter and setter
    @property
    def email(self) -> Union[str, None]: return self.__email

    @email.setter
    def email(self, email: str) -> None: self.__email = email
    
    # Account number getter and setter
    @property
    def account_number(self) -> str: return self.__account_number
    
    @account_number.setter
    def account_number(self, acc_num: str) -> None: self.__account_number = acc_num
    
    # Account name getter and setter
    @property
    def account_name(self) -> Union[str, None]: return self.__account_name
    
    @account_name.setter
    def account_name(self, acc_name: str) -> None: self.__account_name = acc_name
    
    # Account password getter and setter
    @property
    def password(self) -> Union[str, None]: return self.__password
    
    @password.setter
    def password(self, passwd: str) -> None: self.__password = passwd.encode()
    
    # Account pin getter and setter
    @property
    def pin(self) -> Union[str, None]: return self.__pin
    
    @pin.setter
    def pin(self, pin: str) -> None: self.__pin = pin.encode()
    
    # Password salt getter and setter
    @property
    def password_salt(self) -> Union[bytes, str, None]: return self.__passwd_salt
    
    @password_salt.setter
    def password_salt(self, salt: str) -> None: self.__passwd_salt = salt.encode()
    
    # Pin salt getter and setter
    @property
    def pin_salt(self) -> Union[bytes, str, None] : return self.__pin_salt
    
    @pin_salt.setter
    def pin_salt(self, salt: str) -> None: self.__pin_salt = salt.encode()
    
    # Account balance getter and setter
    @property
    def balance(self) -> Union[float, None]: return self.__balance
    
    @balance.setter
    def balance(self, bal: float) -> None: self.__balance += bal
    
    # Authenticated getter and setter
    @property
    def is_connected(self) -> bool: return self.__is_connected
    
    @is_connected.setter
    def is_connected(self, auth: bool) -> None: self.__is_connected = auth
    
    @property
    def trans_msg(self) -> Union[list[str], None]: 
        return f'\nLatest Transaction Details...\nAcct: {self.__account_number}\nAmt: {self.__trans_msg[0]}\nDesc: {self.__trans_msg[1]}\nAvail Bal: {self.__balance}\nDate: {self.__trans_msg[2]}'
    
    @trans_msg.setter
    def trans_msg(self, msg: list[str]) -> None: self.__trans_msg = msg
    
    def get_details(self) -> str:
        return f"\nFetching Details...\nName: {self.__account_name}\nNumber: {self.__account_number}\nBalance: {self.__balance}\n"
