import pygame


transparent_color = (69, 69, 69)


def outline_surf(surface: pygame.Surface, outline_color: tuple[int, int, int]):
    surface.set_colorkey(transparent_color)
    surface_size = surface.get_size()
    new_surface = pygame.Surface((surface_size[0]+2, surface_size[1]+2))
    new_surface.fill(transparent_color)
    new_surface.set_colorkey(transparent_color)

    mask_surf = pygame.mask.from_surface(surface).to_surface(setcolor=outline_color, unsetcolor=transparent_color)
    mask_surf.set_colorkey(transparent_color)

    new_surface.blit(mask_surf, (0, 1))
    new_surface.blit(mask_surf, (2, 1))
    new_surface.blit(mask_surf, (1, 0))
    new_surface.blit(mask_surf, (1, 2))

    new_surface.blit(surface, (1, 1))

    return new_surface
