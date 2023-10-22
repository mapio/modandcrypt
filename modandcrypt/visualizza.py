from tabulate import tabulate

def sgr(what, code = 1, target = None):
  if target is not None and what != target: return what
  if isinstance(what, (list, range)):
    return [f'\033[{code}m{e}\033[0m' for e in what]
  else:
    return f'\033[{code}m{what}\033[0m'

def tabella(vals, header, index):
  print(tabulate(vals, headers = header, showindex = index, tablefmt = 'simple_grid'))
 
