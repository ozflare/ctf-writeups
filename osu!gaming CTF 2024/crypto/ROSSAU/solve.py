n = 5912718291679762008847883587848216166109
p = 59644326261100157131
q = 99132954671935298039

assert(n == p * q)

e = 876603837240112836821145245971528442417
phi_n = (p - 1) * (q - 1)
d = pow(e, -1, phi_n)

print(d)