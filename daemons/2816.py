import base64
import hashlib
import logging
import random
import re
import string
import sys
from dataclasses import dataclass
from typing import Callable, Any

import challenge_config

logging.basicConfig(level=logging.INFO)


@dataclass
class GameResponse:
    too_small_guess: str
    correct_guess: str
    too_large_guess: str


def long_responses():
    return GameResponse(*challenge_config.long_responses)


def short_responses():
    return GameResponse(*challenge_config.short_responses)


@dataclass
class Judger:
    judge: Callable
    response: GameResponse
    hint: Any

    def check_guess(self, guess, answer):
        if guess < answer:
            hint = self.response.too_small_guess
        elif guess == answer:
            hint = self.response.correct_guess
        else:
            hint = self.response.too_large_guess

        logging.info(hint)
        return self.judge(hint)


def b64(message):
    # reversed base64 string
    return str(base64.b64encode(message.encode('utf-8')), 'utf-8')[::-1]


def b64_judger():
    return Judger(b64, long_responses(), challenge_config.hints["b64"])


def md5(message):
    md5_obj = hashlib.md5()
    md5_obj.update(message.encode("utf-8"))
    return md5_obj.hexdigest()


def md5_judger():
    return Judger(md5, short_responses(), challenge_config.hints["md5"])


def ascii_(message):
    return " ".join(map(str, bytearray(message.encode('utf-8'))))


def ascii_judger():
    return Judger(ascii_, long_responses(), challenge_config.hints["ascii"])


def substitute(text, key=challenge_config.substitute_key):
    mapping = dict(zip(string.ascii_letters, key))
    return "".join(mapping[c] if c in mapping else c for c in text.lower())


def substitute_judger():
    return Judger(substitute, long_responses(), challenge_config.hints["substitute"])


def transpose(text, key=challenge_config.transpose_key):
    def fill_multiple(t, length, char):
        return t + char * (length - len(t) % length)

    def split_chunks(t, length):
        return [t[i:i + length] for i in range(0, len(t), length)]

    def transpose_chunk(chunk, k):
        assert len(chunk) == len(k)
        return "".join(chunk[int(transposed_index)] for transposed_index in k)

    text = fill_multiple(text, len(key), '*')
    chunks = split_chunks(text, len(key))
    return "".join(transpose_chunk(c, key) for c in chunks)


def transpose_judger():
    return Judger(transpose, long_responses(), challenge_config.hints["transpose"])


def random_xor(message, format_ascii, format_sequences):
    def ints_to_binary_str(ints):
        return " ".join(format_ascii(x) for x in ints)

    asciis = [ord(c) for c in message]
    random_stream = [random.randrange(2 ** 7) for _ in message]
    xor_result = [x ^ y for x, y in zip(asciis, random_stream)]
    return format_sequences(ints_to_binary_str(random_stream), ints_to_binary_str(xor_result))


def random_xor_judger():
    def format_ascii(x):
        return format(x, '07b')

    def format_sequences(a, b):
        return {"binary sequence one": a, "binary sequence two": b}

    def customized_random_xor(m):
        return random_xor(m, format_ascii, format_sequences)

    return Judger(customized_random_xor, short_responses(), challenge_config.hints["random_xor"])


def random_judger():
    judgers = [b64_judger(), md5_judger(), ascii_judger(), substitute_judger(), transpose_judger(), random_xor_judger()]
    return random.choice(judgers)


class Challenge:
    def __init__(self):
        self.flag = challenge_config.flag
        self.before_input = challenge_config.before_input_reminder

    @staticmethod
    def strip_flag(text):
        return int(re.match(r'fcs22{(\d*)}', text).group(1))

    def challenge(self, message):
        guess = self.strip_flag(message["guess"])
        stripped_flag = self.strip_flag(self.flag)
        logging.info(guess)

        judger = random_judger()
        logging.info(f"using {random_judger} with guess = {guess}")
        return {"response": judger.check_guess(guess, stripped_flag), "hint": judger.hint}


# setup server
import builtins

builtins.Challenge = Challenge

sys.path.insert(0, '/home/samill/Desktop/framework/utils')
import listener

listener.start_server(port=2816)
