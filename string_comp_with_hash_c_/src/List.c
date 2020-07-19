#include<assert.h>
#include<string.h>
#include<stdlib.h>
#include "List.h"

void listNew(mylist *s,int elemsize){
    //void(*free)(void *)
    s -> elemSize = elemsize;
    s -> logicLength = 0;
    s -> maxLength = 4;
    s -> elems = malloc(4*elemsize);
    assert(s->elems != NULL);
}

void listDispose(mylist *s, ){
    //if s->freenfn != NULL
    //for i to s->lengh
    //s->freefn((char *) s->elems + i*s->elemSize)
    //freefn -> free(*(struct->char**))

    free(s -> elems);
}

static void stackGrow(mylist *s){
    s -> maxLength *= 2;
    s -> elems = realloc(s -> elems, s -> maxLength * s -> elemSize);
    assert(s -> elems != NULL);
}

void listAdd(mylist *s,void *elemaddr){
    if(s -> logicLength == s -> maxLength) stackGrow(s);
    void *target = (char *)s -> elems + (s -> logicLength * s -> elemSize);
    memcpy(target,elemaddr,s->elemSize);
    s -> logicLength++;
}

void listGet(mylist *s,void *resaddr, int place){
    assert(place <= s -> logicLength);
    void *source = (char *)s -> elems + (place * s -> elemSize);
    memcpy(resaddr,source,s -> elemSize);
}

