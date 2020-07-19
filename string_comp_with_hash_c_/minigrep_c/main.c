#include <stdio.h>
#include <stdlib.h>
#include <String.h>
#include "list.h"

/*
tets :

    mylist StList;
    listNew(&StList,sizeof(MyStruct),MyStructfree);
    const char *names[] = {"Suraj ","Is ","Doing ","this."};

    for(int i =0; i < 4; i++){
        MyStruct new_struct;
        new_struct.len = strlen(names[i]);
        new_struct.string = strdup(names[i]);
        listAdd(&StList,&new_struct);
    }

    for(int i =0; i < 4; i++){
        MyStruct mystring;
        listGet(&StList,&mystring,i);
        char *rest = strdup(mystring.string);
        printf("%s",rest);
    }
    listDispose(&StList);
    printf("waiting");

    mylist StringList;
    listNew(&StringList,sizeof(char *),StringFree);
    char *names2[] = {"Suraj ","Is ","Doing ","this."};
    for(int i= 0; i < 4; i++ ){
        char* res = strdup(names2[i]);
        listAdd(&StringList,&res);
        char* mystring;
        listGet(&StringList,&mystring,i);
        printf("%s",mystring);
    }
    listDispose(&StringList);
    printf("waiting");
    return 1;

*/

typedef struct{
    unsigned int len;
    char** string;
}MyStruct;

void MyStructfree(void *);
void StringFree(void * elem);


void read_to_string(FILE *fp,mylist* results){
    char ch;
    while((ch = fgetc(fp)) != EOF)
        listAdd(results,&ch);
}


int main(){
    mylist results;
    FILE *fp;
    char ch;
    int w_count;
    listNew(&results,sizeof(char),NULL);

    fp = fopen("rfc822.txt","r");
    if (fp == NULL){
        perror("Error in opening file \n");
        exit(EXIT_FAILURE);
    }
    read_to_string(fp,&results);
    char *token = strtok((char *)results.elems,"\n");
    while(token != NULL){
        w_count++;
        token = strtok(NULL," ");
    }
    printf("\n doc has %d words",w_count);
    listDispose(&results);
    fclose(fp);
}

void MyStructfree(void* elem){
    //[debug]> p  (char *)(*(MyStruct *)(StList -> elems)).string
    //[debug]$15 = 0xc51b50 "Suraj "
    //[debug]>>>>>>cb_gdb:

    //$15 = 0xc51b50 "Suraj "
    char **str_ptr = ((MyStruct *)(elem))->string;
    free(str_ptr); //
    //StringFree((MyStruct*)elem + sizeof(unsigned int));
}


void StringFree(void * elem){
    free(*(char **)elem);
}