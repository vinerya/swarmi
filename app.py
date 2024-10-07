import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Bot Simulation Prototype")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Fighter Jet Class
class FighterJet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.max_speed = 8
        self.acceleration = 0.2
        self.turn_rate = 0.05
        self.drag = 0.99

    def draw(self):
        # Draw the jet as a triangle pointing in the direction of movement
        points = [
            (self.x + math.cos(self.angle) * 20, self.y + math.sin(self.angle) * 20),
            (self.x + math.cos(self.angle + 2.5) * 15, self.y + math.sin(self.angle + 2.5) * 15),
            (self.x + math.cos(self.angle - 2.5) * 15, self.y + math.sin(self.angle - 2.5) * 15)
        ]
        pygame.draw.polygon(screen, BLUE, points)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_rate
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_rate
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        else:
            self.speed *= self.drag  # Apply drag to slow down when not accelerating

        # Limit speed to maximum speed
        self.speed = max(0, min(self.max_speed, self.speed))

        # Update position based on current speed and angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Keep the jet within bounds
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

# Bot Class
class Bot:
    def __init__(self, x, y, target, speed, prediction_offset=0, color=YELLOW):
        self.x = x
        self.y = y
        self.angle = 0  # Initialize Bot angle
        self.target = target
        self.speed = 0
        self.max_speed = speed
        self.acceleration = 0.5
        self.turn_rate = 0.1
        self.prediction_offset = prediction_offset
        self.color = color
        print(f"Bot created at ({self.x}, {self.y}) with prediction offset {self.prediction_offset}")

    def move(self):
        # Move towards the predicted target position with an offset
        predicted_x = self.target.x + math.cos(self.target.angle) * self.prediction_offset
        predicted_y = self.target.y + math.sin(self.target.angle) * self.prediction_offset
        angle_to_target = math.atan2(predicted_y - self.y, predicted_x - self.x)

        # Gradually adjust Bot angle towards the target
        angle_diff = (angle_to_target - self.angle + math.pi) % (2 * math.pi) - math.pi
        if angle_diff > self.turn_rate:
            self.angle += self.turn_rate
        elif angle_diff < -self.turn_rate:
            self.angle -= self.turn_rate
        else:
            self.angle = angle_to_target

        # Accelerate towards max speed
        self.speed += self.acceleration
        self.speed = min(self.speed, self.max_speed)

        # Update position based on current speed and angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        print(f"Bot at ({self.x}, {self.y}) moving towards ({predicted_x}, {predicted_y})")

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)  # Increased size to 10 for better visibility

# Main Function
def main():
    while True:  # Run the game in a loop to allow restarts
        clock = pygame.time.Clock()
        jet = FighterJet(WIDTH // 2, HEIGHT // 2)
        Bots = []
        run = True

        while run:
            clock.tick(60)
            screen.fill(WHITE)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Launch multiple Bots towards the jet from the same source with different behaviors
                        source_x, source_y = WIDTH // 2, HEIGHT // 2  # Fixed source position
                        Bots.append(Bot(source_x, source_y, jet, 10, prediction_offset=0, color=RED))  # Direct Bot
                        Bots.append(Bot(source_x, source_y, jet, 10, prediction_offset=50, color=YELLOW))  # Predictive Bot 1
                        Bots.append(Bot(source_x, source_y, jet, 10, prediction_offset=-50, color=YELLOW))  # Predictive Bot 2

            # Jet Movement
            keys = pygame.key.get_pressed()
            jet.move(keys)
            jet.draw()

            # Bot Movement
            for Bot in Bots:
                Bot.move()
                Bot.draw()

                # Check for collision with the jet
                distance = math.sqrt((Bot.x - jet.x) ** 2 + (Bot.y - jet.y) ** 2)
                if distance < 15:  # Collision threshold
                    print("Bot hit the jet! Restarting...")
                    run = False  # End the current game loop

            # Remove Bots that have moved off-screen
            Bots = [Bot for Bot in Bots if 0 <= Bot.x <= WIDTH and 0 <= Bot.y <= HEIGHT]

            # Update Display
            pygame.display.flip()

if __name__ == "__main__":
    main()