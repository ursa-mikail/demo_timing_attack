import time

# The secret value we're trying to guess
SECRET = "secret123"

def check_password(guess):
    # Check each character with a delay
    for i in range(len(SECRET)):
        if i >= len(guess) or guess[i] != SECRET[i]:
            return False
        # Introduce a slight delay for each correct character
        time.sleep(0.01)
    return len(guess) == len(SECRET)


import string

def timing_attack():
    guessed_password = ""
    possible_characters = string.ascii_lowercase + string.digits
    
    while len(guessed_password) < len(SECRET):
        best_time = 0
        best_char = ''
        
        for char in possible_characters:
            guess = guessed_password + char
            start_time = time.time()
            check_password(guess)
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