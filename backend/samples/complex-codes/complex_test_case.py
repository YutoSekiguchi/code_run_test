#!/usr/bin/env python3

import math
from itertools import islice, takewhile
from functools import lru_cache

# 1. 再帰版（メモ化付き）
class FibonacciRecursive:
    def __init__(self):
        self.memo = {}
    
    def calculate(self, n):
        if n <= 1:
            return n
        if n not in self.memo:
            self.memo[n] = self.calculate(n - 1) + self.calculate(n - 2)
        return self.memo[n]

# 1.5. Python標準のデコレータを使った版
@lru_cache(maxsize=None)
def fibonacci_lru_cache(n):
    if n <= 1:
        return n
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)

# 2. イテレータ版
class FibonacciIterator:
    def __init__(self, limit=float('inf')):
        self.limit = limit
    
    def __iter__(self):
        a, b = 0, 1
        count = 0
        while count < self.limit:
            yield a
            a, b = b, a + b
            count += 1
    
    def to_list(self):
        return list(self)

# 3. 行列累乗版（高速計算）
class FibonacciMatrix:
    def calculate(self, n):
        if n <= 1:
            return n
        
        matrix = [[1, 1], [1, 0]]
        result = self._matrix_power(matrix, n)
        return result[0][1]
    
    def _matrix_multiply(self, a, b):
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ]
    
    def _matrix_power(self, matrix, n):
        if n == 0:
            return [[1, 0], [0, 1]]
        if n == 1:
            return matrix
        
        if n % 2 == 0:
            half = self._matrix_power(matrix, n // 2)
            return self._matrix_multiply(half, half)
        else:
            return self._matrix_multiply(matrix, self._matrix_power(matrix, n - 1))

# 4. ジェネレータ版
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 5. 黄金比を使った近似計算
class FibonacciGoldenRatio:
    PHI = (1 + math.sqrt(5)) / 2
    
    def calculate(self, n):
        return round((self.PHI ** n - (-self.PHI) ** (-n)) / math.sqrt(5))

# デモンストレーション
print("=== フィボナッチ数列の様々な実装 ===")
print()

# 1. 再帰版のデモ
print("1. 再帰版（メモ化付き）")
fib_recursive = FibonacciRecursive()
print("最初の10項: ", end="")
for i in range(10):
    print(fib_recursive.calculate(i), end=" ")
print("\n")

# 1.5. lru_cacheデコレータ版
print("1.5. Python標準のlru_cacheデコレータ版")
print("最初の10項: ", end="")
for i in range(10):
    print(fibonacci_lru_cache(i), end=" ")
print("\n")

# 2. イテレータ版のデモ
print("2. イテレータ版")
print("最初の10項: ", end="")
for n in FibonacciIterator(10):
    print(n, end=" ")
print("\n")

# 3. 行列累乗版のデモ
print("3. 行列累乗版（大きな数も高速）")
fib_matrix = FibonacciMatrix()
print(f"n=50の値: {fib_matrix.calculate(50)}")
print()

# 4. ジェネレータ版のデモ
print("4. ジェネレータ版（遅延評価）")
print("100未満の項: ", end="")
for n in takewhile(lambda x: x < 100, fibonacci_generator()):
    print(n, end=" ")
print("\n")

# 5. 黄金比版のデモ
print("5. 黄金比を使った近似計算")
fib_golden = FibonacciGoldenRatio()
print("最初の10項: ", end="")
for i in range(10):
    print(fib_golden.calculate(i), end=" ")
print("\n")

# おまけ：フィボナッチ数列の性質を調べる
print("\n=== フィボナッチ数列の面白い性質 ===")

# 隣接項の比が黄金比に収束
print(f"隣接項の比（黄金比{FibonacciGoldenRatio.PHI}に収束）:")
fib = FibonacciIterator(15).to_list()
for i in range(5, 11):
    ratio = fib[i] / fib[i-1]
    print(f"F({i})/F({i-1}) = {ratio:.6f}")

# 最初のn項の和
print("\n最初のn項の和の性質（F(n+2) - 1に等しい）:")
for n in range(5, 9):
    sum_n = sum(fib[:n])
    print(f"最初の{n}項の和: {sum_n} = F({n+2}) - 1 = {fib[n+1]} - 1")

# Pythonらしい追加実装
print("\n=== Pythonらしい追加実装 ===")

# リスト内包表記版
def fibonacci_list_comp(n):
    """最初のn項をリスト内包表記で生成（効率は悪い）"""
    fib = lambda n: n if n <= 1 else fib(n-1) + fib(n-2)
    return [fib(i) for i in range(n)]

print("リスト内包表記版（最初の10項）:", fibonacci_list_comp(10))

# ワンライナー版（トリッキー）
fib_oneliner = lambda n: (lambda f, n: f(f, n))(lambda f, n: n if n <= 1 else f(f, n-1) + f(f, n-2), n)
print("ワンライナー版 F(10):", fib_oneliner(10))