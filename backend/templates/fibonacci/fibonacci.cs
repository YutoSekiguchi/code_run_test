using System;
using System.Collections.Generic;
using System.Linq;

// 1. 再帰版（メモ化付き）
public class FibonacciRecursive 
{
    private Dictionary<int, long> memo = new Dictionary<int, long>();
    
    public long Calculate(int n) 
    {
        if (n <= 1) return n;
        if (memo.ContainsKey(n)) return memo[n];
        memo[n] = Calculate(n - 1) + Calculate(n - 2);
        return memo[n];
    }
}

// 2. イテレータ版
public class FibonacciIterator 
{
    private int limit;
    
    public FibonacciIterator(int limit) 
    {
        this.limit = limit;
    }
    
    public IEnumerable<long> Generate() 
    {
        long a = 0, b = 1;
        int count = 0;
        
        while (count < limit) 
        {
            yield return a;
            long temp = a;
            a = b;
            b = temp + b;
            count++;
        }
    }
    
    public List<long> ToList() 
    {
        return Generate().ToList();
    }
}

// 3. 行列累乗版
public class Matrix 
{
    public long[,] M { get; set; }
    
    public Matrix(long a, long b, long c, long d) 
    {
        M = new long[2, 2] { { a, b }, { c, d } };
    }
    
    public static Matrix operator *(Matrix a, Matrix b) 
    {
        return new Matrix(
            a.M[0, 0] * b.M[0, 0] + a.M[0, 1] * b.M[1, 0],
            a.M[0, 0] * b.M[0, 1] + a.M[0, 1] * b.M[1, 1],
            a.M[1, 0] * b.M[0, 0] + a.M[1, 1] * b.M[1, 0],
            a.M[1, 0] * b.M[0, 1] + a.M[1, 1] * b.M[1, 1]
        );
    }
}

public class FibonacciMatrix 
{
    public long Calculate(int n) 
    {
        if (n <= 1) return n;
        var baseMatrix = new Matrix(1, 1, 1, 0);
        var result = MatrixPower(baseMatrix, n);
        return result.M[0, 1];
    }
    
    private Matrix MatrixPower(Matrix baseMatrix, int n) 
    {
        if (n == 0) return new Matrix(1, 0, 0, 1); // 単位行列
        if (n == 1) return baseMatrix;
        
        if (n % 2 == 0) 
        {
            var half = MatrixPower(baseMatrix, n / 2);
            return half * half;
        } 
        else 
        {
            return baseMatrix * MatrixPower(baseMatrix, n - 1);
        }
    }
}

// 4. 黄金比を使った近似計算
public class FibonacciGoldenRatio 
{
    public static readonly double PHI = (1.0 + Math.Sqrt(5.0)) / 2.0;
    
    public long Calculate(int n) 
    {
        return (long)Math.Round((Math.Pow(PHI, n) - Math.Pow(-PHI, -n)) / Math.Sqrt(5.0));
    }
}

// 5. LINQ版
public static class FibonacciLinq 
{
    public static IEnumerable<long> Generate(int count) 
    {
        return Enumerable.Range(0, count)
            .Aggregate(
                new List<long>(),
                (acc, i) => 
                {
                    if (i <= 1) acc.Add(i);
                    else acc.Add(acc[i - 1] + acc[i - 2]);
                    return acc;
                }
            );
    }
}

public class Program 
{
    public static void Main() 
    {
        Console.WriteLine("=== フィボナッチ数列の様々な実装 ===\n");
        
        // 1. 再帰版のデモ
        Console.WriteLine("1. 再帰版（メモ化付き）");
        var fibRecursive = new FibonacciRecursive();
        Console.Write("最初の10項: ");
        for (int i = 0; i < 10; i++) 
        {
            Console.Write($"{fibRecursive.Calculate(i)} ");
        }
        Console.WriteLine("\n");
        
        // 2. イテレータ版のデモ
        Console.WriteLine("2. イテレータ版");
        var fibIter = new FibonacciIterator(10);
        Console.Write("最初の10項: ");
        foreach (var value in fibIter.Generate()) 
        {
            Console.Write($"{value} ");
        }
        Console.WriteLine("\n");
        
        // 3. 行列累乗版のデモ
        Console.WriteLine("3. 行列累乗版（大きな数も高速）");
        var fibMatrix = new FibonacciMatrix();
        Console.WriteLine($"n=50の値: {fibMatrix.Calculate(50)}\n");
        
        // 4. 黄金比版のデモ
        Console.WriteLine("4. 黄金比を使った近似計算");
        var fibGolden = new FibonacciGoldenRatio();
        Console.Write("最初の10項: ");
        for (int i = 0; i < 10; i++) 
        {
            Console.Write($"{fibGolden.Calculate(i)} ");
        }
        Console.WriteLine("\n");
        
        // 5. LINQ版のデモ
        Console.WriteLine("5. LINQ版");
        var fibLinq = FibonacciLinq.Generate(15).ToList();
        Console.Write("最初の15項: ");
        Console.WriteLine(string.Join(" ", fibLinq));
        Console.WriteLine();
        
        // おまけ：フィボナッチ数列の性質を調べる
        Console.WriteLine("=== フィボナッチ数列の面白い性質 ===");
        
        // 隣接項の比が黄金比に収束
        Console.WriteLine($"隣接項の比（黄金比{FibonacciGoldenRatio.PHI:F6}に収束）:");
        var sequence = new FibonacciIterator(15).ToList();
        for (int i = 5; i <= 10; i++) 
        {
            double ratio = (double)sequence[i] / sequence[i - 1];
            Console.WriteLine($"F({i})/F({i - 1}) = {ratio:F6}");
        }
        
        // 最初のn項の和
        Console.WriteLine("\n最初のn項の和の性質（F(n+2) - 1に等しい）:");
        for (int n = 5; n <= 8; n++) 
        {
            long sum = sequence.Take(n).Sum();
            Console.WriteLine($"最初の{n}項の和: {sum} = F({n + 2}) - 1 = {sequence[n + 1]} - 1");
        }
        
        // C#の特殊機能を使った実装
        Console.WriteLine("\n=== C#の特殊機能を使った実装 ===");
        
        // Funcデリゲート版
        Func<int, long> fibFunc = null;
        var memo = new Dictionary<int, long>();
        fibFunc = n => n <= 1 ? n : 
            memo.ContainsKey(n) ? memo[n] : 
            memo[n] = fibFunc(n - 1) + fibFunc(n - 2);
        
        Console.WriteLine($"Funcデリゲート版 F(10): {fibFunc(10)}");
        
        // ローカル関数版
        long FibLocal(int n) 
        {
            static Dictionary<int, long> localMemo = new Dictionary<int, long>();
            if (n <= 1) return n;
            if (localMemo.ContainsKey(n)) return localMemo[n];
            return localMemo[n] = FibLocal(n - 1) + FibLocal(n - 2);
        }
        
        Console.WriteLine($"ローカル関数版 F(10): {FibLocal(10)}");
    }
}