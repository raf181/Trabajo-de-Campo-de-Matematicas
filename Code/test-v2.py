from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import timeit

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
    execution_time = timeit.timeit(lambda: func(*args), number=1)
    return execution_time

def main():
    # Define different magnitudes of prime numbers
    prime_magnitudes = [2048, 3072, 4096, 4096, 8192, 16384]  # Adjust as needed

    # Iterate through each prime magnitude
    for prime_mag in prime_magnitudes:
        # Generate an RSA key pair with the current magnitude
        private_key = generate_key_pair(prime_mag)
        public_key = private_key.public_key()
        message = b"Hello, RSA."

        try:
            # Measure encryption time
            encryption_time = measure_execution_time(
                public_key.encrypt, message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            # Measure decryption time
            decryption_time = measure_execution_time(
                private_key.decrypt, public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )

            print(f"Prime Magnitude: {prime_mag}")
            print(f"Encryption Time: {encryption_time} seconds")
            print(f"Decryption Time: {decryption_time} seconds")
            print("-----------------------")

        except (ValueError, TypeError, AssertionError) as e:
            print(f"Error for prime magnitude {prime_mag}: {e}")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
