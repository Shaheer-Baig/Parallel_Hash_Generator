#include "hasher.h"
#include <openssl/md5.h>
#include <openssl/sha.h>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>

// Convert bytes to hex string
static std::string bytes_to_hex(const unsigned char* data, size_t len) {
    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    for (size_t i = 0; i < len; ++i) {
        ss << std::setw(2) << static_cast<int>(data[i]);
    }
    return ss.str();
}

std::string calculate_md5(const std::string& filepath) {
    try {
        std::ifstream file(filepath, std::ios::binary);
        if (!file.is_open()) {
            return "ERROR: Cannot open file";
        }

        MD5_CTX md5Context;
        MD5_Init(&md5Context);

        char buffer[4096];
        while (file.read(buffer, sizeof(buffer))) {
            MD5_Update(&md5Context, buffer, file.gcount());
        }
        // Handle remaining bytes
        if (file.gcount() > 0) {
            MD5_Update(&md5Context, buffer, file.gcount());
        }

        unsigned char result[MD5_DIGEST_LENGTH];
        MD5_Final(result, &md5Context);

        file.close();
        return bytes_to_hex(result, MD5_DIGEST_LENGTH);
    }
    catch (const std::exception& e) {
        return std::string("ERROR: ") + e.what();
    }
}

std::string calculate_sha256(const std::string& filepath) {
    try {
        std::ifstream file(filepath, std::ios::binary);
        if (!file.is_open()) {
            return "ERROR: Cannot open file";
        }

        SHA256_CTX sha256Context;
        SHA256_Init(&sha256Context);

        char buffer[4096];
        while (file.read(buffer, sizeof(buffer))) {
            SHA256_Update(&sha256Context, buffer, file.gcount());
        }
        // Handle remaining bytes
        if (file.gcount() > 0) {
            SHA256_Update(&sha256Context, buffer, file.gcount());
        }

        unsigned char result[SHA256_DIGEST_LENGTH];
        SHA256_Final(result, &sha256Context);

        file.close();
        return bytes_to_hex(result, SHA256_DIGEST_LENGTH);
    }
    catch (const std::exception& e) {
        return std::string("ERROR: ") + e.what();
    }
}
