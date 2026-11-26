"""第 3 天练习。完成后运行 python day-03/practice.py。"""

from fractions import Fraction
from math import isclose


def longest_consecutive(nums):
    """返回最长连续整数段的长度。重复值只算一次，空输入返回 0。"""
    # 在这里写你的解法。参考解答在同目录的 exercises.md。
    raise NotImplementedError


def fixed_pair_probability():
    """从 8 人中等概率抽 3 人且不放回，返回两名指定的人都入选的概率。"""
    # 可以返回 Fraction 或 float。参考推导在同目录的 exercises.md。
    raise NotImplementedError


def _check_longest_consecutive():
    examples = [
        ([14, 4, 2, 5, 2, 3], 4),
        ([-3, -1, 1, -2], 3),
        ([8, 8, 8], 1),
        ([3, 7, 11], 1),
        ([], 0),
    ]
    for nums, expected in examples:
        result = longest_consecutive(nums.copy())
        if type(result) is not int or result != expected:
            raise AssertionError(f"输入 {nums!r}，应返回 {expected}，实际返回 {result!r}")


def _check_probability():
    expected = Fraction(3, 28)
    result = fixed_pair_probability()
    correct = (isinstance(result, Fraction) and result == expected) or (
        isinstance(result, float) and isclose(result, float(expected), rel_tol=1e-9)
    )
    if not correct:
        raise AssertionError(f"应返回概率 {expected}，实际返回 {result!r}")


if __name__ == "__main__":
    for title, check in [("最长连续序列", _check_longest_consecutive), ("组合计数", _check_probability)]:
        try:
            check()
        except NotImplementedError:
            print(f"{title} · 待完成")
        else:
            print(f"{title} · 自测通过")
