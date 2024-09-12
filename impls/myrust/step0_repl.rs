use std::io::{self, Write};

fn read(input: &String) -> &String {
    input
}

fn eval(input: &String) -> &String {
    input
}

fn print(input: &String) -> &String {
    input
}

fn rep(input: &String) -> &String {
    print(eval(read(input)))
}

fn main() {
    print!("user> ");
    io::stdout().flush().expect("couldn't flush stdout");
    let mut input = String::new();

    let mut bytes = io::stdin()
        .read_line(&mut input)
        .expect("could not read line");

    while bytes != 0 {
        println!("{}", rep(&input).trim());

        print!("user> ");
        io::stdout().flush().expect("couldn't flush stdout");
        input = String::new();
        bytes = io::stdin()
            .read_line(&mut input)
            .expect("could not read line");
    }
}
