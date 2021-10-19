# Septem Attack
Work on attacking the Septem cryptocurrency puzzle as described on [this Reddit thread](https://www.reddit.com/r/bitcoinpuzzles/comments/n61a0a/the_bizarre_septem_puzzle/).


## Puzzle Overview
Septem is a cryptocurrency puzzle described in /r/bitcoinpuzzles, but allegedly originally published on 4Chan. The [PNG image](./wh8hlbzrsfx61.png) uses steganography to hide the puzzle description and the ciphertext. In broad strokes, it is a 7-layer deep nesting doll of encryption (each layer is XOR then Vigenere), each layer with a different key.

## Approach
Each nested layer has (English?) plaintext preceeding binary ciphertext. This plaintext is likely how one can reduce the search space for the XOR key + Vigenere key.

In general, the approach will be to find likely candidates for keys (look for patterns to guess the key period), limit our search space to BIP-39 wordlist matches, then try to parallelize the remaining search.


## Run the Code

### Step 1
Decode the image steganography:
```
stegify decode --carrier ./wh8hlbzrsfx61.png --result ./stegify-result.png
```

### Step 2
Separate the description/hint from the ciphertext:
```
cat ./stegify-result.png | tail -c 7519 | head -c 6685
```
(these numbers were derived from guess-and-check to find the boundaries of the English text / ciphertext)

### Step 3
Run the Python analysis script with `chapter1` as `STDIN`:
```
cat ./chapters/1/ciphertext.data | python3 python/main.py --hint="****face****"
```
Note: `--hint="****face***"` tells the script that the XOR decryption key is 12 characters long with 4 unknown characters, 4 known characters (`face`) and 4 unknown characters. This is useful for restricting the search space.


## Data Files

### Chapter 1
[chapter 1 ciphertext](./chapters/1/ciphertext.data). This was obtained from "Step 2" of "Run the Code".

### Initial Steganography results
[stegify-result.png](./stegify-result.png). This was obtained from "Step 1" of "Run the Code".

### BIP-39 words
[English BIP-39 words](./english.txt) gathered from [Bitcoin BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt)

### wh8hlbzrsfx61.png
![Septem Image](./wh8hlbzrsfx61.png)

### ihKnTsY.png
![Septem Image](./ihKnTsY.png)


## Tools and Reference

### Steganography
- [Stegify](https://github.com/DimitarPetrov/stegify)

### Decryption
- XOR Brute Force
- Vigenere Decryption

### Statistical Analysis
- [Incidence of Coincidence](http://practicalcryptography.com/cryptanalysis/text-characterisation/index-coincidence/)
- [Vigenere Cryptanalysis](http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/)

