from datetime import datetime


class Utils:
    @classmethod    
    def transaction_headers(cls) -> list[str]:
        """
        This method generates the column headers used for each transaction
        :return: A list of the headers for the transaction made by each user
        """
        return ['Account', 'Amount', 'Description', 'Available Balance', 'Date']
    
    @classmethod
    def model_headers(cls) -> list[str]:
        """
        This method generates the column headers used to model each user
        :return: A list of the headers for the model of the users in the bank
        """
        return ['Name', 'BVN', 'Email', 'Account', 'Pin', 'Password', 'Pin-Salt', 'Password-Salt']

    @classmethod
    def get_datetime(cls) -> str:
        """
        This method generates a current datetime stamp for each transaction per user
        :return: A string representation of the current datetime object
        """
        date, time = datetime.now().__str__().split(' ')
        hour, minute, _ = time.split(':')
        return f'{date} {hour}:{minute}'
