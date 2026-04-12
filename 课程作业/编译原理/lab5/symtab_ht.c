#include "symtab.h"

#define TABLE_SIZE 0x1003  // Prime number for better hash distribution

struct symtab {
    struct _node *table[TABLE_SIZE];  // Array for hash table, with separate chaining
};

struct _node {
    entry entry;
    struct _node *next;
};

// ************************************************************
//    Implementation goes here
// ************************************************************

// Hash function to compute the index based on the key
unsigned int hash(char *key) {
    unsigned int hash = 0;
    while (*key) {
        hash = (hash << 5) + *key++;
    }
    return hash % TABLE_SIZE;
}

// Initialize a symbol table
symtab *symtab_init() {
    symtab *self = malloc(sizeof(symtab));
    if (!self) return NULL;
    memset(self->table, 0, sizeof(self->table));  // Initialize all entries to NULL
    return self;
}

// Insert a key-value pair into the hash table
int symtab_insert(symtab *self, char *key, VAL_T value) {
    unsigned int index = hash(key);
    struct _node *ptr = self->table[index];

    // Check if the key already exists in the list at the given index
    while (ptr != NULL) {
        if (strcmp(ptr->entry.key, key) == 0) {
            return 0;  // Key already exists, insertion fails
        }
        ptr = ptr->next;
    }

    // Create a new node and insert at the head of the list
    struct _node *node = malloc(sizeof(struct _node));
    if (!node) return 0;
    entry_init(&node->entry, key, value);
    node->next = self->table[index];
    self->table[index] = node;
    return 1;
}

// Lookup the value associated with a key
VAL_T symtab_lookup(symtab *self, char *key) {
    unsigned int index = hash(key);
    struct _node *ptr = self->table[index];

    // Traverse the linked list at the index
    while (ptr != NULL) {
        if (strcmp(ptr->entry.key, key) == 0) {
            return ptr->entry.value;  // Key found, return value
        }
        ptr = ptr->next;
    }
    return -1;  // Key not found
}

// Remove a key-value pair from the hash table
int symtab_remove(symtab *self, char *key) {
    unsigned int index = hash(key);
    struct _node *ptr = self->table[index];
    struct _node *prev = NULL;

    // Traverse the linked list to find the node to remove
    while (ptr != NULL) {
        if (strcmp(ptr->entry.key, key) == 0) {
            if (prev == NULL) {  // Node is the head of the list
                self->table[index] = ptr->next;
            } else {
                prev->next = ptr->next;
            }
            free(ptr);  // Free the node memory
            return 1;   // Key removed successfully
        }
        prev = ptr;
        ptr = ptr->next;
    }
    return 0;  // Key not found
}
