# BigInt Class Documentation

## Overview

The `BigInt` class is a custom implementation of arbitrary-precision integer arithmetic in Python. It allows for handling integers of unlimited size, with support for different number bases and advanced mathematical operations.

## Key Features

- Arbitrary-precision integer representation
- Support for multiple number bases
- Arithmetic operations for large numbers
- Negative number support
- Factorial calculation
- Interactive REPL (Read-Eval-Print Loop) for testing

## Class Structure

### Initialization

The `BigInt` class can be initialized in multiple ways:

```python
# From an integer
big_num1 = BigInt(12345)

# From a string
big_num2 = BigInt("123456789")

# With a custom base (default is base 10)
big_num3 = BigInt("1010", base=2)  # Binary number
```

### Attributes

- `base`: The numerical base of the BigInt (default: 10)
- `digits`: A list representing the digits of the number

## Supported Operations

### Arithmetic Operations

1. **Addition**: `+`
   - Supports addition of two BigInt numbers
   - Handles positive and negative numbers
   - Preserves sign

2. **Subtraction**: `-`
   - Supports subtraction of two BigInt numbers
   - Handles positive and negative numbers
   - Preserves sign and magnitude differences

3. **Multiplication**: `*`
   - Performs digit-by-digit multiplication
   - Handles sign propagation

4. **Integer Division**: `//`
   - Performs long division
   - Returns quotient as a BigInt
   - Handles sign and remainder

5. **Modulo**: `%`
   - Calculates remainder of division
   - Supports different signs

### Special Methods

- `__abs__()`: Returns absolute value
- `__neg__()`: Returns negation of the number
- `to_int()`: Converts BigInt to Python integer
- `factorial()`: Calculates factorial of the number

## Error Handling

- Division by zero raises `ZeroDivisionError`
- Negative numbers for factorial raise `ValueError`
- Invalid digits for the given base raise `ValueError`

## REPL (Read-Eval-Print Loop)

An interactive console is provided for testing BigInt operations:

```python
# Start the REPL
repl()

# Example interactions
>> BigInt(1000) + BigInt(2000)
Result: 3000
>> BigInt(10).factorial()
Result: 3628800
```

## Implementation Details

### Base Representation

- Supports arbitrary bases (default is base 10)
- Digits are stored in a list from most to least significant
- Leading zeros are automatically removed

### Digit-level Operations

Custom helper functions are used for low-level operations:
- `_list_compare()`: Compares lists of digits
- `_list_subtract()`: Performs digit-level subtraction

## Performance Considerations

- Digit-by-digit arithmetic can be slow for very large numbers
- Time complexity increases with the size of numbers
- Recommended for educational purposes and scenarios requiring arbitrary precision

## Limitations

- Performance may degrade with extremely large numbers
- Limited to basic arithmetic operations
- Not optimized for cryptographic or scientific computing

## Example Usage

```python
# Create large numbers
a = BigInt("123456789" * 10)  # Very large number
b = BigInt("987654321" * 5)   # Another large number

# Perform operations
result_add = a + b
result_mul = a * b
result_div = a // b
result_mod = a % b

# Factorial
big_factorial = BigInt(50).factorial()
```

## Future Improvements

- Implement more advanced mathematical operations
- Optimize performance for large-scale computations
- Add support for floating-point representations
- Implement comparison operators

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.

## License

[Insert appropriate license information]

## Authors

[Your Name/Organization]
