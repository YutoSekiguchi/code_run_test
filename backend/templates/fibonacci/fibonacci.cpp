#include <iostream>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <iomanip>

// 1. 再帰版（メモ化付き）
class FibonacciRecursive {
private:
    std::unordered_map<int, long long> memo;

public:
    long long calculate(int n) {
        if (n <= 1) return n;
        if (memo.find(n) != memo.end()) {
            return memo[n];
        }
        memo[n] = calculate(n - 1) + calculate(n - 2);
        return memo[n];
    }
};

// 2. イテレータ版
class FibonacciIterator {
private:
    int limit;
    int current;
    long long a, b;

public:
    FibonacciIterator(int limit) : limit(limit), current(0), a(0), b(1) {}
    
    bool hasNext() const {
        return current < limit;
    }
    
    long long next() {
        if (current == 0) {
            current++;
            return a;
        }
        long long temp = a;
        a = b;
        b = temp + b;
        current++;
        return temp;
    }
    
    std::vector<long long> toVector() {
        std::vector<long long> result;
        FibonacciIterator iter(limit);
        while (iter.hasNext()) {
            result.push_back(iter.next());
        }
        return result;
    }
};

// 3. 行列累乗版
class Matrix {
public:
    long long m[2][2];
    
    Matrix() {
        m[0][0] = m[0][1] = m[1][0] = m[1][1] = 0;
    }
    
    Matrix(long long a, long long b, long long c, long long d) {
        m[0][0] = a; m[0][1] = b;
        m[1][0] = c; m[1][1] = d;
    }
    
    Matrix operator*(const Matrix& other) const {
        Matrix result;
        result.m[0][0] = m[0][0] * other.m[0][0] + m[0][1] * other.m[1][0];
        result.m[0][1] = m[0][0] * other.m[0][1] + m[0][1] * other.m[1][1];
        result.m[1][0] = m[1][0] * other.m[0][0] + m[1][1] * other.m[1][0];
        result.m[1][1] = m[1][0] * other.m[0][1] + m[1][1] * other.m[1][1];
        return result;
    }
};

class FibonacciMatrix {
public:
    long long calculate(int n) {
        if (n <= 1) return n;
        Matrix base(1, 1, 1, 0);
        Matrix result = matrixPower(base, n);
        return result.m[0][1];
    }

private:
    Matrix matrixPower(Matrix base, int n) {
        if (n == 0) return Matrix(1, 0, 0, 1); // 単位行列
        if (n == 1) return base;
        
        if (n % 2 == 0) {
            Matrix half = matrixPower(base, n / 2);
            return half * half;
        } else {
            return base * matrixPower(base, n - 1);
        }
    }
};

// 4. 黄金比を使った近似計算
class FibonacciGoldenRatio {
private:
    static constexpr double PHI = (1.0 + std::sqrt(5.0)) / 2.0;

public:
    long long calculate(int n) {
        return static_cast<long long>(std::round(
            (std::pow(PHI, n) - std::pow(-PHI, -n)) / std::sqrt(5.0)
        ));
    }
    
    static double getPhi() { return PHI; }
};

// 5. テンプレートを使ったジェネリック版
template<typename T>
class FibonacciGeneric {
public:
    static std::vector<T> generate(int n) {
        std::vector<T> result;
        if (n >= 1) result.push_back(0);
        if (n >= 2) result.push_back(1);
        for (int i = 2; i < n; i++) {
            result.push_back(result[i-1] + result[i-2]);
        }
        return result;
    }
};

int main() {
    std::cout << "=== フィボナッチ数列の様々な実装 ===" << std::endl << std::endl;
    
    // 1. 再帰版のデモ
    std::cout << "1. 再帰版（メモ化付き）" << std::endl;
    FibonacciRecursive fibRecursive;
    std::cout << "最初の10項: ";
    for (int i = 0; i < 10; i++) {
        std::cout << fibRecursive.calculate(i) << " ";
    }
    std::cout << std::endl << std::endl;
    
    // 2. イテレータ版のデモ
    std::cout << "2. イテレータ版" << std::endl;
    std::cout << "最初の10項: ";
    FibonacciIterator fibIter(10);
    while (fibIter.hasNext()) {
        std::cout << fibIter.next() << " ";
    }
    std::cout << std::endl << std::endl;
    
    // 3. 行列累乗版のデモ
    std::cout << "3. 行列累乗版（大きな数も高速）" << std::endl;
    FibonacciMatrix fibMatrix;
    std::cout << "n=50の値: " << fibMatrix.calculate(50) << std::endl << std::endl;
    
    // 4. 黄金比版のデモ
    std::cout << "4. 黄金比を使った近似計算" << std::endl;
    FibonacciGoldenRatio fibGolden;
    std::cout << "最初の10項: ";
    for (int i = 0; i < 10; i++) {
        std::cout << fibGolden.calculate(i) << " ";
    }
    std::cout << std::endl << std::endl;
    
    // 5. テンプレート版のデモ
    std::cout << "5. テンプレート版（ジェネリック）" << std::endl;
    auto sequence = FibonacciGeneric<long long>::generate(15);
    std::cout << "最初の15項: ";
    for (const auto& num : sequence) {
        std::cout << num << " ";
    }
    std::cout << std::endl << std::endl;
    
    // おまけ：フィボナッチ数列の性質を調べる
    std::cout << "=== フィボナッチ数列の面白い性質 ===" << std::endl;
    
    // 隣接項の比が黄金比に収束
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "隣接項の比（黄金比" << FibonacciGoldenRatio::getPhi() << "に収束）:" << std::endl;
    for (int i = 5; i <= 10; i++) {
        double ratio = static_cast<double>(sequence[i]) / sequence[i-1];
        std::cout << "F(" << i << ")/F(" << i-1 << ") = " << ratio << std::endl;
    }
    
    // 最初のn項の和
    std::cout << std::endl << "最初のn項の和の性質（F(n+2) - 1に等しい）:" << std::endl;
    for (int n = 5; n <= 8; n++) {
        long long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += sequence[i];
        }
        std::cout << "最初の" << n << "項の和: " << sum 
                  << " = F(" << n+2 << ") - 1 = " << sequence[n+1] << " - 1" << std::endl;
    }
    
    return 0;
}