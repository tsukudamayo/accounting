import pandas as pd


def budget_to_dataframe(budget_file: str) -> pd.DataFrame:
    df = pd.read_csv(
        budget_file,
        dtype={
                'shop': 'object',
                'price': 'float64',
                'account_names': 'object',
                'category': 'object',
                'is_expenses': 'int8',
                'profit_and_loss': 'int8',
        }
    )

    return df
    


def compute_budjet(df: pd.DataFrame):
    print(df['price'].sum())
    ex_0 = df[df['profit_and_loss'] == 0]
    ex_1 = df[df['profit_and_loss'] == 1]
    ex_2 = df[df['profit_and_loss'] == 2]
    print(ex_0)
    print(ex_1)
    print(ex_2)
    print(ex_0['price'].sum())
    print(ex_1['price'].sum())
    print(ex_2['price'].sum())

    return


def main():
    budget_file = "../../data/balance/budget/budget-202108.csv"
    df = budget_to_dataframe(budget_file)
    compute_budjet(df)


if __name__ == '__main__':
    main()
