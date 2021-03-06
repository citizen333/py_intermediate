def is_chief_detected(num):
    return num == "A555AA"


def calculate_fine(num):
    fine = 0
    if is_super_number(num):
        fine = 1000
    elif is_good_number(num):
        fine = 500
    else:
        fine = 100
    return fine


def is_super_number(num):
    return num[1] == num[2] == num[3]


def is_good_number(num):
    return num[1] == num[2] or num[2] == num[3] or num[3] == num[1]


if __name__ == "__main__":
    fine_sum = 0  # money
    v, num = input().split()  # car speed and registration number
    v = int(v)
    while not is_chief_detected(num):
        if v > 60:
            fine_sum += calculate_fine(num)
        v, num = input().split()
        v = int(v)
    print(fine_sum)

# %%
def gcd(a, b):
    assert a > 0
    assert isinstance(a, int)
    assert b > 0
    assert isinstance(b, int)
    while b != 0:
        r = a % b
        b = a
        a = r
    return a
# %%
gcd(2.0,2)
# %%
