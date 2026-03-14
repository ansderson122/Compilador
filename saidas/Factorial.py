def factorial(n):
    if (n <= 1):
        return 1

    return (n * factorial((n - 1)))

result = factorial(10)
print("Fatorial de 10:")
print(result)
