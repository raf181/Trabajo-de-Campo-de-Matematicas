// ============================================================================ //
// This program generates prime numbers of a given length and saves them to a file
// for use in the RSA encryption algorithm.
//
// Multicore core variant of the prime-gen program.
//
// It uses the Miller-Rabin primality test to check if a number is prime.
// The Miller–Rabin primality test or Rabin–Miller primality test is a probabilistic
// primality test: an algorithm which determines whether a given number is likely to 
// be prime, similar to the Fermat primality test and the Solovay–Strassen primality test.
// ============================================================================ //
use std::fs::File;
use std::io::{self, Write};
use std::time::Instant;
use rayon::prelude::*;

fn is_prime(num: u64) -> bool {
    if num <= 1 {
        false
    } else if num <= 3 {
        true
    } else if num % 2 == 0 || num % 3 == 0 {
        false
    } else {
        let sqrt_num = (num as f64).sqrt() as u64;
        (5..=sqrt_num).step_by(6).all(|i| num % i != 0 && num % (i + 2) != 0)
    }
}

fn find_primes_with_length(length: u32, count: usize) -> Vec<u64> {
    let start = 10u128.pow(length - 1) as u64;
    let end = (10u128.pow(length) - 1) as u64;

    (start..=end)
        .into_par_iter()
        .filter(|&num| is_prime(num))
        .collect::<Vec<_>>() // Collect into a Vec<u64>
        .into_iter()         // Convert back into a standard iterator
        .take(count)
        .collect()
}

fn main() -> io::Result<()> {
    // Measure execution time
    let start_time = Instant::now();

    // Generate and save primes for each length from 1 to 50 in parallel
    (1..=50).into_par_iter().for_each(|length| {
        let result = find_primes_with_length(length, 50);

        // Save results to a JSON file
        let filename = format!("prime_numbers_{}_digits.json", length);
        let filename = filename.trim(); // Trim whitespace
        let mut json_file = File::create(filename).unwrap();
        writeln!(json_file, "{}", serde_json::to_string_pretty(&result).unwrap()).unwrap();
    });

    // Print execution time
    let end_time = start_time.elapsed();
    println!(
        "Results saved to JSON files for each length from 1 to 50 in parallel\n\
         Total Execution Time: {:.15} seconds",
        end_time.as_secs_f64()
    );

    Ok(())
}
