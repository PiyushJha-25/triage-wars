---
title: Triage Wars
emoji: 🚨
colorFrom: red
colorTo: red
sdk: docker
pinned: false
---
# Triage-wars
Multi-agent disaster response AI environment

We've both grown up watching disaster news in India — Uttarakhand, Wayanad, Gujarat. Every time the story is the same: help existed but coordination failed.
In the 2023 Uttarakhand floods people died because help did not arrive on time. The reason was that NDRF, hospitals and government teams could not work together enough. We created an AI system to solve this problem. The AI aims to improve coordination between NDRF, hospitals and government teams. This way help can reach people faster in disasters, like floods.

## What is Triage Wars
Triage Wars is a multi-agent reinforcement learning environment that simulates what would happen after an earthquake. Five different AI agents need to work together to save people who are stuck, keep hospitals from getting too full, and calm down the public. Each agent only has some information about the disaster, which is important because it mimics the way people communicate in a real-world crisis.

## The 5 Agents

| Agent | What They See | What They Cannot See |
|---|---|---|
| **NDRF** | Teams available, per-building trapped and rescued counts | Hospital capacity, available funds, media panic |
| **Hospital** | Current hospital capacity, incoming warnings | Building collapse details, trapped counts, rescue progress |
| **Government** | Emergency declaration status, available funds | On-the-ground rescue progress, specific casualties |
| **NGO** | Volunteer counts, government clearance status | NDRF deployment plans, hospital capacity |
| **Media** | Public panic index, social media rumors | Actual casualty numbers, precise rescue metrics |

## Reward Function
- **Lives Saved:** High positive reward for successfully rescuing trapped civilians before time runs out.
- **Speed:** Time penalty for every hour elapsed to encourage urgency.
- **Hospital Communication:** Bonus points if the hospital is warned before a massive surge of casualties arrives.
- **No Duplicates:** Reward for efficient coordination without NDRF and NGOs deploying redundantly to the same building.
- **Panic Control:** Reward for issuing proper briefings and keeping the public panic index low.

## What The AI Learned
Before they got these AI agents trained, the whole simulation was just a total mess. Rescue crews would all run to one building, completely ignoring everywhere else. Hospitals were suddenly full of patients without any heads-up, and charity groups were basically doing the same job as the government, just getting in each other's way. Because nobody was really communicating, they wasted a huge amount of time, and a lot of the virtual people didn't make it.

But the amazing thing is what happened once these agents were trained. They pretty much learned how to work together by themselves.

The government agents learned to declare emergencies quickly, which let the non-profits legally jump in and lend a hand. Rescue teams realized they should warn hospitals before bringing in a whole bunch of patients. Even the media agents began stopping rumors from spreading, just to help everyone stay calmer. It's genuinely impressive—they just naturally picked up on how to coordinate, and because of that, they ended up saving a lot more lives much faster.
Right now, the rescue rates we have are just simple simulations. If we could get real data from the NDRF and use it, things would be much more accurate.

![Reward Curve Placeholder](/placeholder/reward_curve.png)

## Real World Impact
- **Disaster Preparedness:** Provides a testing ground for real-world disaster response protocols to find bottlenecks before a crisis hits.
- **Resource Allocation:** AI can optimize the dispatch logic of critical but limited assets like helicopters and medical teams.
- **Silo Breakdown:** Demonstrates how establishing simple data-sharing pipelines between agencies dramatically increases overall efficiency.

## Links
- [HuggingFace Space](#)
- [Model Weights](#)
- [Google Colab](#)
- [Demo Video](#)

## How To Run
```bash
uvicorn triage_wars.server.app:app --host 0.0.0.0 --port 8000
```

