import csv
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import timeit

# Función para generar un par de claves RSA con el tamaño de clave especificado
def generate_key_pair(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    return private_key

# Función para medir el tiempo de ejecución de una función dada con argumentos
def measure_execution_time(func, *args):
    execution_time = timeit.timeit(lambda: func(*args), number=1)
    return execution_time

def main():
    # Definir magnitudes mayores de números primos
    prime_magnitudes = [2048, 3072, 4096, 8192, 16384, 32768, 65536, 131072, 262144]  # Ajustar según sea necesario
    results_table = []

    # Iterar a través de cada magnitud de primo
    for prime_mag in prime_magnitudes:
        # Generar un par de claves RSA con la magnitud actual
        private_key = generate_key_pair(prime_mag)
        public_key = private_key.public_key()
        message = b"Hello, RSA."

        try:
            # Medir tiempo de encriptación
            encryption_time = measure_execution_time(
                public_key.encrypt, message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            # Medir tiempo de desencriptación
            decryption_time = measure_execution_time(
                private_key.decrypt, public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            # Almacenar resultados en un diccionario y añadir a la tabla
            results_entry = {
                'Prime Magnitude': prime_mag,
                'Encryption Time (seconds)': encryption_time,
                'Decryption Time (seconds)': decryption_time
            }
            results_table.append(results_entry)

            # Mensaje de salida indicando la finalización para la magnitud de primo actual
            print(f"Testing for prime magnitude {prime_mag} completed.")

        except (ValueError, TypeError, AssertionError) as e:
            print(f"Error for prime magnitude {prime_mag}: {e}")

    # Imprimir la tabla de resultados
    print("\nResults Table:")
    for entry in results_table:
        print(entry)

    # Escribir resultados en un archivo CSV
    csv_filename = 'rsa_results.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Prime Magnitude', 'Encryption Time (seconds)', 'Decryption Time (seconds)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in results_table:
            writer.writerow(entry)

    print(f"\nResults exported to {csv_filename}")

# Ejecutar la función principal cuando se ejecute el script
if __name__ == "__main__":
    main()
