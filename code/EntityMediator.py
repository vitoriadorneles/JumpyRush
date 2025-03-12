from code.Entity import Entity


class EntityMediator:
    @staticmethod
    def __verify_collision_window():
        pass

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range (len(entity_list)):
            game_entity = entity_list[i]
            EntityMediator.__verify_collision_window()