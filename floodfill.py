import numpy, pygame

def fill(surface, position, fill_color):
    fill_color = surface.map_rgb(fill_color)
    surf_array = pygame.surfarray.pixels2d(surface)
    current_color = surf_array[position]
    if current_color != fill_color:

        frontier = [position]
        while len(frontier) > 0:
            x, y = frontier.pop()
            try:
                if surf_array[x, y] != current_color:
                    continue
            except IndexError:
                continue
            surf_array[x, y] = fill_color
            frontier.append((x + 1, y))
            frontier.append((x - 1, y))
            frontier.append((x, y + 1))
            frontier.append((x, y - 1))

        pygame.surfarray.blit_array(surface, surf_array)
