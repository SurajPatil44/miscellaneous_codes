
//use std::num::Wrapping;

use std::env;
use std::process;

use mygrep::Config;

fn main(){
    //let args: Vec<String> = env::args().collect();
    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Problems : {}",err);
        process::exit(1);
    });
    
    if let Err(e) = mygrep::run(config){
        eprintln!("App Error: {}",e);
        process::exit(1);
    }
    
    //eprintln!("{}",content);
}
