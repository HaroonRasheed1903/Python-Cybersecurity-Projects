import hashlib
import time
from Crypto.Hash import MD4

wordlist_file = "wordlist.txt"
target_hash = input("Enter password hash: ")
algorithm = input("Choose algorithm (md5/sha256/sha512/blake2b/blake2s/ntlm): ")
salt = ""
salt_position = ""


def hash_word(word):
    if salt:
        word = salt + word if salt_position == "prefix" else word + salt
    if algorithm == "md5":
        return hashlib.md5(word.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(word.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(word.encode()).hexdigest()
    elif algorithm == "blake2b":
        return hashlib.blake2b(word.encode()).hexdigest()
    elif algorithm == "blake2s":
        return hashlib.blake2s(word.encode()).hexdigest()
    elif algorithm == "ntlm":
        encoded_word = word.encode('utf-16le')
        return MD4.new(encoded_word).hexdigest().upper()
    else:
        raise ValueError("Unsupported algorithm")


def main():
    start = time.time()
    cracked_pass = ""
    with open(wordlist_file, "r") as file:
        words = [line.strip() for line in file]
    for word in words:
        hashed = hash_word(word)
        if hashed == target_hash:
            cracked_pass = word
            break

    end = time.time()
    print(f"Finished in {round(end-start, 2)} seconds")
    if cracked_pass:
        print(f"[+] CRACKED: The password is --> {cracked_pass}")
    else:
        print("The password does not match any in the list...")


if __name__ == "__main__":
    main()