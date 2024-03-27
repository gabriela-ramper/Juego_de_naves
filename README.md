# Juego de naves
Juego de naves en python, implementando la librería PyGame

Este es un juego desarrollado en python que implementa la librería Pygame. El juego presenta la mecánica de desplazar una nave (jugador) en la ventana, además, deberá esquivar enemigos y disparar láseres. El objetivo del juego es derrotar a la mayor cantidad de naves enemigas y mantenerse con vida el mayor tiempo posible.

## Funcionalidades del juego
El juego presenta la siguiente serie de funciones:
- Controlar una nave, moviendola con las flechas del teclado.
- Disparar láseres al presionar la tecla espaciadora, para destruir las naves enemigas e incrementar el puntaje actual.
- Mantener la nave con vida el mayor tiempo posible. Al impactar con una nave enemiga, la barra de vida disminuirá en 20 puntos, desde 100 hasta llegar a 0. El jugador cuenta con cinco vidas en cada ronda.
- El juego finaliza cuando el jugador pierda todas las vidas o decide finalizar el juego cerrando la ventana.
- Para empezar o reiniciar el juego, el jugador debe presionar la tecla L.
- En la pantalla de game over, al presionar la tecla R o cerrar la ventana, se finaliza el juego.


## Instalación y ejecución
1. Instalar la librería Pygame en el entorno de python. Si ya cuenta con esta librería, omitir este paso.

`pip install pygame`

2. Descargar el código fuente del repositorio.
3. Ejecutar el scrip para iniciar el juego.

## Recursos
- Imagenes de naves, explosiones y fondo: [PNGWING](https://www.pngwing.com/es "PNGWING")
- Música de fondo: [Pixabay](https://pixabay.com/es/music/search/suspenso/?theme=m%25C3%25BAsica%2520para%2520videos "Pixabay")
  
## Referencias bibliografícas
Para el desarrollo de este juego, se utilizaron las siguientes guías:
- Lista de reproducción de YouTube: [Curso de pygame #2: Shooter](https://youtube.com/playlist?list=PLuB3bC9rWQAuzlz932pjjFLE1q8caF21N&si=ftRtJr7gHfw0GhRE "Curso de pygame #2: Shooter")
- Pantallas de Inicio y Fin: [PyGame - Video 17](https://www.youtube.com/watch?v=XeY_bKs3v00 "PyGame - Video 17")
