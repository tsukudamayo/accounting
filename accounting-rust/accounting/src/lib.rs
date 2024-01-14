pub struct Expense {
    expense_filepath: String,
    income_filepath: String,
    expense: i32,
    income: i32,
    medical_deduction: i32,
    net_income: i32,
    distribute_rate: i8,
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_read_income_file() {
	
    }
}
