import pygame, random

# ------------Ventana----------
width= 1000
height=650
# ------------Colores----------
negro= (0,0,0)
blanco=(255,255,255)
verde=(20,236,25)
rosado=(249,44,155)

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Juego de naves")

clock = pygame.time.Clock()

# ------------ Funcion para reaparicion naves enemigas ------------
def crear_nave(all_sprites,naves_list):
    nave = Enemigo()
    all_sprites.add(nave)
    naves_list.add(nave)
    
# ------------ Funcion para dibujar texto ----------
def draw_texto(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size) # Fuente texto
    text_surface = font.render(text, True, blanco) # Lugar donde se muestra el texto
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y) # Posicionar en x,y
    surface.blit(text_surface, text_rect) 

# ------------ Funcion para dibujar barra de vida ----------
def draw_vida(surface, x, y, porcentaje):
    bar_lenght = 150
    bar_height = 18
    fill = (porcentaje / 100) * bar_lenght 
    border=pygame.Rect(x,y, bar_lenght, bar_height)
    fill = pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surface,verde,fill)
    pygame.draw.rect(surface, rosado, border, 2)
    
# ------------Clase jugador ----------
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("img/nave.png").convert()
        self.image.set_colorkey(negro)  # Remover fondo negro
        self.rect= self.image.get_rect()
        self.rect.centerx = width // 2 
        self.rect.bottom = height -10
        self.speed_x = 0  # Velocidad horizontal
        self.speed_y=0
        self.lives = 100
        
    def update(self):
        self.speed_x=0
        self.speed_y=0
        keystate= pygame.key.get_pressed()   # Comprobar si alguna tecla fue pulsada
        
        if keystate[pygame.K_LEFT]:
            self.speed_x= -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x= 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
            
        # Actualizar la posición del jugador
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Limitar el movimiento del jugador hacia arriba
        if self.rect.top < height // 2:
            self.rect.top = height // 2
            self.speed_y = 0  # Detener el movimiento hacia arriba
            
        # Limitar el movimiento del jugador hacia abajo
        if self.rect.bottom + self.rect.height // 4 >  height:
            self.rect.bottom = height  - self.rect.height // 4
            
        # Comprobar que la nave no sobrepase la pantalla por la derecha
        if self.rect.right > width:
            self.rect.right= width 
        # Comprobar que la nave no sobrepase la pantalla por la izquierda
        if self.rect.left < 0:
            self.rect.left= 0             

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  # Crear laser, parametro-> posicion
        all_sprites.add(bullet)
        bullets.add(bullet)
        sonido_laser.play()

# ------------ Clase enemigo ----------
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Seleccionar las naves enemigas aleatoriamente de la lista naves_imagenes
        self.image = random.choice(naves_imagenes)
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(width - self.rect.width)   # Valor inicial aleatorio rango de la ventana
        self.rect.y= random.randrange(-100,-40)  # Efecto de caida
        self.speed_y = random.randrange(1, 10)   # Velocidad de enemigos aleatorio
        self.speed_x = random.randrange(-5, 5)   # Movimiento vertical
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Verificar si sobrepasa la ventana
        if (self.rect.top > height + 10) or (self.rect.left < -25) or (self.rect.right > width + 25):
            # Reestablecer elementos
            self.rect.x = random.randrange(width - self.rect.width)   
            self.rect.y= random.randrange(-100,-40)  
            self.speed_y = random.randrange(1, 10) 
    
# ------------ Clase laser o disparo ----------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Inicializar la superclase
        self.image = pygame.image.load("img/laser.png")
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.y= y
        self.rect.x = x
        self.rect.centerx = x
        self.speed_y= -10 # Velocidad del objeto, empezando desde abajo
        
    def update(self):
        self.rect.y += self.speed_y
        # Eliminar las balas cuando sobrepase la ventana
        if self.rect.bottom < 0:
            self.kill()
          
# ------------ Clase explosion ----------      
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = expl_an[0]
        self.rect = self.image.get_rect()
        self.rect.center= center
        self.frame = 0
        
        # Controlar velocidad de imagen
        self.last_update= pygame.time.get_ticks()
        self.frame_rate= 60
        
    def update(self):
        actual = pygame.time.get_ticks()  # Conocer el tiempo transcurrido
        if actual - self.last_update > self.frame_rate:
            self.last_update = actual
            self.frame += 1  # Recorrer los elementos de la lista
            
            if self.frame == len(expl_an): 
                self.kill()
            else:
               center = self.rect.center 
               self.image=expl_an[self.frame]
               self.rect = self.image.get_rect()  # Marco de la imagen
               self.rect.center = center
       
