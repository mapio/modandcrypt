from operator import mul, add

from tabulate import tabulate

# prime related functions

def egcd(a, b):
  s0, s1, t0, t1 = 1, 0, 0, 1
  while b != 0:
    q, a, b = a // b, b, a % b
    s0, s1 = s1, s0 - q * s1
    t0, t1 = t1, t0 - q * t1
  return a, s0, t0

def gcd(a, b):
  return egcd(a, b)[0]

def is_prime(n):
  if n < 2: return False
  i = 2
  while i * i <= n:
    if n % i == 0: return False
    i += 1
  return True

def factors(n):
  i = 2
  while i * i <= n:
    if n % i == 0:
      yield i
      n //= i
    else:
      i += 1
  if n > 1:
    yield n

def φ(n):
  return sum(1 for k in range(1, n + 1) if gcd(n, k) == 1)
  
# modular arithmetic

def expm(b, e, m):
  r = 1
  while e > 0:
    if e % 2 == 1: r = (r * b) % m
    b = (b * b) % m
    e = e // 2
  return r

def invm(a, m):
  if gcd(a, m) != 1: return None
  return egcd(a, m)[1] % m

def rsa(m, k):
  return expm(m, k[0], k[1])  

class Mod:

  class R:
    def __init__(self, n, m):
      self.m = m
      self.n = n % m
    def __add__(self, other):
      if self.m != other.m: raise ValueError()
      return Mod.R(self.n + other.n, self.m)
    def __sub__(self, other):
      if self.m != other.m: raise ValueError()
      return Mod.R(self.n - other.n, self.m)
    def __neg__(self):
      return Mod.R(-self.n, self.m)
    def __mul__(self, other):
      if self.m != other.m: raise ValueError()
      return Mod.R(self.n * other.n, self.m)
    def __truediv__(self, other):
      if self.m != other.m: raise ValueError()
      return Mod.R(self.n * invm(other.n, self.m), self.m)
    def __rtruediv__(self, other):
      if other != 1: raise ValueError()
      return Mod.R(invm(self.n, self.m), self.m)
    def __pow__(self, other):
      if not isinstance(other, int): raise ValueError()
      if other < 0: return Mod.R(invm(self.n, self.m), self.m) ** -other
      return Mod.R(expm(self.n, other, self.m), self.m)
    def __eq__(self, other):
      if isinstance(other, int): other = Mod.R(other, self.m)
      if not isinstance(other, Mod.R): return False
      if self.m != other.m: raise ValueError()
      return self.n == other.n
    def potenze(self):
      res = []
      for i in range(1, self.m):
        p = self ** i
        if not p in res: res.append(p)
      return res
    def __repr__(self):
      return f'[{self.n}]'

  def __init__(self, m):
    self.m = m   
  def __getitem__(self, i):
    return Mod.R(i, self.m)
  def coprimi(self):
    return [self[i] for i in range(1, self.m) if gcd(i, self.m) == 1]
  def somma(self):
    op_table('+', self.m)
  def prodotto(self):
    op_table('*', self.m)
  def prodotto_coprimi(self):
    op_table('*', self.m, True)
  def generatori(self):
    N = self.coprimi()
    H = [ansi_boldify('**')] + ansi_boldify(list(range(1, 1 + φ(self.m))))
    print(tabulate([r.potenze() for r in N], headers = H, showindex = ansi_boldify(N), tablefmt = 'simple_grid'))

# display

def ansi_boldify(param):
  if isinstance(param, list):
    return [f'\033[1m{e}\033[0m' for e in param]
  else:
    return f'\033[1m{param}\033[0m'

def ansi_color(param, color):
  if isinstance(param, list):
    return [f'\033[{color}m{e}\033[0m' for e in param]
  else:
    return f'\033[{color}m{param}\033[0m'

def op_table(op, n, restrict = False):
  def col(v, t, c):
    return v if v != t else ansi_color(v, c)
  M = Mod(n)
  first = 1 if op == '*' else 0
  N = [M[i] for i in range(first, n)]
  if op == '*':
    if restrict: N = [M[i] for i in range(first, n) if gcd(i, n) == 1]
    vals = [[col(col(i * j, 1, 92), 0, 91) for i in N] for j in N]
  else:
    vals = [[col(i + j, 0, 92) for i in N] for j in N]
  H = ansi_boldify(N)
  table = list(tabulate(vals, headers = H, showindex = H, tablefmt = "simple_grid"))
  table[table.index('\n') + 4] = ansi_boldify(op)
  print(''.join(table))

# goedelize text

def to_number(msg, length = 20):
  b = (msg.encode('utf-8') + b' ' * length)[:length]
  return int.from_bytes(b, 'big')

def from_number(n, length = 20):
  return int.to_bytes(n, length, 'big').decode('utf-8').strip()
