#Visualizing a robot localizing itself in a 1 dimensional world.
#todo:
#expand changeWorld for all tiles
#clean up comments
#use text to label buttons


import pygame

p = [0,1,0,0,0,0,0,0,0,0]
world = ['g','r','g','r','g','g','g','r','g','g']

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

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gray = (120,120,120)

# screen size [width,height]
size=[1000,600]
screen=pygame.display.set_mode(size)


running = True
clock=pygame.time.Clock()

def changeWorld(x):
  if x<100:
    if world[0]=='r':
      world[0]='g'
    else:
      world[0]='r'

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


def updatePD(x):
  global p
  if x < 200:
    p = sense(p,'g')
  elif x >= 200 and x < 400:
    p = sense(p,'r')
  elif x >= 600 and x < 800:
    p = move(p,-1)
  elif x >=800:
    p = move(p,1)

def getCommand():
  global running
  wait = True
  while wait:
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT: # If user clicked close
        wait = False
        running=False # Flag that we are done so we exit this loop
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        wait = False
        if y<100:
          changeWorld(x)
        elif y>400:
          updatePD(x)

#show world
def colorWorld():
  for i in range(len(world)):
    #pygame.draw.rect(screen,color,[x,y,sizex,sizey],border_width)a
    if world[i] == 'r':
      pygame.draw.rect(screen,red,[i*100,0,97,100],0)
    else:
      pygame.draw.rect(screen,green,[i*100,0,97,100],0)

#show robot's probability distribution
def colorPD():
  global p
  for i in range(len(p)):
    #make height scale according to probability
    height = p[i]*300
    pygame.draw.rect(screen,white,[i*100,100+(300-height),97,height],0)

def showButtons():
  #sense buttons
  pygame.draw.rect(screen,green,[0,400,197,200],0)
  pygame.draw.rect(screen,red,[200,400,197,200],0)
  #do nothing
  pygame.draw.rect(screen,gray,[400,400,197,200],0)
  #move buttons
  pygame.draw.rect(screen,blue,[600,400,197,200],0)
  pygame.draw.rect(screen,blue,[800,400,197,200],0)

def startLocalization():
  global running
  while running:
    screen.fill(black)
    colorWorld()
    colorPD()
    showButtons()

    pygame.display.flip()
    clock.tick(60)

    getCommand()


def main():
    pygame.init()
    pygame.display.set_caption("1d Robot Localization")

    startLocalization()

    pygame.quit ()

if __name__ == "__main__":
    main()
