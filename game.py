#!/usr/bin/python3

"""
Basic PyGame setup
"""

# Get access to relevant libraries
import sys, pygame, random

# Start PyGame
pygame.init()
pygame.display.set_caption("Advanced PyGame example")

# Define globals
width  = 1024
height = 768
size   = width, height
black  = 0, 0, 0
font   = pygame.font.Font(None, 128)

# Image loading function
def load_image(filename: str) -> pygame.Surface:
    surface = pygame.image.load(filename).convert()
    return surface

# Any (possibly animated) graphic
class Prop:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.rect = surface.get_rect()

    def update(self):
        pass

    def blit(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)

class BackgroundProp(Prop):
    def __init__(self, size: float):
        # Make the surface
        surface = pygame.Surface(size).convert()
        surface.fill(black)
        
        # Set up text
        text = font.render("Hello Python!", 1, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = surface.get_rect().centerx

        # Draw it on the background surface
        surface.blit(text, text_rect)

        # Call the super class constructor
        super().__init__(surface)

    def update(self):
        # Change the text color
        text = font.render("Hello Python", 1,
                           (random.randrange(255),
                            random.randrange(255),
                            random.randrange(255)))
        text_rect = text.get_rect()
        text_rect.centerx = self.surface.get_rect().centerx
        self.surface.blit(text, text_rect)
    
# Complex objects
class Actor:
    def __init__(self, prop: Prop):
        self.prop = prop

    def update(self):
        pass

    def blit(self, screen: pygame.Surface):
        self.prop.blit(screen)

# Moving object
class MovingActor(Actor):
    def __init__(self, prop: Prop, speed: list):
        # Call the super class constructor
        super().__init__(prop)
        self.speed = speed

    def update(self):
        self.prop.rect = self.prop.rect.move(self.speed)

        if self.prop.rect.left < 0 or \
           self.prop.rect.right > size[0]:
            self.speed[0] = -self.speed[0]

        if self.prop.rect.top < 0 or \
           self.prop.rect.bottom > size[1]:
            self.speed[1] = -self.speed[1]
        
# Base game logic
class Game:    
    def __init__(self):
        # Set some parameters
        self.screen = pygame.display.set_mode(size)
        self.props  = {}
        self.actors = {}
        
        # Make a background prop
        self.props["background"] = BackgroundProp(size)
        
        # Create actors
        self.actors["arthur"]       = MovingActor(Prop(load_image("arthur.jpg")), [1, 1])
        self.actors["black_knight"] = MovingActor(Prop(load_image("black_knight.jpg")), [2, 2])
        self.actors["foot"]         = MovingActor(Prop(load_image("foot.jpg")), [3, 3])
        
    def update(self):                    
        for prop in self.props.values():
            # Update the prop
            prop.update()
            
            # Draw the prop
            prop.blit(self.screen)
                    
        for actor in self.actors.values():
            # Update the actor
            actor.update()

            # Draw the actor
            actor.blit(self.screen)
        
        # Display the result of what we drew
        pygame.display.flip()

# Base program logic
def program():
    game = Game()
    
    # Loop until escape is pressed
    while pygame.key.get_pressed()[pygame.K_ESCAPE] == 0:
        # Process each event
        for event in pygame.event.get():
            # If the user clicks the close button, the QUIT event is triggered
            if event.type == pygame.QUIT:
                # Exit the program entirely
                sys.exit()

        # Update the game state
        game.update()

# Start the program
program()
