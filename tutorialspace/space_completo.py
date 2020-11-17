import pygame
from pygame import mixer
import random
import math


#Inicializando o pygame e criando a janela com titulo e icone
pygame.init() #inicializa o pygame
screen=pygame.display.set_mode([800,600]) #cria uma janela com as dimensoes especificadas, para nos referimos a ela usaremos a variavel screen
pygame.display.set_caption("Space Invaders") #cria o titulo
icon=pygame.image.load("space/ufo.png") #define o icone, guarda na variavel icon
pygame.display.set_icon(icon) 

#Guarda dados da Imagem de fundo
background=pygame.image.load('space/background.png')

#Musica de fundo
mixer.music.load('space/background.wav')
mixer.music.play(-1) #-1 : toca em loop


# Cria dados do Jogador
playerImg=pygame.image.load('space/player.png') #carrega a imagem e salva na variavel playerImg
playerX=370 #x inicial
playerY=480 #y inicial
playerX_change=0 #variavel que usaremos para dar movimento a nave

# Cria dados dos inimigos. Como sao varios , iremos armazenar em uma lista
enemyImg=[] #dados das imagens
enemyX=[] 
enemyY=[]
enemyX_change=[] #iremos dar movimento aos inimigos em x e y
enemyY_change=[]
num_enemies=6 #numero de inimigos
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('space/enemy1.png'))
    enemyX.append(random.randint(0,700)) #nasce em um lugar aleatorio
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2) # o inimigo ja comeca se movimentando , nao espera input do teclado
    enemyY_change.append(40) # sempre que atingir uma borda, o inimigo se move para baixo

# Dados da Bala
# estado ready - a bala acertou alguem , ou chegou ao limite superior da tela (podemos atirar denovo)
# estado fire - uma bala foi atirada
bulletImg=pygame.image.load('space/bullet.png')
bulletX=0 #so declaramos a variavel, o valor X será igual ao da nave quando atirou
bulletY=480
bulletY_change=6 # velocidade da bala
bullet_state='ready'

#Pontuacao
score_value=0
font=pygame.font.Font('freesansbold.ttf',32) #carrega fonte e salva na variavel 'font' , freesansbold é uma fonte padrao, podemos mudar
textX=10
textY=10

#Texto de game over
over_font=pygame.font.Font('freesansbold.ttf',64)

# Funcoes para desenhar os objetos que queremos  .blit = desenha a imagem

def player(x,y):
    screen.blit(playerImg,(x,y)) #desenha a imagem do player na tela

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y)) #desenha o inimigo indice i

def fire_bullet(x,y):
    global bullet_state # acessa a variavel global (fora da funcao) bullet_state
    bullet_state= 'fire'
    screen.blit(bulletImg,(x+16,y+10)) # esses valores são para centralizar a bala

# Outras funcionalidades

def isCollision(enemyX,enemyY,bulletX,bulletY):  #funcao para detectar colisoes
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score=font.render("Score : " + str(score_value),True,(255,255,255)) #renderiza o texto com a fonte 'font' e guarda na variavel score ; 2 argumento: Se for True vai 'suavizar'
    screen.blit(score, (x,y))

def game_over_text():
    over_text=over_font.render('GAME OVER',True,(255,0,255))
    screen.blit(over_text,(200,250))


# Ambiente de jogo
gameLoop=True 
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
            if event.key == pygame.K_SPACE and bullet_state == 'ready': #se apertarmos espaco , e se pudermos atirar no momento
                bullet_Sound=mixer.Sound('space/laser.wav')
                bullet_Sound.play()
                bulletX=playerX
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP: # se deixarmos de pressionar as setas do teclado , a nave para de se mexer
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0
    
    #Movimento do jogador
    playerX+= playerX_change #atualiza o valor da coordenada x do jogador , pode ter ficado parado ou se movimentado
    if playerX <= 0: # Para nao sair dos limites da janela do jogo
        playerX=0
    elif playerX >= 736:
        playerX=736
    
    #Movimento dos inimigos e verificar colisão
    for i in range(num_enemies): # para cada inimigo
        #Condicao de Game over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i]+= enemyX_change[i] #atualiza o valor da coordenada x do inimigo
        if enemyX[i] <= 0:
            enemyX_change[i]=2 #Quando chegar ao limite da esquerda da tela, definir a movimentacao para a direita, e vice versa
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]=-2
            enemyY[i]+= enemyY_change[i]
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY) # verifica colisao da bala com inimigo
        if collision:
            explosion_Sound=mixer.Sound('space/explosion.wav')
            explosion_Sound.play()
            bulletY=480
            bullet_state='ready'
            score_value+=1
            enemyX[i]=random.randint(0,700)
            enemyY[i]=random.randint(50,150) 
        enemy(enemyX[i],enemyY[i],i) # a cada iteracao do while, desenha o inimigo 
   
   # movimento da bala
    if bulletY <=0: #se a bala sair da tela , podemos atirar denovo
        bulletY=480
        bullet_state='ready'
    if bullet_state == 'fire': #enquanto estiver no estado 'fire', a bala vai se movendo para cima
        fire_bullet(bulletX,bulletY) #desenha a bala continuamente
        bulletY -= bulletY_change 
    
    player(playerX,playerY) #a cada iteracao do while,desenha o player
    show_score(textX,textY) #mostra o score
    pygame.display.update() #mantem a janela do jogo aberta
