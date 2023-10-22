from time import thread_time_ns

NS_PER_S = 10 ** 9

def cronometra(azione):
  t0 = thread_time_ns()
  azione()
  t1 = thread_time_ns()
  return (t1 - t0) / NS_PER_S