from collections import Counter
from unicodedata import normalize
from string import ascii_uppercase 
from urllib.request import urlopen

import matplotlib.pyplot as plt

SEMPLICI = ascii_uppercase + ' \n'
NUM_SEMPLICI = len(SEMPLICI)
SEMPLICI_VISUALIZZABILI = list(SEMPLICI[:-2]) + ['␢', '↩']

POS2LETTERA = dict(zip(range(NUM_SEMPLICI), SEMPLICI))
LETTERA2POS = dict(zip(SEMPLICI, range(NUM_SEMPLICI)))

def a_visualizzazione(testo):
  return ''.join(SEMPLICI_VISUALIZZABILI[LETTERA2POS[c]] for c in semplifica(testo))

def semplifica(testo):
  return ''.join(c for c in normalize('NFD', testo).upper() if c in SEMPLICI)

def a_posizioni(testo):
  return [LETTERA2POS[c] for c in semplifica(testo)]

def da_posizioni(posizioni):
  return ''.join(POS2LETTERA[p] for p in posizioni)

def a_bytes(testo):
  return list(testo.encode('utf-8'))

def a_numero(testo):
  numero = 0
  for b in a_bytes(testo): numero = numero * 256 + b
  return numero

def da_bytes(bs):
  return bytes(bs).decode('utf-8')

def da_numero(numero):
  res = []
  while numero > 0:
    numero, b = numero // 256, numero % 256
    res.append(b)
  return bytes(reversed(res)).decode('utf-8')

def istogramma_lettere(testo):
  cnt = Counter() 
  cnt.update(semplifica(testo))
  plt.bar(SEMPLICI_VISUALIZZABILI, [cnt[c] if c in cnt else 0 for c in SEMPLICI])
  plt.yticks([])
  plt.show()
  return cnt
  
def da_gutenberg(url):
  with urlopen(url) as inf: return inf.read().decode('utf-8-sig')