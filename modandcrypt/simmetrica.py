from itertools import cycle, islice

from .testo import NUM_SEMPLICI, LETTERA2POS, POS2LETTERA, semplifica, da_posizioni, a_posizioni
from .visualizza import tabella, sgr

def inverti(chiave):
  return ''.join(POS2LETTERA[-LETTERA2POS[c] % NUM_SEMPLICI] for c in semplifica(chiave))

def orologio_somma(posizioni, chiave):
  return [(p + c) % NUM_SEMPLICI for p, c in zip(posizioni, cycle(chiave))]

def _ost(testo, chiave, passi):
  def cp(testo):
    testo = semplifica(testo)
    return [f'{c}:{p}' for c, p in zip(testo, a_posizioni(testo))]
  testo = semplifica(testo)
  p_testo = a_posizioni(testo)
  chiave = semplifica(chiave)
  p_chiave = a_posizioni(chiave)
  trasf = da_posizioni(orologio_somma(p_testo, p_chiave))
  tabella([
    cp(testo),
    islice(cycle(cp(chiave)), len(testo)),
    cp(trasf)
  ], index = sgr(passi))
  return trasf

def cifra(chiaro, chiave):
  return _ost(chiaro, chiave, ['p', 'k', 'c'])

def decifra(cifrato, chiave):
  return _ost(cifrato, inverti(chiave), ['c', 'k', 'p'])