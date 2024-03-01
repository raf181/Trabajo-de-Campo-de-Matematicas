from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import time

# Function to generate an RSA key pair with the specified key size
def generate_key_pair(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    return private_key

# Function to measure the execution time of a given function with arguments
def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

def main():
    # Define different magnitudes of prime numbers
    prime_magnitudes = [512, 1024, 2048, 4096]  # Adjust as needed
    results_table = []

    # Iterate through each prime magnitude
    for prime_mag in prime_magnitudes:
        # Generate an RSA key pair with the current magnitude
        private_key = generate_key_pair(prime_mag)
        message = b"Hello, RSA!"

        try:
            # Measure encryption time
            encryption_result, encryption_time = measure_execution_time(
                private_key.public_key().encrypt, message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            # Measure decryption time
            decryption_result, decryption_time = measure_execution_time(
                private_key.decrypt, encryption_result, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            # Store results in a dictionary and add to the table
            results_entry = {
                'Prime Magnitude': prime_mag,
                'Encryption Time': encryption_time,
                'Decryption Time': decryption_time
            }
            results_table.append(results_entry)

        except Exception as e:
            print(f"Error for prime magnitude {prime_mag}: {e}")

    # Print the results table
    print("Results Table:")
    for entry in results_table:
        print(entry)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
