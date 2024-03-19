from user import User
from typing import Union


class Bank_Model(User):
    def __init__(self) -> None:
        self.__currency: str = 'NGN'
        self.__users: list[User] = list()
        self.__name: Union[str, None] = None
        self.__auth_users: list[User] = list()
        
    # Bank currency getter
    @property
    def currency(self) -> str: return self.__currency
    
    # Bank name getter and setter
    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, name: str) -> None: self.__name = name
    
    def validate(self, user: User) -> bool:
        if user.auth():
            return True
        else:
            self.__auth_users.remove(user)
            return False

    
    # Bank users getter and setter
    @property
    def users(self) -> None:
        if self.__users:
            print(f'\n{self.__name} Registered Users')
            for id, user in enumerate(self.__users):
                print(f'{id+1}. Name: {user.get_account_name()}, Account Number: {user.get_account_number()}')
        else: print('No Registered Users!')
    
    @users.setter
    def users(self, user: User) -> None: self.__users.append(user)
    
    # Authenticated users getter and setter
    @property
    def auth_users(self) -> None:
        if self.__auth_users:
            print(f'\n{self.__name} Authenticated Users:')
            for id, user in enumerate(self.__auth_users):
                print(f'{id+1}. Name: {user.get_account_name()}, Account Number: {user.get_account_number()}')
        else: print('No Authenticated Users!')
    
    @auth_users.setter
    def auth_users(self, user: User) -> None: self.__auth_users.append(user)
    