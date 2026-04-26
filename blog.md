---
title: Triage Wars — Teaching AI to Save Lives Through Multi-Agent Coordination
tags:
  - reinforcement-learning
  - multi-agent
  - disaster-response
  - qwen2.5
  - grpo
  - lora
  - openenv
---

# Triage Wars: When Coordination is the Difference Between Life and Death

The TV screen flickered with the terrifying images we had seen too many times before. It was 2023, and the Wayanad landslides were tearing through entire villages. We watched as a news anchor, his voice thick with exhaustion, described rescue teams standing by just miles away from trapped families. They were unable to reach them simply because they had been sent to the wrong coordinates. We watched as paramedics waited at makeshift hospitals with empty beds, while on the ground, volunteers desperately dug through the thick mud with their bare hands, unaware that professional medical help was so close. 

Growing up as engineering students in India, we watched this tragic story repeat itself. We saw the Uttarakhand floods devastate the mountains in 2013, the Gujarat earthquakes shatter lives earlier in our childhood, and countless other crises where the margins between life and death were razor thin. Every single time, the chaotic aftermath revealed the exact same heartbreaking truth: people weren’t dying because there was a lack of resources, a lack of funding, or a lack of brave heroes. They were dying because of coordination failures. 

During a disaster, five different agencies might be on the ground—the government, the military, local police, hospitals, and NGOs—but they are all operating in their own information silos. When communication lines snap and panic sets in, a dozen life-saving decisions must be made in the dark. 

This genuine frustration is what led us to build **Triage Wars** for the Meta OpenEnv Hackathon. We asked ourselves a simple question: What if we could use AI not to replace human heroes, but to teach disparate agencies how to coordinate perfectly when every second counts?

## Building the Chaos: The Triage Wars Environment

We wanted to build something that mirrored the messy, fragmented reality of a disaster zone. We didn't want an omniscient AI that magically knows where everything is; we wanted a simulation of real life. So, using **FastAPI** and Meta's **OpenEnv**, we built a multi-agent reinforcement learning (RL) environment simulating the aftermath of a devastating earthquake. 

In this environment, we created five distinct AI agents. But to us, they aren't just blocks of code; they are the digital counterparts of the very real people who step up when disaster strikes. 

Crucially, each agent operates with *partial observability*. They only know what they can see from their specific vantage point, just like humans in the thick of a crisis:

*   **The NDRF (National Disaster Response Force) Agent**: These are the boots on the ground. They can see the immediate debris, the trapped victims directly in front of them, and the immediate physical hazards. But they are blind to the hospital capacity miles away, or the long-term resource availability.
*   **The Hospital Agent**: Operating in the chaotic triage center, they manage life and death based on incoming medical supplies, available beds, and patient severity. But they cannot see the live conditions at the disaster site or the transportation bottlenecks slowing down the ambulances.
*   **The Government Agent**: Sitting in the command control room, they see the high-level metrics—overall budget, broad casualty reports, and mass resource allocation. However, they lack the granular, site-specific details, like the exact location of a specific trapped family.
*   **The NGO Agent**: They coordinate the community volunteers and local supply distribution points. They know the neighborhood's pulse better than anyone, but they are completely shut out of classified government data and specialized medical supply levels.
*   **The Media Agent**: They are the bridge to the public, monitoring verified news updates, general alerts, and public sentiment. But they aren't privy to confidential, real-time tactical rescue plans.

Our goal was to drop these five agents into a simulated disaster and force them to do what human agencies struggle to do: talk to each other, share the right information at the right time, and save lives.

## The Breakthrough

Training five separate agents to communicate when they are essentially wearing blindfolds is incredibly difficult. For this massive task, we utilized the **Qwen2.5 1.5B** model, fine-tuning it using **GRPO** (Group Relative Policy Optimization) with **LoRA** (Low-Rank Adaptation) adapters. Because we were working with limited student resources, we ran our entire training pipeline on a humble **Google Colab T4 GPU**.

For the first few dozen episodes, it was pure chaos. The agents behaved exactly like uncoordinated, panicking human teams. The NDRF would rescue victims but send them to a hospital that was already full. The Government would allocate precious resources to areas the NGO had already covered. The score was dismal; in Episodes 1-10, our average reward—a metric directly tied to lives saved and efficient coordination—hovered at just **23.42**.

But then, something incredible started to happen. 

As we pushed through the **200 training episodes**, feeding real environment rewards back for gradient updates, we watched the model genuinely learn. The agents started to form a shared, cohesive understanding of the disaster zone. The NDRF agent learned to query the Hospital agent before dispatching victims. The Government agent started listening to the NGO's local insights to allocate resources more effectively.

It felt like a profound breakthrough moment. We weren't just watching a loss curve go down on a monitor; we were watching digital responders learn to collaborate and save lives. By Episodes 191-200, the average reward had climbed to **36.63**—an overall improvement of **56.4%**. The reward curve wasn't just a graph to us; it was mathematical proof that the devastating coordination silos we’d watched on the news could actually be broken down.

![Triage Wars Training Reward Curve](https://huggingface.co/132ragini/triage-wars-llm/resolve/main/reward_curve_final%20(1).png)
*The reward curve across 200 training episodes. The red moving average line shows the agent improving from 23.42 to 36.63 — a 56.4% improvement in coordination quality.*

## Why This Matters

We didn't build Triage Wars just to win a hackathon. We built it because we genuinely believe this technology can be a blueprint for the future of disaster management.This is named triage wars because triage itself means sorting and prioritizing based on urgency and availability of resources.In our case these resources are the NDRF teams, hospital capacity, government funds and NGO volunteers.

Imagine a world where real-world response commanders can sit down in a risk-free simulation and practice coordinating against AI agents that mimic the unpredictability of a real crisis. Imagine using these models to predict resource bottlenecks before they happen, allowing governments to position life-saving supplies exactly where they will be needed. 

Most importantly, we hope to demonstrate mathematically that shared intelligence and coordinated action save more lives than isolated heroics. 

## Try It Yourself

We want to share this work with the world. We’ve open-sourced our models, the environment, and the code so you can run Triage Wars yourself, break it, improve it, and perhaps help us take it further.

*   **Model:** [huggingface.co/132ragini/triage-wars-llm](https://huggingface.co/132ragini/triage-wars-llm)
*   **Environment:** [huggingface.co/spaces/132ragini/triage-wars-env](https://huggingface.co/spaces/132ragini/triage-wars-env)
*   **Environment API Docs:** [132ragini-triage-wars-env.hf.space/docs](https://132ragini-triage-wars-env.hf.space/docs)
*   **GitHub:** [github.com/PiyushJha-25/triage-wars](https://github.com/PiyushJha-25/triage-wars)
*   **Training Notebook:** [Open in Colab](https://colab.research.google.com/drive/1vyvgkzfMS4R22RY8nZF7PRWmgG8DPKA_?usp=sharing)
*   **Blog:** [huggingface.co/132ragini/triage-wars-llm](https://huggingface.co/132ragini/triage-wars-llm)

## What's Next

We are just two engineering students, but our vision for this project is vast. Our immediate next steps are to integrate actual historical data from the NDRF to make the simulations even more realistic. We want to scale up to larger foundational models capable of more complex, multi-step planning, and introduce even more agents to represent local law enforcement and civilian volunteer networks. 

When the next disaster strikes, we don't want to be helplessly watching coordination failures on the news. We want to know that the teams on the ground have the best possible training and systems to work as one. That’s what Triage Wars is all about.
