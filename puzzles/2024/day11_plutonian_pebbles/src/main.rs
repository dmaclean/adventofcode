use log::{debug, trace};
use env_logger;
use petgraph::graph::{DiGraph, NodeIndex};
use petgraph::visit::EdgeRef;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Stone {
    num: u64,
    length: u8
}

struct Node {
    stone: Stone,
    children: Vec<Child>
}

struct Child {
    weight: u8,
    node: Node
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

struct TransitionGraph {
    graph: DiGraph<u64, u8>,
    node_map: HashMap<u64, NodeIndex>,
}

impl TransitionGraph {
    fn new() -> Self {
        Self {
            graph: DiGraph::new(),
            node_map: HashMap::new(),
        }
    }

    fn get_or_create_node(&mut self, num: u64) -> NodeIndex {
        if let Some(&node_idx) = self.node_map.get(&num) {
            node_idx
        } else {
            let node_idx = self.graph.add_node(num);
            self.node_map.insert(num, node_idx);
            node_idx
        }
    }

    fn add_transition(&mut self, from: u64, to: u64, blinks: u8) {
        let from_idx = self.get_or_create_node(from);
        let to_idx = self.get_or_create_node(to);
        self.graph.add_edge(from_idx, to_idx, blinks);
    }

    fn add_abbreviated_transitions(&mut self) {
        debug!("Adding abbreviated transitions to graph");
        // Single-digit transitions
        self.add_transition(0, 1, 1);
        debug!("Added: 0 -(1)-> 1");
        
        // 1's transitions (cost 3)
        for &to in &[0, 2, 2, 4] {
            self.add_transition(1, to, 3);
            debug!("Added: 1 -(3)-> {}", to);
        }

        // 2's transitions (cost 3)
        for &to in &[0, 4, 4, 8] {
            self.add_transition(2, to, 3);
            debug!("Added: 2 -(3)-> {}", to);
        }

        // 3's transitions (cost 3)
        for &to in &[0, 0, 7, 2] {
            self.add_transition(3, to, 3);
            debug!("Added: 3 -(3)-> {}", to);
        }

        // 4's transitions (cost 3)
        for &to in &[0, 6, 8, 9] {
            self.add_transition(4, to, 3);
            debug!("Added: 4 -(3)-> {}", to);
        }

        // 5's transitions (cost 5)
        for &to in &[0, 0, 2, 2, 4, 8, 8, 8] {
            self.add_transition(5, to, 5);
            debug!("Added: 5 -(5)-> {}", to);
        }

        // 6's transitions (cost 5)
        for &to in &[2, 4, 4, 5, 5, 6, 7, 9] {
            self.add_transition(6, to, 5);
            debug!("Added: 6 -(5)-> {}", to);
        }

        // 7's transitions (cost 5)
        for &to in &[0, 2, 2, 3, 6, 6, 7, 8] {
            self.add_transition(7, to, 5);
            debug!("Added: 7 -(5)-> {}", to);
        }

        // 8's transitions (two paths)
        self.add_transition(8, 8, 4); // Short path
        debug!("Added: 8 -(4)-> 8");
        for &to in &[2, 2, 3, 6, 7, 7] { // Long path
            self.add_transition(8, to, 5);
            debug!("Added: 8 -(5)-> {}", to);
        }

        // 9's transitions (cost 5)
        for &to in &[1, 3, 4, 6, 6, 8, 8, 9] {
            self.add_transition(9, to, 5);
            debug!("Added: 9 -(5)-> {}", to);
        }
    }

    fn process_stone(&self, stone: &Stone, blink_limit: u8) -> usize {
        let mut stone_instances: HashMap<(u64, u8), HashSet<(u64, u8)>> = HashMap::new();
        let mut stone_queue = vec![(stone.num, 0)];
        stone_instances.insert((stone.num, 0), HashSet::new());

        while let Some((current_num, blinks_used)) = stone_queue.pop() {
            debug!("  Processing num {} at blink {}", current_num, blinks_used);
            if blinks_used >= blink_limit {
                debug!("    Skipping - exceeded blink limit");
                continue;
            }

            let current_stone = Stone {
                num: current_num,
                length: current_num.to_string().len() as u8,
            };

            if current_num > 9 {
                debug!("    Processing large number {}", current_num);
                let next_stones = current_stone.transition();
                let next_blinks = blinks_used + 1;
                
                if next_blinks <= blink_limit {
                    let current_key = (current_num, blinks_used);
                    for stone in next_stones {
                        let next_key = (stone.num, next_blinks);
                        stone_instances.entry(current_key)
                            .or_insert_with(HashSet::new)
                            .insert(next_key);
                        
                        debug!("      Queueing {} for processing at blink {}", 
                            stone.num, next_blinks);
                        stone_queue.push((stone.num, next_blinks));
                        stone_instances.insert(next_key, HashSet::new());
                    }
                }
            } else if let Some(&node_idx) = self.node_map.get(&current_num) {
                debug!("    Found in transition graph");
                for edge in self.graph.edges(node_idx) {
                    let next_blinks = blinks_used + edge.weight();
                    let next_num = self.graph[edge.target()];
                    debug!("      Edge to {} with weight {} (total blinks: {})", 
                        next_num, edge.weight(), next_blinks);
                    
                    if next_blinks <= blink_limit {
                        let current_key = (current_num, blinks_used);
                        let next_key = (next_num, next_blinks);
                        
                        stone_instances.entry(current_key)
                            .or_insert_with(HashSet::new)
                            .insert(next_key);
                        
                        debug!("        Queueing {} for processing at blink {}", next_num, next_blinks);
                        stone_queue.push((next_num, next_blinks));
                        stone_instances.insert(next_key, HashSet::new());
                    } else {
                        debug!("        Skipping - would exceed blink limit");
                    }
                }
            }
        }

        // Count stones at the final state
        let mut final_stones = HashSet::new();
        for (&(num, blinks), transitions) in &stone_instances {
            if transitions.is_empty() && blinks <= blink_limit {
                final_stones.insert((num, blinks));
            }
        }

        debug!("Final count for stone {}: {} stones", stone.num, final_stones.len());
        final_stones.len()
    }
}

fn main() {
    env_logger::init();
    debug!("Starting stone processing...");

    let input = std::fs::read_to_string("sample_input.txt")
        .expect("Failed to read input file");

    let initial_stones = extract_stones(&input);
    debug!("Loaded {} initial stones", initial_stones.len());

    let mut graph = TransitionGraph::new();
    graph.add_abbreviated_transitions();

    let result: usize = initial_stones.iter()
        .map(|stone| {
            let count = graph.process_stone(stone, 3);
            debug!("Stone {} produced {} stones", stone.num, count);
            count
        })
        .sum();
    
    println!("Final result: {}", result);
}
