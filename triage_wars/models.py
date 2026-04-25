from openenv.core import Action, Observation, State

class TriageAction(Action):
    ndrf_building_a_teams: int = 0
    ndrf_building_b_teams: int = 0
    ndrf_building_c_teams: int = 0
    ndrf_hospital_warning: bool = False
    ndrf_casualty_estimate: int = 0
    hospital_surge_activated: bool = False
    hospital_ambulances_deployed: int = 0
    emergency_declared: bool = False
    funds_released: int = 0
    ngo_building_assigned: str = ""
    ngo_volunteers_deployed: int = 0
    press_briefing_issued: bool = False
    panic_management_message: str = ""

class TriageObservation(Observation):
    hours_elapsed: float
    total_trapped: int
    total_rescued: int
    buildings_status: dict
    ndrf_obs: dict
    hospital_obs: dict
    govt_obs: dict
    ngo_obs: dict
    media_obs: dict
    episode_done: bool
    current_reward: float
    step_number: int

class TriageState(State):
    data: dict = {}
