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
  def elementi(self):
    return [self[i] for i in range(self.m)]
  def elementi_coprimi(self):
    return [self[i] for i in range(1, self.m) if gcd(i, self.m) == 1]
  def somma(self):
    N = self.elementi()
    vals = [[_sgr(i + j, 92, 0) for i in N] for j in N]
    H = _sgr(N)
    print(tabulate(vals, headers = [_sgr('+')] + H, showindex = H, tablefmt = "simple_grid"))
  def prodotto(self):
    N = self.elementi()[1:]
    vals = [[_sgr(_sgr(i * j, 92, 1), 91, 0) for i in N] for j in N]
    H = _sgr(N)
    _table(vals, [_sgr('*')] + H, H)
  def prodotto_coprimi(self):
    N = self.elementi_coprimi()
    vals = [[_sgr(_sgr(i * j, 92, 1), 91, 0) for i in N] for j in N]
    H = _sgr(N)
    _table(vals, [_sgr('*')] + H, H)
  def generatori(self):
    N = self.elementi_coprimi()
    vals = [r.potenze() for r in N]
    t = φ(self.m)
    H = [_sgr('**')] + _sgr(range(1, 1 + t))
    I = [_sgr(n) if len(v) != t else _sgr(_sgr(n), 96) for n, v in zip(N, vals)]
    _table(vals, H, I)

# display

def _table(vals, header, index):
  print(tabulate(vals, headers = header, showindex = index, tablefmt = 'simple_grid'))
 
def _sgr(what, code = 1, target = None):
  if target is not None and what != target: return what
  if isinstance(what, (list, range)):
    return [f'\033[{code}m{e}\033[0m' for e in what]
  else:
    return f'\033[{code}m{what}\033[0m'

# goedelize text

def to_number(msg, length = 20):
  b = (msg.encode('utf-8') + b' ' * length)[:length]
  return int.from_bytes(b, 'big')

def from_number(n, length = 20):
  return int.to_bytes(n, length, 'big').decode('utf-8').strip()
