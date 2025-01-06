"""
Bowen Dai
RSA part ii
Goal: 
The part ii of this project deals with the conversion between characters and numbers during encryption and decryption 
and implements a menu to let the user encrypts, decrypts or sets up a RSA system.
This program contains the following functions:
    - encrypt_text_to_integer_blocks: convert message to encrypted code
    - text_to_uft8_string: convert each character in the message to its uft8 then add 100 to make each uft8 3 digit long
    - message_block: slice a long message to block of the required length
    - encrypt_list: encrypt each number according to the public key

    - decrypt_integer_blocks_to_text: decrypt the encrypted code to the original message
    - decrypt_list: decrypt the encrypted code to the original uft8 
    - decrypted_message_to_decrypted_string: turn each decrypted block to string and add zero if necessary
    - decrypted_string: join a list of string to a long string and add 0 at the end if necessary
    - string_to_text: convert numbers in a long string to the character which has the corresponding uft8 of the string

    -check_int: check the whether the user inputs an integer, if not keep ask the user to input one until the input is an integer
"""
import RSA_project_part_i

def encrypt_text_to_integer_blocks ( public_key : tuple [int , int ], message : str ,block_length : int ):
    """ 
    This function converts a typed message into a list of encrypted blocks. 
    If someone wants to send Alice a secret message ,this function returns what they should send. 
    """
    utf8_str = text_to_utf8_string(message)
    int_message_block = message_blocks(utf8_str, block_length)
    encrypted_message_blocks = encrypt_list(int_message_block, public_key)

    return encrypted_message_blocks


def text_to_utf8_string ( message : str ) -> str :
    """
    This function converts each character in a string to its UFT-8 then add 100 make each character 3 digits long.
    """
    integer_message = "" # We start with an empty string , and will add to it as we convert the text to UTF -8.
    for letter in message :
    # You can use + to concatenate strings .
        integer_message = integer_message + str(ord(letter)+100)
        #add 100 to avoid the bug caused by 3 consecutive 0
    return integer_message


def message_blocks ( numeric_message :str , block_length :int ) -> list :
    """
    This function slices a long string to a list of equal length strings
    """
    blocks = [] # We will build a list of integers.
    for i in range (0 , len ( numeric_message ) , block_length ):
        blocks.append(int(numeric_message[i:i+block_length]))

    return blocks


def encrypt_list ( message_list : list , public_key : tuple [int , int]) -> list [int]:
    """ 
    This function should encrypt each integer in a list using the provided public key. 
    """
    encrypted_list = []
    m = public_key[0]

    for message in message_list:
        encrypted_list.append(RSA_project_part_i.encrypt((m, public_key[1]), message))

    return encrypted_list


def decrypt_integer_blocks_to_text ( private_key : tuple [int , int , int ], encrypted_message : list [int], block_length : int ):
    """ 
    This function takes a list of encrypted integers, decrypts them, and then converts them to text using UTF -8. 
    This is what Alice will see once she decrypts Bob's message .
    """
    decrypted_int  = decrypt_list(encrypted_message, private_key)
    decrypted_str = decrypted_string(decrypted_message_to_decrypted_string(decrypted_int, block_length))
    bobs_message = string_to_text(decrypted_str)
    return bobs_message


def decrypt_list ( encrypted_message_list : list [int], private_key : tuple [int, int, int]):
    """
    This function decrypts each element in the encrypted_message_list and return a list of decrypted numbers.
    """
    decrypted_list = []
    for x in encrypted_message_list :
        # decrypt each element in the encrypted list and put them in decrypted_list
        decrypted_list.append(RSA_project_part_i.decrypt(private_key, x))
    return decrypted_list


def decrypted_message_to_decrypted_string ( decrypted_message_list : list [int], block_length : int ):
    """ 
    This function replaces each block of the decrypted message by the original string that created the block .
    Every block except the last block must have length block_length .
    If the block started with a zero (or two zeros ), we must pad the block to full length .
    The last block must have a length which makes the total message divisible by 3.
    Since we added 100 at the beginning , the last block may need to be padded with a zero .
    """
    decrypted_message_string = []

    for num in decrypted_message_list:
        decrypted_message_string.append(str(num).zfill(block_length))
    decrypted_message_string.pop()
    decrypted_message_string.append(str(decrypted_message_list[-1]))
    return decrypted_message_string # return list of numeric strings


def decrypted_string ( decrypted_list : list )->str:
    """
    This function joins the decrypted list to a string.
    """
    decrypted = ''
    decrypted_str = decrypted.join(decrypted_list)
    while len(decrypted_str)%3 != 0:
        decrypted_str = decrypted_str + '0'
    return decrypted_str


def string_to_text ( decrypted: str ):
    """
    This function decrypts the joined string to characters using the UTF-8
    """
    message = ""  # Start with an empty message and add to it with a for loop .
    for i in range(0, len(decrypted),3):
        utf8 = int(decrypted[i: i+3])-100
        message = message + chr(utf8)
    return message

def check_int (user_input: str) -> str: 
    """
    This function takes a string as input and check if the string represents an integer. 
    If the string does not represent an integer, keep asking the user to input an integer until the user inputs an integer.
    Return the string when user input a string which represents an integer.
    """
    while not user_input.isdigit():
        user_input = input("Please enter a integer here:")
    return user_input


