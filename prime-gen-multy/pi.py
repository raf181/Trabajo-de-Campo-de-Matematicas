import json
import timeit
import math

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    
    # Check divisibility by all numbers from 5 to the square root of num
    for i in range(5, int(math.sqrt(num)) + 1, 6):
        if num % i == 0 or num % (i + 2) == 0:
            return False
    
    return True

def find_primes_with_length(length, count):
    start = 10 ** (length - 1)
    end = 10 ** length

    primes = []
    num = start
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes

# Measure execution time
start_time = timeit.default_timer()

# Generate and save primes for each length from 1 to 50
for length in range(20, 51):
    result = find_primes_with_length(length, 50)

    # Save results to a JSON file
    filename = f"prime_numbers_{length}_digits.json"
    with open(filename, 'w') as json_file:
        json.dump(result, json_file)

# Print execution time
end_time = timeit.default_timer()
execution_time = end_time - start_time
print(f"Results saved to JSON files for each length from 1 to 50")
print(f"Total Execution Time: {execution_time:.15f} seconds")
