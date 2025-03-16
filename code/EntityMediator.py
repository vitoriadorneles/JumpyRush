from code.Background import Background
from code.Entity import Entity
from code.Obstacle import Obstacle
from code.Player import Player


class EntityMediator:
    def __init__(self):
        self.rect = None

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Obstacle):
            if ent.rect.right < 0:
                ent.health = 0


    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        if ent1.rect.colliderect(ent2.rect):  # Verifica se as áreas dos retângulos se sobrepõem
            if isinstance(ent1, Player) and isinstance(ent2, Obstacle):  # Verifica o tipo de interação válida
                ent1.health -= ent2.damage  # Reduz a saúde do jogador
                ent1.last_damage = ent2.name
                print(f"🔥 Colisão detectada! {ent1.name} colidiu com {ent2.name}. Saúde restante: {ent1.health}")

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list[:]:  # Crie uma cópia da lista para evitar problemas ao remover itens
            if ent.health <= 0:
                print(f"🛑 {ent.name} foi removido devido a saúde <= 0.")
                entity_list.remove(ent)

