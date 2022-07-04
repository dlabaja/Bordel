use std::io::*;
use rand::Rng;
use std::cmp::Ordering;
use std::cmp::Ordering::Less;

fn main() {
    println!("Let's play a number guessing game!");
    loop {
        game();
        println!("Wanna play again? (Y/n)");
        if read_input().trim().to_lowercase() == "n" {
            std::process::exit(0);
        }
    }
}

fn game() {
    let mut guess = 0;
    let rnd = rand::thread_rng().gen_range(1..101);
    println!("Write down a number from 1 to 100");

    while guess != rnd {
        guess = parse_int(read_input());
        if guess == 0 { continue; }

        match guess.cmp(&rnd) {
            Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        };
    }
}

fn parse_int(input: String) -> i32 {
    return match input.trim().parse::<i32>() {
        Ok(i) => {
            if !(1..101).contains(&i) {
                println!("The number has to be from 1 to 100");
                return 0;
            }
            i
        }
        Err(_) => {
            println!("Invalid number");
            0
        }
    };
}

fn read_input() -> String {
    let mut input = String::new();
    stdin()
        .read_line(&mut input).unwrap();
    return input;
}