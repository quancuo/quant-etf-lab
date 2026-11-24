"""第 2 天练习。完成后运行 python day-02/practice.py。"""

from fractions import Fraction
from math import isclose


def group_anagrams(words):
    """把异位词分组并返回列表的列表。保留重复项和空字符串。"""
    # 在这里写你的解法。参考解答在同目录的 exercises.md。
    raise NotImplementedError


def biased_coin_posterior():
    """等概率选择正面率为 0.5 或 0.8 的硬币。给定正面，返回选到后者的概率。"""
    # 可以返回 Fraction 或 float。参考推导在同目录的 exercises.md。
    raise NotImplementedError


def _normalize_groups(groups):
    if not isinstance(groups, list) or any(
        not isinstance(group, list) or any(not isinstance(word, str) for word in group)
        for group in groups
    ):
        raise AssertionError(f"请返回由字符串列表组成的列表，实际返回 {groups!r}")
    return sorted(sorted(group) for group in groups)


def _check_group_anagrams():
    examples = [
        (["tea", "eat", "bat", "tab"], [["tea", "eat"], ["bat", "tab"]]),
        (["tea", "eat", "tea", "et", "tee"], [["tea", "eat", "tea"], ["et"], ["tee"]]),
        (["", "a", "", "aa"], [["", ""], ["a"], ["aa"]]),
        ([""], [[""]]),
    ]
    for words, expected in examples:
        result = group_anagrams(words.copy())
        if _normalize_groups(result) != _normalize_groups(expected):
            raise AssertionError(f"输入 {words!r}，应分组为 {expected!r}，实际返回 {result!r}")


def _check_posterior():
    expected = Fraction(8, 13)
    result = biased_coin_posterior()
    correct = (isinstance(result, Fraction) and result == expected) or (
        isinstance(result, float) and isclose(result, float(expected), rel_tol=1e-9)
    )
    if not correct:
        raise AssertionError(f"应返回概率 {expected}，实际返回 {result!r}")


if __name__ == "__main__":
    for title, check in [("字母异位词分组", _check_group_anagrams), ("贝叶斯", _check_posterior)]:
        try:
            check()
        except NotImplementedError:
            print(f"{title} · 待完成")
        else:
            print(f"{title} · 自测通过")
