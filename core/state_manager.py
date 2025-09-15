class StateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = None

    def change(self, new_state):
        self.current_state = new_state

    def handle_events(self):
        if self.current_state:
            self.current_state.handle_events()

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self):
        if self.current_state:
            self.current_state.render()