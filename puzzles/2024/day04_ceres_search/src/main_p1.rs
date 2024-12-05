use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

fn main() -> io::Result<()> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let crossword: Vec<Vec<char>> = reader
        .lines()
        .map(|line| line.unwrap().chars().collect())
        .collect();

    let mut found_count: i32 = 0;
    for i in 0..crossword.len() {
        for j in 0..crossword[i].len() {
            if crossword[i][j] != 'X' {
                continue;
            }

            // Check backwards
            if j >= 3 && crossword[i][j - 1] == 'M' && crossword[i][j - 2] == 'A' && crossword[i][j - 3] == 'S' {
                println!("Found backwards at ({}, {})", i, j);
                found_count += 1;
            }

            // Check forwards
            if j + 3 < crossword[i].len() && crossword[i][j + 1] == 'M' && crossword[i][j + 2] == 'A' && crossword[i][j + 3] == 'S' {
                println!("Found forwards at ({}, {})", i, j);
                found_count += 1;
            }

            // Check up
            if i >= 3 && crossword[i - 1][j] == 'M' && crossword[i - 2][j] == 'A' && crossword[i - 3][j] == 'S' {
                println!("Found up at ({}, {})", i, j);
                found_count += 1;
            }

            // Check down
            if i + 3 < crossword.len() && crossword[i + 1][j] == 'M' && crossword[i + 2][j] == 'A' && crossword[i + 3][j] == 'S' {
                println!("Found down at ({}, {})", i, j);
                found_count += 1;
            }

            // Check diagonal-up-left
            if i >= 3 && j >= 3 && crossword[i - 1][j - 1] == 'M' && crossword[i - 2][j - 2] == 'A' && crossword[i - 3][j - 3] == 'S' {
                println!("Found diagonal-up-left at ({}, {})", i, j);
                found_count += 1;
            }

            // Check diagonal-up-right
            if i >= 3 && j + 3 < crossword[i].len() && crossword[i - 1][j + 1] == 'M' && crossword[i - 2][j + 2] == 'A' && crossword[i - 3][j + 3] == 'S' {
                println!("Found diagonal-up-right at ({}, {})", i, j);
                found_count += 1;
            }

            // Check diagonal-down-left
            if i + 3 < crossword.len() && j >= 3 && crossword[i + 1][j - 1] == 'M' && crossword[i + 2][j - 2] == 'A' && crossword[i + 3][j - 3] == 'S' {
                println!("Found diagonal-down-left at ({}, {})", i, j);
                found_count += 1;
            }

            // Check diagonal-down-right
            if i + 3 < crossword.len() && j + 3 < crossword[i].len() && crossword[i + 1][j + 1] == 'M' && crossword[i + 2][j + 2] == 'A' && crossword[i + 3][j + 3] == 'S' {
                println!("Found diagonal-down-right at ({}, {})", i, j);
                found_count += 1;
            }
        }
    }
    println!("Found {} words", found_count);

    Ok(())
}
