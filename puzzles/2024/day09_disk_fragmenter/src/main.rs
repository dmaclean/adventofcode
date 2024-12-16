fn main() {
    let input = std::fs::read_to_string("sample_input2.txt").unwrap();
    // let input = "12345";
    let disk_map: Vec<char> = input.chars().collect();
    let mut disk: Vec<char> = create_disk(&disk_map);
    println!("{:?}", disk);
    disk = defrag(disk);
    println!("{:?}", disk);
    let checksum = checksum(&disk);
    println!("{:?}", checksum);
}

fn checksum(disk: &Vec<char>) -> u64 {
    let mut checksum = 0;
    let mut idx = 0;
    while disk[idx] != '.' {
        checksum += disk[idx].to_digit(10).unwrap() as u64 * idx as u64;
        idx += 1;
    }
    checksum
}

fn defrag(mut disk: Vec<char>) -> Vec<char> {
    let mut i = 0;
    let mut j = disk.len() - 1;
    while i < j {
        if disk[i] != '.' {
            // There's already a block here, so we don't need to do anything
            i += 1;
            continue;
        }
        // If we got here then there's an empty space that needs to be filled
        while disk[j] == '.' && j > i {
            j -= 1;
        }
        if j <= i {
            break;
        }
        disk[i] = disk[j];
        disk[j] = '.';
        i += 1;
        j -= 1;
    }
    disk
}

fn create_disk(disk_map: &Vec<char>) -> Vec<char> {
    let mut disk: Vec<char> = vec![];
    let mut is_file = true;
    let mut index = 0;
    for i in 0..disk_map.len() {
        let val = disk_map[i].to_digit(10).unwrap();
        for _ in 0..val {
            if is_file {
                disk.push(index.to_string().chars().next().unwrap());
            } else {
                disk.push('.');
            }
        }
        if is_file {
            index += 1;
        }
        is_file = !is_file;

    }
    disk
}
