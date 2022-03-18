import glob
from typing import List

import numpy as np
import pandas as pd


class ExpensesCalculator:
    def __init__(self, income_dir, expenses_dir):
        self.expenses_dir = expenses_dir
        self.income_dir = income_dir
        self.expense = 0
        self.income = 0
        self.medical_deduction = 0
        self.net_income = 0

    def compute_expense(self):
        expenses_files = glob.glob(self.expenses_dir)
        expenses_df_object = load_expenses_file(expenses_files)
        expenses_df = apply_type_to_expense_df(expenses_df_object)
        medical_deduction = compute_medical_deduction(expenses_df)
        print('medical_deduction: ', medical_deduction)
        distributed_expenses = distribute_expenses(expenses_df)
        print('distributed_expenses: ', distributed_expenses)
        expense = compute_expenses(expenses_df)
        print('expense: ', expense)
        self.expense = np.int64(expense + distributed_expenses)
        self.medical_deduction = medical_deduction

        return self.expense

    def compute_income(self):
        self.income = compute_income(self.income_dir)
        
        return self.income

    def compute_net_income(self):
        self.net_income = self.income - self.expense

        return self.net_income

    def show_statements(self):
        # expenses
        expenses_files = glob.glob(self.expenses_dir)
        expenses_df_object = load_expenses_file(expenses_files)
        expenses_df = apply_type_to_expense_df(expenses_df_object)
        print(expenses_df.groupby("category").sum())
        # income
        income_files = glob.glob(self.income_dir)
        income_df_object = load_expenses_file(income_files)
        income_df = apply_type_to_income_df(income_df_object)
        print(income_df.groupby("customer").sum())

        
def compute_income(income_filepath: str) -> np.int64:
    df = pd.read_csv(income_filepath)

    return df.income.sum()


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

    # debug
    # for f in expenses_files:
    #     print(f)
    #     pd.read_csv(
    #         f,
    #         dtype={
    #             'timestamp': 'object',
    #             'shop': 'object',
    #             'price': 'float64',
    #             'category': 'object',
    #             'is_expenses': 'int8',
    #         },
    #     )

    return expenses_table_df

def load_income_file(income_files: List) -> pd.DataFrame:
    expenses_table_df = pd.concat(
        [pd.read_csv(
            f,
            dtype={
                'date': 'object',
                'income': 'float64',
                'customer': 'object',
            },
         )
         for f in expenses_files])

def compute_medical_deduction(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_medical_deduction = expenses_df[expenses_df['is_expenses'] == 2]
    print(is_medical_deduction)
    sum_medical_deduction = is_medical_deduction['price'].sum()

    return np.int64(sum_medical_deduction - 100000)


def distribute_expenses(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_ditribute = expenses_df[expenses_df['is_expenses'] == 3]
    distribute_rate = 2

    return np.int64(is_ditribute['price'].sum() / distribute_rate)


def compute_expenses(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_expenses = expenses_df[expenses_df['is_expenses'] == 1]

    return np.int64(is_expenses['price'].sum())


def main():
    income_dir = '../../data/balance/income/income_2021.csv'
    expenses_dir = '../../data/balance/expenses/2021/expense_*'
    calculator = ExpensesCalculator(income_dir, expenses_dir)
    print('----- income -----')
    calculator.compute_income()
    print(calculator.income)
    print('----- expense -----')
    calculator.compute_expense()
    print(calculator.expense)
    print('----- net income -----')
    calculator.compute_net_income()
    print(calculator.net_income)
    print('----- medical deduction -----')
    print(calculator.medical_deduction)
    print("----- statements -----")
    print(calculator.show_statements())
    


if __name__ == "__main__":
    main()
