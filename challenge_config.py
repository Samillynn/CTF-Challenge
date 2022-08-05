long_responses = ['Bro be cautious! This is too small!',
                  'This number is just right! Congratulations!',
                  'Bro be cautious! This is too large!']

short_responses = ['larger', 'correct', 'smaller']

before_input_reminder = 'Give me your guess number in the format of {"guess": "fcs22{YOUR GUESS}"}, ' \
                        'e.g. {"guess": "fcs22{100}"}\n'

transpose_key = '521304'
substitute_key = 'fcpevqkzgmtrayonujdlwhbxsi'
hints = {
    "b64": "It is starting with '='",
    "md5": "It is a one-word response. Try brute force.",
    "ascii": "Pay attention to the range of numbers.",
    "substitute": f"The secret key of this cipher is {substitute_key}",
    "transpose": f"The secret key of this cipher is {transpose_key}",
    "random_xor": "What can you do if you are provided with 2 binary sequences?",
}
