import java.math.BigInteger;
import java.util.*;
import java.util.function.Supplier;
import java.util.stream.Stream;

public class Solution {
    
    // 1. 再帰版（メモ化付き）
    static class FibonacciRecursive {
        private Map<Integer, BigInteger> memo = new HashMap<>();
        
        public BigInteger calculate(int n) {
            if (n <= 1) return BigInteger.valueOf(n);
            
            return memo.computeIfAbsent(n, k -> 
                calculate(k - 1).add(calculate(k - 2))
            );
        }
    }
    
    // 2. イテレータ版
    static class FibonacciIterator implements Iterable<BigInteger> {
        private final int limit;
        
        public FibonacciIterator(int limit) {
            this.limit = limit;
        }
        
        @Override
        public Iterator<BigInteger> iterator() {
            return new Iterator<BigInteger>() {
                private BigInteger a = BigInteger.ZERO;
                private BigInteger b = BigInteger.ONE;
                private int count = 0;
                
                @Override
                public boolean hasNext() {
                    return count < limit;
                }
                
                @Override
                public BigInteger next() {
                    if (!hasNext()) {
                        throw new NoSuchElementException();
                    }
                    
                    BigInteger current = a;
                    BigInteger temp = a;
                    a = b;
                    b = temp.add(b);
                    count++;
                    
                    return current;
                }
            };
        }
        
        public List<BigInteger> toList() {
            List<BigInteger> result = new ArrayList<>();
            for (BigInteger fib : this) {
                result.add(fib);
            }
            return result;
        }
    }
    
    // 3. 行列累乗版（高速計算）
    static class FibonacciMatrix {
        public BigInteger calculate(int n) {
            if (n <= 1) return BigInteger.valueOf(n);
            
            BigInteger[][] matrix = {{BigInteger.ONE, BigInteger.ONE}, 
                                   {BigInteger.ONE, BigInteger.ZERO}};
            BigInteger[][] result = matrixPower(matrix, n);
            return result[0][1];
        }
        
        private BigInteger[][] matrixMultiply(BigInteger[][] a, BigInteger[][] b) {
            return new BigInteger[][] {
                {a[0][0].multiply(b[0][0]).add(a[0][1].multiply(b[1][0])), 
                 a[0][0].multiply(b[0][1]).add(a[0][1].multiply(b[1][1]))},
                {a[1][0].multiply(b[0][0]).add(a[1][1].multiply(b[1][0])), 
                 a[1][0].multiply(b[0][1]).add(a[1][1].multiply(b[1][1]))}
            };
        }
        
        private BigInteger[][] matrixPower(BigInteger[][] matrix, int n) {
            if (n == 0) {
                return new BigInteger[][] {{BigInteger.ONE, BigInteger.ZERO}, 
                                         {BigInteger.ZERO, BigInteger.ONE}};
            }
            if (n == 1) return matrix;
            
            if (n % 2 == 0) {
                BigInteger[][] half = matrixPower(matrix, n / 2);
                return matrixMultiply(half, half);
            } else {
                return matrixMultiply(matrix, matrixPower(matrix, n - 1));
            }
        }
    }
    
    // 4. ジェネレータ版（Stream使用）
    static class FibonacciGenerator {
        public static Stream<BigInteger> generate() {
            return Stream.generate(new Supplier<BigInteger>() {
                private BigInteger a = BigInteger.ZERO;
                private BigInteger b = BigInteger.ONE;
                private boolean first = true;
                
                @Override
                public BigInteger get() {
                    if (first) {
                        first = false;
                        return a;
                    }
                    
                    BigInteger current = b;
                    BigInteger temp = a;
                    a = b;
                    b = temp.add(b);
                    return current;
                }
            });
        }
    }
    
    // 5. 黄金比を使った近似計算
    static class FibonacciGoldenRatio {
        private static final double PHI = (1 + Math.sqrt(5)) / 2;
        
        public long calculate(int n) {
            return Math.round((Math.pow(PHI, n) - Math.pow(-PHI, -n)) / Math.sqrt(5));
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=== フィボナッチ数列の様々な実装 ===");
        System.out.println();
        
        // 1. 再帰版のデモ
        System.out.println("1. 再帰版（メモ化付き）");
        FibonacciRecursive fibRecursive = new FibonacciRecursive();
        System.out.print("最初の10項: ");
        for (int i = 0; i < 10; i++) {
            System.out.print(fibRecursive.calculate(i) + " ");
        }
        System.out.println("\n");
        
        // 2. イテレータ版のデモ
        System.out.println("2. イテレータ版");
        System.out.print("最初の10項: ");
        for (BigInteger fib : new FibonacciIterator(10)) {
            System.out.print(fib + " ");
        }
        System.out.println("\n");
        
        // 3. 行列累乗版のデモ
        System.out.println("3. 行列累乗版（大きな数も高速）");
        FibonacciMatrix fibMatrix = new FibonacciMatrix();
        System.out.println("n=50の値: " + fibMatrix.calculate(50));
        System.out.println();
        
        // 4. ジェネレータ版のデモ
        System.out.println("4. ジェネレータ版（遅延評価）");
        System.out.print("100未満の項: ");
        FibonacciGenerator.generate()
            .takeWhile(n -> n.compareTo(BigInteger.valueOf(100)) < 0)
            .forEach(n -> System.out.print(n + " "));
        System.out.println("\n");
        
        // 5. 黄金比版のデモ
        System.out.println("5. 黄金比を使った近似計算");
        FibonacciGoldenRatio fibGolden = new FibonacciGoldenRatio();
        System.out.print("最初の10項: ");
        for (int i = 0; i < 10; i++) {
            System.out.print(fibGolden.calculate(i) + " ");
        }
        System.out.println("\n");
        
        // おまけ：フィボナッチ数列の性質を調べる
        System.out.println("=== フィボナッチ数列の面白い性質 ===");
        
        // 隣接項の比が黄金比に収束
        System.out.println("隣接項の比（黄金比" + 
            String.format("%.6f", FibonacciGoldenRatio.PHI) + "に収束）:");
        List<BigInteger> fibList = new FibonacciIterator(15).toList();
        for (int i = 5; i <= 10; i++) {
            double ratio = fibList.get(i).doubleValue() / fibList.get(i-1).doubleValue();
            System.out.println(String.format("F(%d)/F(%d) = %.6f", i, i-1, ratio));
        }
        
        // 最初のn項の和
        System.out.println("\n最初のn項の和の性質（F(n+2) - 1に等しい）:");
        for (int n = 5; n <= 8; n++) {
            BigInteger sum = fibList.subList(0, n).stream()
                .reduce(BigInteger.ZERO, BigInteger::add);
            System.out.println(String.format("最初の%d項の和: %s = F(%d) - 1 = %s - 1", 
                n, sum, n+2, fibList.get(n+1)));
        }
    }
}