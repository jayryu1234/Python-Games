""" Turtle in Pygame

We really miss the turtle module from Python's standard library. It was a great
way to introduce programming, so let's make something similar in PyGame, using
objects. 

"""
import math
import random
import pygame

def event_loop():
    turtle = Turtle(screen, screen.get_width() // 2, screen.get_height() // 2) 
    """Wait until user closes the window"""
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            turtle.left(45)
        if keys[pygame.K_d]:
            turtle.left(-45)
        if keys[pygame.K_w]:
            turtle.forward(45)
        if keys[pygame.K_s]:
            turtle.forward(-45)
        if keys[pygame.K_SPACE]:
            turtle.make_square()
        screen.fill("white")
        pygame.draw.circle(screen, "white", (turtle.x, turtle.y), 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

class Turtle:
    def __init__(self, screen, x: int, y: int):
        self.x = x
        self.y = y
        self.screen = screen
        self.angle = 0  # Angle in degrees, starting facing right
    def make_square(self):
        for _ in range(4):
            self.forward(100)  # Move forward by 100 pixels
            self.left(90)  # Turn left by 90 degrees
    def forward(self, distance):
        # Calculate new position based on current angle
        radian_angle = math.radians(self.angle)

        start_x = self.x  # Save the starting position
        start_y = self.y

        # Calculate the new position displacement
        dx = math.cos(radian_angle) * distance
        dy = math.sin(radian_angle) * distance

        # Update the turtle's position
        self.x += dx
        self.y -= dy

        # Draw line to the new position
        pygame.draw.line(self.screen, black, (start_x, start_y), (self.x, self.y), 2)

    def left(self, angle):
        # Turn left by adjusting the angle counterclockwise
        self.angle = (self.angle + angle) % 360


# Main loop

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turtle Style Drawing")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

screen.fill(white)
 # Start at the center of the screen

# Draw a square using turtle-style commands


# Display the drawing
pygame.display.flip()
def make_and_move_turtle():
    
    turtley = Turtle(screen, random.randint(1, 100), random.randint(1, 100))  # Start at the center of the screen
    print(turtley.x)
    print(turtley.y)
make_and_move_turtle()
# Wait to quit
event_loop()

# Quit Pygame
pygame.quit()

