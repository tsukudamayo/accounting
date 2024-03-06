use std::error::Error;

use polars::prelude::{CsvReader, SerReader};

type _Result<T> = Result<T, Box<dyn Error>>;

pub struct Expense {
    expense_filepath: String,
    income_filepath: String,
    expense: i32,
    income: i32,
    medical_deduction: i32,
    net_income: i32,
    distribute_rate: i8,
}

fn read_income_file(filepath: &str) -> _Result<i32> {
    unimplemented!();
}

fn compute_income(filepath: &str) -> _Result<i32> {
    let df = CsvReader::from_path(filepath)?
        .infer_schema(None)
        .has_header(true)
        .finish()?;
    println!("{}", df);
    let all_income = df["income"].sum()?;
    Ok(all_income)
}

fn show_expenses_each_month(filepath: &str) -> _Result<()> {
    let df = CsvReader::from_path(filepath)?
        .infer_schema(None)
        .has_header(true)
        .finish()?;
    println!("{}", df);
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::{compute_income, show_expenses_each_month};

    #[test]
    fn test_compute_income_file() {
	let filepath = "../sample_data/income_xxxx.csv";
	let test_income = compute_income(filepath);
	let expected = 1200000;
	assert_eq!(test_income.unwrap(), expected);
    }

    #[test]
    fn test_show_expense_each_month() {
	let filepath = "../sample_data/income_xxxx.csv";
	let result = show_expenses_each_month(filepath);
	assert!(result.is_ok());
    }
}
