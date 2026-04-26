import random
from typing import Optional, Any
from openenv.core import Environment
from triage_wars.models import TriageAction, TriageObservation, TriageState

class TriageWarsEnvironment(Environment[TriageAction, TriageObservation, TriageState]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = {}

    def reset(self, seed: Optional[int] = None, episode_id: Optional[str] = None, **kwargs: Any) -> TriageObservation:
        if seed is not None:
            random.seed(seed)
            
        self._state = {
            "buildings": {
                "A": {"trapped": random.randint(100, 400), "rescued": 0},
                "B": {"trapped": random.randint(100, 400), "rescued": 0},
                "C": {"trapped": random.randint(100, 400), "rescued": 0},
            },
            "ndrf_teams": random.randint(2, 5),
            "hospital_capacity": random.randint(200, 400),
            "ngo_volunteers": random.randint(100, 300),
            "public_panic_index": random.uniform(0.5, 0.9),
            "hours_elapsed": 0.0,
            "total_rescued": 0,
            "emergency_declared": False,
            "hospital_warned": False,
            "episode_done": False,
            "current_reward": 0.0,
            "step_number": 0
        }
        self._state["total_initial_trapped"] = sum(b["trapped"] for b in self._state["buildings"].values())
        return self._get_obs()

    def step(self, action: TriageAction, timeout_s: Optional[float] = None, **kwargs: Any) -> TriageObservation:
        if "buildings" not in self._state:
            self.reset()
            
        # Simulate rescues based on action
        rescued_a = min(self._state["buildings"]["A"]["trapped"], action.ndrf_building_a_teams * 20)
        self._state["buildings"]["A"]["trapped"] -= rescued_a
        self._state["buildings"]["A"]["rescued"] += rescued_a

        rescued_b = min(self._state["buildings"]["B"]["trapped"], action.ndrf_building_b_teams * 20)
        self._state["buildings"]["B"]["trapped"] -= rescued_b
        self._state["buildings"]["B"]["rescued"] += rescued_b

        rescued_c = min(self._state["buildings"]["C"]["trapped"], action.ndrf_building_c_teams * 20)
        self._state["buildings"]["C"]["trapped"] -= rescued_c
        self._state["buildings"]["C"]["rescued"] += rescued_c

        # NGO rescues
        rescued_ngo = 0
        if action.ngo_building_assigned in ["A", "B", "C"]:
            b_name = action.ngo_building_assigned
            rescued_ngo = min(self._state["buildings"][b_name]["trapped"], action.ngo_volunteers_deployed // 5)
            self._state["buildings"][b_name]["trapped"] -= rescued_ngo
            self._state["buildings"][b_name]["rescued"] += rescued_ngo

        newly_rescued = rescued_a + rescued_b + rescued_c + rescued_ngo
        self._state["total_rescued"] += newly_rescued

        self._state["hours_elapsed"] += 1.0
        self._state["step_number"] += 1

        if action.ndrf_hospital_warning:
            self._state["hospital_warned"] = True
        if action.emergency_declared:
            self._state["emergency_declared"] = True

        # Calculate reward
        lives_saved_percentage = (self._state["total_rescued"] / self._state["total_initial_trapped"]) if self._state["total_initial_trapped"] > 0 else 0
        
        duplicate = False
        if action.ngo_building_assigned == "A" and action.ndrf_building_a_teams > 0: duplicate = True
        if action.ngo_building_assigned == "B" and action.ndrf_building_b_teams > 0: duplicate = True
        if action.ngo_building_assigned == "C" and action.ndrf_building_c_teams > 0: duplicate = True

        reward = (lives_saved_percentage * 50.0) - (self._state["hours_elapsed"] * 1.5)
        if self._state["hospital_warned"]:
            reward += 15.0
        if not duplicate:
            reward += 10.0

        self._state["current_reward"] = float(reward)

        # Check termination
        if self._state["step_number"] >= 12 or self._state["total_rescued"] >= self._state["total_initial_trapped"]:
            self._state["episode_done"] = True

        return self._get_obs()

    def _get_obs(self) -> TriageObservation:
        return TriageObservation(
            hours_elapsed=float(self._state["hours_elapsed"]),
            total_trapped=int(self._state["total_initial_trapped"]),
            total_rescued=int(self._state["total_rescued"]),
            buildings_status=dict(self._state["buildings"]),
            ndrf_obs={
                "teams_available": self._state["ndrf_teams"],
                "buildings": dict(self._state["buildings"])
            },
            hospital_obs={
                "capacity": self._state["hospital_capacity"], 
                "warned": self._state["hospital_warned"]
            },
            govt_obs={
                "emergency_declared": self._state["emergency_declared"],
                "funds_available": 5000
            },
            ngo_obs={
                "volunteers": self._state["ngo_volunteers"],
                "clearance": self._state["emergency_declared"]
            },
            media_obs={
                "panic_index": self._state["public_panic_index"],
                "social_media_rumor": int(self._state["total_initial_trapped"]) * 2
            },
            episode_done=bool(self._state["episode_done"]),
            current_reward=float(self._state["current_reward"]),
            step_number=int(self._state["step_number"])
        )

    @property
    def state(self) -> TriageState:
        return TriageState(data=self._state)
