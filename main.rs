use std::io::*;
use rand::Rng;
use lazy_static::lazy_static;
use std::sync::{Mutex, MutexGuard};

lazy_static! {static ref RND: Mutex<i32> = Mutex::new(0);
    static ref GUESS : Mutex<i32> = Mutex::new(0);}

fn main() {
    let mut wanna_play = true;
    while wanna_play {
        game();
        println!("Wanna play again? (Y/n)");
        if read_input().to_lowercase() == "n" {
            wanna_play = false;
        }
    }
}

fn game(){
    *get_guess() = 0;
    *get_rnd() = rand::thread_rng().gen_range(1..100);
    println!("Write down a number from 1 to 100");
    while *get_guess() != *get_rnd(){
        if parse_int(read_input()) {
            if *get_guess() == *get_rnd() {
                //guess is right
                break;
            }
            //guess is higher/lower
            println!("{}", generate_string(*GUESS.lock().unwrap()));
        }
    }
    println!("You won!")
}

fn get_guess() -> MutexGuard<'static, i32> {
    return GUESS.lock().unwrap();
}

fn get_rnd() -> MutexGuard<'static, i32> {
    return RND.lock().unwrap();
}

fn generate_string(guess: i32) -> &'static str {
    if guess > *get_rnd() {
        return "Too high!";
    }
    return "Too low!";
}

fn parse_int(input: String) -> bool {
    return match input.trim().parse::<i32>() {
        Ok(i) => {
            if i < 1 || i > 100 {
                println!("The number has to be from 1 to 100");
                return false;
            }
            *get_guess() = i;
            true
        }
        Err(..) => {
            println!("Invalid number");
            false
        }
    };
}

fn read_input() -> String{
    let mut input = String::new();
    stdin()
        .read_line(&mut input).unwrap();
    return input;
}