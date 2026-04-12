#include "symtab.h"

/*
 * symbol table type, binary tree impl
 */
struct symtab {
    entry entry;
    struct symtab *left, *right;
};

// ************************************************************
//    Implementation goes here
// ************************************************************

symtab *symtab_init(){
    symtab *self = malloc(sizeof(symtab));
    if (self != NULL) {
        memset(self, '\0', sizeof(symtab));
        self->left = self->right = NULL;
    }
    return self;
}

int symtab_insert(symtab *self, char *key, VAL_T value){
    if (self == NULL) {
        return 0;
    }

    // Traverse tree and insert at appropriate position
    symtab **current = &self;
    while (*current != NULL) {
        int cmp = strcmp((*current)->entry.key, key);

        // Key already exists
        if (cmp == 0) {
            return 0;
        } else if (cmp > 0) {
            current = &(*current)->left;
        } else {
            current = &(*current)->right;
        }
    }

    // Insert new node
    *current = malloc(sizeof(symtab));
    if (*current == NULL) return 0;
    memset(*current, '\0', sizeof(symtab));
    entry_init(&(*current)->entry, key, value);
    (*current)->left = (*current)->right = NULL;

    return 1;
}

VAL_T symtab_lookup(symtab *self, char *key){
    while (self != NULL) {
        int cmp = strcmp(self->entry.key, key);

        if (cmp == 0) {
            return self->entry.value;
        } else if (cmp > 0) {
            self = self->left;
        } else {
            self = self->right;
        }
    }

    // Key not found
    return -1;
}

int symtab_remove(symtab *self, char *key){
    symtab *parent = NULL;
    symtab *current = self;
    symtab *tmp = NULL;

    // Search for the node to remove
    while (current != NULL && strcmp(current->entry.key, key) != 0) {
        parent = current;
        if (strcmp(key, current->entry.key) < 0) {
            current = current->left;
        } else {
            current = current->right;
        }
    }

    // If the key was not found
    if (current == NULL) {
        return 0;
    }

    // Case 1: Node has no children
    if (current->left == NULL && current->right == NULL) {
        if (parent == NULL) { // Root node
            free(current);
            return 1;
        }
        if (parent->left == current) {
            parent->left = NULL;
        } else {
            parent->right = NULL;
        }
        free(current);
    }
    // Case 2: Node has one child
    else if (current->left == NULL || current->right == NULL) {
        tmp = current->left ? current->left : current->right;
        if (parent == NULL) { // Root node
            *self = *tmp;
        } else if (parent->left == current) {
            parent->left = tmp;
        } else {
            parent->right = tmp;
        }
        free(current);
    }
    // Case 3: Node has two children
    else {
        symtab *successor = current->right;
        symtab *successor_parent = current;

        // Find the successor (smallest in the right subtree)
        while (successor->left != NULL) {
            successor_parent = successor;
            successor = successor->left;
        }

        // Replace current entry with successor entry
        current->entry = successor->entry;

        // Remove successor
        if (successor_parent->left == successor) {
            successor_parent->left = successor->right;
        } else {
            successor_parent->right = successor->right;
        }
        free(successor);
    }

    return 1;
}
