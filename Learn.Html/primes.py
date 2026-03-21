"""打印所有小于等于 1000 的素数。"""

from math import isqrt


def is_prime(n: int) -> bool:
    """当 n 为素数时返回 True。"""
    if n < 2:
        return False
    # 仅试除到整数平方根，适合处理较小的上界。
    limit = isqrt(n)
    for factor in range(2, limit + 1):
        if n % factor == 0:
            return False
    return True


if __name__ == "__main__":
    primes = [number for number in range(2, 1001) if is_prime(number)]
    print(", ".join(map(str, primes)))
