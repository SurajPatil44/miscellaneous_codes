fn get_int_nums_from_text(text : &str) -> Vec<i32>{

    let mut text = String::from(text);
    //padding to catch last trailing number
    text.push('_');
    let mut result : Vec<i32> = Vec::new();
    let mut out = 0;
    let mut is_neg = false;
    let mut here = false;
    for chr in text.chars(){
        let chr = chr as u8;
        if chr == '-' as u8{
            is_neg = true;
        }
        else if chr >= '0' as u8 && chr <= '9' as u8 {
            here = true;
            out *= 10;
            out += chr as i32 - '0' as i32;
        }
        else{
            match (here,is_neg){
                (true,true) => {
                    out *= -1;
                    result.push(out);
                    out = 0;
                    is_neg = false;
                    here = false;
                },
                (true,false) => {
                    here = false;
                    is_neg = false;
                    result.push(out);
                    out = 0;
                }
                (_,_) => {
                    is_neg = false;
                    here = false;
                }
            }
        }
    }
    result
}  
        
fn main(){
    let input = "here is 20 rs -40";
    let mut text = String::from(input);
    let res = get_int_nums_from_text(&mut text);
    println!("{:?}",res);
}