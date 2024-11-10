class State:
    """Base class for all states in the game."""
    def __init__(self):
        self.next_state = None

    def handle_events(self, events):
        """Process events."""
        pass

    def update(self):
        """Update the game state."""
        pass

    def render(self, screen):
        """Render content on the screen."""
        pass