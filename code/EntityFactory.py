from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Obstacle import Obstacle
from code.Player import Player
from code.Background import Background


class EntityFactory:
    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), speed=5):
        match entity_name:
            case 'PlayerImg':
                player_img = []
                for i in range(7):
                    player_img.append(Player(f'PlayerImg{i}', (25, WIN_HEIGHT - 130)))
                return player_img

            case 'Level1Bg':
                bg_list = []
                for i in range(4):
                    bg_list.append(Background(f'Level1Bg{i}', (0, 0)))
                    bg_list.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
                return bg_list

            case 'Obstacle1Img0':
                obstacle = Obstacle('Obstacle1Img0', (WIN_WIDTH + 50, 220))
                obstacle.speed = speed  # Define a velocidade do obstáculo
                return obstacle

            case 'Obstacle1Img1':
                obstacle = Obstacle('Obstacle1Img1', (WIN_WIDTH + 20, 200))
                obstacle.speed = speed  # Define a velocidade do obstáculo
                return obstacle

            case _:
                raise ValueError(f"Entidade desconhecida: {entity_name}")
