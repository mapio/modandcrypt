from .primi import MCD, MCDE, φ
from .visualizza import tabella, sgr

def expm(b, e, m):
  r = 1
  while e > 0:
    if e % 2 == 1: r = (r * b) % m
    b = (b * b) % m
    e = e // 2
  return r

def invm(a, m):
  if MCD(a, m) != 1: return None
  return MCDE(a, m)[1] % m

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
    def __hash__(self):
      return hash((self.n, self.m))
    def rappresentante(self):
      return self.n
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
    return [self[i] for i in range(1, self.m) if MCD(i, self.m) == 1]
  def somma(self):
    N = self.elementi()
    vals = [[sgr(i + j, 92, 0) for i in N] for j in N]
    H = sgr(N)
    tabella(vals, [sgr('+')] + H, H)
  def prodotto(self):
    N = self.elementi()[1:]
    vals = [[sgr(sgr(i * j, 92, 1), 91, 0) for i in N] for j in N]
    H = sgr(N)
    tabella(vals, [sgr('*')] + H, H)
  def prodotto_coprimi(self):
    N = self.elementi_coprimi()
    vals = [[sgr(sgr(i * j, 92, 1), 91, 0) for i in N] for j in N]
    H = sgr(N)
    tabella(vals, [sgr('*')] + H, H)
  def generatori(self):
    N = self.elementi_coprimi()
    vals = [r.potenze() for r in N]
    t = φ(self.m) # this can take a while!
    H = [sgr('**')] + sgr(range(1, 1 + t))
    I = [sgr(n) if len(v) != t else sgr(sgr(n), 96) for n, v in zip(N, vals)]
    tabella(vals, H, I)
