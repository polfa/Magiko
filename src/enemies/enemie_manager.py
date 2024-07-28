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
        already_hit = False
        hit = False
        if self.player_hit and not player.is_hitting():
            self.player_hit = False

        for enemie in self.enemies:
            enemie.update(player, screen)
            if already_hit or self.player_hit:
                continue
            is_hit, hit_type = enemie.check_player_hit(player)
            if not enemie.alive:
                self.remove_enemie(enemie)
            if is_hit:
                hit = True
            if is_hit and hit_type == "first":
                already_hit = True
        if hit:
            self.player_hit = True


