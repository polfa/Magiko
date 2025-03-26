from src.enemies.enemie_manager import EnemieManager


class WavesLevel1:
    def __init__(self, base):
        self.current_wave = 0
        self.waves = [
            self.wave_1(base),
            self.wave_2(base),
            self.wave_3(base),
            self.wave_4(base),
            self.wave_5(base),
        ]
        self.wave_cool_down = 100
        self.cool_down = self.wave_cool_down

    def next_wave(self):
        if self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            return self.waves[self.current_wave]
        return False

    def is_current_wave_over(self):
        is_empty = self.waves[self.current_wave].is_empty()
        if is_empty:
            if self.cool_down == self.wave_cool_down:
                self.cool_down -= 1
                return False
            elif self.cool_down > 0:
                self.cool_down -= 1
                return False
            else:
                self.cool_down = self.wave_cool_down
                return True

        return is_empty

    def get_current_wave(self):
        return self.waves[self.current_wave]

    @staticmethod
    def wave_1(base):
        enemie_manager = EnemieManager()
        enemie_manager.add_enemie("bad_goblin", (1600, base))
        enemie_manager.add_enemie("bad_goblin", (1600, base))
        return enemie_manager

    @staticmethod
    def wave_2(base):
        enemie_manager = EnemieManager()
        enemie_manager.add_enemie("bad_goblin", (100, base))
        enemie_manager.add_enemie("bad_goblin", (300, base))
        enemie_manager.add_enemie("bad_goblin", (1000, base))
        return enemie_manager

    @staticmethod
    def wave_3(base):
        enemie_manager = EnemieManager()
        enemie_manager.add_enemie("bad_goblin", (100, base))
        enemie_manager.add_enemie("bad_goblin", (300, base))
        enemie_manager.add_enemie("bad_goblin", (1000, base))
        enemie_manager.add_enemie("bad_goblin", (1200, base))
        enemie_manager.add_enemie("bad_goblin", (1400, base))
        return enemie_manager

    @staticmethod
    def wave_4(base):
        enemie_manager = EnemieManager()
        enemie_manager.add_enemie("bad_goblin", (100, base))
        enemie_manager.add_enemie("bad_goblin", (300, base))
        enemie_manager.add_enemie("bad_goblin", (1000, base))
        enemie_manager.add_enemie("bad_goblin", (1200, base))
        enemie_manager.add_enemie("bad_goblin", (1400, base))
        enemie_manager.add_enemie("bad_goblin", (1600, base))
        return enemie_manager

    @staticmethod
    def wave_5(base):
        enemie_manager = EnemieManager()
        enemie_manager.add_enemie("bad_goblin", (100, base))
        enemie_manager.add_enemie("bad_goblin", (300, base))
        enemie_manager.add_enemie("bad_goblin", (1000, base))
        enemie_manager.add_enemie("bad_goblin", (1200, base))
        enemie_manager.add_enemie("bad_goblin", (1400, base))
        enemie_manager.add_enemie("bad_goblin", (1600, base))
        enemie_manager.add_enemie("bad_goblin", (1800, base))
        enemie_manager.add_enemie("bad_goblin", (100, base))
        enemie_manager.add_enemie("bad_goblin", (300, base))
        enemie_manager.add_enemie("bad_goblin", (1000, base))
        enemie_manager.add_enemie("bad_goblin", (1200, base))
        enemie_manager.add_enemie("bad_goblin", (1400, base))
        enemie_manager.add_enemie("bad_goblin", (1600, base))
        enemie_manager.add_enemie("bad_goblin", (1800, base))
        return enemie_manager