# ------------ Funcion para mostrar pantalla de game over ----------   
def show_screen_gameover():
    screen.blit(background,[0,0])
    draw_texto(screen, "GAME OVER", 65, width // 2, height // 3)
    draw_texto(screen, "Puntaje final: "+str(score), 55, width // 2, height * (7/16))
    
    draw_texto(screen,"REINTENTAR", 35, width // 2, height *(9/16))
    draw_texto(screen, "Presiona la tecla L para empezar",25, width//2, height * (10/16))  
    
    draw_texto(screen,"FINALIZAR", 35, width // 2, height *(12/16))
    draw_texto(screen, "Presiona la tecla R para finalizar",25, width//2, height * (13/16))  
    pygame.display.flip()
    
    esperando= True
    while esperando:
        clock.tick(60)
        # Verificar si el jugador quiere cerrar la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_l]:
            esperando=False
            
        if tecla[pygame.K_r]:
            quit()
                    
# ------------ Funcion para mostrar pantalla de inicio ----------  
def show_screen_inicio():
    screen.blit(background,[0,0])
    draw_texto(screen, "JUEGO DE NAVES", 65, width // 2, height // 4)
    draw_texto(screen,"Desplázate con las flechas, dispara con la tecla", 40, width // 2, height *(4/9))
    draw_texto(screen,"espaciadora y evita a los enemigos", 40, width // 2, height *(5/9))
    draw_texto(screen, "Presiona la tecla L para empezar",30, width//2, height * (7/9))  
    pygame.display.flip()
    
    esperando= True
    while esperando:
        clock.tick(60)
        # Verificar si el jugador quiere cerrar la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_l]:
            esperando=False
        
# ------------ Seleccionar naves enemigas ----------
naves_imagenes=[]
rutas=["img/e1.png", "img/e2.png", "img/e3.png"]

for img in rutas:
    naves_imagenes.append(pygame.image.load(img).convert())   # Iterar en cada valor de las imagenes en la lista rutas

# ------------Cargar imagen de fondo ----------
background = pygame.image.load("img/fondo.png").convert()

# ------------Cargar imgagen de explosion ----------
expl_an=[]
for i in range(4):
    archivo="img/expl0{}.png".format(i)
    expl_img = pygame.image.load(archivo).convert()
    expl_img.set_colorkey(negro)
    expl_scale= pygame.transform.scale(expl_img,(70,70))
    expl_an.append(expl_scale)

# ------------Cargar sonidos ----------
sonido_laser= pygame.mixer.Sound("img/laser.ogg")
sonido_explosion= pygame.mixer.Sound("img/explosion.wav")
pygame.mixer.music.load("img/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.2) # Modular volumen

# ------------ Implementar game over ----------
game_over=True
inicio=True
game=True

pygame.mixer.music.play(loops =-1)  # Repite infinitamente

while game:
    if inicio:
        show_screen_inicio()
        inicio=False
        game_over=False
        # ------------ Creacion listas ----------
        all_sprites=pygame.sprite.Group()
        naves_list = pygame.sprite.Group()  # Almecenamiento naves
        bullets= pygame.sprite.Group() # Almecenamiento disparos
        player = Jugador()
        all_sprites.add(player)

        for i in range(5):
            crear_nave(all_sprites,naves_list)
            
        score=0   # Inicializar marcador
        
    elif game_over:
        # ------------ Pantalla de game over  ------------
        show_screen_gameover()
        game_over= False
        all_sprites=pygame.sprite.Group()
        naves_list = pygame.sprite.Group()  # Almecenamiento naves
        bullets= pygame.sprite.Group( ) # Almecenamiento disparos
        player = Jugador()
        all_sprites.add(player)

        for i in range(5):
            crear_nave(all_sprites,naves_list)
            
        score=0   # Reiniciar marcador
        

    clock.tick(60)   # Establecer reloj a 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game=False

        # ------------ Disparar al presionar la tecla espaciadora ------------
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                player.shoot()
            
    all_sprites.update()
    
    # ------------ Detectar colisiones (naves/laser) ----------
    colision = pygame.sprite.groupcollide(naves_list, bullets, True, True)  # Colisiones del grupo naves y grupo laser
    for n in colision:
        score +=1
        sonido_explosion.play()   # Sonido de explosion 
        
        explosion=Explosion(n.rect.center)
        all_sprites.add(explosion)
        
        # Reaparicion naves enemigas
        crear_nave(all_sprites,naves_list)
    
    # ------------ Detectar colisiones (Jugador/naves) ----------
    colision= pygame.sprite.spritecollide(player, naves_list, True)  # True -> Desaparecen los objetos que chocan
    if colision:
        # Por cada colision, disminuye nivel de vida
        player.lives -= 10
        # Reaparicion naves enemigas
        crear_nave(all_sprites,naves_list)
        
        if player.lives <=0:
            game_over= True   # Pierde todas las vidas      
            
    screen.blit(background, [0,0])
    all_sprites.draw(screen)  # Dibujar en pantalla
    
    # Dibujar puntaje en pantalla
    draw_texto(screen, str(score), 42, 900, 15)  
    # Dibujar vida en pantalla
    draw_vida(screen, 5, 5, player.lives)
    
    pygame.display.flip()
    
pygame.quit()