if __name__ == "__main__":
    """
    This function create an menu in which the user can chose to encrypt, decrypt or set up a RSA system.
    """
    running = True
    while running:
        print ('\033[1m  Main menu  \033[0m')
        print("""Welcome to RSA encryption & decryption. This is the main menu of the program.
Please type the corresponding number to use different functions for the program or type \"exit\" to terminate this program.
    1. encrypt your message with public key
    2. decrypt a message with private key
    3. generate public and private keys to set up RSA""")
        user_input = input("Type your choice here: ")
        print(" ")

        if user_input == "1":
            print ("""\033[1m  Encryption  \033[0m
Please enter the public key""")
            N = check_int(input("modulo = "))
            k = int(check_int(input("public exponent = ")))
            public_key = (int(N), k)
            print("Please chose a block length which is smaller than N's length")
            valid_block_length = False
            while not valid_block_length:
                block_length = int(input("block length = "))
                if (block_length < len(N)):
                    valid_block_length = True
                else:
                    print("Please choose block length smaller than {}".format(len(N)))
            
            running_1 = True
            while running_1:
                message = input("Please enter the message to encrypt: ")
                print("""The encrypted message is: {}
Enter \"b\" to go back to the main menu.
Press any other key to continue to encrypt another message with the same setup
                    """.format(encrypt_text_to_integer_blocks(public_key, message, block_length)))
                user_choice = input()
                if user_choice == "b":
                    print(" ")
                    running_1 = False

            
        elif user_input == "2":
            print ("""\033[1m  Decryption  \033[0m
Please enter the private key
Please enter the 2 prime factors of the modulo""")
            prime_list = []
            for i in range(2):
                valid_factors = False
                while not valid_factors:
                    p = int(check_int(input("prime factor {} = ".format(i+1))))
                    if RSA_project_part_i.check_prime(p):
                        valid_factors = True
                    else:
                        print("{} is not a prime. Please enter a prime number.".format(p))
                prime_list.append(p)

            private_exponent = int(check_int(input("private exponent = ")))
            private_key = (prime_list[0], prime_list[1], private_exponent)
            running_2 = True
            while running_2:
                print("Please type the encrypted message and click \"enter\" after the each term. When you finish to type every term, enter \"end\".")
                message_input = True
                message_list = []
                while message_input:
                    message = input()
                    if message == "end":
                        print(" ")
                        message_input = False
                    elif message.isdigit():
                        message_list.append(int(message))
                    else:
                        print("Invalid input. Please enter a number or \"end\".")
                block_length = int(check_int(input("Please enter the block length of the message: ")))

                print("""The message is: {}
                      
Enter \"b\" to go back to the main menu
Press any other key to continue to decrypt another message with the same setup
""".format(decrypt_integer_blocks_to_text(private_key, message_list, block_length)))
                user_choice = input()
                print(" ")
                if user_choice == "b":
                    running_2 = False

        elif user_input == "3":
            print ('\033[1m  set up RSA  \033[0m')
            running_3 = True
            while running_3:
                print("""Type \"p\" to use 2 prime numbers of your choice to generate public and private key.
Type \"r\" to generate random prime numbers for the public and private keys.
Type \"b\" to go back to the main menu""")
                user_choice = input("Type your choice here: ")
                if user_choice == "p":
                    print("Type the 2 primes")
                    prime_set = set()
                    while not len(prime_set) == 2:
                        p = int(check_int(input("prime = ")))
                        if RSA_project_part_i.check_prime(p):
                            prime_set.add(p)
                        else: 
                            print("{} is not a prime number. Please enter a prime number".format(p))


                    keys = RSA_project_part_i.generate_key(prime_set.pop(), prime_set.pop())
                    print("the public key is: {}".format(keys[0]))
                    print("the private key is: {}".format(keys[1]))

                elif user_choice == "r":
                    print("""Type \"n\" to choose approximately the size of prime that you wish to generate.
Type \"d\" to use default size of primes""")
                    valid_input = False
                    while not valid_input:
                        user_choice = input("Type your choice here: ")
                        if user_choice == "n":
                            n = int(check_int(input("Type the approximate size as the exponent of 2: the size of prime numbers I choose is approximately 2^")))
                            two_primes = RSA_project_part_i.two_primes(n)
                            print("The prime number around 2^{} are: {} and {}".format(n, two_primes[0], two_primes[1]))
                            valid_input = True
                        elif user_choice == "d":
                            print("The default size of the prime is 2^10.")
                            two_primes = RSA_project_part_i.two_primes(10)
                            print("The randomly generated primes are: {}, {}".format(two_primes[0],two_primes[1]))
                            valid_input = True
                        else:
                            print("Please type: \"n\" or \"d\"")
                    keys = RSA_project_part_i.generate_key(two_primes[0], two_primes[1])
                    print("""The public key is: {}
The private key is: {}
                          """.format(keys[0], keys[1]))
                    
                elif user_choice == "b":
                    print(" ")
                    running_3 = False
                else:
                    print("Invalid input. Please enter \"p\", \"r\" or \"b\".")
        elif user_input == "exit":
            print("Thank you for using this program.")
            running = False
        else:
            print("Invalid option. Please enter 1, 2, 3 or \"exit\". ")

            