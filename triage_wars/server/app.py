from openenv.core import create_app
from triage_wars.server.triage_wars_environment import TriageWarsEnvironment
from triage_wars.models import TriageAction, TriageObservation

app = create_app(TriageWarsEnvironment, TriageAction, TriageObservation)
