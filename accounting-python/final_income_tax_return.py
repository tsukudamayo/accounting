import glob
from typing import List

import numpy as np
import pandas as pd


class ExpensesCalculator:
    def __init__(self, income_filepath, expenses_filepath):
        self.expenses_filepath = expenses_filepath
        self.income_filepath = income_filepath
        self.expense = 0
        self.income = 0
        self.medical_deduction = 0
        self.net_income = 0
        self.distribute_rate = 2

    def compute_expense(self):
        expenses_files = glob.glob(self.expenses_filepath)
        expenses_df_object = load_expenses_file(expenses_files)
        expenses_df = apply_type_to_expense_df(expenses_df_object)
        medical_deduction = compute_medical_deduction(expenses_df)
        print('medical_deduction: ', medical_deduction)
        distributed_expenses = distribute_expenses(expenses_df, self.distribute_rate)
        print('distributed_expenses: ', distributed_expenses)
        expense = compute_expenses(expenses_df)
        print('expense: ', expense)
        self.expense = np.int64(expense + distributed_expenses)
        self.medical_deduction = medical_deduction

        return self.expense

    def show_expenses_each_month(self) -> None:
        expenses_files = glob.glob(self.expenses_filepath)
        expenses_df = load_expenses_file(expenses_files)
        show_expneses_each_month(expenses_df, self.distribute_rate)

    def compute_income(self) -> np.int64:
        self.income = compute_income(self.income_filepath)
        
        return self.income

    def show_income_each_month(self) -> None:
        show_income_each_month(self.income_filepath)

    # TODO specify return type
    def compute_net_income(self):
        self.net_income = self.income - self.expense

        return self.net_income

    def show_statements(self) -> None:
        # expenses
        expenses_files = glob.glob(self.expenses_filepath)
        expenses_df_object = load_expenses_file(expenses_files)
        expenses_df = apply_type_to_expense_df(expenses_df_object)
        print(expenses_df.groupby("category").sum())
        # income
        income_files = glob.glob(self.income_filepath)
        income_df_object = load_expenses_file(income_files)
        income_df = apply_type_to_income_df(income_df_object)
        print(income_df.groupby("customer").sum())

        
def compute_income(income_filepath: str) -> np.int64:
    df = pd.read_csv(income_filepath)

    return df.income.sum()


def show_income_each_month(income_filepath: str) -> None:
    df = pd.read_csv(income_filepath)
    df_income_timestamp: pd.DataFrame = df.loc[:, ["timestamp", "income"]]
    df_income_timestamp["timestamp"] = pd.to_datetime(df_income_timestamp["timestamp"])
    df_income_timestamp.set_index(["timestamp"], inplace=True)
    print(df_income_timestamp.resample(rule="M").sum())


def apply_type_to_expense_df(expenses_df: pd.DataFrame) -> pd.DataFrame:
    expenses_df = expenses_df.astype(
        {
         'timestamp': 'object',
         'shop': 'object',
         'price': 'float64',
         'category': 'object',
         'is_expenses': 'int8',
         }
    )
    expenses_df['timestamp'] = pd.to_datetime(expenses_df['timestamp'])

    return expenses_df


def apply_type_to_income_df(income_df: pd.DataFrame) -> pd.DataFrame:
    income_df = income_df.astype(
        {
         "timestamp": "object",
         "income": "float64",
         "customer": "object",
         },
        
     )
    income_df["timestamp"] = pd.to_datetime(income_df["timestamp"])

    return income_df


def load_expenses_file(expenses_files: List) -> pd.DataFrame:
    expenses_table_df = pd.concat(
        [pd.read_csv(
            f,
            dtype={
                'timestamp': 'object',
                'shop': 'object',
                'price': 'float64',
                'category': 'object',
                'is_expenses': 'int8',
            },
         )
         for f in expenses_files])

    return expenses_table_df

def load_income_file(income_files: List) -> List[pd.DataFrame]:
    return pd.concat(
        [pd.read_csv(
            f,
            dtype={
                'date': 'object',
                'income': 'float64',
                'customer': 'object',
            },
         )
         for f in income_files])


def compute_medical_deduction(expenses_df: pd.DataFrame) -> np.int64:
    is_medical_deduction = expenses_df[expenses_df['is_expenses'] == 2]
    print(is_medical_deduction)
    sum_medical_deduction = is_medical_deduction['price'].sum()

    return np.int64(sum_medical_deduction - 100000)


def distribute_expenses(expenses_df: pd.DataFrame, distribute_rate: int) -> np.int64:
    is_ditribute = expenses_df[expenses_df['is_expenses'] == 3]

    return np.int64(is_ditribute['price'].sum() / distribute_rate)


def compute_expenses(expenses_df: pd.DataFrame) -> np.int64:
    is_expenses = expenses_df[expenses_df['is_expenses'] == 1]

    return np.int64(is_expenses['price'].sum())


def show_expneses_each_month(
    expenses_df: pd.DataFrame,
    distribute_rate: int,
) -> None:
    _expenses_df = expenses_df[expenses_df["is_expenses"] == 1]
    _distibuted_expenses_df = expenses_df[expenses_df["is_expenses"] == 3]
    _distibuted_expenses_df["price"] = _distibuted_expenses_df["price"] / distribute_rate
    is_expenses = pd.concat([_expenses_df, _distibuted_expenses_df])
    df_price_timestamp = is_expenses.loc[:, ["timestamp", "price"]]
    df_price_timestamp["timestamp"] = pd.to_datetime(df_price_timestamp["timestamp"])
    df_price_timestamp.set_index(["timestamp"], inplace=True)
    print(df_price_timestamp.resample(rule="M").sum())


def main():
    income_filepath = '../../data/balance/income/income_2022.csv'
    expenses_filepath = '../../data/balance/expenses/2022/expense_*'
    calculator = ExpensesCalculator(income_filepath, expenses_filepath)
    print('----- income -----')
    calculator.compute_income()
    print(calculator.income)
    print('----- income each month -----')
    calculator.show_income_each_month()
    print('----- expense -----')
    calculator.compute_expense()
    print(calculator.expense)
    print('----- expense each month -----')
    print(calculator.show_expenses_each_month())
    print('----- net income -----')
    calculator.compute_net_income()
    print(calculator.net_income)
    print('----- medical deduction -----')
    print(calculator.medical_deduction)
    print("----- statements -----")
    print(calculator.show_statements())
    

if __name__ == "__main__":
    main()
