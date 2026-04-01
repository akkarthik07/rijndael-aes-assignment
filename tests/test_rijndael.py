import ctypes
import os
import sys
import random

#Load the compiled shared library
rijndael = ctypes.CDLL('./rijndael.so')

AES_BLOCK_SIZE_128 = 0
AES_BLOCK_SIZE_256 = 1
AES_BLOCK_SIZE_512 = 2

ByteArray16 = ctypes.c_ubyte * 16

#sEt the argument types for the add_round_key function
rijndael.add_round_key.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]

def test_add_round_key():
    print("Testing add_round_key...")
    for i in range(3):
        block_data = bytes(random.randint(0, 255) for _ in range(16))
        key_data = bytes(random.randint(0, 255) for _ in range(16))

        expected = bytes(b ^ k for b, k in zip(block_data, key_data))

        block = ByteArray16(*block_data)
        round_key = ByteArray16(*key_data)

        rijndael.add_round_key(block, round_key, AES_BLOCK_SIZE_128)
        result = bytes(block)

        assert result == expected, (
            f"Test {i+1} FAILED\n"
            f"  block:    {list(block_data)}\n"
            f"  key:      {list(key_data)}\n"
            f"  expected: {list(expected)}\n"
            f"  got:      {list(result)}"
        )
        print(f"  Test {i+1} passed")
    print("add_round_key: ALL PASSED\n")

# Run the tests
if __name__ == "__main__":
    test_add_round_key()