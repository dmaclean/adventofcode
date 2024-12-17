use std::fs;
use std::io;
use std::fmt;

/// Represents a disk block that can either contain a file or be empty.
/// 
/// This enum is used to model the state of each position on the disk:
/// - `File(usize)`: Contains a file with its index
/// - `Empty`: Represents an empty block
#[derive(Debug, Clone, PartialEq)]
enum Block {
    File(usize),
    Empty,
}

/// Custom error type for disk operations.
/// 
/// Encapsulates different types of errors that can occur during disk operations:
/// - `IoError`: Represents filesystem-related errors
/// - `ParseError`: Represents errors during parsing of input data
#[derive(Debug)]
enum DiskError {
    IoError(io::Error),
    ParseError(String),
}

// Implement Display for better error messages
impl fmt::Display for DiskError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DiskError::IoError(err) => write!(f, "IO error: {}", err),
            DiskError::ParseError(msg) => write!(f, "Parse error: {}", msg),
        }
    }
}

impl From<io::Error> for DiskError {
    fn from(err: io::Error) -> Self {
        DiskError::IoError(err)
    }
}

/// Main entry point of the program.
/// 
/// Reads the input file, creates a disk representation, defragments it,
/// and calculates the final checksum.
/// 
/// # Errors
/// 
/// Returns a `DiskError` if:
/// - The input file cannot be read
/// - The file contents cannot be parsed correctly
fn main() -> Result<(), DiskError> {
    let input = fs::read_to_string("input.txt")?;
    let disk_map: Vec<char> = input.chars().collect();
    let mut disk = create_disk(&disk_map)?;
    disk = defrag(disk);
    let checksum = calculate_checksum(&disk);
    println!("{}", checksum);
    Ok(())
}

/// Calculates the checksum of the disk by multiplying each file's index by its position.
/// 
/// The checksum is calculated by:
/// 1. Finding each file block on the disk
/// 2. Multiplying its index by its current position
/// 3. Summing all these products
/// 
/// # Parameters
/// 
/// * `disk` - A slice of `Block` elements representing the current state of the disk
/// 
/// # Returns
/// 
/// Returns a `u64` representing the calculated checksum value
/// 
/// # Example
/// 
/// ```
/// let disk = vec![Block::File(0), Block::File(1), Block::Empty];
/// let checksum = calculate_checksum(&disk);
/// // checksum = (0 * 0) + (1 * 1) = 1
/// ```
fn calculate_checksum(disk: &[Block]) -> u64 {
    disk.iter()
        .enumerate()
        .filter_map(|(pos, block)| {
            if let Block::File(index) = block {
                Some(*index as u64 * pos as u64)
            } else {
                None
            }
        })
        .sum()
}

/// Defragments the disk by moving all files to the beginning of the disk.
/// 
/// This function implements a two-pointer approach to defragmentation:
/// 1. Scans from left to find empty blocks
/// 2. Scans from right to find file blocks
/// 3. Swaps these blocks to consolidate files at the beginning
/// 
/// # Parameters
/// 
/// * `disk` - A vector of `Block` elements representing the disk to be defragmented
/// 
/// # Returns
/// 
/// Returns a new `Vec<Block>` with all files moved to the beginning and empty blocks at the end
/// 
/// # Example
/// 
/// ```
/// let disk = vec![Block::Empty, Block::File(1), Block::Empty, Block::File(0)];
/// let defragged = defrag(disk);
/// // Result: [Block::File(1), Block::File(0), Block::Empty, Block::Empty]
/// ```
fn defrag(mut disk: Vec<Block>) -> Vec<Block> {
    let mut left = 0;
    let mut right = disk.len() - 1;
    
    while left < right {
        // Skip non-empty blocks from the left
        while left < disk.len() && disk[left] != Block::Empty {
            left += 1;
        }
        
        // Skip empty blocks from the right
        while right > left && disk[right] == Block::Empty {
            right -= 1;
        }
        
        if left >= right {
            break;
        }
        
        // Swap blocks
        disk.swap(left, right);
        left += 1;
        right -= 1;
    }
    
    disk
}

/// Creates a disk representation from the input map.
/// 
/// Processes the input map where:
/// - Each character represents a count of consecutive blocks
/// - Alternating counts represent files and empty spaces
/// - File blocks are numbered sequentially starting from 0
/// 
/// # Parameters
/// 
/// * `disk_map` - A slice of characters where each character is a digit representing
///                the count of consecutive blocks (files or empty spaces)
/// 
/// # Returns
/// 
/// Returns a `Result` containing either:
/// - `Vec<Block>` representing the initial state of the disk
/// - `DiskError` if the input contains invalid characters
/// 
/// # Example
/// 
/// ```
/// let disk_map = vec!['2', '1'];  // 2 files followed by 1 empty space
/// let disk = create_disk(&disk_map)?;
/// // Result: Ok([Block::File(0), Block::File(0), Block::Empty])
/// ```
fn create_disk(disk_map: &[char]) -> Result<Vec<Block>, DiskError> {
    let mut disk = Vec::new();
    let mut file_index = 0;
    let mut is_file = true;

    for (i, &ch) in disk_map.iter().enumerate() {
        let count = ch.to_digit(10).ok_or_else(|| {
            DiskError::ParseError(format!(
                "Invalid character '{}' at position {}: expected digit",
                ch, i
            ))
        })? as usize;
            
        let block = if is_file {
            Block::File(file_index)
        } else {
            Block::Empty
        };
        
        disk.extend(std::iter::repeat(block).take(count));
        
        if is_file {
            file_index += 1;
        }
        is_file = !is_file;
    }
    
    Ok(disk)
}
