import math
my_list = [85, 98, 79, 96, 99, 85, 79, 94, 105, 96, 77, 108, 91, 91, 105, 105, 108, 92, 100, 87, 94, 120, 103, 98, 104,
           112, 94, 102, 99, 98, 98, 94, 109, 99, 101, 93, 98, 109, 86, 92, 97, 92, 97, 77, 104, 92, 112, 113, 97, 90,
           117, 84, 89, 72, 81, 106, 97, 99, 91, 88, 113, 99, 99, 102, 108, 88, 87, 95, 91, 85, 108, 84, 103, 112, 98,
           92, 85, 119, 101, 88, 107, 107, 96, 115, 96, 89, 89, 90, 82, 95, 100, 93, 96, 89, 85]
print(len(my_list))

print(min(my_list))
print(max(my_list))

h = (max(my_list) - min(my_list))/(1 + 3.322*math.log(95))
print(h)
my_list.sort()
print(max(my_list))
print(sum(my_list))
sum1 = 0
for el in my_list:
    sum1 = sum1 + el*el
print(sum1/95)