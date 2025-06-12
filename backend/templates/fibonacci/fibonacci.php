<?php

// 1. 再帰版（メモ化付き）
class FibonacciRecursive {
    private $memo = [];
    
    public function calculate($n) {
        if ($n <= 1) return $n;
        if (isset($this->memo[$n])) {
            return $this->memo[$n];
        }
        $this->memo[$n] = $this->calculate($n - 1) + $this->calculate($n - 2);
        return $this->memo[$n];
    }
}

// 2. イテレータ版
class FibonacciIterator implements Iterator {
    private $limit;
    private $position = 0;
    private $a = 0;
    private $b = 1;
    private $current = 0;
    
    public function __construct($limit = PHP_INT_MAX) {
        $this->limit = $limit;
    }
    
    public function rewind(): void {
        $this->position = 0;
        $this->a = 0;
        $this->b = 1;
        $this->current = 0;
    }
    
    public function current() {
        return $this->current;
    }
    
    public function key() {
        return $this->position;
    }
    
    public function next(): void {
        if ($this->position == 0) {
            $this->current = $this->a;
        } else {
            $temp = $this->a;
            $this->a = $this->b;
            $this->b = $temp + $this->b;
            $this->current = $temp;
        }
        $this->position++;
    }
    
    public function valid(): bool {
        return $this->position < $this->limit;
    }
    
    public function toArray() {
        $result = [];
        foreach ($this as $value) {
            $result[] = $value;
        }
        return $result;
    }
}

// 3. 行列累乗版
class FibonacciMatrix {
    public function calculate($n) {
        if ($n <= 1) return $n;
        $matrix = [[1, 1], [1, 0]];
        $result = $this->matrixPower($matrix, $n);
        return $result[0][1];
    }
    
    private function matrixMultiply($a, $b) {
        return [
            [$a[0][0] * $b[0][0] + $a[0][1] * $b[1][0], $a[0][0] * $b[0][1] + $a[0][1] * $b[1][1]],
            [$a[1][0] * $b[0][0] + $a[1][1] * $b[1][0], $a[1][0] * $b[0][1] + $a[1][1] * $b[1][1]]
        ];
    }
    
    private function matrixPower($matrix, $n) {
        if ($n == 0) return [[1, 0], [0, 1]];
        if ($n == 1) return $matrix;
        
        if ($n % 2 == 0) {
            $half = $this->matrixPower($matrix, intval($n / 2));
            return $this->matrixMultiply($half, $half);
        } else {
            return $this->matrixMultiply($matrix, $this->matrixPower($matrix, $n - 1));
        }
    }
}

// 4. ジェネレータ版
function fibonacciGenerator() {
    $a = 0;
    $b = 1;
    while (true) {
        yield $a;
        $temp = $a;
        $a = $b;
        $b = $temp + $b;
    }
}

// 5. 黄金比を使った近似計算
class FibonacciGoldenRatio {
    const PHI = 1.6180339887498948;
    
    public function calculate($n) {
        return round((pow(self::PHI, $n) - pow(-self::PHI, -$n)) / sqrt(5));
    }
}

// 6. 配列を使った版
function fibonacciArray($n) {
    if ($n <= 0) return [];
    if ($n == 1) return [0];
    
    $fib = [0, 1];
    for ($i = 2; $i < $n; $i++) {
        $fib[$i] = $fib[$i-1] + $fib[$i-2];
    }
    return $fib;
}

// デモンストレーション
echo "=== フィボナッチ数列の様々な実装 ===\n\n";

// 1. 再帰版のデモ
echo "1. 再帰版（メモ化付き）\n";
$fibRecursive = new FibonacciRecursive();
echo "最初の10項: ";
for ($i = 0; $i < 10; $i++) {
    echo $fibRecursive->calculate($i) . " ";
}
echo "\n\n";

// 2. イテレータ版のデモ
echo "2. イテレータ版\n";
echo "最初の10項: ";
$fibIter = new FibonacciIterator(10);
foreach ($fibIter as $value) {
    echo $value . " ";
}
echo "\n\n";

// 3. 行列累乗版のデモ
echo "3. 行列累乗版（大きな数も高速）\n";
$fibMatrix = new FibonacciMatrix();
echo "n=50の値: " . $fibMatrix->calculate(50) . "\n\n";

// 4. ジェネレータ版のデモ
echo "4. ジェネレータ版（遅延評価）\n";
echo "100未満の項: ";
foreach (fibonacciGenerator() as $value) {
    if ($value >= 100) break;
    echo $value . " ";
}
echo "\n\n";

// 5. 黄金比版のデモ
echo "5. 黄金比を使った近似計算\n";
$fibGolden = new FibonacciGoldenRatio();
echo "最初の10項: ";
for ($i = 0; $i < 10; $i++) {
    echo $fibGolden->calculate($i) . " ";
}
echo "\n\n";

// 6. 配列版のデモ
echo "6. 配列版\n";
$fibArray = fibonacciArray(15);
echo "最初の15項: " . implode(" ", $fibArray) . "\n\n";

// おまけ：フィボナッチ数列の性質を調べる
echo "=== フィボナッチ数列の面白い性質 ===\n";

// 隣接項の比が黄金比に収束
echo "隣接項の比（黄金比" . number_format(FibonacciGoldenRatio::PHI, 6) . "に収束）:\n";
for ($i = 5; $i <= 10; $i++) {
    $ratio = $fibArray[$i] / $fibArray[$i-1];
    echo "F($i)/F(" . ($i-1) . ") = " . number_format($ratio, 6) . "\n";
}

// 最初のn項の和
echo "\n最初のn項の和の性質（F(n+2) - 1に等しい）:\n";
for ($n = 5; $n <= 8; $n++) {
    $sum = array_sum(array_slice($fibArray, 0, $n));
    echo "最初の{$n}項の和: $sum = F(" . ($n+2) . ") - 1 = " . $fibArray[$n+1] . " - 1\n";
}

// PHPの特殊機能を使った実装
echo "\n=== PHPの特殊機能を使った実装 ===\n";

// クロージャ版
$fibonacciClosure = function($n) use (&$fibonacciClosure) {
    static $memo = [];
    if ($n <= 1) return $n;
    if (isset($memo[$n])) return $memo[$n];
    return $memo[$n] = $fibonacciClosure($n-1) + $fibonacciClosure($n-2);
};

echo "クロージャ版 F(10): " . $fibonacciClosure(10) . "\n";

// 匿名関数とarray_mapを使った版
$numbers = range(0, 9);
$fibValues = array_map($fibonacciClosure, $numbers);
echo "匿名関数版（最初の10項）: " . implode(" ", $fibValues) . "\n";

?>