#include <stdlib.h>
#include <stdio.h>
#include <assert.h>


//add vec implementaion list.h for dynamic allocation

void get_num_from_string(const char *,const int,int*,int *);
void print_array(const int *,const int );

int main(){
    
    //char *input = "global_string = test\nglobal_integer = 5\n[server]\nip = `27.0.0.1\nport = 80\n[[peers]]\nip = 127.0.0.1\nport = 8080\n[[peers]]\nip = 127.0.0.1 ";
    char *input = "here is 20 rs -40";
    char one_char;
    unsigned int i = 0;
    unsigned int arr_len = 0;
    int *arr;
    while(1){
        one_char = input[i];
        if(one_char == '\0') break;
        i++;
    }
    arr = (int *)malloc(sizeof(int) * i);
    if (arr == NULL){
        exit(1);
    }
    get_num_from_string(input,i,arr,&arr_len);  
    //printf("found %d results ",arr_len);
    print_array(arr,arr_len);
    free(arr);
}

void get_num_from_string(const char *text,const int len,int *result,int *_len){
    
    /*
    if(*_len == 0 && nums_found == 0){
        printf("\n_len %d \n",*_len);
        nums_found++;
        *_len = nums_found;
        printf("\n_len %d \n",*_len);       
    }
    */
    int nums_found = *_len;
    int iter = 0,out = 0,is_neg = 0,found = 0;
    /*
    //padding the text to catch any traling number --> not needed in c
    char *new_text = (char *)malloc(sizeof(char) * len + 1);
    memcpy(new_text,text,len);
    new_text[len+1] = '_'
    */
    for(iter = 0; iter <= len ; iter++){
        if (text[iter] == '-') is_neg = 1;
        else if (text[iter] >= '0' && text[iter] <= '9'){
            found = 1;
            out *= 10;
            //out *= 10;
			out += text[iter] - '0';
        }
        else{
            if( found && is_neg){
                out *= -1;
                *(result + nums_found) = out;
                out = 0 ;
                //printf("\n%d",out);
                found = 0;
                is_neg = 0;
                nums_found++;
            }else if( found && !is_neg){
                //out = 1;
                //printf("\n%d",out);
                *(result + nums_found) = out;
                out = 0;
                found = 0;
                is_neg = 0;
                nums_found++;
            }else{
            }
        }    
    }
    *_len = nums_found;
}

void print_array(const int *res,const int len){
    unsigned int iter = 0;
    printf("\n[");
    for( iter = 0; iter < len ; iter++ ){
        printf("%d",res[iter]);
        printf(",");
    }
    printf("]");
}
    