from utils import Utils
from os.path import isfile
from csv import DictReader, DictWriter
from typing import Any, Mapping, Union


class Transaction_IO:
    def __init__(self, filename: str) -> None:
        self.file: str = filename

    def import_data(self, data) -> None:
        if isfile(self.file):
            # Fetching data from CSV
            imported_data = list()

            try:
                with open(self.file, 'r') as transactions:
                    transaction_reader = DictReader(transactions)
                    for row in transaction_reader: imported_data.append(row)

                if imported_data:
                    transaction_keys: list[str] = list()
                    for transaction in data['transactions']:
                        transaction_keys.append(transaction['Description'])

                    # Preventing duplicate entries
                    for transaction in imported_data:
                        if transaction['Description'] in transaction_keys: continue
                        else:
                            data['transactions'].append(transaction)
            except PermissionError: print('Reading Denied: Unable to access the file!')

    def export_data(self, data) -> None:
        # Writing data to CSV
        try:
            with open(self.file, 'w', newline='') as transactions:
                fieldnames: list[str] = Utils.transaction_headers()
                transaction_writer = DictWriter(transactions, fieldnames=fieldnames)
                transaction_writer.writeheader()

                for transaction in data['transactions']: transaction_writer.writerow(transaction)
        except PermissionError: print('Writing Denied: Unable to access the file!')


class Model_IO:
    def __init__(self, filename: str) -> None:
        self.file: str = filename

    def import_data(self, data) -> None:
        if isfile(self.file):
            # Fetching data from CSV
            imported_data = list()

            try:
                with open(self.file, 'r') as models:
                    model_reader = DictReader(models)
                    for row in model_reader: imported_data.append(row)

                if imported_data:
                    model_keys: list[str] = list()
                    for model in data['models']:
                        model_keys.append(model['Account'])

                    # Preventing duplicate entries
                    for model in imported_data:
                        if model['Account'] in model_keys: continue
                        else:
                            data['models'].append(model)
            except PermissionError: print('Reading Denied: Unable to access the file!')

    def export_data(self, data) -> None:
        # Writing data to CSV
        try:
            with open(self.file, 'w', newline='') as models:
                fieldnames: list[str] = Utils.model_headers()
                model_writer = DictWriter(models, fieldnames=fieldnames)
                model_writer.writeheader()

                for model in data['models']: model_writer.writerow(model)
        except PermissionError: print('Writing Denied: Unable to access the file!')
