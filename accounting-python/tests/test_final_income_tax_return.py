from final_income_tax_return import compute_income


def test_compute_income():
    get = compute_income('./income/income_2020.csv')

    assert get == 6833194
