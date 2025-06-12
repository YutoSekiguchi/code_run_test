#!/usr/bin/env node

// 1. 再帰版（メモ化付き）
class FibonacciRecursive {
  constructor() {
    this.memo = {};
  }
  
  calculate(n) {
    if (n <= 1) return n;
    if (!(n in this.memo)) {
      this.memo[n] = this.calculate(n - 1) + this.calculate(n - 2);
    }
    return this.memo[n];
  }
}

// 2. イテレータ版
class FibonacciIterator {
  constructor(limit = Infinity) {
    this.limit = limit;
  }
  
  *[Symbol.iterator]() {
    let a = 0, b = 1;
    let count = 0;
    
    while (count < this.limit) {
      yield a;
      [a, b] = [b, a + b];
      count++;
    }
  }
  
  toArray() {
    return [...this];
  }
}

// 3. 行列累乗版（高速計算）
class FibonacciMatrix {
  calculate(n) {
    if (n <= 1) return n;
    
    const matrix = [[1, 1], [1, 0]];
    const result = this.matrixPower(matrix, n);
    return result[0][1];
  }
  
  matrixMultiply(a, b) {
    return [
      [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
      [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
    ];
  }
  
  matrixPower(matrix, n) {
    if (n === 0) return [[1, 0], [0, 1]];
    if (n === 1) return matrix;
    
    if (n % 2 === 0) {
      const half = this.matrixPower(matrix, Math.floor(n / 2));
      return this.matrixMultiply(half, half);
    } else {
      return this.matrixMultiply(matrix, this.matrixPower(matrix, n - 1));
    }
  }
}

// 4. ジェネレータ版
function* fibonacciGenerator() {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// 5. 黄金比を使った近似計算
class FibonacciGoldenRatio {
  constructor() {
    this.PHI = (1 + Math.sqrt(5)) / 2;
  }
  
  calculate(n) {
    return Math.round((Math.pow(this.PHI, n) - Math.pow(-this.PHI, -n)) / Math.sqrt(5));
  }
}

// ヘルパー関数
function takeWhile(generator, predicate) {
  const result = [];
  for (const value of generator) {
    if (!predicate(value)) break;
    result.push(value);
  }
  return result;
}

// デモンストレーション
console.log("=== フィボナッチ数列の様々な実装 ===");
console.log();

// 1. 再帰版のデモ
console.log("1. 再帰版（メモ化付き）");
const fibRecursive = new FibonacciRecursive();
process.stdout.write("最初の10項: ");
for (let i = 0; i < 10; i++) {
  process.stdout.write(fibRecursive.calculate(i) + " ");
}
console.log("\n");

// 2. イテレータ版のデモ
console.log("2. イテレータ版");
process.stdout.write("最初の10項: ");
for (const n of new FibonacciIterator(10)) {
  process.stdout.write(n + " ");
}
console.log("\n");

// 3. 行列累乗版のデモ
console.log("3. 行列累乗版（大きな数も高速）");
const fibMatrix = new FibonacciMatrix();
console.log(`n=50の値: ${fibMatrix.calculate(50)}`);
console.log();

// 4. ジェネレータ版のデモ
console.log("4. ジェネレータ版（遅延評価）");
process.stdout.write("100未満の項: ");
const under100 = takeWhile(fibonacciGenerator(), n => n < 100);
for (const n of under100) {
  process.stdout.write(n + " ");
}
console.log("\n");

// 5. 黄金比版のデモ
console.log("5. 黄金比を使った近似計算");
const fibGolden = new FibonacciGoldenRatio();
process.stdout.write("最初の10項: ");
for (let i = 0; i < 10; i++) {
  process.stdout.write(fibGolden.calculate(i) + " ");
}
console.log("\n");

// おまけ：フィボナッチ数列の性質を調べる
console.log("\n=== フィボナッチ数列の面白い性質 ===");

// 隣接項の比が黄金比に収束
console.log(`隣接項の比（黄金比${fibGolden.PHI}に収束）:`);
const fib = new FibonacciIterator(15).toArray();
for (let i = 5; i <= 10; i++) {
  const ratio = fib[i] / fib[i-1];
  console.log(`F(${i})/F(${i-1}) = ${ratio.toFixed(6)}`);
}

// 最初のn項の和
console.log("\n最初のn項の和の性質（F(n+2) - 1に等しい）:");
for (let n = 5; n <= 8; n++) {
  const sum = fib.slice(0, n).reduce((a, b) => a + b, 0);
  console.log(`最初の${n}項の和: ${sum} = F(${n+2}) - 1 = ${fib[n+1]} - 1`);
}