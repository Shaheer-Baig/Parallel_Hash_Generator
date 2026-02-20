#ifndef HASHER_H
#define HASHER_H

#include <string>

// Calculate MD5 hash of a file
std::string calculate_md5(const std::string& filepath);

// Calculate SHA-256 hash of a file
std::string calculate_sha256(const std::string& filepath);

#endif // HASHER_H
