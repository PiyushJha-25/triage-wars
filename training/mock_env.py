import random

class MockTriageEnv:
    def __init__(self):
        self.total_trapped = 0
        self.total_rescued = 0
        self.hours_elapsed = 0

    async def reset(self):
        self.total_trapped = random.randint(500, 1200)
        self.total_rescued = 0
        self.hours_elapsed = 0
        return self._obs()

    async def step(self, action=None):
        self.hours_elapsed += 2
        
        # Rescue 50-150 people per step
        rescued_this_step = random.randint(50, 150)
        # Ensure we don't rescue more than trapped
        rescued_this_step = min(rescued_this_step, self.total_trapped - self.total_rescued)
        self.total_rescued += rescued_this_step
        
        # Calculate reward
        reward = (self.total_rescued / self.total_trapped) * 50 - self.hours_elapsed * 0.5
        
        # Check if done
        done = self.hours_elapsed >= 24 or self.total_rescued >= self.total_trapped
        
        return self._obs(), reward, done, {}

    def _obs(self):
        return {
            "total_trapped": self.total_trapped,
            "total_rescued": self.total_rescued,
            "hours_elapsed": self.hours_elapsed,
            "ndrf_obs": {
                "available_personnel": random.randint(100, 500),
                "equipment_status": random.choice(["Optimal", "Degraded", "Critical"]),
                "deployed_teams": random.randint(5, 20)
            },
            "hospital_obs": {
                "available_beds": random.randint(10, 100),
                "critical_supplies": random.choice(["Sufficient", "Low", "Exhausted"]),
                "triage_capacity": random.randint(20, 150)
            },
            "govt_obs": {
                "funds_available_lakhs": random.randint(100, 1000),
                "infrastructure_damage": random.choice(["Low", "Moderate", "Severe"]),
                "public_panic_level": random.randint(1, 10)
            },
            "ngo_obs": {
                "volunteer_count": random.randint(50, 300),
                "relief_camps_active": random.randint(2, 10),
                "food_packets_available": random.randint(1000, 5000)
            },
            "media_obs": {
                "public_sentiment": random.choice(["Positive", "Anxious", "Outraged"]),
                "trending_hashtags": random.choice(["#RescueOps", "#DisasterRelief", "#WhereIsHelp"]),
                "news_coverage_intensity": random.randint(1, 10)
            }
        }