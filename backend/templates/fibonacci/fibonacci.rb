#!/usr/bin/env ruby

# 1. 再帰版（メモ化付き）
class FibonacciRecursive
  def initialize
    @memo = {}
  end
  
  def calculate(n)
    return n if n <= 1
    @memo[n] ||= calculate(n - 1) + calculate(n - 2)
  end
end

# 2. イテレータ版
class FibonacciIterator
  include Enumerable
  
  def initialize(limit = Float::INFINITY)
    @limit = limit
  end
  
  def each
    a, b = 0, 1
    count = 0
    
    while count < @limit
      yield a
      a, b = b, a + b
      count += 1
    end
  end
end

# 3. 行列累乗版（高速計算）
class FibonacciMatrix
  def calculate(n)
    return n if n <= 1
    
    matrix = [[1, 1], [1, 0]]
    result = matrix_power(matrix, n)
    result[0][1]
  end
  
  private
  
  def matrix_multiply(a, b)
    [
      [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
      [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
    ]
  end
  
  def matrix_power(matrix, n)
    return [[1, 0], [0, 1]] if n == 0
    return matrix if n == 1
    
    if n.even?
      half = matrix_power(matrix, n / 2)
      matrix_multiply(half, half)
    else
      matrix_multiply(matrix, matrix_power(matrix, n - 1))
    end
  end
end

# 4. ジェネレータ版
def fibonacci_generator
  Enumerator.new do |y|
    a, b = 0, 1
    loop do
      y << a
      a, b = b, a + b
    end
  end
end

# 5. 黄金比を使った近似計算
class FibonacciGoldenRatio
  PHI = (1 + Math.sqrt(5)) / 2
  
  def calculate(n)
    ((PHI ** n - (-PHI) ** (-n)) / Math.sqrt(5)).round
  end
end

# デモンストレーション
puts "=== フィボナッチ数列の様々な実装 ==="
puts

# 1. 再帰版のデモ
puts "1. 再帰版（メモ化付き）"
fib_recursive = FibonacciRecursive.new
print "最初の10項: "
10.times { |i| print "#{fib_recursive.calculate(i)} " }
puts "\n"

# 2. イテレータ版のデモ
puts "2. イテレータ版"
print "最初の10項: "
FibonacciIterator.new(10).each { |n| print "#{n} " }
puts "\n"

# 3. 行列累乗版のデモ
puts "3. 行列累乗版（大きな数も高速）"
fib_matrix = FibonacciMatrix.new
print "n=50の値: #{fib_matrix.calculate(50)}"
puts "\n"

# 4. ジェネレータ版のデモ
puts "4. ジェネレータ版（遅延評価）"
print "100未満の項: "
fibonacci_generator.take_while { |n| n < 100 }.each { |n| print "#{n} " }
puts "\n"

# 5. 黄金比版のデモ
puts "5. 黄金比を使った近似計算"
fib_golden = FibonacciGoldenRatio.new
print "最初の10項: "
10.times { |i| print "#{fib_golden.calculate(i)} " }
puts "\n"

# おまけ：フィボナッチ数列の性質を調べる
puts "\n=== フィボナッチ数列の面白い性質 ==="

# 隣接項の比が黄金比に収束
puts "隣接項の比（黄金比#{FibonacciGoldenRatio::PHI}に収束）:"
fib = FibonacciIterator.new(15).to_a
(5..10).each do |i|
  ratio = fib[i].to_f / fib[i-1]
  puts "F(#{i})/F(#{i-1}) = #{ratio.round(6)}"
end

# 最初のn項の和
puts "\n最初のn項の和の性質（F(n+2) - 1に等しい）:"
(5..8).each do |n|
  sum = fib[0...n].sum
  puts "最初の#{n}項の和: #{sum} = F(#{n+2}) - 1 = #{fib[n+1]} - 1"
end
