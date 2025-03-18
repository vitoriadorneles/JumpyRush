from code.Player import Player
from code.Obstacle import Obstacle


class EntityMediator:
    @staticmethod
    def verify_collision(entity_list):
        for entity in entity_list:
            if isinstance(entity, Obstacle) and entity.rect.right < 0:  # Obstacle fora da tela
                entity_list.remove(entity)

            for other_entity in entity_list:
                if entity != other_entity and entity.rect.colliderect(other_entity.rect):
                    if isinstance(entity, Player) and isinstance(other_entity, Obstacle):
                        print("Game Over! Player colidiu com um obstáculo!")
                        return "game_over"
        return "running"
