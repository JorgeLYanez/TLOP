import pygame
import sys
from settings import *
from level import Level

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 60)
        self.selected_option = 0

        # Cargar la imagen de la mona china
        self.monkey_image = pygame.image.load('graphics/monsters/raccoon/attack/image-removebg-preview_3_1.png')  
        self.monkey_rect = self.monkey_image.get_rect()
        self.monkey_image2 = pygame.image.load('graphics/font/fondoPayin.png')  
        self.monkey_rect2 = self.monkey_image.get_rect()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))  # Color de fondo del menú
        self.screen.blit(self.monkey_image, self.monkey_rect)
        self.screen.blit(self.monkey_image2, self.monkey_rect2)
        title_text = self.title_font.render("Main Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100))
        self.screen.blit(title_text, title_rect)

        options = ["Start Game", "Quit"]
        for i, option in enumerate(options):
            text = self.font.render(option, True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, HEIGTH // 2 + i * 50))
            if i == self.selected_option:
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 4)  # Resaltar la opción seleccionada
            self.screen.blit(text, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return True  # Iniciar juego
                    elif self.selected_option == 1:
                        pygame.quit()
                        sys.exit()

        return False  # No iniciar juego

    def run(self):
        while True:
            if self.handle_events():
                break
            self.draw_menu()
            pygame.display.update()
            self.clock.tick(FPS)

class Game:
    def __init__(self):
        # Configuración general
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('The Leyend of Payin')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.is_player_dead = False  # Variable para controlar si el jugador está muerto o no
        self.show_game_over = False

        # Sonido
        self.main_sound = pygame.mixer.Sound('./audio/main.ogg')
        self.main_sound.set_volume(0.5)

    def restart_game(self):
        # Reiniciar el juego y al jugador
        self.is_player_dead = False
        self.show_game_over = False
        self.level = Level()  # Crear una nueva instancia de Level para reiniciar el nivel

    def play_music(self):
        self.main_sound.play(loops=-1)

    def run(self):
        main_menu = MainMenu(self.screen)
        main_menu.run()

        self.play_music()  # Reproducir la música principal

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    elif event.key == pygame.K_RETURN:
                        if self.is_player_dead and self.show_game_over:
                            self.restart_game()
                            main_menu = MainMenu(self.screen)
                            main_menu.run()
                            self.play_music()  # Reproducir la música principal nuevamente

            if self.level.player.health <= 0:
                if not self.is_player_dead:
                    self.is_player_dead = True
                    self.show_game_over = True
                    self.main_sound.stop()  # Detener la música cuando el jugador muere

            if self.is_player_dead and self.show_game_over:
                self.screen.fill((0, 0, 0))  # Cambiar el color de fondo a negro

                # Mostrar "GAME OVER" en rojo en el centro de la pantalla
                font = pygame.font.Font(None, 100)
                text_surface = font.render("GAME OVER PRESS ENTER", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(text_surface, text_rect)

                # Verificar si se pulsa la tecla Enter para volver al menú principal
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.show_game_over = False
                    self.restart_game()  # Reiniciar el juego
                    main_menu = MainMenu(self.screen)
                    main_menu.run()
                    self.play_music()  # Reproducir la música principal nuevamente

            # Verificar si la experiencia del jugador es mayor a 5100
            if self.level.player.exp > 7000:
                self.is_player_dead = True
                self.show_game_over = True
                self.screen.fill((0, 0, 0))  # Cambiar el color de fondo a negro

                # Mostrar "YOU WIN!" en verde en el centro de la pantalla
                font = pygame.font.Font(None, 100)
                text_surface = font.render("YOU WIN!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(text_surface, text_rect)

                # Cargar la imagen que deseas mostrar después de ganar el juego
                win_image = pygame.image.load("./graphics/font/creditos.png")
                win_image_rect = win_image.get_rect(center=(WIDTH // 2, HEIGTH // 2))
                self.screen.blit(win_image, win_image_rect)

                pygame.display.update()
                pygame.time.delay(8000)  # Esperar 10 segundos antes de salir del juego
                pygame.quit()
                sys.exit()
            else:
                self.is_player_dead = False
                if not self.show_game_over:
                    self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
