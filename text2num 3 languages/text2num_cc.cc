#include <string>
#include <vector>
#include <iostream>

using namespace std;


//add vec implementaion list.h for dynamic allocation

vector<int> get_num_from_string(string);
//void print_array(vector<int>);

int main(){
    
    //char *input = "global_string = test\nglobal_integer = 5\n[server]\nip = `27.0.0.1\nport = 80\n[[peers]]\nip = 127.0.0.1\nport = 8080\n[[peers]]\nip = 127.0.0.1 ";
    string input = "here is 20 rs -40";
    char one_char;
    unsigned int i = 0;
    unsigned int arr_len = 0;
    vector <int> arr;
    //arr = (int *)malloc(sizeof(int) * i);
    arr = get_num_from_string(input);  
    //printf("found %d results ",arr_len);
    //print_array(arr);
    //sfree(arr);
    std::cout << "\n[";
    for(unsigned int i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << ',';
    std::cout <<"]";
}

vector <int> get_num_from_string(string text)
{
    vector<int> results;
    //padding, as usual c is great
    text.push_back('_');
    unsigned int iter = 0;
    int out = 0,is_neg = 0,found = 0;
    for(iter = 0; iter < text.length() ; iter++){
        if ((char) text[iter] == '-') is_neg = 1;
        else if ((char) text[iter] >= '0' && (char) text[iter] <= '9'){
            found = 1;
            out *= 10;
            //out *= 10;
			out += (int) ((char) text[iter] - '0');
        }
        else{
            if( found && is_neg){
                out *= -1;
                results.push_back(out);
                out = 0 ;
                //printf("\n%d",out);
                found = 0;
                is_neg = 0;
                //nums_found++;
            }else if( found && !is_neg){
                //out = 1;
                //printf("\n%d",out);
                results.push_back(out);
                out = 0;
                found = 0;
                is_neg = 0;
               // nums_found++;
            }else{
            }
        }    
    }
    
    return results;
}

    