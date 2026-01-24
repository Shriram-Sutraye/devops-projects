# calculator.py - A simple calculator module

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

# Main entry point (for demo purposes)
if __name__ == "__main__":
    print("🧮 Simple Calculator")
    print(f"  5 + 3 = {add(5, 3)}")
    print(f"  10 - 4 = {subtract(10, 4)}")
    print(f"  6 * 7 = {multiply(6, 7)}")
    print(f"  20 / 4 = {divide(20, 4)}")
    print("✅ Calculator is working!")
