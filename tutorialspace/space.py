import pygame
import random
import math

#Inicializando o pygame e criando a janela com titulo e icone
pygame.init() #inicializa o pygame
screen=pygame.display.set_mode([800,600]) #cria uma janela com as dimensoes especificadas, para nos referimos a ela usaremos a variavel screen
pygame.display.set_caption("Space Invaders") #cria o titulo
icon=pygame.image.load("space/ufo.png") #define o icone
pygame.display.set_icon(icon)

#Imagem de fundo
background=pygame.image.load('space/background.png')

# Jogador
playerImg=pygame.image.load('space/player.png') #carrega a imagem e salva na variavel playerImg
playerX=370 #x inicial
playerY=480
playerX_change=0 #variavel que usaremos para dar movimento a nave

# Inimigo
enemyImg=pygame.image.load('space/enemy1.png')
enemyX=random.randint(0,700) #nasce em um lugar aleatorio
enemyY=random.randint(50,150)
enemyX_change=2 # o inimigo ja comeca se movimentando , nao espera input do teclado
enemyY_change=40 # sempre que atingir uma borda, o inimigo se move para baixo

# Bala
# estado ready - a bala acertou alguem , ou chegou ao limite superior da tela (podemos atirar denovo)
# estado fire - uma bala foi atirada
bulletImg=pygame.image.load('space/bullet.png')
bulletX=0 #so declaramos a variavel, o valor X será igual ao da nave quando atirou
bulletY=480
bulletY_change=6 # velocidade da bala
bullet_state='ready'

score=0

def player(x,y):
    screen.blit(playerImg,(x,y)) #desenha a imagem do player na tela

def enemy(x,y):
    screen.blit(enemyImg,(x,y)) #desenha o inimigo

def fire_bullet(x,y):
    global bullet_state # acessa a variavel global bullet_state
    bullet_state= 'fire'
    screen.blit(bulletImg,(x+16,y+10)) # esses valores são para centralizar a bala

def isCollision(enemyX,enemyY,bulletX,bulletY): #funcao para detectar colisao entre inimigo e bala
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

gameLoop=True # Variavel booleana para deixar o jogo rodando
while gameLoop:
    screen.fill([0,0,0]) #preenche a tela com alguma cor
    screen.blit(background,(0,0)) #preenche a tela com a imagem de fundo
    for event in pygame.event.get(): # Aqui iremos ver os eventos que estão acontecendo
        if event.type == pygame.QUIT: # Se clicarmos no botao de fechar
            gameLoop=False
        if event.type == pygame.KEYDOWN: # se alguma tecla foi pressionada (keyup = soltar tecla)
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change= 2
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bulletX=playerX
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP: # se deixarmos de pressionar as setas do teclado , a nave para de se mexer
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0

    playerX+= playerX_change #atualiza o valor da coordenada x do jogador , pode ter ficado parado ou se movimentado
    if playerX <= 0: # Para nao sair dos limites da janela do jogo
        playerX=0
    elif playerX >= 736:
        playerX=736

    enemyX+= enemyX_change #atualiza o valor da coordenada x do inimigo
    if enemyX <= 0:
        enemyX_change=2 #Quando chegar ao limite da esquerda da tela, definir a movimentacao para a direita, e vice versa
        enemyY+= enemyY_change
    elif enemyX >= 736:
        enemyX_change=-2
        enemyY+= enemyY_change
    # movimento da bala
    if bulletY <=0: #se a bala sair da tela , podemos atirar denovo
        bulletY=480
        bullet_state='ready'
    if bullet_state == 'fire': #enquanto estiver no estado 'fire', a bala vai se movendo para cima
        fire_bullet(bulletX,bulletY) #desenha a bala continuamente
        bulletY -= bulletY_change 

    #colisao da bala com inimigo
    collision = isCollision(enemyX,enemyY,bulletX,bulletY)
    if collision:
        bulletY=480
        bullet_state='ready'
        score+=1
        print(score)
        enemyX=random.randint(0,700)
        enemyY=random.randint(50,150)

    player(playerX,playerY) #desenha continuamente o player e o inimigo
    enemy(enemyX,enemyY)
    pygame.display.update() #mantem a janela do jogo aberta
