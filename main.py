import pygame
import math
pygame.init()
h = 700
l = 1000
screen = pygame.display.set_mode((l, h))
pygame.display.set_caption("Projectile Simulation")
clock = pygame.time.Clock()
f = pygame.font.Font(None, 36)

#Constants
speed = 50
angle = 45
g = 9.81 #m/s^2
# for this we will need to create what the ratio/meter will be
# 1 meter = 10 pixels
meter = 10
#Now this will make the projectile's coordinates
y = h - 50

class Projectile:
    def __init__(self, speed, angle):
        self.x = 0.0
        self.y = 0.0
        self.speed = speed
        self.angle = math.radians(angle)

        #the actual formula is vx = speed * cos(angle)
        # vy = speed * sin(angle)
        self.vx = self.speed * math.cos(self.angle)
        self.vy = -self.speed * math.sin(self.angle)

        self.path = []
        self.active = True
    def update(self, dt):
        if not self.active:
            return
        
        #This will be used to add gravity to the simulation
        self.vy += g * dt

        #This will update the position
        self.x += self.vx * dt
        self.y += self.vy * dt

        #This will add it on the array.
        #So basically it will add every point of the path of the projectile
        self.path.append((self.x, self.y))

        #This will be when the projectile hits the ground
        if self.y <= 0 and len(self.path) > 1:
            self.y = 0
            self.active = False
 
projectiles = []
running = True

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(
                    Projectile(10,45)
                )
            elif event.key == pygame.K_UP:
                angle += 1
            elif event.key == pygame.K_DOWN:
                angle -= 1
            elif event.key == pygame.K_RIGHT:
                speed += 1
            elif event.key == pygame.K_LEFT:
                speed = max(1, speed - 1)
            elif event.key == pygame.K_r:
                projectiles.clear()
    screen.fill((255, 255, 255))


    #This will make the physics calculations
    initvy = speed * math.sin(math.radians(angle))
    maxH = (initvy ** 2) / (2 * g)
    flightT = (2 * initvy)/g
    rangeD = (
        speed ** 2 * math.sin(2 * math.radians(angle))
    ) / g

    #This will be used to display text
    lines = [
        f"Launch Speed: {speed: .1f} m/s",
        f"Launch Angle: {angle: .1f} degrees",
        f"Max Height: {maxH: .1f}m",
        f"Flight Time: {flightT: .1f} s",
        f"Range: {rangeD: .1f} m",
        "",
        "Space = Launch Projectile",
        "Up/Down = Adjust Angle",
        "Left/Right = Adjust Speed",
        "R = Reset Projectiles"
    ]
    for i, text in enumerate(lines):
        surface = f.render(text, True, (0,0,0))
        screen.blit(surface, (20, 20 + i * 35))

    pygame.display.flip()

#This helps u to stop the code when you click the x
pygame.quit()
