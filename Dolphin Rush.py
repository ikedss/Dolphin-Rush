from os import system, name as OSname
from getkey import getkey, keys
from threading import Thread
from random import randint
from cursor import hide, show
from sys import stdout
from time import sleep

aceleracao = [0.20, 0.16, 0.12, 0.10, 0.08, 0.05]
vida = 5
IMG_golfinho = "🐬"
IMG_obstaculo = "🌑"
IMG_vida = "❤️"
IMG_dano = "💔"
IMG_PlanoDeFundo = " "

hide()
y, x = -6, 2
pontuacao, espaco, nivel = 0, 0, 0
running = True
order = "null"
comprimento = 45
largura = 11

mapa = [[IMG_PlanoDeFundo] * comprimento for _ in range(largura)]
mapa[y][x] = IMG_golfinho

def clear(t = 0):
  sleep(t)
  system('cls' if OSname == 'nt' else 'clear')

def printt(string, delay = 0.005):
  for character in string:
    stdout.write(character)
    stdout.flush()
    sleep(delay)
  print()

def display():
  print("\033[H", end = "")
  print((IMG_vida + " ") * vida, "")
  for row in mapa:
    print(" ".join(map(str,row[0:-5])))

def scroll():
  global pontuacao, espaco, nivel
  mapa[y][x] = IMG_PlanoDeFundo
  for row in mapa:
    if row[2] in IMG_obstaculo:
      pontuacao += 1
    del row[0]
    row.append(IMG_PlanoDeFundo)
  if pontuacao < 1:
    if espaco <= 0:
      mapa[y][-1] = IMG_obstaculo[0]
      espaco = 7
  elif pontuacao < 8:
    if espaco <= 0:
      mapa[y][-1] = IMG_obstaculo[0]
      mapa[y][-2] = IMG_obstaculo[0]
      espaco = 7
    nivel = 1
  elif pontuacao < 80:
    if espaco <= 0:
      mapa[y][-1] = IMG_obstaculo[0]
      mapa[y][-2] = IMG_obstaculo[0]
      mapa[y][-3] = IMG_obstaculo[0]
      espaco = 7
      PosBloco = randint(3,9)
      mapa[PosBloco-1][-3] = IMG_obstaculo[0]
      mapa[PosBloco][-1] = IMG_obstaculo[0]
      mapa[PosBloco+1][-3] = IMG_obstaculo[0]
    nivel = 2
  elif pontuacao < 200:
    if espaco <= 0:
      mapa[y][-1] = IMG_obstaculo[0]
      mapa[y][-2] = IMG_obstaculo[0]
      mapa[y][-3] = IMG_obstaculo[0]
      espaco = 7
      PosBloco = randint(3,9)
      mapa[PosBloco-2][-1] = IMG_obstaculo[0]
      mapa[PosBloco][-2] = IMG_obstaculo[0]
      mapa[PosBloco+1][-1] = IMG_obstaculo[0]
      mapa[PosBloco+1][+1] = IMG_obstaculo[0]
      if y < -6:
        mapa[0][-1] = IMG_obstaculo[0]
        mapa[1][-1] = IMG_obstaculo[0]
      if y > -6:
        mapa[-1][-1] = IMG_obstaculo[0]
        mapa[-2][-1] = IMG_obstaculo[0]
    nivel = 3
  else:
    if espaco <= 0:
      mapa[y][-2] = IMG_obstaculo[0]
      mapa[y][-2] = IMG_obstaculo[0]
      mapa[y][-3] = IMG_obstaculo[0]
      mapa[y][-3] = IMG_obstaculo[0]
      espaco = 7
      PosBloco = randint(3,6)
      mapa[PosBloco-2][-1] = IMG_obstaculo[0]
      mapa[PosBloco-1][-2] = IMG_obstaculo[0]
      mapa[PosBloco][-1] = IMG_obstaculo[0]
      mapa[PosBloco+1][-2] = IMG_obstaculo[0]
      mapa[PosBloco+2][-1] = IMG_obstaculo[0]
      if y < -6:
        mapa[0][-1] = IMG_obstaculo[0]
        mapa[1][-1] = IMG_obstaculo[0]
      if y > -6:
        mapa[-1][+1] = IMG_obstaculo[0]
        mapa[-2][+1] = IMG_obstaculo[0]
    nivel = 4
  espaco += -1

def death():
  global vida, running
  vida += -1
  mapa[y][x] = IMG_dano
  display()
  if vida <= 0:
    running = False

def update():
  global y, pontuacao, order
  if order == "up":
    order = "null"
    y -= 1
  if order == "down":
    order = "null"
    y -= -1
  if y >= 0:
    y -= 1
  try:
    if mapa[y][x] in IMG_obstaculo:
      mapa[y][x] = IMG_PlanoDeFundo
      death()
    else:
      mapa[y][x] = IMG_golfinho
      display()
  except: y -= -1

def keypress(key):
  global order
  if key == keys.UP or key == "w": order = "up"
  if key == keys.DOWN or key == "s": order = "down"

class KeyboardThread(Thread):
    def __init__(self, input_cbk = None, name = 'keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name = name)
        self.start()

    def run(self):
        while running:
            self.input_cbk(getkey())

def run():
  while running:
    scroll()
    update()
    sleep(aceleracao[nivel])
  
  death()
  if pontuacao < 30:
    print("você passou por", pontuacao, "obstáculos... decepcionante (ಠ_ಠ)")
  elif pontuacao < 200:
    print("você passou por", pontuacao, "obstáculos, parabéns(/◕ヮ◕)/")
  else:
    print("você passou por", pontuacao, "obstáculos, nice (▀̿̿Ĺ̯̿▀̿ ̿)")

printt("Use as setas ᐱ e ᐯ para se movimentar", 0.02)
clear(1)

kthread = KeyboardThread(keypress)
run()

while True:
  show()
  awn = input("se quiser recomeçar precione enter\n").lower()
  hide()
  clear()
  if awn == "y" or awn == "yes" or awn == "":
    clear()
    y, x = -6, 2
    pontuacao = 0
    vida = 5
    running = True
    kthread = KeyboardThread(keypress)
    run()
  else:
    break
    show()