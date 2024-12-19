use log::{debug, trace};
use env_logger;
use petgraph::graph::{DiGraph, NodeIndex};
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Stone {
    num: u64,
    length: u8
}

#[derive(Debug)]
struct Job {
    iteration: u32,
    stone_idx: NodeIndex,
}

impl Stone {
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

fn create_stone_from_string(s: &str) -> Stone {
    let num = s.parse::<u64>().expect("Failed to parse number");
    let length = num.to_string().len() as u8;
    Stone { num, length }
}

fn extract_stones(s: &str) -> Vec<Stone> {
    s.split_whitespace()
        .map(|s| create_stone_from_string(s))
        .collect()
}

fn process_stones(initial_stones: Vec<Stone>) -> usize {
    let mut graph = DiGraph::new();
    let mut stone_to_idx: HashMap<Stone, NodeIndex> = HashMap::new();
    let mut queue = VecDeque::new();
    let mut final_stones = HashMap::new();
    
    debug!("Processing {} initial stones", initial_stones.len());
    
    // Add initial stones to graph and queue
    for stone in initial_stones {
        let idx = *stone_to_idx
            .entry(stone.clone())
            .or_insert_with(|| graph.add_node(stone.clone()));
        
        queue.push_back(Job {
            iteration: 0,
            stone_idx: idx,
        });
    }

    let mut processed = 0;
    let mut last_logged = std::time::Instant::now();
    let log_interval = std::time::Duration::from_secs(5);

    // Process queue
    while let Some(Job { iteration, stone_idx }) = queue.pop_front() {
        processed += 1;
        
        // Add more frequent logging for debugging
        if processed % 10_000_000 == 0 || last_logged.elapsed() >= log_interval {
            let current_stone = &graph[stone_idx];
            debug!(
                "Processed {} jobs, Queue: {}, Stones: {}, Iter: {}, Current stone: {} (len {})", 
                processed,
                queue.len(),
                stone_to_idx.len(),
                iteration,
                current_stone.num,
                current_stone.length
            );
            last_logged = std::time::Instant::now();
        }

        if iteration >= 75 {
            *final_stones.entry(stone_idx).or_insert(0) += 1;
            continue;
        }

        let current_stone = graph[stone_idx].clone();
        let next_stones = current_stone.transition();

        for next_stone in next_stones {
            let next_idx = *stone_to_idx
                .entry(next_stone.clone())
                .or_insert_with(|| graph.add_node(next_stone));
            
            // Add edge if it doesn't exist
            if !graph.contains_edge(stone_idx, next_idx) {
                graph.add_edge(stone_idx, next_idx, ());
            }

            queue.push_back(Job {
                iteration: iteration + 1,
                stone_idx: next_idx,
            });
        }
    }

    debug!(
        "Finished processing. Total jobs: {}, Final unique stones: {}", 
        processed,
        stone_to_idx.len()
    );

    // Sum up all the counts in final_stones
    final_stones.values().sum()
}

fn main() {
    env_logger::init();
    debug!("Starting stone processing...");

    let input = std::fs::read_to_string("input.txt")
        .expect("Failed to read input file");

    let initial_stones = extract_stones(&input);
    debug!("Loaded {} initial stones", initial_stones.len());
    
    let result = process_stones(initial_stones);
    
    println!("Final result: {}", result);
}
