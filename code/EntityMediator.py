from code.Background import Background
from code.Entity import Entity
from code.Obstacle import Obstacle


class EntityMediator:
    def __init__(self):
        self.rect = None

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Obstacle):
            if ent.rect.right < 0:
                ent.health = 0

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            game_entity = entity_list[i]
            EntityMediator.__verify_collision_window(game_entity)

    @staticmethod
    def check_collision(player, obstacles):
        for obstacle in obstacles:
            if isinstance(obstacle, Background):
                continue
            if obstacle.rect.right < 0:
                continue
            print(
                f"🟢 Testando colisão: {obstacle.name} | Posição: {obstacle.rect.topleft} | Tamanho: {obstacle.rect.size}")

            if player.rect.colliderect(obstacle.rect):
                print(f"🔥 Colisão confirmada com {obstacle.name}!")
                return True
        return False

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                entity_list.remove(ent)
