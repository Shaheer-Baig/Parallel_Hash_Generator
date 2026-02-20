#include <iostream>
#include <vector>
#include <string>
#include <filesystem>
#include <fstream>
#include <omp.h>
#include <chrono>
#include <mutex>
#include "hasher.h"

namespace fs = std::filesystem;

// Mutex for synchronized writing to output file
std::mutex output_mutex;

// Collect all files in a directory recursively
std::vector<std::string> collect_files(const std::string& directory) {
    std::vector<std::string> files;
    
    try {
        for (const auto& entry : fs::recursive_directory_iterator(directory)) {
            if (entry.is_regular_file()) {
                files.push_back(entry.path().string());
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error traversing directory: " << e.what() << std::endl;
    }
    
    return files;
}

int main(int argc, char* argv[]) {
    // Check command line arguments
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <directory_path> [hash_type]" << std::endl;
        std::cout << "  hash_type: md5 or sha256 (default: sha256)" << std::endl;
        return 1;
    }

    std::string directory = argv[1];
    std::string hash_type = "sha256";
    
    if (argc >= 3) {
        hash_type = argv[2];
        if (hash_type != "md5" && hash_type != "sha256") {
            std::cerr << "Invalid hash type. Use 'md5' or 'sha256'" << std::endl;
            return 1;
        }
    }

    // Check if directory exists
    if (!fs::exists(directory) || !fs::is_directory(directory)) {
        std::cerr << "Error: Directory does not exist: " << directory << std::endl;
        return 1;
    }

    std::cout << "=== Parallel File Hash Generator ===" << std::endl;
    std::cout << "Directory: " << directory << std::endl;
    std::cout << "Hash Type: " << hash_type << std::endl;
    
    // Check OpenMP
    #ifdef _OPENMP
        std::cout << "OpenMP: Enabled" << std::endl;
        std::cout << "Max Threads: " << omp_get_max_threads() << std::endl;
    #else
        std::cout << "OpenMP: Disabled (running single-threaded)" << std::endl;
    #endif
    
    std::cout << std::endl;

    // Collect all files
    std::cout << "Collecting files..." << std::endl;
    auto start_collect = std::chrono::high_resolution_clock::now();
    std::vector<std::string> files = collect_files(directory);
    auto end_collect = std::chrono::high_resolution_clock::now();
    
    std::cout << "Found " << files.size() << " files in " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_collect - start_collect).count() 
              << " ms" << std::endl;

    if (files.empty()) {
        std::cout << "No files found." << std::endl;
        return 0;
    }

    // Open output file
    std::string output_filename = "hash_results_" + hash_type + ".txt";
    std::ofstream output_file(output_filename, std::ios::trunc);
    
    if (!output_file.is_open()) {
        std::cerr << "Error: Cannot create output file" << std::endl;
        return 1;
    }

    // Write header
    output_file << "File Hash Results (" << hash_type << ")" << std::endl;
    output_file << "Directory: " << directory << std::endl;
    output_file << "Total Files: " << files.size() << std::endl;
    output_file << "============================================" << std::endl;
    output_file << std::endl;
    output_file.close();

    std::cout << "Computing hashes in parallel..." << std::endl;
    auto start_hash = std::chrono::high_resolution_clock::now();

    // Progress counter
    int processed = 0;
    int total = files.size();

    // PARALLEL REGION - EREW PRAM Model
    // Each thread reads its own exclusive file (Exclusive Read)
    // Each thread writes to the shared output file with mutex protection (Exclusive Write)
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < files.size(); ++i) {
        const std::string& filepath = files[i];
        
        // Calculate hash (EREW: Exclusive Read - each thread reads different file)
        std::string hash;
        if (hash_type == "md5") {
            hash = calculate_md5(filepath);
        } else {
            hash = calculate_sha256(filepath);
        }

        // Fault Tolerance: If error occurs, retry once
        if (hash.find("ERROR") == 0) {
            std::cerr << "Error hashing file, retrying: " << filepath << std::endl;
            // Retry
            if (hash_type == "md5") {
                hash = calculate_md5(filepath);
            } else {
                hash = calculate_sha256(filepath);
            }
        }

        // SYNCHRONIZATION: Critical section for writing to shared output file
        {
            std::lock_guard<std::mutex> lock(output_mutex);
            
            // Write to output file
            std::ofstream output(output_filename, std::ios::app);
            output << hash << "  " << filepath << std::endl;
            output.close();

            // Update progress
            processed++;
            if (processed % 10 == 0 || processed == total) {
                std::cout << "Progress: " << processed << "/" << total << " files processed" << std::endl;
            }
        }
    }

    auto end_hash = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_hash - start_hash).count();

    std::cout << std::endl;
    std::cout << "=== Results ===" << std::endl;
    std::cout << "Total files processed: " << files.size() << std::endl;
    std::cout << "Time taken: " << duration << " ms" << std::endl;
    std::cout << "Average time per file: " << (files.size() > 0 ? duration / files.size() : 0) << " ms" << std::endl;
    std::cout << "Results saved to: " << output_filename << std::endl;

    return 0;
}
