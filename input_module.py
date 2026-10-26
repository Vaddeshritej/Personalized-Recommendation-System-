"""
input_module.py
Collects the raw user profile from the terminal.
"""

from utils import print_heading, safe_int_input


def collect_profile() -> dict:
    """Prompts the user for all profile fields and returns them as a dict."""
    print_heading("PERSONALIZED RECOMMENDATION SYSTEM")
    print("Please answer the following questions to build your profile.\n")

    name = input("Name: ").strip() or "Guest"
    age = safe_int_input("Age: ", default=20)
    background = input("Background (e.g. student, engineer, artist): ").strip() or "Not specified"
    interests = input("Interests (comma separated, e.g. action, sci-fi, thriller): ").strip() or "general"
    skill_level = input("Skill Level (beginner/intermediate/expert - as a viewer/critic): ").strip() or "beginner"
    preferred_category = input("Preferred Category/Genre: ").strip() or "any"
    goal = input("Goal (e.g. relax, learn, family time, date night): ").strip() or "entertainment"
    preferences = input("Other Preferences (e.g. short movies, no violence, English only): ").strip() or "none"
    num_recommendations = safe_int_input("Number of Recommendations wanted (default 5): ", default=5)

    profile = {
        "name": name,
        "age": age,
        "background": background,
        "interests": interests,
        "skill_level": skill_level,
        "preferred_category": preferred_category,
        "goal": goal,
        "preferences": preferences,
        "num_recommendations": num_recommendations,
    }
    return profile
