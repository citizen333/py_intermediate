import sys

a = float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])

x_1 = (-b + (b**2 - 4*a*c)**0.5) / (2*a)
x_2 = (-b - (b**2 - 4*a*c)**0.5) / (2*a)

print(int(x_1))
print(int(x_2))