import json
import os
import random

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



public_key, private_key = generate_keypair(key_length=8)  # Replace * with the desired key length
message = 27575756757671

# Función de cifrado
ciphertext = pow(message, public_key[1], public_key[0])
# Función de descifrado
decrypted_message = pow(ciphertext, private_key[1], private_key[0])

print(f"Public Key: {public_key}")
print(f"Private Key: {private_key}")
print(f"=================================================================================================")
print(f"Original Message: {message}")
print(f"Encrypted Message: {ciphertext}")
print(f"Decrypted Message: {decrypted_message}")
