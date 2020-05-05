import sys

if len(sys.argv) != 2:
    print("Usage: python3 compute_error_rate.py decoded_file")
    sys.exit(1)

decoded_file = sys.argv[1]

with open(decoded_file) as f:
    decoded_codewords = [l.rstrip('\n') for l in f.readlines()]

print('Number of codewords:', len(decoded_codewords))
bit_errors_total = 0
block_errors_total = 0
total_length = 0
for codeword in decoded_codewords:
    bit_errors = codeword.count('1')
    if bit_errors != 0:
        block_errors_total += 1
    bit_errors_total += bit_errors
    total_length += len(codeword)

print('Bit error rate:','%.2f%%'%((bit_errors_total/total_length)*100))
print('Block error rate:','%.2f%%'%((block_errors_total/len(decoded_codewords))*100))
