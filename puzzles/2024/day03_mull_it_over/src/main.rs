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
    let re = Regex::new(r"mul\((?P<v1>\d{1,3}),(?P<v2>\d{1,3})\)|do\(\)|don't\(\)").unwrap();

    let content = reader.lines()
        .map(|l| l.unwrap())
        .collect::<Vec<String>>()
        .join("");

    let total = determine_sum_for_line(&content, &re);
    println!("{}", total);
    Ok(())
}

/// Calculates the sum of all multiplication expressions in a single line, respecting enable/disable controls.
///
/// The function processes multiplication expressions in the format `mul(x,y)` where x and y are 1-3 digit numbers.
/// It also handles control expressions:
/// - `do()` enables multiplication processing
/// - `don't()` disables multiplication processing
/// 
/// When processing is disabled, multiplication expressions are ignored until a `do()` is encountered.
///
/// # Arguments
/// * `line` - A string slice containing multiplication expressions and control statements
/// * `re` - A compiled regex pattern for matching multiplication and control expressions
///
/// # Returns
/// * `i32` - The sum of all multiplication results in the line while processing was enabled
///
/// # Example
/// ```
/// let re = Regex::new(r"mul\((?P<v1>\d{1,3}),(?P<v2>\d{1,3})\)|do\(\)|don't\(\)").unwrap();
/// let result = determine_sum_for_line("mul(2,3) don't() mul(4,5) do() mul(6,7)", &re);
/// assert_eq!(result, 48); // (2 * 3) + (6 * 7) = 6 + 42 = 48, mul(4,5) is ignored
/// ```
fn determine_sum_for_line(line: &str, re: &Regex) -> i32 {
    let mut enabled = true;
    re.captures_iter(line)
        .map(|cap| {
            let val = cap.get(0).unwrap().as_str();
            let found_enable = val.find("do()") != None;
            if found_enable {
                enabled = true;
                return 0;
            }

            let found_disable = val.find("don't()") != None;
            if found_disable {
                enabled = false;
                return 0;
            }

            if !enabled {
                return 0;
            }

            let v1 = cap.name("v1").unwrap().as_str().parse::<i32>().unwrap();
            let v2 = cap.name("v2").unwrap().as_str().parse::<i32>().unwrap();
            v1 * v2
        })
        .sum()
}
