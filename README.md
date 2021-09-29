# Septem Attack
Work on attacking the Septem cryptocurrency puzzle as described on [this Reddit thread](https://www.reddit.com/r/bitcoinpuzzles/comments/n61a0a/the_bizarre_septem_puzzle/).


## Puzzle Overview
Septem is a cryptocurrency puzzle described in /r/bitcoinpuzzles, but allegedly originally published on 4Chan. The [PNG image](./wh8hlbzrsfx61.png) uses steganography to hide the puzzle description and the ciphertext. In broad strokes, it is a 7-layer deep nesting doll of encryption (each layer is XOR then Vigenere), each layer with a different key.


## Data Files

### Chapter 1
[chapter 1 ciphertext](./chapter1)

### Initial Steganography results
[stegify-result.png](./stegify-result.png)

### BIP-39 words
[English BIP-39 words](./english.txt) gahtered from [Bitcoin BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt)

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

