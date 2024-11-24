import sys

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    try:
        number = int(sys.argv[1])
        if is_prime(number):
            print(f"{number} is a prime number.")
        else:
            print(f"{number} is not a prime number.")
    except ValueError:
        print("Please enter a valid integer.")
        sys.exit(1)

# Unit tests
def test_is_prime():
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(5) == True
    assert is_prime(10) == False
    assert is_prime(13) == True
    assert is_prime(17) == True
    assert is_prime(20) == False
    assert is_prime(-3) == False
    assert is_prime(1) == False

test_is_prime()