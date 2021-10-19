import re

# Calculate the Index of Coincidence of a string.
# This function strips non-alpha chars (so they are not factored in the result).
# Reference: http://practicalcryptography.com/cryptanalysis/text-characterisation/index-coincidence/
def index_of_coincidence(plaintext):
    plaintext = re.sub(r'[^a-z]', '', plaintext.lower())
    counts = list()
    totcount = 0
    for i in range(0, 26):
        counts.insert(i, 0)
    for this_char in plaintext:
        counts[ord(this_char) - 97] += 1
        totcount += 1
    sum = 0
    for i in range(0, 26):
        sum += counts[i] * (counts[i] - 1)
    ic = sum / (totcount * (totcount - 1))
    return ic


# Calculate the Chi^2 metric of this plaintext against expected distribution of English characters.
# This function strips non-alpha chars (so they are not factored in the result).
# Reference: http://practicalcryptography.com/cryptanalysis/text-characterisation/chi-squared-statistic/
def chi_squared_english(plaintext):
    plaintext = re.sub(r'[^a-z]', '', plaintext.lower())
    expected = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,
        0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978,
        0.02360, 0.00150, 0.01974, 0.00074
    ]
    total_count = 0
    counts = []
    i = 0
    while (i < 26):
        counts.insert(i, 0)
        i += 1
    i = 0
    while (i < len(plaintext)):
        counts[ord(plaintext[i]) - 97] += 1
        total_count += 1
        i += 1
    sum1 = 0.0
    i = 0
    while (i < 26):
        sum1 = sum1 + ((counts[i] - total_count * expected[i]) ** 2) / (total_count * expected[i])
        i += 1
    return sum1
