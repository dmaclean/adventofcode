use log::{debug, trace, info};
use env_logger;
use std::collections::HashMap;

/// Represents a stone with a numeric value and its string length.
/// Each stone can be transformed according to specific rules based on
/// its properties.
#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Stone {
    /// The numeric value of the stone
    num: u64,
    /// The number of digits in the stone's numeric value
    length: u8
}

impl Stone {
    /// Transforms the stone according to the following rules:
    /// - If the stone's value is 0, it becomes 1
    /// - If the stone's length is even, it splits into two stones (left and right halves)
    /// - If the stone's length is odd, its value is multiplied by 2024
    /// 
    /// Returns a vector of new stones produced by the transformation.
    fn transition(&self) -> Vec<Stone> {
        if self.num == 0 {
            trace!("Stone {} (len {}) -> [1]", self.num, self.length);
            vec![Stone { num: 1, length: 1 }]
        } else if self.length % 2 == 0 {
            let num_str = self.num.to_string();
            let mid = self.length as usize / 2;
            let left = &num_str[..mid];
            let right = &num_str[mid..];
            
            trace!("Stone {} (len {}) splits -> [{}, {}]", 
                self.num, self.length, left, right);
            
            vec![
                create_stone_from_string(left),
                create_stone_from_string(right),
            ]
        } else {
            let new_num = self.num * 2024;
            let new_stone = Stone {
                num: new_num,
                length: new_num.to_string().len() as u8,
            };
            trace!("Stone {} (len {}) multiplies -> [{}] (len {})", 
                self.num, self.length, new_stone.num, new_stone.length);
            
            vec![new_stone]
        }
    }
}

/// Creates a new Stone from a string representation of a number.
/// The length is automatically calculated from the number of digits.
///
/// # Arguments
/// * `s` - A string slice containing a valid number
///
/// # Panics
/// Panics if the string cannot be parsed as a u64
fn create_stone_from_string(s: &str) -> Stone {
    let num = s.parse::<u64>().expect("Failed to parse number");
    let length = num.to_string().len() as u8;
    Stone { num, length }
}

/// Extracts a vector of Stones from a space-separated string of numbers.
///
/// # Arguments
/// * `s` - A string slice containing space-separated numbers
///
/// # Returns
/// A vector of Stone objects created from the input numbers
fn extract_stones(s: &str) -> Vec<Stone> {
    s.split_whitespace()
        .map(|s| create_stone_from_string(s))
        .collect()
}

/// Recursively processes a stone for a given number of blinks, using memoization
/// to avoid redundant calculations.
///
/// # Arguments
/// * `stone` - The stone to process
/// * `blinks_left` - Number of transformations remaining
/// * `memo` - Memoization cache storing previously calculated results
///
/// # Returns
/// The total number of stones that will be produced after all transformations
fn process_stone(stone: &Stone, blinks_left: u8, memo: &mut HashMap<(Stone, u8), usize>) -> usize {
    // Check if we've seen this combination before
    let key = (stone.clone(), blinks_left);
    if let Some(&result) = memo.get(&key) {
        return result;
    }

    if blinks_left == 0 {
        trace!("Stone {}", stone.num);
        return 1;
    }

    let mut count = 0;
    let children = stone.transition();
    for child in children {
        count += process_stone(&child, blinks_left - 1, memo);
    }

    // Store the result before returning
    memo.insert(key, count);
    count
}

/// Main function that:
/// 1. Initializes logging
/// 2. Reads input from "input.txt"
/// 3. Processes each initial stone for 75 blinks
/// 4. Prints the total number of stones produced and cache statistics
fn main() {
    env_logger::init();
    debug!("Starting stone processing...");

    let input = std::fs::read_to_string("input.txt")
        .expect("Failed to read input file");

    let initial_stones = extract_stones(&input);
    debug!("Loaded {} initial stones", initial_stones.len());

    let mut memo = HashMap::new();
    let result: usize = initial_stones.iter()
        .map(|stone| {
            info!("Processing stone {} from {}", stone.num, input);
            let count = process_stone(stone, 75, &mut memo);
            debug!("Stone {} produced {} stones", stone.num, count);
            count
        })
        .sum();
    
    println!("Final result: {}", result);
    println!("Memoization cache size: {}", memo.len());
}
