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
        # print(expenses_result.columns)
        # print(type(expenses_result))
        expenses_df = apply_type_to_expenses_df(expenses_df_object)
        # print(apply_type_df)
        # print(apply_type_df['price'].sum())
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


def compute_income(income_filepath: str) -> np.int64:
    df = pd.read_csv(income_filepath)

    return df.income.sum()


def apply_type_to_expenses_df(expenses_df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
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


def load_expenses_file(expenses_files: List) -> np.int64:
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

def compute_medical_deduction(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_medical_deduction = expenses_df[expenses_df['is_expenses'] == 2]
    print(is_medical_deduction)
    sum_medical_deduction = is_medical_deduction['price'].sum()

    return np.int64(sum_medical_deduction - 100000)


def distribute_expenses(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_ditribute = expenses_df[expenses_df['is_expenses'] == 3]

    return np.int64(is_ditribute['price'].sum())


def compute_expenses(expenses_df: pd.core.frame.DataFrame) -> np.int64:
    is_expenses = expenses_df[expenses_df['is_expenses'] == 2]

    return np.int64(is_expenses['price'].sum())


def main():
    income_dir = '../../data/balance/income/income_2020.csv'
    expenses_dir = '../../data/balance/expenses/expenses*'
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


if __name__ == "__main__":
    main()
