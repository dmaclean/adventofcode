use std::collections::{HashMap, HashSet};

fn main() {
    let input = std::fs::read_to_string("input.txt").unwrap();
    let lines = input.lines().collect::<Vec<&str>>();
    let mut page_map: HashMap<&str, HashSet<&str>> = HashMap::new();
    let mut found_divider = false;
    let mut page_number_sum = 0;
    for line in lines {
        if line.is_empty() {
            found_divider = true;
            println!("page_map: {:?}", page_map);
            continue;
        }
        if !found_divider {
            let parts = line.split("|").collect::<Vec<&str>>();
            let page = parts[0];
            let queue = parts[1];
            page_map
                .entry(page)
                .and_modify(|set| {
                    set.insert(queue);
                })
                .or_insert_with(|| {
                    let mut set = HashSet::new();
                    set.insert(queue);
                    set
                });
        } else {
            let pages = line.split(",").collect::<Vec<&str>>();
            // println!("{:?}", pages);
            let mut order_correct = true;
            for i in 0..pages.len() {
                if i == 0 {
                    continue;
                }
                let page = pages[i];
                let map_vals = match page_map.get(page) {
                    Some(vals) => vals,
                    None => {
                        continue;
                    }
                };
                let prev_pages = &pages[0..i];
                for prev_page in prev_pages {
                    if map_vals.contains(prev_page) {
                        order_correct = false;
                        break;
                    }
                }
            }
            if order_correct {
                page_number_sum += pages[pages.len() / 2].parse::<i32>().unwrap();
            }
        }
    }
    println!("page_number_sum: {}", page_number_sum);
}
