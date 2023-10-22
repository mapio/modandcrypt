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
  tabella([
    cp(testo),
    islice(cycle(cp(chiave)), len(testo)),
    cp(da_posizioni(orologio_somma(p_testo, p_chiave)))
  ], index = sgr(passi))

def cifra(chiaro, chiave):
  _ost(chiaro, chiave, ['chiaro', 'chiave', 'cifrato'])

def decifra(cifrato, chiave):
  _ost(cifrato, inverti(chiave), ['cifrato', 'chiave', 'chiaro'])