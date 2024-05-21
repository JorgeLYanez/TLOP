import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Configuración general
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('The Leyend of Payin')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.is_player_dead = False  # Variable para controlar si el jugador está muerto o no

        # Sonido
        self.main_sound = pygame.mixer.Sound('./audio/main.ogg')
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

    def restart_game(self):
        # Reiniciar el juego y al jugador
        self.is_player_dead = False
        self.level = Level()  # Crear una nueva instancia de Level para reiniciar el nivel

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    elif event.key == pygame.K_RETURN:  # Verificar si se presionó la tecla "Enter"
                        if self.is_player_dead:
                            self.restart_game()


            if self.level.player.health <= 0:
                if not self.is_player_dead:
                    self.is_player_dead = True
                    self.screen.fill((0, 0, 0))  # Cambiar el color de fondo a negro

                # Mostrar "GAME OVER" en rojo en el centro de la pantalla
                font = pygame.font.Font(None, 100)
                text_surface = font.render("GAME OVER", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(text_surface, text_rect)

                # Detener la música cuando el jugador muere
                self.main_sound.stop()
                    
            # Verificar si la experiencia del jugador es mayor a 7000
            if self.level.player.exp > 7000:
                self.screen.fill((0, 0, 0))  # Cambiar el color de fondo a negro
                font = pygame.font.Font(None, 100)
                text_surface = font.render("YOU WIN!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(text_surface, text_rect)

                # Cargar la imagen que deseas mostrar después de ganar el juego
                win_image = pygame.image.load("./graphics/font/creditos.png")
                win_image_rect = win_image.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(win_image, win_image_rect)

                pygame.display.update()
                pygame.time.delay(8000)  # Esperar 3 segundos antes de salir del juego
                pygame.quit()
                sys.exit()
            else:
                self.is_player_dead = False
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
