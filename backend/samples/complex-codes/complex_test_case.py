def is_prime(n):
    """Prime number check using trial division method"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check divisibility by odd numbers from 3 to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def quicksort(arr):
    """Quicksort implementation"""
    if len(arr) <= 1:
        return arr
    
    # Choose pivot as middle element for better efficiency
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

def sieve_of_eratosthenes(limit):
    """Generate prime numbers up to limit using Sieve of Eratosthenes"""
    if limit < 2:
        return []
    
    # Initialize sieve array
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    i = 2
    while i * i <= limit:
        if sieve[i]:
            # Mark multiples of i as composite
            j = i * i
            while j <= limit:
                sieve[j] = False
                j += i
        i += 1
    
    # Create list of prime numbers
    primes = []
    for i in range(2, limit + 1):
        if sieve[i]:
            primes.append(i)
    
    return primes

def fibonacci_sequence(n):
    """Generate first n Fibonacci numbers"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

def prime_factors(n):
    """Prime factorization of n"""
    factors = []
    d = 2
    
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

def gcd(a, b):
    """Greatest Common Divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Least Common Multiple"""
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    """Matrix multiplication"""
    if len(A[0]) != len(B):
        raise ValueError("Matrix dimensions don't match")
    
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def complex_processing_demo():
    """Demo function combining multiple algorithms"""
    print("=== Prime Filter with Quicksort Demo ===\n")
    
    # 1. Generate primes up to 100
    print("1. Generate primes up to 100 using Sieve of Eratosthenes:")
    primes_100 = sieve_of_eratosthenes(100)
    print(f"Number of primes: {len(primes_100)}")
    print(f"First 10: {primes_100[:10]}")
    print(f"Last 10: {primes_100[-10:]}\n")
    
    # 2. Fibonacci sequence up to 15th term
    print("2. Fibonacci sequence (first 15 terms):")
    fib_15 = fibonacci_sequence(15)
    print(fib_15)
    
    # 3. Extract primes from Fibonacci sequence
    fib_primes = [n for n in fib_15 if is_prime(n)]
    print(f"Prime numbers in Fibonacci sequence: {fib_primes}\n")
    
    # 4. Filter and sort primes from test array
    test_numbers = [97, 23, 58, 11, 89, 34, 17, 42, 73, 29, 67, 91, 13, 56, 37]
    print("3. Test number array:")
    print(f"Original array: {test_numbers}")
    
    # Extract primes only
    prime_numbers = [n for n in test_numbers if is_prime(n)]
    print(f"Prime numbers only: {prime_numbers}")
    
    # Sort using quicksort
    sorted_primes = quicksort(prime_numbers)
    print(f"After sorting: {sorted_primes}\n")
    
    # 5. Prime factorization demo
    print("4. Prime factorization demo:")
    test_nums = [24, 60, 100, 147, 999]
    for num in test_nums:
        factors = prime_factors(num)
        print(f"{num} = {' x '.join(map(str, factors))}")
    print()
    
    # 6. GCD and LCM
    print("5. Greatest Common Divisor and Least Common Multiple:")
    pairs = [(48, 18), (100, 75), (17, 19)]
    for a, b in pairs:
        gcd_val = gcd(a, b)
        lcm_val = lcm(a, b)
        print(f"gcd({a}, {b}) = {gcd_val}, lcm({a}, {b}) = {lcm_val}")
    print()
    
    # 7. Matrix multiplication demo
    print("6. Matrix multiplication:")
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    C = matrix_multiply(A, B)
    
    print("Matrix A:")
    for row in A:
        print(row)
    print("Matrix B:")
    for row in B:
        print(row)
    print("A x B =")
    for row in C:
        print(row)

# Run demo
if __name__ == "__main__":
    complex_processing_demo()
