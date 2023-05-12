import pygame
import random
from main import UserAgent, CDNNode

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Music Simulation")

# Set up colors
background_color = (255, 255, 255)
cdn_node_color = (0, 0, 255)
user_agent_color = (0, 255, 0)
station_color = (255, 0, 0)

# Set up simulation objects
n_cdn_nodes = 5
n_user_agents = 10
n_stations = 10
cdn_nodes = [CDNNode(random.randint(0, width), random.randint(0, height)) for _ in range(n_cdn_nodes)]
user_agents = [UserAgent(random.randint(0, width), random.randint(0, height), cdn_nodes) for _ in range(n_user_agents)]
stations = [(random.randint(0, width), random.randint(0, height)) for _ in range(n_stations)]


def get_network_color(state):
    if state == 'active':
        return (0, 255, 0)
    elif state == 'inactive':
        return (255, 0, 0)
    else:
        return (255, 255, 255)


def draw_stations(stations):
    for station in stations:
        pygame.draw.circle(screen, station.color, (station.x, station.y), 10)


# Function to draw the simulation objects
def draw_objects():
    screen.fill(background_color)

    for node in cdn_nodes:
        pygame.draw.circle(screen, node.color, (node.x, node.y), 8)

    for agent in user_agents:
        pygame.draw.circle(screen, user_agent_color, agent.position, 5)

    for station in stations:
        pygame.draw.circle(screen, station_color, station, 8)

    for network_state, (node1, node2) in network_connections.items():
        pygame.draw.line(screen, get_network_color(network_state), (node1.x, node1.y), (node2.x, node2.y), 2)

    draw_stations(stations)

    move_button.draw(screen)

    pygame.display.flip()



class Button:
    def __init__(self, x, y, width, height, text, color, font_size, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def toggle_movement():
    global move_agents
    move_agents = not move_agents

move_button = Button(10, 10, 100, 40, "Toggle Move", (200, 200, 200), 24, toggle_movement)



# Main loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)  # Limit the frame rate to 30 FPS

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        move_button.is_clicked(event)

    draw_objects()

if move_agents:
    for agent in user_agents:
        agent.move_randomly(width, height)



def cdn_simulation():
    # Set up the simulation environment with user agents, CDN nodes, and servers

    for time_step in range(num_time_steps):
        # Make user agents request content from CDN nodes
        for user_agent in user_agents:
            cdn_node = find_cdn_node(user_agent.location)
            content = cdn_node.request_content(user_agent, time_step)

            # Update user agent's history and location
            user_agent.update_history(content, time_step)
            user_agent.update_location(time_step)

        # Update CDN nodes' content and frontloaded content
        for cdn_node in cdn_nodes:
            cdn_node.update_content()
            cdn_node.update_frontloaded_content()

        return cdn_cost

def frontloaded_simulation():
    # Set up the simulation environment with user agents, CDN nodes, and servers

    for time_step in range(num_time_steps):
        # Make user agents request content from CDN nodes
        for user_agent in user_agents:
            cdn_node = find_cdn_node(user_agent.location)

            # Use the recommendation engine to get frontloaded content
            recommendations = recommendation_engine.get_recommendations(user_agent, time_step)
            cdn_node.set_frontloaded_content(recommendations)

            content = cdn_node.request_content(user_agent, time_step)

            # Update user agent's history and location
            user_agent.update_history(content, time_step)
            user_agent.update_location(time_step)

        return frontloading_cost

        # Update CDN nodes' content and frontloaded content
        for cdn_node in cdn_nodes:
            cdn_node.update_content()
            cdn_node.update_frontloaded_content()


# Clean up
pygame.quit()



