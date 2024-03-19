from bank import Bank
from user import User
from os import name, system


def main():
    # Creating a bank instance
    bank1: Bank = Bank()

    # Creating two user instances
    user1: User = User(bank1)
    user2: User = User(bank1)

    # Registering the user in the bank
    bank1.register(user1)
    bank1.register(user2)

    # Logging in a user
    user1.login()
    user2.login()

    # Authenticating a user
    bank1.login(user1)
    bank1.login(user2)
    
    # Logging out a user
    # user1.logout()
    # user2.logout()

    # Getting a list of registered users from the bank
    bank1.get_users()

    # Getting a list of authenticated users from the bank
    bank1.get_auth_users()
    
    # Testing deposit functionality
    # user1.deposit()
    # user2.deposit()
    
    # Testing withdrawal functionality
    # user2.withdraw()
    # user2.withdraw()

    # Testing transfer functionality
    bank1.transfer(sender=user1, receiver=user2)

if __name__ == '__main__':
    system('cls' if name == 'nt' else 'clear')
    main()
    