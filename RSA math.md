- RSA book: [Handbook of Applied Cryptography (uwaterloo.ca)](https://cacr.uwaterloo.ca/hac/)
	- chapter 2:[chap2.pdf (uwaterloo.ca)](https://cacr.uwaterloo.ca/hac/about/chap2.pdf)
	- chapter 4: [chap4.pdf (uwaterloo.ca)](https://cacr.uwaterloo.ca/hac/about/chap4.pdf)
	- chapter 8:[chap8.pdf (uwaterloo.ca)](https://cacr.uwaterloo.ca/hac/about/chap8.pdf)
    
Prime number generation: 
- Miller–Rabin primality test, source: [How can I generate large prime numbers for RSA? - Cryptography Stack Exchange](https://crypto.stackexchange.com/questions/71/how-can-i-generate-large-prime-numbers-for-rsa)

## "RSA" Encryption:
RSA (Rivest-Shamir-Adleman) is a widely used cryptographic algorithm for encryption and decryption, named after its inventors. It relies on the mathematical properties of large prime numbers to provide secure communication over insecure channels. Here's a brief summary of how RSA encryption and decryption work:

1. Key Generation:
    - Choose two distinct large prime numbers, p and q.
    - Compute the modulus $n = p * q$.
    - Compute Euler's totient function $φ(n) = (p - 1) * (q - 1)$.
    - Select a public exponent e, which is typically a small prime, such as $65537 (2^16 + 1)$
    - or 3. e must be greater than 1 and less than φ(n).
    - Calculate the private exponent d, which is the modular multiplicative inverse of e modulo $φ(n$). In other words, $(e * d) mod φ(n) = 1$.

1. Encryption:
    - Convert the plaintext message into a numerical representation M, where M is an integer such that 0 < M < n.
    - Use the recipient's public key (n, e) to encrypt the message.
    - Calculate the ciphertext $C = M^e (mod n)$, where "^" represents exponentiation and "mod" is the modulus operation.

1. Decryption:

    - The recipient uses their private key (n, d) to decrypt the ciphertext C.
    - Calculate the original message $M = C^d (mod n)$, where "^" represents exponentiation and "mod" is the modulus operation.

It's important to note that the security of RSA relies on the difficulty of factoring large composite numbers (n) into their prime factors (p and q). As long as the primes are large enough, the algorithm is secure against brute-force attacks.

RSA is widely used for secure communication and digital signatures, making it a fundamental component of modern cryptographic systems. However, it can be computationally intensive, especially for very large numbers, and alternative cryptographic algorithms like Elliptic Curve Cryptography (ECC) are also commonly used to address these computational challenges.