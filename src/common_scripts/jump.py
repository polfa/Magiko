class Jump:
    def __init__(self, entity, jump_power=10, jump_speed=0, gravity=0.2, jump_cooldown=15):
        # jumping attributes
        self.jumping = False
        self.jump_power = jump_power
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.cooldown = jump_cooldown
        self.no_jump_time = self.cooldown  # time since it stopped jumping
        self.limit_bottom = entity.pos[1]

    def update(self, entity):
        if self.jumping:
            entity.pos = (entity.pos[0], entity.pos[1] - self.jump_speed)
            self.jump_speed -= self.gravity
            if entity.pos[1] >= self.limit_bottom:
                self.jumping = False
                self.jump_speed = self.jump_power
                entity.pos = (entity.pos[0], self.limit_bottom)
        else:
            if self.no_jump_time < self.cooldown:
                self.no_jump_time += 1

    def is_jumping(self):
        return self.jumping

    def start_jump(self, entity):
        if self.no_jump_time == self.cooldown and not self.jumping:
            self.jumping = True
            self.no_jump_time = 0
            self.jump_speed = self.jump_power
            return True
        return False



