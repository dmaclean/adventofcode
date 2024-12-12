use std::fs;

#[derive(Debug)]
struct Equation {
    result: i64,
    operands: Vec<i64>,
}

fn is_valid_equation(eq: &Equation) -> bool {
    let mut solutions: Vec<i64> = Vec::new();
    for i in 0..eq.operands.len() {
        if solutions.len() == 0 {
            solutions.push(eq.operands[i]);
            continue;
        }
        let mut new_solutions: Vec<i64> = Vec::new();
        for solution in solutions {
            new_solutions.push(solution + eq.operands[i]);
            new_solutions.push(solution * eq.operands[i]);
        }
        solutions = new_solutions;
    }
    solutions.contains(&eq.result)
}

fn extract_equations(input: &str) -> Vec<Equation> {
    let lines = input.lines();
    let mut equations: Vec<Equation> = Vec::new();
    for line in lines {
        let parts = line
            .split(": ")
            .collect::<Vec<&str>>();
        let result = parts[0]
            .split(" ")
            .last()
            .unwrap()
            .parse::<i64>()
            .unwrap();
        let operands = parts[1]
            .split(" ")
            .map(|s| s.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        equations.push(Equation { result, operands });
    }
    equations
}

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();
    let equations = extract_equations(&input);
    let mut result = 0;
    for eq in equations {
        if is_valid_equation(&eq) {
            result += eq.result;
        }
    }
    println!("{}", result);
}
