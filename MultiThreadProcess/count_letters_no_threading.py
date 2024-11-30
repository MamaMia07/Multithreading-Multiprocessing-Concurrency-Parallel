import json
import urllib.request
import time


def count_letters(url, frequency):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count


def without_threading():
    frequency = {}
    for c in "abcdefghijklmnoprqstuwxyz":
        frequency[c] = 0
    start = time.time()
    for i in range(1000, 1050):
        count_letters(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)
    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("Done, time taken: ", end - start)

def main():
    without_threading()


main()