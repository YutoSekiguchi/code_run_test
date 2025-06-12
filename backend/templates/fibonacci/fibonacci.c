#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 1. 再帰版（メモ化付き）
long long memo[100];
int memo_init = 0;

void init_memo() {
    if (!memo_init) {
        for (int i = 0; i < 100; i++) {
            memo[i] = -1;
        }
        memo_init = 1;
    }
}

long long fibonacci_recursive(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2);
    return memo[n];
}

// 2. 反復版
long long fibonacci_iterative(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1, temp;
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// 3. 行列累乗版の構造体とヘルパー関数
typedef struct {
    long long m[2][2];
} Matrix;

Matrix matrix_multiply(Matrix a, Matrix b) {
    Matrix result;
    result.m[0][0] = a.m[0][0] * b.m[0][0] + a.m[0][1] * b.m[1][0];
    result.m[0][1] = a.m[0][0] * b.m[0][1] + a.m[0][1] * b.m[1][1];
    result.m[1][0] = a.m[1][0] * b.m[0][0] + a.m[1][1] * b.m[1][0];
    result.m[1][1] = a.m[1][0] * b.m[0][1] + a.m[1][1] * b.m[1][1];
    return result;
}

Matrix matrix_power(Matrix base, int n) {
    if (n == 0) {
        Matrix identity = {{{1, 0}, {0, 1}}};
        return identity;
    }
    if (n == 1) return base;
    
    if (n % 2 == 0) {
        Matrix half = matrix_power(base, n / 2);
        return matrix_multiply(half, half);
    } else {
        return matrix_multiply(base, matrix_power(base, n - 1));
    }
}

long long fibonacci_matrix(int n) {
    if (n <= 1) return n;
    Matrix base = {{{1, 1}, {1, 0}}};
    Matrix result = matrix_power(base, n);
    return result.m[0][1];
}

// 4. 黄金比を使った近似計算
long long fibonacci_golden_ratio(int n) {
    double phi = (1.0 + sqrt(5.0)) / 2.0;
    double psi = (1.0 - sqrt(5.0)) / 2.0;
    return (long long)round((pow(phi, n) - pow(psi, n)) / sqrt(5.0));
}

// 配列を使ったフィボナッチ数列生成
void generate_fibonacci_sequence(long long *sequence, int n) {
    if (n >= 1) sequence[0] = 0;
    if (n >= 2) sequence[1] = 1;
    for (int i = 2; i < n; i++) {
        sequence[i] = sequence[i-1] + sequence[i-2];
    }
}

int main() {
    printf("=== フィボナッチ数列の様々な実装 ===\n\n");
    
    init_memo();
    
    // 1. 再帰版のデモ
    printf("1. 再帰版（メモ化付き）\n");
    printf("最初の10項: ");
    for (int i = 0; i < 10; i++) {
        printf("%lld ", fibonacci_recursive(i));
    }
    printf("\n\n");
    
    // 2. 反復版のデモ
    printf("2. 反復版\n");
    printf("最初の10項: ");
    for (int i = 0; i < 10; i++) {
        printf("%lld ", fibonacci_iterative(i));
    }
    printf("\n\n");
    
    // 3. 行列累乗版のデモ
    printf("3. 行列累乗版（大きな数も高速）\n");
    printf("n=50の値: %lld\n\n", fibonacci_matrix(50));
    
    // 4. 黄金比版のデモ
    printf("4. 黄金比を使った近似計算\n");
    printf("最初の10項: ");
    for (int i = 0; i < 10; i++) {
        printf("%lld ", fibonacci_golden_ratio(i));
    }
    printf("\n\n");
    
    // 5. 配列版のデモ
    printf("5. 配列版\n");
    long long sequence[15];
    generate_fibonacci_sequence(sequence, 15);
    printf("最初の15項: ");
    for (int i = 0; i < 15; i++) {
        printf("%lld ", sequence[i]);
    }
    printf("\n\n");
    
    // おまけ：フィボナッチ数列の性質を調べる
    printf("=== フィボナッチ数列の面白い性質 ===\n");
    
    // 隣接項の比が黄金比に収束
    double phi = (1.0 + sqrt(5.0)) / 2.0;
    printf("隣接項の比（黄金比%.6fに収束）:\n", phi);
    for (int i = 5; i <= 10; i++) {
        double ratio = (double)sequence[i] / sequence[i-1];
        printf("F(%d)/F(%d) = %.6f\n", i, i-1, ratio);
    }
    
    // 最初のn項の和
    printf("\n最初のn項の和の性質（F(n+2) - 1に等しい）:\n");
    for (int n = 5; n <= 8; n++) {
        long long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += sequence[i];
        }
        printf("最初の%d項の和: %lld = F(%d) - 1 = %lld - 1\n", 
               n, sum, n+2, sequence[n+1]);
    }
    
    return 0;
}