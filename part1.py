import pygame, requests, sys, os


class Map(object):
    def __init__(self):
        self.lat = 55.751861
        self.lon = 37.619058
        self.zoom = 16
        self.type = "map"


def load_map(mp):
    params = {
        "ll": ",".join([str(mp.lon), str(mp.lat)]),
        "z": str(mp.zoom),
        "l": str(mp.type)
    }
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = Map()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()