extern crate rsa;
extern crate rand;
extern crate csv;
extern crate rayon;

use crate::rsa::PublicKey;
use rsa::{RSAPrivateKey, PaddingScheme};
use rand::rngs::OsRng;
use std::time::Instant;
use rayon::prelude::*;
use std::sync::{Arc, Mutex};

fn generate_key_pair(key_size: usize) -> RSAPrivateKey {
    let mut rng = OsRng;
    RSAPrivateKey::new(&mut rng, key_size).expect("failed to generate a key")
}

fn measure_execution_time<F: FnOnce()>(f: F) -> f64 {
    let start = Instant::now();
    f();
    let duration = start.elapsed();
    duration.as_secs_f64()
}

fn main() {
    let prime_magnitudes = vec![2048, 3072, 4096, 8192, 16384, 32768, 65536, 131072, 262144];
    let results_table = Arc::new(Mutex::new(Vec::new()));

    prime_magnitudes.par_iter().for_each(|&prime_mag| {
        let private_key = generate_key_pair(prime_mag);
        let public_key = &private_key;
        let message = b"Hello, RSA.";

        let encryption_time = measure_execution_time(|| {
            public_key.encrypt(&mut OsRng, PaddingScheme::new_pkcs1v15_encrypt(), message).expect("failed to encrypt");
        });

        let encrypted_message = public_key.encrypt(&mut OsRng, PaddingScheme::new_pkcs1v15_encrypt(), message).expect("failed to encrypt");

        let decryption_time = measure_execution_time(|| {
            private_key.decrypt(PaddingScheme::new_pkcs1v15_encrypt(), &encrypted_message).expect("failed to decrypt");
        });

        let results_entry = (prime_mag, encryption_time, decryption_time);

        let mut results_table = results_table.lock().unwrap();
        results_table.push(results_entry);

        println!("Testing for prime magnitude {} completed.", prime_mag);
    });

    let results_table = Arc::try_unwrap(results_table).unwrap().into_inner().unwrap();

    println!("\nResults Table:");
    for entry in &results_table {
        println!("{:?}", entry);
    }

    let csv_filename = "rsa_results.csv";
    let mut wtr = csv::Writer::from_path(csv_filename).expect("failed to create a csv writer");

    wtr.write_record(&["Prime Magnitude", "Encryption Time (seconds)", "Decryption Time (seconds)"]).expect("failed to write header");

    for entry in &results_table {
        wtr.write_record(&[entry.0.to_string(), entry.1.to_string(), entry.2.to_string()]).expect("failed to write record");
    }

    wtr.flush().expect("failed to write to csv file");

    println!("\nResults exported to {}", csv_filename);
}
