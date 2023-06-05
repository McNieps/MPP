import time


class Effect:
    EFFECTS = []

    def __init__(self, lifetime):
        self.start_time = time.time()
        self.lifetime = lifetime
        self.to_delete = False

        self.EFFECTS.append(self)

    @classmethod
    def update_all(cls, delta):
        for i in range(len(cls.EFFECTS)-1, -1, -1):
            cls.EFFECTS[i].update(delta)

            if cls.EFFECTS[i].to_delete:
                cls.EFFECTS.pop(i)

    def update(self, delta):
        if time.time() > self.start_time + self.lifetime:
            self.to_delete = True

    @classmethod
    def render_all(cls, surface):
        for effect in cls.EFFECTS:
            effect.render(surface)

    def render(self, surface):
        pass
