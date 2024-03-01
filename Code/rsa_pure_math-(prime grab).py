import json
import os
import random
import time
import csv

def generate_keypair(key_length):
    # Paso 1: Elegir dos números primos distintos p y q
    p = generate_prime_number(key_length)
    q = generate_prime_number(key_length)
    
    # Paso 2: Calcular n = pq
    n = p * q
    
    # Paso 3: Calcular φ(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)

    # Paso 4: Elegir un entero e tal que 1 < e < φ(n) y gcd(e, φ(n)) = 1
    e = choose_public_exponent(phi_n)

    # Paso 5: Calcular d, el inverso multiplicativo modular de e (mod φ(n))
    d = modular_inverse(e, phi_n)

    # Clave pública: (n, e), Clave privada: (n, d)
    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def generate_prime_number(key_length):
    # Función para coger un número primo aleatorio de los almacenados en el archivo
    file_name = f"prime_numbers_{key_length}_digits.json"
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Prime number file {file_name} not found.")
    with open(file_name, 'r') as file:
        primes = json.load(file)

    return random.choice(primes)

def choose_public_exponent(phi_n):
    # Función para elegir un exponente público e
    e = random.randrange(2, phi_n)
    while gcd(e, phi_n) != 1:
        e = random.randrange(2, phi_n)
    return e

def gcd(a, b):
    # Función para calcular el máximo común divisor
    while b:
        a, b = b, a % b
    return a

def modular_inverse(a, m): # Función para calcular el inverso multiplicativo modular usando el Algoritmo Extendido de Euclides
    # Guarda el valor original de m
    m0 = m
    # Inicializa x0 y x1
    x0, x1 = 0, 1
    # Mientras a sea mayor que 1
    while a > 1:
        # Calcula el cociente
        q = a // m
        # Actualiza a y m
        m, a = a % m, m
        # Actualiza x0 y x1
        x0, x1 = x1 - q * x0, x0
    # Si x1 es negativo, suma m0 para hacerlo positivo
    return x1 + m0 if x1 < 0 else x1


# Number of runs
num_runs = 10
# Range of key lengths to test
key_length_range = range(1, 26)
# List to store run-specific timing results
all_run_results = []

for key_length in key_length_range:
    key_length_results = {"Key Length": key_length}

    for run in range(1, num_runs + 1):
        # Dictionary to store timing results for the current run
        run_results = {"Run": run}

        # Generate Key Pair
        start_time_keygen = time.perf_counter()
        public_key, private_key = generate_keypair(key_length)  
        end_time_keygen = time.perf_counter()
        run_results["Key Generation"] = end_time_keygen - start_time_keygen

        # Sample Message
        message = 27575756757671

        # Encryption
        start_time_encryption = time.perf_counter()
        ciphertext = pow(message, public_key[1], public_key[0])
        end_time_encryption = time.perf_counter()
        run_results["Encryption"] = end_time_encryption - start_time_encryption

        # Decryption
        start_time_decryption = time.perf_counter()
        decrypted_message = pow(ciphertext, private_key[1], private_key[0])
        end_time_decryption = time.perf_counter()
        run_results["Decryption"] = end_time_decryption - start_time_decryption

        # Total (Encryption + Decryption)
        run_results["Total (Encryption + Decryption)"] = run_results["Encryption"] + run_results["Decryption"]

        # Append results for the current run to the list
        all_run_results.append({**key_length_results, **run_results})

# Save Run-Specific Results to CSV
csv_file = "key_length_results.csv"
header = ["Key Length", "Run", "Key Generation", "Encryption", "Decryption", "Total (Encryption + Decryption)"]

with open(csv_file, mode="w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(all_run_results)

# Output Run-Specific Results
print("=================================================================================================")
print(f"Run-specific results saved to: {csv_file}")