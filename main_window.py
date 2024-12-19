import pygame
import numpy as np


from game_online import Game
from menu import Menu
from databases import Database_With_Users
from registration import Registration
from game_over import Game_Over
from game_win import Game_Win
import pygame_widgets
from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.textbox import TextBox
from pygame import K_1, K_2
from settings import Settings



pygame.init()
WINDOW_HEIGHT, WINDOW_WEIGHT = 1000, 1000
HOST, PORT = "localhost", 12200


class Main_Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WEIGHT))
        self.RUN = True
        pygame.display.set_caption('Bad Pix Battle')
        self.clock = pygame.time.Clock()

        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'avtorize_screen': (200, 100, 50),
            'border_colour': (0, 0, 0),
            'butttonsfon_colour_defaut': (255, 255, 255),
            'buttton_colour_defaut': (100, 100, 100),
            'buttton_colour_hover': (255, 255, 255),
            'buttton_colour_clicked': (255, 0, 0),

            'text_colours': (0, 0, 0),

        }
        self.widgets = np.array([])

        self.database_users = Database_With_Users()
        self.user = None

        #self.view_logo()
        pygame.mixer.music.load('music/music.mp3')
        pygame.mixer.music.play()
        self.listen_all()

    def view_logo(self):
        """
        Показ логотипа на 2 секунды
        """
        logo = pygame.image.load('ааав.jpeg')
        self.screen.fill((255, 255, 255))
        self.screen.blit(logo, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)


    def listen_all(self):
        self.list_active_surface = {'menu': Menu(self),
                                    'game': Game(self),
                                    'registration': Registration(self),
                                    'game_over': Game_Over(self),
                                    'game_win': Game_Win(self),
                                    'settings': Settings(self)}
        self.active_surface = 'registration'
        self.options_window_widget = np.array([])
        self.update_window = True

        while self.RUN:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.RUN = False
            self.key = pygame.key.get_pressed()
            if self.key[K_1]:
                self.restart_surface('game_over')
            if self.key[K_2]:
                self.restart_surface('game_win')
            if self.update_window:
                self.list_active_surface[self.active_surface].create_widgets()
                self.update_window = False
            self.list_active_surface[self.active_surface].listen()
            pygame_widgets.update(events)
            pygame.display.update()
            self.clock.tick(30)


    def restart_surface(self, name):
        del self.widgets
        self.widgets = np.array([])
        self.active_surface = name
        print(self.active_surface)
        self.update_window = True



    def log_in(self, login, passoword):
        if len(login) > 3 and len(passoword) > 3:
            if self.database_users.add_user("Новый пользователь", login, passoword):
                self.user = self.database_users.find_user(login, passoword)
                print(self.user)
                self.restart_surface('menu')


    def log_up(self, login, passoword):
        if len(login) > 8 and len(passoword) > 8:
            self.user = self.database_users.find_user(login, passoword)
            print(self.user)
            if self.user:
                self.restart_surface('menu')

    def rename_user(self, name):
        self.database_users.update_name_users(name, self.user[0])
        self.user = self.database_users.find_user(self.user[2], self.user[3])

    def music_on(self):
        pygame.mixer.music.unpause()

    def music_off(self):
        pygame.mixer.music.pause()


    def create_buttons(self, coords, size, shape, texts, funcs,
                       border=10, colour=False, colour1=False,  colour2=False, colour3=False):
        button_array = ButtonArray(
            self.screen,
            x=coords[0],
            y=coords[1],
            width=size[0],
            height=size[1],
            shape=shape,
            border=border,
            texts=texts,
            colour=colour if colour else self.colors['butttonsfon_colour_defaut'],
            inactiveColours=[colour1 if colour1 else self.colors['buttton_colour_defaut']] * len(texts),
            hoverColours=[colour2 if colour2 else self.colors['buttton_colour_hover']] * len(texts),
            pressedColours=[colour3 if colour3 else self.colors['buttton_colour_clicked']] * len(texts),
            onClicks=funcs
        )
        self.widgets = np.append(self.widgets, [button_array])


    def create_button(self, coords, size, text, r, func, colour=False, border_colour=False, colour1=False, colour2=False, colour3=False):
        print(colour, self.colors['buttton_colour_defaut'])
        button = Button(
            self.screen,
            x=coords[0],
            y=coords[1],
            width=size[0],
            height=size[1],
            text=text,
            fontSize=10,
            colour=colour if colour else self.colors['buttton_colour_defaut'],
            borderThickness=5,
            borderColour=border_colour if border_colour else self.colors['border_colour'],
            hoverColour=colour1 if colour1 else self.colors['buttton_colour_hover'],
            pressedColour=colour2 if colour3 else self.colors['buttton_colour_clicked'],
            radius=r,
            onClick=func)
        self.widgets = np.append(self.widgets, [button])

    def create_textbox(self, coords, size, border_colour=False, text_colour=False, r=10, bd=5):
        textbox = TextBox(
        self.screen,
        x=coords[0],
        y=coords[1],
        width=size[0],
        height=size[1],
        fontSize=50,
        borderColour=border_colour if border_colour else self.colors['border_colour'],
        textColour=text_colour if text_colour else self.colors['text_colours'],
        radius=r,
        borderThickness=bd)
        self.widgets = np.append(self.widgets, [textbox])

    def create_text(self, text, size, pos, color, background):
        f = pygame.font.SysFont('Century Gothic', size)
        text = f.render(text, 1, color)
        self.screen.blit(text, pos)
if __name__ == "__main__":
    Main_Window().__init__()