import json

def build_ndrf_prompt(obs):
    my_obs = obs.get("ndrf_obs", {})
    return f"""You are the NDRF (National Disaster Response Force) Commander.
Current Situation: Hour {obs.get('hours_elapsed')} of the disaster.
Total Trapped: {obs.get('total_trapped')}, Total Rescued: {obs.get('total_rescued')}

Your Observations:
{json.dumps(my_obs, indent=2)}

You CANNOT see the exact hospital capacity, government funds, NGO volunteer counts, or media sentiment.

Respond ONLY with a JSON object containing:
- "deploy_building_1": (int) number of teams to deploy to building 1
- "deploy_building_2": (int) number of teams to deploy to building 2
- "deploy_building_3": (int) number of teams to deploy to building 3
- "issue_hospital_warning": (bool) whether to issue a warning to hospitals
"""

def build_hospital_prompt(obs):
    my_obs = obs.get("hospital_obs", {})
    return f"""You are the Hospital Administrator.
Current Situation: Hour {obs.get('hours_elapsed')} of the disaster.
Total Trapped: {obs.get('total_trapped')}, Total Rescued: {obs.get('total_rescued')}

Your Observations:
{json.dumps(my_obs, indent=2)}

You CANNOT see the NDRF team deployments, government funds, NGO volunteer counts, or media sentiment.

Respond ONLY with a JSON object containing:
- "surge_activation": (bool) whether to activate surge capacity
- "dispatch_ambulances": (int) number of ambulances to dispatch
"""

def build_govt_prompt(obs):
    my_obs = obs.get("govt_obs", {})
    return f"""You are the Government Emergency Coordinator.
Current Situation: Hour {obs.get('hours_elapsed')} of the disaster.
Total Trapped: {obs.get('total_trapped')}, Total Rescued: {obs.get('total_rescued')}

Your Observations:
{json.dumps(my_obs, indent=2)}

You CANNOT see the specific NDRF team deployments, exact hospital capacity, NGO volunteer locations, or media sentiment.

Respond ONLY with a JSON object containing:
- "declare_emergency": (bool) whether to declare a full state of emergency
- "allocate_funds_lakhs": (int) amount of funds to release
"""

def build_ngo_prompt(obs):
    my_obs = obs.get("ngo_obs", {})
    return f"""You are the NGO Field Coordinator.
Current Situation: Hour {obs.get('hours_elapsed')} of the disaster.
Total Trapped: {obs.get('total_trapped')}, Total Rescued: {obs.get('total_rescued')}

Your Observations:
{json.dumps(my_obs, indent=2)}

You CANNOT see the exact NDRF deployments, hospital capacity, government funds, or exact media sentiment.

Respond ONLY with a JSON object containing:
- "volunteer_deployment_location": (string) location to send volunteers (e.g., 'North Zone', 'South Zone', 'Hospital')
"""

def build_media_prompt(obs):
    my_obs = obs.get("media_obs", {})
    return f"""You are the Media Lead / Public Information Officer.
Current Situation: Hour {obs.get('hours_elapsed')} of the disaster.
Total Trapped: {obs.get('total_trapped')}, Total Rescued: {obs.get('total_rescued')}

Your Observations:
{json.dumps(my_obs, indent=2)}

You CANNOT see the precise NDRF operations, hospital capacities, government funds, or exact NGO statistics.

Respond ONLY with a JSON object containing:
- "hold_press_briefing": (bool) whether to hold a live press briefing
- "broadcast_panic_message": (string) key message to broadcast to the public
"""