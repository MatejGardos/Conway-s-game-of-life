import pygame, time
import numpy as np

WIDTH = 800
HEIGHT = 600

COLOR_BG = (10,10,10)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)

FPS = 60

def update(surface, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row,col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_BG

            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE

        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE

        pygame.draw.rect(surface, color, (col*size, row*size, size-1, size-1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    cells = np.zeros((HEIGHT//10, WIDTH//10))
    screen.fill(COLOR_GRID)

    update(screen, cells, 10)

    #pygame.display.flip()
    pygame.display.update()

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:
                # continuesly running
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

                # next step
                if event.key == pygame.K_RIGHT:
                    cells = update(screen, cells, 10, with_progress=True)
                    pygame.display.update()

                # clean the screen
                if event.key == pygame.K_r:
                    screen.fill(COLOR_GRID)
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pygame.display.update()

        # add "life"
        if pygame.mouse.get_pressed()[0] and not running:
            pos = pygame.mouse.get_pos()
            cells[pos[1]//10, pos[0]//10] = 1
            update(screen, cells, 10)
            pygame.display.update()

        # remove "life"
        if pygame.mouse.get_pressed()[2] and not running:
            pos = pygame.mouse.get_pos()
            cells[pos[1]//10, pos[0]//10] = 0
            update(screen, cells, 10)
            pygame.display.update()


        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

            time.sleep(0.1)

        
        clock.tick(FPS)

if __name__ == "__main__":
    main()