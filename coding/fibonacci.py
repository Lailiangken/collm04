# filename: fibonacci.py
def fibonacci(n):
    if n <= 0:
        return "Invalid input. Please provide a positive integer."
    elif n == 1:
        return [0]
    else:
        fibonacci_series = [0, 1]
        for i in range(2, n):
            next_num = fibonacci_series[-1] + fibonacci_series[-2]
            fibonacci_series.append(next_num)
        return fibonacci_series

n = 10  # Change n to the desired number of Fibonacci numbers
result = fibonacci(n)
print(result)