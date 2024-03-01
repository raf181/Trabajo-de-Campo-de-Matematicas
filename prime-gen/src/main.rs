// ============================================================================ //
// This program generates prime numbers of a given length and saves them to a file
// for use in the RSA encryption algorithm.
//
// Single core variant of the prime-gen program.
//
// It uses the Miller-Rabin primality test to check if a number is prime.
// The Miller–Rabin primality test or Rabin–Miller primality test is a probabilistic
// primality test: an algorithm which determines whether a given number is likely to 
// be prime, similar to the Fermat primality test and the Solovay–Strassen primality test.
// ============================================================================ //
use std::fs::File;
use std::io::{self, Write};
use std::time::Instant;

fn is_prime(num: u128) -> bool {
    if num <= 1 {
        return false;
    }
    if num <= 3 {
        return true;
    }
    if num % 2 == 0 || num % 3 == 0 {
        return false;
    }

    // Check divisibility by all numbers from 5 to the square root of num
    let sqrt_num = (num as f64).sqrt() as u128;
    for i in (5..=sqrt_num).step_by(6) {
        if num % i == 0 || num % (i + 2) == 0 {
            return false;
        }
    }

    true
}

fn find_primes_with_length(length: u32, count: usize) -> Vec<u128> {
    let start = 10u128.pow(length - 1);
    let end = 10u128.pow(length);

    let mut primes = Vec::with_capacity(count);
    let mut num = start;
    while primes.len() < count {
        if is_prime(num) {
            primes.push(num);
        }
        num += 1;
    }

    primes
}

fn main() -> io::Result<()> {
    // Measure execution time
    let start_time = Instant::now();

    // Generate and save primes for each length from 1 to 50
    for length in 25..=50 {
        let result = find_primes_with_length(length, 5);

        // Save results to a JSON file
        let filename = format!("prime_numbers_{}_digits.json", length);
        let mut json_file = File::create(filename)?;

        writeln!(json_file, "{}", serde_json::to_string_pretty(&result).unwrap())?;
    }

    // Print execution time
    let end_time = start_time.elapsed();
    println!(
        "Results saved to JSON files for each length from 1 to 50\n\
         Total Execution Time: {:.15} seconds",
        end_time.as_secs_f64()
    );

    Ok(())
}
