from random import randint

from src.enemies.bad_goblin import BadGoblin


class EnemieManager:
    def __init__(self):
        self.enemies = []
        self.ENEMIE_TYPES = {"bad_goblin": BadGoblin()}
        self.player_hit = False

    def is_empty(self):
        return len(self.enemies) == 0

    def add_enemie(self, enemie, pos):
        self.enemies.append(self.ENEMIE_TYPES[enemie].new(pos))

    def remove_enemie(self, enemie):
        self.enemies.remove(enemie)

    def update(self, player, screen):
        already_hit = []
        hit = False
        is_primary = player.state.value == "primary"
        is_secondary = player.state.value == "secondary"
        is_ultimate = player.state.value == "ultimate"
        if not player.is_hitting():
            self.player_hit = False

        enemies_copy = self.enemies.copy()
        for enemie in enemies_copy:
            enemie.update(player, screen)
            if enemie in already_hit or self.player_hit:
                continue
            if is_primary and len(already_hit) > 0:
                continue
            attack = enemie.check_player_hit(player)
            is_hit = attack is not None
            if not is_hit:
                continue
            if not enemie.alive:
                random = randint(0, 10)
                print(random)
                if random == 0 or random == 1:
                    player.level.add_mana_potion(enemie.pos)
                elif random == 2:
                    player.level.add_health_potion(enemie.pos)
                elif random > 2:
                    player.level.add_coin(enemie.pos)
                self.remove_enemie(enemie)

            if is_hit:
                hit = True
                already_hit.append(enemie)
        if hit:
            self.player_hit = True


