#ifndef LIST_H_INCLUDED
#define LIST_H_INCLUDED


typedef void (*freefn)(void *);

typedef struct {
    void *elems;
    int elemSize;
    int logicLength;
    int maxLength;
    freefn freefn;
}mylist;


void listNew(mylist *s,int elemsize,void (*freefn)(void *));
void listDispose(mylist *s);
void listAdd(mylist *s,void *elemaddr);
void listGet(mylist *s,void *resaddr,int place);
void listRemove(mylist *s,int place);

#endif // LIST_H_INCLUDED
