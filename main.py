import pygame

from states.already_voted import AlreadyVotedState
from states.identification import IdentificationState
from states.identification_failure import IdentificationFailureState
from states.successful_auth import SuccessfulAuthState
from states.too_many_attempts import TooManyAttemptsState
from states.vote import VoteState
from states.end_state import EndState
from states.enroll_finger import EnrollFinger

from states.confirming_vote import ConfirmingVote

from states.finalize_section import FinalizeSection

from states.config import screen, clock
from biometry.fingerprint_sensor import FingerprintSensor


finger_sensor = FingerprintSensor()

states = {
    "Identification": IdentificationState(finger_sensor),
    "IdentificationFailure": IdentificationFailureState(), 
    "TooManyAttempts": TooManyAttemptsState(),
    "SuccessfulAuth": SuccessfulAuthState(),
    "AlreadyVoted": AlreadyVotedState(),
    "Finalize Section": FinalizeSection(),
    "Vote Vereador": VoteState(candidate_number_size=5, position="Vereador", next_state="Vote Prefeito"),
    "Vote Prefeito": VoteState(candidate_number_size=2, position="Prefeito", next_state="Confirming Vote"), 
    "Confirming Vote": ConfirmingVote(),
    "End": EndState(),
    "EnrollFinger": EnrollFinger(finger_sensor)
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
