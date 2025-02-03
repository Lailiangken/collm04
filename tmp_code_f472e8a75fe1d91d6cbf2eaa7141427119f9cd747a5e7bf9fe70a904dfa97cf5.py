def fibonacci(n):
    result = []
    a, b = 0, 1
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result

fibonacci_15 = fibonacci(15)
for num in fibonacci_15:
    print(num)
