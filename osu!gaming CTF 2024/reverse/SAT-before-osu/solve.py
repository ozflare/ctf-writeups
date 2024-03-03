import z3

a = z3.Int('a')
b = z3.Int('b')
c = z3.Int('c')
d = z3.Int('d')
e = z3.Int('e')
f = z3.Int('f')
g = z3.Int('g')
h = z3.Int('h')
i = z3.Int('i')
j = z3.Int('j')
k = z3.Int('k')
l = z3.Int('l')
m = z3.Int('m')
n = z3.Int('n')
o = z3.Int('o')
p = z3.Int('p')
q = z3.Int('q')
r = z3.Int('r')
s = z3.Int('s')
t = z3.Int('t')
u = z3.Int('u')
v = z3.Int('v')
w = z3.Int('w')
x = z3.Int('x')
y = z3.Int('y')
z = z3.Int('z')
solver = z3.Solver()

solver.add(b + c + w == 314)
solver.add(t + d + u == 290)
solver.add(p + w + e == 251)
solver.add(v + l + j == 274)
solver.add(a + t + b == 344)
solver.add(b + j + m == 255)
solver.add(h + o + u == 253)
solver.add(q + l + o == 316)
solver.add(a + g + j == 252)
solver.add(q + x + q == 315)
solver.add(t + n + m == 302)
solver.add(d + b + g == 328)
solver.add(e + o + m == 246)
solver.add(v + v + u == 271)
solver.add(f + o + q == 318)
solver.add(s + o + j == 212)
solver.add(j + j + n == 197)
solver.add(s + u + l == 213)
solver.add(q + w + j == 228)
solver.add(i + d + r == 350)
solver.add(e + k + u == 177)
solver.add(w + n + a == 288)
solver.add(r + e + u == 212)
solver.add(q + l + f == 321)

print(solver.check())
print(solver.model())

answer = {
    'r': 115,
    'm': 89,
    'i': 112,
    'v': 111,
    'h': 95,
    'q': 95,
    'f': 114,
    'c': 117,
    'p': 121,
    'a': 111,
    't': 118,
    'w': 82,
    'k': 80,
    'x': 125,
    'g': 90,
    'd': 123,
    'j': 51,
    'b': 115,
    'o': 109,
    'e': 48,
    'u': 49,
    's': 52,
    'l': 112,
    'n': 95
}

for k, v in sorted(answer.items()):
    print(chr(v), end='')