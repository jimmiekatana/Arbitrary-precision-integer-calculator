class BigInt:
    def __init__(self, value=0, base=10):
        self.base = base
        self.digits = []
        if isinstance(value, int):
            if value == 0:
                self.digits = [0]
            else:
                while value > 0:
                    self.digits.append(value % base)
                    value //= base
                self.digits.reverse()
        elif isinstance(value, str):
            self.from_str(value, base)
        elif isinstance(value, list):
            # Allow initialization from a list of digits
            self.digits = value
        
        self._validate_digits()

    def _validate_digits(self):
        """Validate that all digits are within the base range."""
        for digit in self.digits:
            if digit < 0 or digit >= self.base:
                raise ValueError(f"Digit {digit} is out of range for base {self.base}")

    def from_str(self, value, base=10):
        self.base = base
        self.digits = []
        value = value.strip()
        
        # Handle negative numbers
        sign = 1
        if value.startswith('-'):
            sign = -1
            value = value[1:]
        
        if value == '0':
            self.digits = [0]
        else:
            for char in value:
                self.digits.append(int(char, base))
        
        if sign == -1:
            self.digits = [-d for d in self.digits]

    def __str__(self):
        # Handle negative numbers in string representation
        if self.digits and self.digits[0] < 0:
            return '-' + ''.join(str(abs(digit)) for digit in self.digits)
        return ''.join(str(abs(digit)) for digit in self.digits)

    def __repr__(self):
        return f"BigInt({str(self)})"

    def to_int(self):
        result = 0
        for digit in self.digits:
            result = result * self.base + abs(digit)
        return result * (1 if self.digits[0] >= 0 else -1)

    def _normalize(self):
        """Remove leading zeros."""
        while len(self.digits) > 1 and self.digits[0] == 0:
            self.digits.pop(0)

    def __abs__(self):
        """Return the absolute value of the BigInt."""
        result = BigInt()
        result.digits = [abs(d) for d in self.digits]
        result.base = self.base
        return result

    def __neg__(self):
        """Return the negation of the BigInt."""
        result = BigInt()
        result.digits = [-d for d in self.digits]
        result.base = self.base
        return result

    def __add__(self, other):
        # Handle different sign scenarios
        if self.digits[0] < 0 and other.digits[0] >= 0:
            return other - abs(self)
        elif self.digits[0] >= 0 and other.digits[0] < 0:
            return self - abs(other)
        
        sign = 1 if self.digits[0] >= 0 else -1
        carry = 0
        result_digits = []
        a_digits = [abs(d) for d in self.digits[::-1]]
        b_digits = [abs(d) for d in other.digits[::-1]]
        max_len = max(len(a_digits), len(b_digits))
        
        for i in range(max_len):
            a_digit = a_digits[i] if i < len(a_digits) else 0
            b_digit = b_digits[i] if i < len(b_digits) else 0
            total = a_digit + b_digit + carry
            carry = total // self.base
            result_digits.append(total % self.base)
        
        if carry:
            result_digits.append(carry)

        result_digits.reverse()
        result = BigInt()
        result.digits = [sign * d for d in result_digits]
        result._normalize()
        return result

    def __sub__(self, other):
        # Handle different sign scenarios
        if self.digits[0] < 0 and other.digits[0] < 0:
            return abs(other) - abs(self)
        elif self.digits[0] < 0:
            return -abs(self) - other
        elif other.digits[0] < 0:
            return self + abs(other)
        
        # Ensure first number is larger
        if abs(self) < abs(other):
            result = other - self
            result.digits = [-d for d in result.digits]
            return result
        
        borrow = 0
        result_digits = []
        a_digits = self.digits[::-1]
        b_digits = other.digits[::-1]
        max_len = max(len(a_digits), len(b_digits))
        
        for i in range(max_len):
            a_digit = a_digits[i] if i < len(a_digits) else 0
            b_digit = b_digits[i] if i < len(b_digits) else 0
            total = a_digit - b_digit - borrow
            if total < 0:
                total += self.base
                borrow = 1
            else:
                borrow = 0
            result_digits.append(total)
        
        result_digits.reverse()
        result = BigInt()
        result.digits = result_digits
        result._normalize()
        return result

    def __mul__(self, other):
        # Multiply BigInt * BigInt
        sign = 1
        if self.digits[0] < 0:
            sign *= -1
        if other.digits[0] < 0:
            sign *= -1
        
        result_digits = [0] * (len(self.digits) + len(other.digits))
        a_digits = [abs(d) for d in self.digits]
        b_digits = [abs(d) for d in other.digits]
        
        for i in range(len(a_digits) - 1, -1, -1):
            carry = 0
            for j in range(len(b_digits) - 1, -1, -1):
                mul = a_digits[i] * b_digits[j] + result_digits[i + j + 1] + carry
                carry = mul // self.base
                result_digits[i + j + 1] = mul % self.base
            result_digits[i + j] = carry

        result = BigInt()
        result.digits = [sign * d for d in result_digits]
        result._normalize()
        return result

    def __floordiv__(self, other):
        # Check for division by zero
        if other.to_int() == 0:
            raise ZeroDivisionError("Division by zero")
        
        # Handle sign
        sign = 1
        if self.digits[0] < 0:
            sign *= -1
        if other.digits[0] < 0:
            sign *= -1
        
        dividend = [abs(d) for d in self.digits]
        divisor = [abs(d) for d in other.digits]
        quotient = []
        
        # Long division algorithm
        remainder = []
        for digit in dividend:
            remainder.append(digit)
            while len(remainder) > 1 and remainder[0] == 0:
                remainder.pop(0)
            count = 0
            while _list_compare(remainder, divisor) >= 0:
                remainder = _list_subtract(remainder, divisor)
                count += 1
            quotient.append(count)
        
        result = BigInt()
        result.digits = [sign * d for d in quotient]
        result._normalize()
        return result

    def __mod__(self, other):
        # Check for modulo by zero
        if other.to_int() == 0:
            raise ZeroDivisionError("Modulo by zero")
        
        # Determine sign
        sign = 1 if self.digits[0] >= 0 else -1
        
        dividend = [abs(d) for d in self.digits]
        divisor = [abs(d) for d in other.digits]
        
        # Long division algorithm to get remainder
        remainder = []
        for digit in dividend:
            remainder.append(digit)
            while len(remainder) > 1 and remainder[0] == 0:
                remainder.pop(0)
            while _list_compare(remainder, divisor) >= 0:
                remainder = _list_subtract(remainder, divisor)
        
        result = BigInt()
        result.digits = [sign * d for d in remainder]
        result._normalize()
        return result

    def factorial(self):
        # Factorial implementation
        if self.to_int() < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if self.to_int() <= 1:
            return BigInt(1)
        
        result = BigInt(1)
        current = BigInt(1)
        
        while current.to_int() <= self.to_int():
            result *= current
            current += BigInt(1)
        
        return result

def _list_compare(a, b):
    """Compare two lists of digits lexicographically."""
    if len(a) > len(b):
        return 1
    elif len(a) < len(b):
        return -1
    
    for x, y in zip(a, b):
        if x > y:
            return 1
        elif x < y:
            return -1
    return 0

def _list_subtract(a, b):
    """Subtract two lists of digits."""
    a = a[::-1]
    b = b[::-1]
    result = []
    borrow = 0
    
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        total = x - y - borrow
        
        if total < 0:
            total += 10  # Assuming base 10 for subtraction
            borrow = 1
        else:
            borrow = 0
        
        result.append(total)
    
    while result and result[-1] == 0:
        result.pop()
    
    return result[::-1] or [0]

def repl():
    print("Welcome to BigInt REPL! Type 'exit' to quit.")
    while True:
        expr = input(">> ")
        if expr == 'exit':
            break
        try:
            result = eval(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()