use std::collections::{HashMap, HashSet};

/// Reads the input file and returns a vector of strings, one for each line
/// 
/// # Arguments
/// * `filename` - The path to the input file to read
/// 
/// # Returns
/// A vector containing each line of the input file as a String
fn read_input(filename: &str) -> Vec<String> {
    std::fs::read_to_string(filename)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

/// Builds a mapping of pages to their associated queues and finds the divider index
/// 
/// # Arguments
/// * `lines` - Slice of strings containing the input data
/// 
/// # Returns
/// A tuple containing:
/// * HashMap mapping page identifiers to their set of valid queues
/// * usize representing the index of the empty line divider
fn build_page_map<'a>(lines: &[String]) -> (HashMap<&str, HashSet<&str>>, usize) {
    let mut page_map = HashMap::new();
    let mut divider_index = 0;
    
    for (i, line) in lines.iter().enumerate() {
        if line.is_empty() {
            divider_index = i;
            break;
        }
        
        let parts: Vec<&str> = line.split('|').collect();
        let (page, queue) = (parts[0], parts[1]);
        
        page_map
            .entry(page)
            .and_modify(|set: &mut HashSet<&str>| { set.insert(queue); })
            .or_insert_with(|| {
                let mut set = HashSet::new();
                set.insert(queue);
                set
            });
    }
    
    (page_map, divider_index)
}

/// Processes a sequence of pages and determines if they need reordering
/// 
/// # Arguments
/// * `line` - A string containing comma-separated page identifiers
/// * `page_map` - Reference to the HashMap containing page-to-queue mappings
/// 
/// # Returns
/// * Some(i32) - The middle page number if reordering was needed
/// * None - If no reordering was necessary
fn process_page_sequence(line: &str, page_map: &HashMap<&str, HashSet<&str>>) -> Option<i32> {
    let pages: Vec<&str> = line.split(',').collect();
    let mut pages_sorted = pages.clone();
    
    pages_sorted.sort_by(|a, b| {
        let b_in_a_set = page_map.get(a)
            .map(|a_set| a_set.contains(b))
            .unwrap_or(false);
            
        if b_in_a_set {
            std::cmp::Ordering::Less
        } else {
            std::cmp::Ordering::Greater
        }
    });

    if pages_sorted != pages {
        println!("Original: {:?}", pages);
        println!("Sorted: {:?}", pages_sorted);
        pages_sorted[pages_sorted.len() / 2].parse().ok()
    } else {
        None
    }
}

/// Main function that orchestrates the page processing workflow
/// 
/// Reads the input file, builds the page map, processes each sequence,
/// and outputs the sum of middle page numbers for sequences that required reordering
fn main() {
    let lines = read_input("input.txt");
    let (page_map, divider_index) = build_page_map(&lines);
    
    let page_number_sum: i32 = lines[divider_index + 1..]
        .iter()
        .filter_map(|line| process_page_sequence(line, &page_map))
        .sum();
    
    println!("page_number_sum: {}", page_number_sum);
}
