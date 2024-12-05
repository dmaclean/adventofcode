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
            if crossword[i][j] != 'A' 
                || i == 0 
                || i == crossword.len() - 1 
                || j == 0 
                || j == crossword[i].len() - 1 
            {
                // Skip if the letter isn't 'A' or we are on the edge of the crossword
                continue;
            }

            if (
                // Diagonal top-left to bottom-right is either M-A-S or S-A-M
                (crossword[i-1][j-1] == 'M' && crossword[i+1][j+1] == 'S') ||
                (crossword[i-1][j-1] == 'S' && crossword[i+1][j+1] == 'M')
            ) && (
                // Diagonal top-right to bottom-left is either M-A-S or S-A-M
                (crossword[i-1][j+1] == 'M' && crossword[i+1][j-1] == 'S') ||
                (crossword[i-1][j+1] == 'S' && crossword[i+1][j-1] == 'M')
            ) {
                found_count += 1;
            }
        }
    }
    println!("Found {} words", found_count);

    Ok(())
}
