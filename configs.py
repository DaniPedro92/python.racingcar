import pygame
pygame.init()

class window:
    WIDTH = 1000
    HEIGHT = 1000
    TITLE = "Racing Car"
    ICON = pygame.image.load("imgs/flag.ico")
   
class img:
    GRASS = None
    BACKGROUND = None
    TRACK = None
    FINISH = None
    FINISH_RESIZE = None
    FINISH_MASK = None
    FINISH_IMAGE = None
    MY_CAR = None
    CPU_CAR = None
    BARRIER = None
    BARRIER_MASK = None
    OIL = None
    OIL_MASK = None
    BOOST = None
    BOOST_MASK = None
    TRACK_BORDER = None
    TRACK_BORDER_MASK = None
    TRACK_ROAD = None
    PIT_STOP = None
    PIT_STOP_MASK = None
    MENU_OUT_GAME = None
    MENU_IN_GAME = None
    CHECKPOINT = None
    CHECKPOINT_MASK = None
    lights_images = [
        "lights1.png",
        "lights2.png",
        "lights3.png",
        "lights4.png",
        "lights5.png",
        "lights6.png"
    ]
    VICTORY = None
    LOSER = None
    START = None
    EXIT = None
    PAUSE = None

    @classmethod
    def load_images(cls):
        cls.GRASS = pygame.image.load("imgs/background_grass.jpg").convert()
        cls.BACKGROUND = pygame.image.load("imgs/background_menu.jpg").convert_alpha()
        cls.TRACK = pygame.image.load("imgs/track.png").convert_alpha()
        cls.FINISH = pygame.image.load("imgs/finish.png").convert()
        cls.FINISH_RESIZE = pygame.transform.scale(cls.FINISH, (82, 20)).convert()
        cls.FINISH_MASK = pygame.mask.from_surface(cls.FINISH_RESIZE)
        cls.FINISH_IMAGE = pygame.image.load("imgs/finish_image.png").convert_alpha()
        cls.MY_CAR = pygame.image.load("imgs/mycar (2).png").convert_alpha()
        cls.CPU_CAR = pygame.image.load("imgs/racing_car.png").convert_alpha()
        cls.BARRIER = pygame.image.load("imgs/barrier.png").convert()
        cls.BARRIER_MASK = pygame.mask.from_surface(cls.BARRIER)
        cls.OIL = pygame.image.load("imgs/oil.png").convert_alpha()
        cls.OIL_MASK = pygame.mask.from_surface(cls.OIL)
        cls.BOOST = pygame.image.load("imgs/boost.png").convert_alpha()
        cls.BOOST_MASK = pygame.mask.from_surface(cls.BOOST)
        cls.TRACK_BORDER = pygame.image.load("imgs/track_margens.png").convert_alpha()
        cls.TRACK_BORDER_MASK = pygame.mask.from_surface(cls.TRACK_BORDER)
        cls.PIT_STOP = pygame.image.load("imgs/pitstop.png").convert_alpha()
        cls.PIT_STOP_MASK = pygame.mask.from_surface(cls.PIT_STOP)
        cls.TRACK_ROAD = pygame.image.load("imgs/track_road.png").convert()
        cls.MENU_OUT_GAME = pygame.image.load("imgs/menu.png").convert()
        cls.MENU_IN_GAME = pygame.image.load("imgs/menu_in_game.png").convert()
        cls.CHECKPOINT = pygame.image.load("imgs/checkpoint.jpg").convert_alpha()
        cls.CHECKPOINT_MASK = pygame.mask.from_surface(cls.CHECKPOINT)
        cls.LIGHTS_SURFACES = []
        for image_name in cls.lights_images:
            light_img = pygame.image.load(f"imgs/{image_name}").convert_alpha()
            cls.LIGHTS_SURFACES.append(light_img)
        cls.LOSER = pygame.image.load("imgs/loser.jpg").convert_alpha()
        cls.VICTORY = pygame.image.load("imgs/victory.jpg").convert_alpha()
        cls.START = pygame.image.load("imgs/start.png").convert_alpha()
        cls.EXIT = pygame.image.load("imgs/exit.png").convert_alpha()
        cls.PAUSE = pygame.image.load("imgs/pause.png").convert_alpha

    
class sound:
    STARTING_LIGHTS = pygame.mixer.Sound("sounds/startinglights_sound.mp3")
    INTRO = pygame.mixer.Sound("sounds/formula-1-theme-song.mp3")
    MUSIC_VOLUME = 1
    SOUND_VOLUME = 1
    



