#include "symtab.h"

/*
 * symbol table type, linked list implementation
 */
struct symtab {
    entry entry;
    struct symtab *next;
};

// ************************************************************
//    Your implementation goes here
// ************************************************************

void entry_init(entry *self, char *key, Type *value) {
    strncpy(self->key, key, KEY_LEN);
    self->key[KEY_LEN] = '\0';
    memcpy(&self->value, value, sizeof(Type));
}

symtab *symtab_init(){
    symtab *self = malloc(sizeof(symtab));
    memset(self, '\0', sizeof(symtab));
    self->next = NULL;
    return self;
}

int symtab_insert(symtab *self, char *key, Type *value) {
    symtab *ptr = self;
    while (ptr->next != NULL) {
        if (strcmp(ptr->entry.key, key) == 0)
            return 0; // Duplicate key
        ptr = ptr->next;
    }
    symtab *node = malloc(sizeof(symtab));
    memset(node, '\0', sizeof(symtab));
    entry_init(&node->entry, key, value);
    node->next = NULL;
    ptr->next = node;
    return 1;
}

Type *symtab_lookup(symtab *self, char *key) {
    symtab *ptr = self;
    while (ptr != NULL) {
        if (strcmp(ptr->entry.key, key) == 0)
            return &ptr->entry.value;
        ptr = ptr->next;
    }
    return NULL; // Not found
}

int symtab_remove(symtab *self, char *key) {
    symtab *ptr = self, *tmp;
    while (ptr->next != NULL) {
        if (strcmp(ptr->next->entry.key, key) == 0) {
            tmp = ptr->next;
            ptr->next = ptr->next->next;
            free(tmp);
            return 1;
        }
        ptr = ptr->next;
    }
    return 0;
}
