use regex::Regex;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};
use csv::Writer;
use std::process::Command;

fn main() -> Result<(), Box<dyn Error>> {
    let pdf_path = "sample.pdf";
    let output_txt = "sample.txt";
    let output = Command::new("pdftotext")
        .arg("-enc")
        .arg("UTF-8")
        .arg(pdf_path)
	.arg(output_txt)
	.output();

    match output {
	Ok(output) if output.status.success() => {
	    let text = String::from_utf8_lossy(&output.stdout);
	    println!("text\n:{}", text);
	}
	Ok(_) => eprintln!("Error"),
	Err(e) => eprintln!("{}", e),
    }
	
    
    let input_file = "sample.txt";  // テキストデータを保存したファイル
    let output_file = "output.csv"; // 出力するCSVファイル

    let file = File::open(input_file)?;
    let reader = BufReader::new(file);

    let mut csv_writer = Writer::from_path(output_file)?;
    
    // CSVヘッダー
    csv_writer.write_record(&["transaction_date", "description", "debit_amount"])?;
    // 正規表現（日付変換を含む）
    let re = Regex::new(r"(\d{2})/(\d{2})/(\d{2})\s+(.+?)\s+JPY\s+([\d,]+\.?\d*)")?;

    for line in reader.lines() {
        let line = line?;
	// println!("{}", line);
        if let Some(captures) = re.captures(&line) {
	    println!("OK");
	    println!("{:?}", captures);
            let year = format!("20{}", &captures[1]); // `25` → `2025`
	    println!("{}", year);
            let month = &captures[2];
	    println!("{}", month);
            let day = &captures[3];
	    println!("{}", year);
            let formatted_date = format!("{}-{}-{}", year, month, day); // `2025-02-01`


            let description = captures[4].trim().replace("／ＮＦＣ", ""); // 余分な文字を削除
            let amount = captures[5].replace(",", ""); // `4,100.00` → `4100`

            // CSVに書き込み
            csv_writer.write_record(&[formatted_date, description, amount])?;
        } else {
	    println!("NG");
	}
    }

    csv_writer.flush()?;
    println!("CSVファイルが出力されました: {}", output_file);

    Ok(())

}
