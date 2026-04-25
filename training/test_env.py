import asyncio
from triage_wars.client import TriageWarsEnv
from triage_wars.models import TriageAction

async def main():
    async with TriageWarsEnv("ws://localhost:8000") as env:
        # Reset and print
        result = await env.reset()
        print(f"Total Trapped: {result.observation.total_trapped}")
        print(f"Hours Elapsed: {result.observation.hours_elapsed}")
        
        # Step and print
        action = TriageAction()
        result = await env.step(action)
        print(f"Current Reward: {result.observation.current_reward}")
        print(f"Episode Done: {result.observation.episode_done}")

if __name__ == "__main__":
    asyncio.run(main())
