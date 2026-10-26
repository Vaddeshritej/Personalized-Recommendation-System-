"""
main.py
Entry point for the Personalized Recommendation System.
Orchestrates all modules through a terminal menu loop.
"""

from utils import print_heading

from input_module import collect_profile
from profile_module import display_profile
from preference_module import analyze_preferences, display_preferences
from prompt_module import generate_prompt, display_prompt
from recommendation_module import get_recommendations, display_recommendations
from ranking_module import rank_recommendations, display_ranking
from explanation_module import generate_explanations, display_explanations
from feedback_module import collect_feedback, refine_analysis, display_refined
from intent_module import detect_intent, display_intent
from save_module import save_recommendations


MENU_TEXT = """
1. Generate Recommendation
2. Show Profile
3. Explain Recommendation
4. Refine Recommendation
5. Save Recommendation
6. Exit
"""


class AppState:
    """Holds the session state shared across menu actions."""

    def __init__(self):
        self.profile = None
        self.analysis = None
        self.ranked = None
        self.explanations = {}
        self.excluded_titles = []


def action_generate(state: AppState):
    state.analysis = analyze_preferences(state.profile)
    display_preferences(state.analysis)

    prompt = generate_prompt(state.profile, state.analysis)
    display_prompt(prompt)

    recs = get_recommendations(
        state.analysis,
        top_n=state.profile["num_recommendations"],
        exclude_titles=state.excluded_titles,
    )
    display_recommendations(recs)

    state.ranked = rank_recommendations(recs, top_n=state.profile["num_recommendations"])
    display_ranking(state.ranked)

    state.explanations = generate_explanations(state.ranked, state.profile, state.analysis)
    display_explanations(state.explanations)


def action_show_profile(state: AppState):
    display_profile(state.profile)


def action_explain(state: AppState):
    if state.ranked is None or state.ranked.empty:
        print("No recommendations yet. Choose 'Generate Recommendation' first.")
        return
    display_explanations(state.explanations)


def action_refine(state: AppState):
    if state.ranked is None or state.ranked.empty:
        print("No recommendations yet. Choose 'Generate Recommendation' first.")
        return

    feedback = collect_feedback(state.ranked)
    state.excluded_titles.extend(feedback["disliked"])
    state.analysis = refine_analysis(state.analysis, feedback)

    recs = get_recommendations(
        state.analysis,
        top_n=state.profile["num_recommendations"],
        exclude_titles=state.excluded_titles,
    )
    state.ranked = rank_recommendations(recs, top_n=state.profile["num_recommendations"])
    display_refined(state.ranked)

    state.explanations = generate_explanations(state.ranked, state.profile, state.analysis)
    display_explanations(state.explanations)


def action_save(state: AppState):
    if state.ranked is None or state.ranked.empty:
        print("No recommendations yet. Choose 'Generate Recommendation' first.")
        return
    save_recommendations(state.profile, state.ranked, state.explanations)


ACTIONS_BY_NUMBER = {
    "1": ("GENERATE_RECOMMENDATION", action_generate),
    "2": ("SHOW_PROFILE", action_show_profile),
    "3": ("EXPLAIN_RECOMMENDATION", action_explain),
    "4": ("REFINE_RECOMMENDATION", action_refine),
    "5": ("SAVE_RECOMMENDATION", action_save),
}


def run_menu_choice(state: AppState, choice: str) -> bool:
    """
    Executes one menu choice. Returns False if the app should exit,
    True otherwise. Accepts either a menu number ('1'-'6') or free text,
    which is routed through intent detection.
    """
    if choice.strip() in ACTIONS_BY_NUMBER:
        intent, action = ACTIONS_BY_NUMBER[choice.strip()]
        display_intent(choice, intent)
        action(state)
        return True

    if choice.strip() == "6":
        display_intent(choice, "EXIT")
        return False

    # Free-text input: detect intent and route accordingly.
    intent = detect_intent(choice)
    display_intent(choice, intent)

    if intent == "EXIT":
        return False
    elif intent == "SHOW_PROFILE":
        action_show_profile(state)
    elif intent == "EXPLAIN_RECOMMENDATION":
        action_explain(state)
    elif intent == "REFINE_RECOMMENDATION":
        action_refine(state)
    elif intent == "SAVE_RECOMMENDATION":
        action_save(state)
    else:
        action_generate(state)

    return True


def main():
    state = AppState()
    state.profile = collect_profile()
    display_profile(state.profile)

    running = True
    while running:
        print(MENU_TEXT)
        choice = input("Choose an option (1-6) or type what you want: ").strip()
        running = run_menu_choice(state, choice)

    print("\nThank you for using the Personalized Recommendation System. Goodbye!")


if __name__ == "__main__":
    main()
