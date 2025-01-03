use log::{debug, trace};
use env_logger;
use std::collections::{HashMap, VecDeque};

struct Task{
    total_blinks_so_far: u8,
    blinks: u8,
    stones_gained: u8,
    stones_to_enqueue: Vec<u8>
}

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Stone {
    num: u64,
    length: u8
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

fn process_stones(initial_stones: Vec<Stone>, task_map: &HashMap<u64, Vec<Task>>, blink_limit: u8) -> usize {
    initial_stones.iter()
        .map(|stone| {
            debug!("Starting to process stone: {}", stone.num);
            let mut total_stones: usize = 1; // Count the initial stone
            let mut stone_queue: VecDeque<(Stone, u8)> = VecDeque::new(); // (Stone, blinks_used)
            let mut task_queue: VecDeque<(u8, Vec<u8>)> = VecDeque::new(); // (blinks_used, stones_to_process)
            stone_queue.push_back((stone.clone(), 0));

            while let Some((current_stone, blinks_used)) = stone_queue.pop_front() {
                debug!("Processing stone {} at blink {}", current_stone.num, blinks_used);
                if (0..=9).contains(&current_stone.num) {
                    // We've reached a single digit, use the task map
                    for task in task_map.get(&current_stone.num).unwrap() {
                        debug!("  Using task map for {}: +{} stones, {} new stones to enqueue", 
                            current_stone.num, task.stones_gained, task.stones_to_enqueue.len());
                        if task.total_blinks_so_far > 0 {
                            total_stones += task.stones_gained as usize;
                        }
                        // Only enqueue new stones if we haven't used all blinks
                        if blinks_used + task.blinks <= blink_limit {
                            debug!("  Can still blink {} more times, adding task with {} stones", 
                                blink_limit - (blinks_used + task.blinks), task.stones_to_enqueue.len());
                            task_queue.push_back((blinks_used + task.blinks, task.stones_to_enqueue.clone()));
                        } else {
                            debug!("  No more blinks available after {} + {}", blinks_used, task.blinks);
                        }
                    }
                } else {
                    // Process larger numbers until they become single digits
                    if blinks_used >= blink_limit {
                        debug!("  Skipping stone {} - no more blinks available", current_stone.num);
                        continue; // Skip if we've used all blinks
                    }
                    
                    let next_stones = current_stone.transition();
                    if next_stones.len() == 2 {
                        debug!("  Stone {} split into two - adding 1 to total", current_stone.num);
                        total_stones += 1; // Count the split
                    }
                    
                    for stone in next_stones {
                        debug!("  Enqueueing stone {} at blink {}", stone.num, blinks_used + 1);
                        stone_queue.push_back((stone, blinks_used + 1));
                    }
                }
            }

            // Process the task queue
            while let Some((blinks_used, stones)) = task_queue.pop_front() {
                debug!("Processing task at blink {} with {} stones", blinks_used, stones.len());
                for &stone_num in &stones {
                    if let Some(tasks) = task_map.get(&(stone_num as u64)) {
                        for task in tasks {
                            if blinks_used + task.blinks <= blink_limit {
                                debug!("  Processing stone {} at blink {}", stone_num, blinks_used);
                                total_stones += task.stones_gained as usize;
                                task_queue.push_back((blinks_used + task.blinks, task.stones_to_enqueue.clone()));
                            }
                        }
                    }
                }
            }

            debug!("Final count for initial stone {}: {}", stone.num, total_stones);
            total_stones
        })
        .sum()
}

fn main() {
    env_logger::init();
    debug!("Starting stone processing...");

    let input = std::fs::read_to_string("sample_input.txt")
        .expect("Failed to read input file");

    let initial_stones = extract_stones(&input);
    debug!("Loaded {} initial stones", initial_stones.len());

    let mut task_map: HashMap<u64, Vec<Task>> = HashMap::new();
    task_map.insert(0, vec![Task{total_blinks_so_far: 0, blinks: 1, stones_gained: 0, stones_to_enqueue: vec![1]}]);
    task_map.insert(1, vec![Task{total_blinks_so_far: 0, blinks: 3, stones_gained: 3, stones_to_enqueue: vec![0, 2, 2, 4]}]);
    task_map.insert(2, vec![Task{total_blinks_so_far: 0, blinks: 3, stones_gained: 3, stones_to_enqueue: vec![0, 4, 4, 8]}]);
    task_map.insert(3, vec![Task{total_blinks_so_far: 0, blinks: 3, stones_gained: 3, stones_to_enqueue: vec![0, 0, 7, 2]}]);
    task_map.insert(4, vec![Task{total_blinks_so_far: 0, blinks: 3, stones_gained: 3, stones_to_enqueue: vec![0, 6, 8, 9]}]);
    task_map.insert(5, vec![Task{total_blinks_so_far: 0, blinks: 5, stones_gained: 7, stones_to_enqueue: vec![0, 0, 2, 2, 4, 8, 8, 8]}]);
    task_map.insert(6, vec![Task{total_blinks_so_far: 0, blinks: 5, stones_gained: 7, stones_to_enqueue: vec![2, 4, 4, 5, 5, 6, 7, 9]}]);
    task_map.insert(7, vec![Task{total_blinks_so_far: 0, blinks: 5, stones_gained: 5, stones_to_enqueue: vec![0, 2, 2, 3, 6, 6, 7, 8]}]);
    task_map.insert(8, vec![
        Task{total_blinks_so_far: 0, blinks: 5, stones_gained: 5, stones_to_enqueue: vec![2, 2, 3, 6, 7, 7]},
        Task{total_blinks_so_far: 0, blinks: 4, stones_gained: 0, stones_to_enqueue: vec![8]},
    ]);
    task_map.insert(9, vec![Task{total_blinks_so_far: 0, blinks: 5, stones_gained: 5, stones_to_enqueue: vec![1, 3, 4, 6, 6, 8, 8, 9]}]);

    let result = process_stones(initial_stones, &task_map, 6);
    
    println!("Final result: {}", result);
}
