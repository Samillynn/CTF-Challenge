import base64


def b64(response):
    return str(base64.b64decode(response[::-1].encode('utf-8')))


def transpose(response, key="421350"):
    def split_chunks(t, length):
        return [t[i:i + length] for i in range(0, len(t), length)]

    def transpose_chunk(chunk, k):
        assert len(chunk) == len(k)
        return "".join(chunk[int(transposed_index)] for transposed_index in k)

    chunks = split_chunks(response, len(key))
    return "".join(transpose_chunk(c, key) for c in chunks)


def random_xor(s1, s2):
    return "".join(chr(int(x, 2) ^ int(y, 2)) for (x, y) in zip(s1.split(), s2.split()))


if __name__ == '__main__':
    print(b64("=ECbsFWbzBybvRHIzlGIzlGaUBSIzV3bpRXdhNGIlJGIvJnQ"))
    print(transpose("eor Bbiacu tTsu!o ssi hisoto  *lalm!"))
    print(random_xor("1101001 1101110 1001100 0110011 0100110 0110010", "0000101 0001111 0111110 1010100 1000011 1000000"))
