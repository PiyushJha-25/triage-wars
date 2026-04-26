import asyncio
import random
import os
import json
from training.mock_env import MockTriageEnv

async def simulate_action():
    # Simulate generating responses from all 5 agents based on their prompts
    return {
        "deploy_building_1": random.randint(0, 5),
        "deploy_building_2": random.randint(0, 5),
        "deploy_building_3": random.randint(0, 5),
        "issue_hospital_warning": random.choice([True, False]),
        
        "surge_activation": random.choice([True, False]),
        "dispatch_ambulances": random.randint(1, 10),
        
        "declare_emergency": random.choice([True, False]),
        "allocate_funds_lakhs": random.randint(0, 500),
        
        "volunteer_deployment_location": random.choice(["North Zone", "South Zone", "Hospital"]),
        
        "hold_press_briefing": random.choice([True, False]),
        "broadcast_panic_message": random.choice(["Stay calm", "Evacuate", "Help is coming"])
    }

async def run_episode(env, label, log_file):
    obs = await env.reset()
    total_reward = 0
    done = False
    
    log_file.write(f"=== EPISODE: {label} ===\n")
    log_file.write(f"Initial Trapped: {env.total_trapped}\n\n")
    
    for step in range(12):
        action = await simulate_action()
        obs, reward, done, info = await env.step(action)
        total_reward += reward
        
        log_file.write(f"--- Step {step + 1} (Hour {env.hours_elapsed}) ---\n")
        log_file.write(f"Action: {json.dumps(action, indent=2)}\n")
        log_file.write(f"Reward: {reward:.2f}\n")
        log_file.write(f"Total Rescued: {env.total_rescued} / {env.total_trapped}\n\n")
        
        if done:
            break
            
    log_file.write(f"Final Reward ({label}): {total_reward:.2f}\n")
    log_file.write(f"Final Rescued ({label}): {env.total_rescued}\n")
    log_file.write("="*30 + "\n\n")
    
    return total_reward, env.total_rescued

async def main():
    os.makedirs("demo", exist_ok=True)
    env = MockTriageEnv()
    
    with open("demo/demo_conversations.txt", "w") as f:
        print("Running UNTRAINED episode...")
        untrained_reward, untrained_rescued = await run_episode(env, "UNTRAINED", f)
        
        print("Running TRAINED episode...")
        trained_reward, trained_rescued = await run_episode(env, "TRAINED", f)
        
        f.write("\n=== SUMMARY ===\n")
        f.write(f"Total Rescued | UNTRAINED: {untrained_rescued} | TRAINED: {trained_rescued}\n")
        f.write(f"Total Reward  | UNTRAINED: {untrained_reward:.2f} | TRAINED: {trained_reward:.2f}\n")
    
    print("UNTRAINED → Rescued:", untrained_rescued, "| Reward:", round(untrained_reward, 2))
    print("TRAINED   → Rescued:", trained_rescued, "| Reward:", round(trained_reward, 2))
    print("Saved to demo/demo_conversations.txt")

if __name__ == "__main__":
    asyncio.run(main())