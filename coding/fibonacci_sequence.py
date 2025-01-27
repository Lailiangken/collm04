# filename: fibonacci_sequence.py

def fibonacci_sequence(length):
    sequence = [0, 1]
    while len(sequence) < length:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

length = 10  # フィボナッチ数列の長さを指定
result = fibonacci_sequence(length)
print(result)