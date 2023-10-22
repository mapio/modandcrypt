from functools import reduce
from operator import mul, add

def MCDE(a, b):
  s0, s1, t0, t1 = 1, 0, 0, 1
  while b != 0:
    q, a, b = a // b, b, a % b
    s0, s1 = s1, s0 - q * s1
    t0, t1 = t1, t0 - q * t1
  return a, s0, t0

def MCD(a, b):
  return MCDE(a, b)[0]

def è_primo(n):
  if n < 2: return False
  i = 2
  while i * i <= n:
    if n % i == 0: return False
    i += 1
  return True

def fattorizza(n):
  res = []
  i = 2
  while i * i <= n:
    if n % i == 0:
      res.append(i)
      n //= i
    else:
      i += 1
  if n > 1: res.append(n)
  return res

def moltiplica(lst):
  return reduce(mul, lst, 1)

def φ(n):
  return sum(1 for k in range(1, n + 1) if MCD(n, k) == 1)
  
