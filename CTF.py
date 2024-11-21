from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        #os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        #os.remove(file_name)
    
def count_vote(vote):
    with open(r"D:\2024\Crypto 2\Final Count.txt", "r") as f:
        lines = f.readlines()
    with open(r"D:\2024\Crypto 2\Final Count.txt", "w") as f:
        for row in lines: 
            row = row.split(":")
            if row[0] == vote:
                row[1] = str(int(row[1]) + 1)
            f.write(row[0] + ": " + row[1] + "\n")

   


if __name__ == "__main__":
    Redfield = 0
    Barsoum = 0
    Hanna = 0
    vote = ""

    with open(r"D:\2024\Crypto 2\key.txt","rb") as f:
        key = f.read()
    enc = Encryptor(key)
    clear = lambda: os.system('cls')

    name = input("Name: ")
    validation_number = input("Validation number: ")
    valid = False

    enc.decrypt_file(r"D:\2024\Crypto 2\valid numbers.txt.enc")
    with open(r"D:\2024\Crypto 2\valid numbers.txt", "r") as f:
        clear()
        lines = f.readlines()
        for row in lines:
            row = row.split(":")
            #print(row[0])
            if row[1].find(validation_number) != -1 and row[0].strip().find(name) != -1:
                print("validation number found: " + row[0])
                valid = True
        enc.encrypt_file(r"D:\2024\Crypto 2\valid numbers.txt")



    if valid:
        
        with open(r"D:\2024\Crypto 2\valid numbers.txt", "w") as f:
            for row in lines:
                row = row.split(":")
                #if line[0] == name:
                if row[1].strip() != validation_number:
                    f.write(row[0] + ": " + row[1])
        
        print("valid user")
        while True:
            #clear()
            choice = int(input(
                "1. Press '1' to Vote for Barsoum.\n2. Press '2' to vote for Redfield.\n3. Press '3' to vote for Hanna.\n"))
            clear()
            if choice == 1:
                Barsoum += 1
                vote = "Barsoum"
                print("You voted for Barsoum!")
                break
            elif choice == 2:
                Redfield += 1
                vote = "Redfield"
                print("You voted for Redfield")
                break
            elif choice == 3:
                Hanna += 1
                vote = "Hanna"
                print("You voted for Hanna")
                break
            else:
                print("Please select a valid option!")
        with open(r"D:\2024\Crypto 2\voted numbers.txt", "a") as f:
            f.writelines(validation_number + ": " + name + " voted for: " + vote + "\n")
        
        count_vote(vote)

    else: 
        print("user not found")

