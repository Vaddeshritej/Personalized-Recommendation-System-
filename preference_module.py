"""
preference_module.py
Analyzes the raw profile into a structured preference summary:
primary/secondary interests, skill level, goal, preference and constraints.
"""

from utils import print_heading


def analyze_preferences(profile: dict) -> dict:
    """Breaks the profile down into a structured analysis dict."""
    interests_list = [i.strip() for i in profile["interests"].split(",") if i.strip()]
    if not interests_list:
        interests_list = ["general"]

    primary_interest = interests_list[0]
    secondary_interests = interests_list[1:] if len(interests_list) > 1 else []

    preferences_list = [p.strip() for p in profile["preferences"].split(",") if p.strip()]
    constraints = [p for p in preferences_list if p.lower() != "none"]

    analysis = {
        "primary_interest": primary_interest,
        "secondary_interests": secondary_interests,
        "skill_level": profile["skill_level"],
        "goal": profile["goal"],
        "preferred_category": profile["preferred_category"],
        "constraints": constraints,
        "search_terms": interests_list + [profile["preferred_category"]],
    }
    return analysis


def display_preferences(analysis: dict):
    """Prints the preference analysis under the PREFERENCE ANALYSIS heading."""
    print_heading("PREFERENCE ANALYSIS")
    print(f"Primary Interest    : {analysis['primary_interest']}")
    secondary = ", ".join(analysis["secondary_interests"]) if analysis["secondary_interests"] else "None"
    print(f"Secondary Interests : {secondary}")
    print(f"Skill Level         : {analysis['skill_level']}")
    print(f"Goal                : {analysis['goal']}")
    print(f"Preferred Category  : {analysis['preferred_category']}")
    constraints = ", ".join(analysis["constraints"]) if analysis["constraints"] else "None"
    print(f"Constraints         : {constraints}")
