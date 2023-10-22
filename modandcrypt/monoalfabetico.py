from itertools import cycle

from .testo import NUM_SEMPLICI, LETTERA2POS, POS2LETTERA, semplifica

def inverti(chiave):
  return ''.join(POS2LETTERA[-LETTERA2POS[c] % NUM_SEMPLICI] for c in semplifica(chiave))

def orologio_somma(posizioni, chiave):
  return [(p + LETTERA2POS[c]) % NUM_SEMPLICI for p, c in zip(posizioni, cycle(semplifica(chiave)))]
