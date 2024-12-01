import json
import urllib.request
import time
from threading import Thread

finished_count=0

def count_letters(url, frequency):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count += 1


def with_threading():
    frequency = {}
    for c in "abcdefghijklmnoprqstuwxyz":
        frequency[c] = 0
    start = time.time()
    for i in range(1000, 1050):
        Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)).start()
    while finished_count <50: #Po wyjściu z tej pętli i uruchomieniu wszystkich 50 wątków musimy śledzić ten warunek, jeśli jest on mniejszy niż 50.
        time.sleep(0.5) #jesli nie jest, musimy poczekać, aż wątki się zakończą ( sprawdza co 0,5sek, czy wątki zostały zakończone, czy nie.)
    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("Done, time taken: ", end - start)
    print(finished_count)


def main():
    with_threading()


main()