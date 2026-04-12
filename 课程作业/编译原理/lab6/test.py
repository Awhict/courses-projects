#!/usr/bin/env python3
# encoding: utf-8

import ctypes
from ctypes import POINTER, Structure, c_char_p, c_int, c_void_p, byref

# Load the shared library
lib = ctypes.CDLL('./libsymtab.so')

# Define Type structure
class Type(Structure):
    _fields_ = [
        ("name", ctypes.c_char * 32),
        ("category", ctypes.c_int),
        ("primitive", ctypes.c_int),
    ]

# Define symtab structure
class Symtab(Structure):
    pass

# Function prototypes
lib.symtab_init.restype = POINTER(Symtab)

lib.symtab_insert.argtypes = [POINTER(Symtab), c_char_p, POINTER(Type)]
lib.symtab_insert.restype = c_int

lib.symtab_lookup.argtypes = [POINTER(Symtab), c_char_p]
lib.symtab_lookup.restype = POINTER(Type)

lib.symtab_remove.argtypes = [POINTER(Symtab), c_char_p]
lib.symtab_remove.restype = c_int

# Initialize a new symbol table
symtab = lib.symtab_init()

# Create a Type instance
def create_type(name, category, primitive=None):
    t = Type()
    t.name = name.encode('utf-8')
    t.category = category
    t.primitive = primitive if primitive is not None else 0
    return t

# Test cases
try:
    # Insert a primitive type (int)
    int_type = create_type("int", 0, 0)  # PRIMITIVE = 0, INT = 0
    assert lib.symtab_insert(symtab, b"x", byref(int_type)) == 1, "Insert failed"

    # Lookup the inserted type
    result = lib.symtab_lookup(symtab, b"x")
    assert result, "Lookup failed"
    assert result.contents.name.decode('utf-8') == "int", "Lookup returned incorrect name"
    assert result.contents.category == 0, "Lookup returned incorrect category"

    print("Test 1: Insert and lookup for a primitive type passed.")

    # Attempt to insert the same key (should fail)
    assert lib.symtab_insert(symtab, b"x", byref(int_type)) == 0, "Duplicate insert should fail"

    print("Test 2: Duplicate insert passed.")

    # Remove the key
    assert lib.symtab_remove(symtab, b"x") == 1, "Remove failed"

    print("Test 3: Remove passed.")

    # Lookup the removed key (should fail)
    assert lib.symtab_lookup(symtab, b"x") is None, "Lookup after removal should fail"

    print("Test 4: Lookup after removal passed.")

except AssertionError as e:
    print(f"Test failed: {e}")

