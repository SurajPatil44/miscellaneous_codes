//how would you write a grep if you use C program

use std::fs;
use std::error::Error;

pub struct Config{
    fname : String,
    pattern : String,
    case_insensitive : bool
}


impl Config{
    pub fn new(mut args: std::env::Args) -> Result<Self,&'static str>{
        args.next(); //filename
        /*
        let file = args[1].clone();
        let pattern = args[2].clone();
        */
        let file = match args.next(){
            Some(arg) => arg,
            None => return Err("Filename is not provided")
        };
        let pattern = match args.next(){
            Some(arg) => arg,
            None => return Err("Query pattern is not provided")
        };
        
        
        let case_insensitive = match args.next(){
            Some(arg) => {
                let arg = String::from(arg);
                if arg == "1"{
                    true
                }else{
                    false
                }
            },
            None => false
        };
        
        Ok(Config{fname:file,
               pattern,
               case_insensitive
        })
    }
}

#[derive(Debug)]
struct Position{
    lineno : u32,
    pos : u32,
    line : String
}

fn myHash(text : &str) -> usize{

    /*
    unsigned long
    hash(unsigned char *str)
    {
        unsigned long hash = 5381;
        int c;

        while (c = *str++)
            hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

        return hash;
    }
    */
    let mut hash = 5138usize;
    
    //let it be as it is case sensitivity will take care as different function
    
    for chr in text.chars(){
        hash = hash.wrapping_mul(33);
        hash = hash.wrapping_add(chr as usize);
    }        
    
    hash
}


pub fn run(config : Config) -> Result<(),Box<dyn Error>>{
    
    let contents = fs::read_to_string(config.fname)?;
    //&contents
    for po in search(&contents,&config.pattern,config.case_insensitive){
        eprintln!("{} {} {} ",po.lineno,po.pos,po.line);
    }
    Ok(())
}

fn search(text :&str, query: &str, case: bool) -> Vec<Position>{
    
    //this is lots of overhead 
    
    let mut text_s = String::new();
    let mut query_s = String::new();
    if !case{
        text_s = String::from(text).to_lowercase().to_string();    
        query_s = String::from(query).to_lowercase().to_string();
    }else{
        text_s = String::from(text).to_string();
        query_s = String::from(query).to_string();
    }
    
    //need to find some zero copy method to lowercase &str 
    
    let len1 = text.len();
    let len2 = query.len();
    let q_hash = myHash(&query_s);
    let mut last_nl = 0;
    let mut last_nl_pos = 0;
    let mut prev_nl_pos = 0;
    let mut block : Vec<Position> = Vec::with_capacity(5);
    
    for (i,chr) in text_s.chars().enumerate()
    {
        if i <= (len1 - len2)
        { 
            if chr == '\n'{
                last_nl += 1 as u32;
                prev_nl_pos = last_nl_pos;
                last_nl_pos = i as u32 ;    
            }
            
            if myHash(&text_s[i..i+len2]) == q_hash
            {
                let num = i as u32 - last_nl_pos;
                block.push(Position{
                    lineno : last_nl + 1,
                    pos : num + 1,
                    line : String::from(&text[prev_nl_pos as usize..last_nl_pos as usize])
                });
            }
        }
    }
    block
}

