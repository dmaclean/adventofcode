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

/// Defragments the disk by moving whole files to the leftmost possible position.
/// 
/// This function implements the following strategy:
/// 1. Identifies all files and their positions
/// 2. Processes files in decreasing order of file ID
/// 3. For each file:
///    - Finds the leftmost span of empty blocks that can fit the file
///    - Moves the entire file to that position if found
/// 
/// # Parameters
/// 
/// * `disk` - A vector of `Block` elements representing the disk to be defragmented
/// 
/// # Returns
/// 
/// Returns a new `Vec<Block>` with files moved according to the strategy
fn defrag(mut disk: Vec<Block>) -> Vec<Block> {
    // First, collect information about all files
    let mut files: Vec<(usize, usize, usize)> = Vec::new(); // (file_id, start_pos, length)
    let mut current_file_id = None;
    let mut start_pos = 0;
    let mut length = 0;

    // Find all files and their positions
    for (pos, block) in disk.iter().enumerate() {
        match block {
            Block::File(id) => {
                if current_file_id == Some(*id) {
                    length += 1;
                } else {
                    if current_file_id.is_some() {
                        files.push((current_file_id.unwrap(), start_pos, length));
                    }
                    current_file_id = Some(*id);
                    start_pos = pos;
                    length = 1;
                }
            }
            Block::Empty => {
                if current_file_id.is_some() {
                    files.push((current_file_id.unwrap(), start_pos, length));
                    current_file_id = None;
                    length = 0;
                }
            }
        }
    }
    // Handle the last file if it extends to the end
    if current_file_id.is_some() {
        files.push((current_file_id.unwrap(), start_pos, length));
    }

    // Sort files by ID in descending order
    files.sort_by(|a, b| b.0.cmp(&a.0));

    // Process each file
    for (file_id, current_start, length) in files {
        let mut best_position = None;
        let mut current_empty_start = None;
        let mut current_empty_length = 0;

        // Find the leftmost suitable empty space
        for (pos, block) in disk.iter().enumerate() {
            if pos >= current_start {
                break; // Don't look beyond the file's current position
            }

            match block {
                Block::Empty => {
                    if current_empty_start.is_none() {
                        current_empty_start = Some(pos);
                    }
                    current_empty_length += 1;

                    if current_empty_length >= length {
                        best_position = current_empty_start;
                        break;
                    }
                }
                Block::File(_) => {
                    current_empty_start = None;
                    current_empty_length = 0;
                }
            }
        }

        // Move the file if we found a suitable position
        if let Some(new_start) = best_position {
            // Clear the old position
            for i in current_start..current_start + length {
                disk[i] = Block::Empty;
            }
            // Place the file in its new position
            for i in new_start..new_start + length {
                disk[i] = Block::File(file_id);
            }
        }
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
