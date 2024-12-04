use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use regex::Regex;

/// Processes an input file containing multiplication expressions in the format `mul(x,y)`
/// and calculates their sum.
///
/// # Returns
/// * `io::Result<()>` - Ok if the file was successfully processed, Err for IO errors
///
/// # Errors
/// This function will return an error if:
/// * The input file cannot be opened
/// * There are issues reading lines from the file
fn main() -> io::Result<()> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let re = Regex::new(r"mul\((?P<v1>\d{1,3}),(?P<v2>\d{1,3})\)").unwrap();

    let mut total = 0;
    for line in reader.lines() {
        let line = line?;
        let matches: i32 = determine_sum_for_line(&line, &re);
        total += matches;
    }
    println!("{}", total);
    Ok(())
}

/// Calculates the sum of all multiplication expressions in a single line.
///
/// # Arguments
/// * `line` - A string slice containing zero or more multiplication expressions
/// * `re` - A compiled regex pattern for matching multiplication expressions
///
/// # Returns
/// * `i32` - The sum of all multiplication results in the line
///
/// # Example
/// ```
/// let re = Regex::new(r"mul\((?P<v1>\d{1,3}),(?P<v2>\d{1,3})\)").unwrap();
/// let result = determine_sum_for_line("mul(2,3) and mul(4,5)", &re);
/// assert_eq!(result, 26); // (2 * 3) + (4 * 5) = 6 + 20 = 26
/// ```
fn determine_sum_for_line(line: &str, re: &Regex) -> i32 {
    re.captures_iter(line)
        .map(|cap| {
            let v1 = cap.name("v1").unwrap().as_str().parse::<i32>().unwrap();
            let v2 = cap.name("v2").unwrap().as_str().parse::<i32>().unwrap();
            v1 * v2
        })
        .sum()
}
