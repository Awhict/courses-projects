#ifndef SYMTAB_H
#define SYMTAB_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KEY_LEN 32

typedef struct symtab symtab;

/* Type definitions */
typedef struct Type {
    char name[32]; // Name of the type or variable
    enum { PRIMITIVE, ARRAY, STRUCTURE } category; // Type category
    union {
        enum { INT, FLOAT, CHAR } primitive;      // For primitive types
        struct Array *array;                     // For arrays
        struct FieldList *structure;             // For structures
    };
} Type;

typedef struct Array {
    struct Type *base; // Base type of the array
    int size;          // Size of the array
} Array;

typedef struct FieldList {
    char name[32];          // Field name
    struct Type *type;      // Type of the field
    struct FieldList *next; // Pointer to the next field
} FieldList;

/* Symbol table entry */
typedef struct entry {
    char key[KEY_LEN + 1]; // Symbol name
    Type value;            // Symbol information
} entry;

void entry_init(entry *self, char *key, Type *value);

/* Symbol table operations */
symtab *symtab_init();
int symtab_insert(symtab *, char *, Type *);
Type *symtab_lookup(symtab *, char *);
int symtab_remove(symtab *, char *);

#endif /* SYMTAB_H */