import pygame

from states.identification import IdentificationState
from states.vote import VoteState
from states.end_state import EndState

from states.confirming_vote import ConfirmingVote

from states.config import screen, clock


states = {
    "Identification": IdentificationState(), 
    "Vote Vereador": VoteState(candidate_number_size=5, position="Vereador", next_state="Vote Prefeito"),
    "Vote Prefeito": VoteState(candidate_number_size=2, position="Prefeito", next_state="Confirming Vote"), 
    "Confirming Vote": ConfirmingVote(),
    "End": EndState()
}
current_state = states["Identification"]

while True:
    events = pygame.event.get()
    current_state.handle_events(events)

    if current_state.next_state:
        current_state = states[current_state.next_state]
        current_state.next_state = None  # Reset the next_state

    current_state.update()
    current_state.render(screen)

    pygame.display.flip()
    clock.tick(60)
