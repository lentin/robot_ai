#p: probabilities for n locations of robot in 1d world

#the world, red and green
world = ['g','r','r','g','g']

#measurements
measurements = ['r','r']

#movements, 0: stay, 1: moved right, -1: moved left
movements = [1,1]

#sensing vars, sense is product followed by normalization
#if we sense X, p*pHit chance of being at X location
#               p*pMiss chance of being at !X location
#after sense X, robot is pHit/pMiss times more likely to be at X locations
#probabilities have to be normalized after multiplication
pHit = .6
pMiss = .2

#movement vars, moving is a convolution
#pExact: move to where we predicted, or over/undershoot
pExact = .8
pOvershoot = .1
pUndershoot = .1


#uniform distribution, maximum confusion, where are we??
def init_probabilities(n):
  p = []
  for i in range(n):
    p = p + [1.0/n]
  return p

#robot sense color
def sense(p,Z):
  #sum for renormalizing
  s = 0

  q=p[:]
  #after sensing red:
  for i in range(len(p)):
    #check if world is Z at i'th location
    hit = (world[i] == Z)
    #calculate new probabilities
    q[i] = hit * q[i] * pHit + (1-hit) * q[i] * pMiss
    s = s + q[i]

  #renormalize probabilities
  for i in range(len(p)):
    q[i] = q[i] / s

  return q

#robot move, 1: move right 1
def move(p,U):
  q = p[:]
  n = len(p)
  #convolution, add probability for exact, undershooting, and overshooting for each position
  for i in range(n):
    q[i] = pExact*p[(i-U)%n] + pUndershoot*p[(i-U-1)%n] + pOvershoot*p[(i-U+1)%n]
  return q


#initial or 'prior' belief
#uniform distribution, maximum confusion, where are we??
p = init_probabilities(len(world))
#p = [0,1,0,0,0]
print p

for i in range(len(measurements)):

  #get 'posterior' sense belief
  p = sense(p,measurements[i])
  print 'After Sensing: ' + str(measurements[i])
  print ['%.2f' % x for x in p]

  p = move(p,movements[i])
  print 'After Moving: ' + str(movements[i])
  print ['%.2f' % x for x in p]
