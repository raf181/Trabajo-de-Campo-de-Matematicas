# =============================================================================
# Title: RSA Encryption and Decryption using Pure Math
# author: IB student KKJ634 (raf181)
# =============================================================================
import random

def generate_keypair(key_length):
    # Paso 1: Elegir dos números primos distintos p y q
    print(f"Generating prime numbers...")
    p = generate_prime_number(key_length)
    q = generate_prime_number(key_length)
    # Paso 2: Calcular n = pq
    print(f"Calculating n...")
    n = p * q
    # Paso 3: Calcular φ(n) = (p-1)(q-1)
    print(f"Calculating φ(n)...")
    phi_n = (p - 1) * (q - 1)
    # Paso 4: Elegir un entero e tal que 1 < e < φ(n) y gcd(e, φ(n)) = 1.
    print(f"Choosing public exponent e...")
    e = choose_public_exponent(phi_n)
    # Paso 5: Calcular d, el inverso multiplicativo modular de e (mod φ(n))
    print(f"Calculating private exponent d...")
    d = modular_inverse(e, phi_n)

    # Clave pública: (n, e), Clave privada: (n, d)
    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def generate_prime_number(digit_length):
    # Generate a prime number with the specified digit length
    lower_bound = 10 ** (digit_length - 1)
    upper_bound = 10 ** digit_length - 1
    return random.choice([n for n in range(lower_bound, upper_bound + 1) if is_prime(n)])

def is_prime(n):
    # Check if a number is prime
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

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

def modular_inverse(a, m):
    # Función para calcular el inverso multiplicativo modular usando el Algoritmo Extendido de Euclides
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

public_key, private_key = generate_keypair(key_length=6)  # Replace * with the desired key length
message = 275757
ciphertext = pow(message, public_key[1], public_key[0])
decrypted_message = pow(ciphertext, private_key[1], private_key[0])

print(f"=================================================================================================")
print(f"Public Key: {public_key}")
print(f"Private Key: {private_key}")
print(f"=================================================================================================")
print(f"Original Message: {message}")
print(f"Encrypted Message: {ciphertext}")
print(f"Decrypted Message: {decrypted_message}")
print(f"=================================================================================================")
print(f"Original Message == Decrypted Message: {message == decrypted_message}")