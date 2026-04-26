import asyncio
import random
import os
import aiohttp
import matplotlib.pyplot as plt

BASE_URL = "http://localhost:8080"

async def env_reset(session):
    async with session.post(f"{BASE_URL}/reset", json={}) as r:
        data = await r.json()
        return data.get("observation", data)

async def env_step(session, action):
    async with session.post(f"{BASE_URL}/step", json={"action": action}) as r:
        if r.status != 200:
            return {}, 0, True
        data = await r.json()
        obs = data.get("observation", {})
        reward = obs.get("current_reward", 0)
        done = obs.get("episode_done", False)
        return obs, reward, done

async def simulate_action():
    return {
        "ndrf_building_a_teams": random.randint(0, 3),
        "ndrf_building_b_teams": random.randint(0, 3),
        "ndrf_building_c_teams": random.randint(0, 3),
        "ndrf_hospital_warning": random.choice([True, False]),
        "ndrf_casualty_estimate": random.randint(100, 400),
        "hospital_surge_activated": random.choice([True, False]),
        "hospital_ambulances_deployed": random.randint(1, 8),
        "emergency_declared": random.choice([True, False]),
        "funds_released": random.randint(0, 2000),
        "ngo_building_assigned": random.choice(["A", "B", "C", "shelter"]),
        "ngo_volunteers_deployed": random.randint(50, 200),
        "press_briefing_issued": random.choice([True, False]),
        "panic_management_message": random.choice(["Stay calm", "Evacuate", "Help is coming"])
    }

def save_plots(episode_rewards, episode_rescued, episode):
    os.makedirs("outputs/plots", exist_ok=True)
    window_size = 10

    def moving_average(data):
        if len(data) < window_size:
            return []
        return [sum(data[i-window_size:i])/window_size for i in range(window_size, len(data)+1)]

    ma_rewards = moving_average(episode_rewards)
    ma_rescued = moving_average(episode_rescued)

    plt.figure(figsize=(10, 5))
    plt.plot(episode_rewards, label='Episode Reward', alpha=0.3)
    if ma_rewards:
        plt.plot(range(window_size-1, len(episode_rewards)), ma_rewards, label='Moving Avg (10)', color='red')
    plt.title('Training Rewards over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'outputs/plots/reward_curves_ep{episode}.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(episode_rescued, label='Lives Saved', alpha=0.3)
    if ma_rescued:
        plt.plot(range(window_size-1, len(episode_rescued)), ma_rescued, label='Moving Avg (10)', color='blue')
    plt.title('Lives Saved over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Lives Saved')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'outputs/plots/rescued_curves_ep{episode}.png')
    plt.close()

async def main():
    print("Starting 200 episodes...\n")
    episode_rewards = []
    episode_rescued = []

    async with aiohttp.ClientSession() as session:
        for episode in range(1, 201):
            obs = await env_reset(session)
            total_reward = 0
            total_rescued = 0

            for step in range(12):
                action = await simulate_action()
                obs, reward, done = await env_step(session, action)
                total_reward += reward
                total_rescued = obs.get("total_rescued", 0)
                if done:
                    break

            episode_rewards.append(total_reward)
            episode_rescued.append(total_rescued)

            if episode % 10 == 0:
                avg = sum(episode_rewards[-10:]) / 10
                print(f"Episode {episode:3d} | Reward: {total_reward:6.1f} | Avg(10): {avg:6.1f} | Rescued: {total_rescued}")

            if episode % 50 == 0:
                save_plots(episode_rewards, episode_rescued, episode)

    save_plots(episode_rewards, episode_rescued, 200)
    print("\nDone! Check outputs/plots/")

if __name__ == "__main__":
    asyncio.run(main())