import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    csv_file = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    date_format = "%d-%m-%Y"
    @classmethod
    def init_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) # dataFrame -> a pandas object that allow to acess/create, columns on different files, ex: csv, excel.
            df.to_csv(cls.csv_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.csv_file, "a", newline="") as csvfile: # context Manager
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added!!")
        
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        
        df['date'] = pd.to_datetime(df['date'], format=CSV.date_format)
        df['amount'] = df['amount'].astype(float)
        start_date = datetime.strptime(start_date, CSV.date_format)
        end_date = datetime.strptime(end_date, CSV.date_format)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date) # & -> same as and, but use in pandas mask sh*t 
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print('No transaction found in the given date range.')
        else:
            print(f'transactions from {start_date.strftime(CSV.date_format)} to {end_date.strftime(CSV.date_format)}')
            print(
                filtered_df.to_string(
                    index=False, formatters={'date': lambda x: x.strftime(CSV.date_format)}
                )
            )
            
            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print('\nSummary:')
            print(f'Total Income: ${total_income:.2f}')
            print(f'Total Expense: ${total_expense:.2f}')
            print(f'Net saving: ${(total_income - total_expense):.2f}')
            
        return filtered_df
    
    
def add():
    CSV.init_csv()
    date = get_date('Enter the date of the transaction (dd-mm-yyyy) or Enter: ', 
        allow_default=True,)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index('date', inplace=True)
    
    income_df = (
        df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)
    )
    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['amount'], label='Income', color='g')
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print('\n1. Add a new transaction')
        print('2. View transactions and a summary within a date range')
        print('3. Exit')
        choice = input('Enter your choice (1-3): ')
        
        if choice == '1':
            add()
        elif choice == "2":
            start_date = get_date('Enter the start date (dd-mm-yyyy): ')
            end_date = get_date('Enter ehe end date (dd-mm-yyyy): ')
            df = CSV.get_transactions(start_date, end_date)
            if input('Do you wanna see a plot? (y/n)').lower() == 'y':
                plot_transactions(df)
        elif choice == "3":
            print('Exiting...')
            break
        else:
            print('Invalid choice. Enter 1, 2 or 3.')
            
if __name__ == '__main__':
    main()