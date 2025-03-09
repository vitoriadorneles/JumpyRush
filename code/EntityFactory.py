from code.Background import Background
from code.Const import WIN_WIDTH


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position= (0, 0)):
        match entity_name:
            case 'Level1Bg':
                bg_list = []
                for i in range(4):
                    bg_list.append(Background(f'Level1Bg{i}', (0, 0)))
                    bg_list.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
                return bg_list
