from openenv.core import EnvClient
from triage_wars.models import TriageAction, TriageObservation

from openenv.core.client_types import StepResult

class TriageWarsEnv(EnvClient):
    action_type = TriageAction
    observation_type = TriageObservation

    def _parse_result(self, result: dict) -> StepResult[TriageObservation]:
        obs_dict = result.get("observation", result)
        obs = TriageObservation(**obs_dict)
        return StepResult(
            observation=obs,
            reward=result.get("reward", 0.0),
            done=result.get("done", False)
        )

    def _parse_state(self, state: dict) -> dict:
        return state

    def _step_payload(self, action: TriageAction) -> dict:
        return action.model_dump()
