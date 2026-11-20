##用字典扫过已经看过的数值 
class Solution :
    def twosum(self , nums :list[int] , target: int) -> list[int] :
        seen = {}
        for i ,value in enumerate(nums):
            complement = target - value 

            if complement in seen :
                return [seen[complement],i]
                seen [value] = i

        raise ValueError("未找到有效数对")



# 力扣按这个结构接收你的解法
class Solution:
    # nums 是整数列表，target 是目标整数，返回值是两个整数下标
    # self 代表当前的 Solution 对象，力扣调用方法时会自动传入
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # 字典保存「之前见过的数字 → 该数字的下标」
        seen = {}

        # enumerate 同时给出下标 i 和该位置上的数字 value
        for i, value in enumerate(nums):
            # 计算补数：当前数字加上它，刚好等于 target
            complement = target - value

            # 检查这个补数是否已经作为键出现在字典里
            if complement in seen:
                # seen[complement] 是补数的下标，i 是当前数字的下标
                # 找到答案后立即返回，函数在这里结束
                return [seen[complement], i]

            # 这一步没找到配对，就记录当前数字，供后面的数字查找
            seen[value] = i

        # 循环结束仍未找到配对时抛出异常
        # 力扣保证有解，符合题意的输入会在上面的 return 结束
        raise ValueError("未找到有效数对")