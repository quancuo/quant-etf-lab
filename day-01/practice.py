"""第 1 天练习。完成后运行 python day-01/practice.py。"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """返回两个不同的下标，对应元素之和等于 target。题目保证答案唯一。"""
    # 在这里写你的解法。参考解答在同目录的 exercises.md。
    raise NotImplementedError


def coin_game_counts(n: int) -> tuple[int, int]:
    """枚举甲抛 n+1 次、乙抛 n 次的结果，返回（甲严格领先的结果数，总结果数）。"""
    # n 为非负整数。每次抛掷公平且独立，平局只计入总结果数。
    # 在这里写你的枚举。手算表和证明在同目录的 exercises.md。
    raise NotImplementedError


def _check_two_sum() -> None:
    examples = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([6, 6], 12, [0, 1]),
        ([-4, 9, 6, 2], 5, [0, 1]),
        ([4, 1, 7], 8, [1, 2]),
    ]
    for nums, target, expected in examples:
        result = two_sum(nums.copy(), target)
        if (
            not isinstance(result, list)
            or any(type(index) is not int for index in result)
            or sorted(result) != expected
        ):
            raise AssertionError(
                f"输入 {nums}，目标 {target}，应返回下标 {expected}（顺序不限），实际返回 {result!r}"
            )


def _check_coin_game() -> None:
    examples = [(0, (1, 2)), (1, (4, 8)), (2, (16, 32)), (3, (64, 128))]
    for n, expected in examples:
        result = coin_game_counts(n)
        if (
            not isinstance(result, tuple)
            or any(type(count) is not int for count in result)
            or result != expected
        ):
            raise AssertionError(f"n={n} 时应返回 {expected}，实际返回 {result!r}")


if __name__ == "__main__":
    for title, check in [("两数之和", _check_two_sum), ("抛硬币游戏", _check_coin_game)]:
        try:
            check()
        except NotImplementedError:
            print(f"{title} · 待完成")
        else:
            print(f"{title} · 自测通过")
