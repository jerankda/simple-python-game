import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the player object
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        # Change the speed of the player
        self.change_x += x
        self.change_y += y

    def update(self):
        # Find a new position for the player
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Test')

# Create the player object
player = Player(50, 50)

# Create the walls
wall_list = pygame.sprite.Group()

# Create the level
level = [
    "WWWWWWWWWWWWWWWWWWW",
    "W                  W",
    "W         WWWWWW   W",
    "W   WWWW       W   W",
    "W   W        WWWW  W",
    "W WWW  WWWW        W",
    "W                  W",
    "WWWWWWWWWWWWWWWWWWW"
]

# Go through the level and add the walls to the list
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            wall = Wall(x, y, 10, 10)
            wall_list.add(wall)
        x += 10
    y += 10
    x = 0

# Set the player object's walls attribute
player.walls = wall_list

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Main program loop
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    # --- Game Logic
    player.update()

    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)

    # Draw the walls
    wall_list.draw(screen)

    # Draw the player
    screen.blit(player.image, player.rect)

    # Update the screen
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit
pygame.quit()
