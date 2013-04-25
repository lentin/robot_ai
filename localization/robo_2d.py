#p: probabilities for n locations of robot in 2d world

#the world, red and green
world = [['r','g','g','r','r'],
         ['r','r','g','r','r'],
         ['r','r','g','g','r'],
         ['r','r','r','r','r']]

#measurements
measurements = ['g','g','g','g','g']

#movements, 0,0: stay, 0,1: move right, 1,0: move down
movements = [[0,0],[0,1],[1,0],[1,0],[0,1]]

#sensing vars, sense is product followed by normalization
#if we sense X, p*pHit chance of being at X location
#               p*pMiss chance of being at !X location
#after sense X, robot is pHit/pMiss times more likely to be at X locations
#probabilities have to be normalized after multiplication
pHit = .7

#movement vars, moving is a convolution
#pExact: move to where we predicted, 1-pExact: stay put
pExact = .8


#uniform distribution, maximum confusion, where are we??
def init_probabilities(n):
  q =[]
  for i in range(len(world)):
    p = []
    for j in range(len(world[0])):
      p = p + [1.0/n]
    q = q + [p]
  return q

#robot sense color
def sense(p,Z):
  #sum for renormalizing
  s = 0

  #lists of lists actual copy
  q = [x[:] for x in p]
  #after sensing Z:
  for i in range(len(p)):
    for j in range(len(p[0])):
      #check if world is Z at i/j'th location
      hit = (world[i][j] == Z)
      #calculate new probabilities
      q[i][j] = hit * q[i][j] * pHit + (1-hit) * q[i][j] * (1-pHit)
      s = s + q[i][j]

  #renormalize probabilities
  for i in range(len(p)):
    for j in range(len(p[0])):
      q[i][j] = q[i][j] / s

  return q

#robot move, 1: move right 1
def move(p,U):
  #lists of lists actual copy
  q = [x[:] for x in p]
  m = len(p)
  n = len(p[0])
  #no move
  if U == [0,0]:
    return p
  #horizontal moves
  if U[1] != 0:
    for i in range(m):
      for j in range(n):
        q[i][j] = pExact*p[i][(j-U[1])%n] + (1-pExact)*p[i][j]
  #vertical moves
  if U[0] != 0:
    for i in range(m):
      for j in range(n):
        q[i][j] = pExact*p[(i-U[0])%m][j] + (1-pExact)*p[i][j]
      #q[i] = pExact*p[(i-U)%n] + pUndershoot*p[(i-U-1)%n] + pOvershoot*p[(i-U+1)%n]
  return q


#initial or 'prior' belief
#uniform distribution, maximum confusion, where are we??
p = init_probabilities(len(world)*len(world[0]))
#p = [0,1,0,0,0]
#  print p
#  print ['%.2f' % x for x in p]
for x in p:
  print ['%.2f' % y for y in x]

for i in range(len(measurements)):

  p = move(p,movements[i])
  print 'After Moving: ' + str(movements[i])
  for x in p:
    print ['%.2f' % y for y in x]
  
  p = sense(p,measurements[i])
  print 'After Sensing: ' + str(measurements[i])
  for x in p:
    print ['%.2f' % y for y in x]
