"""
feedback_module.py
Collects user feedback on the current recommendations and produces an
updated preference analysis + exclusion list used to refine results.
"""

from utils import print_heading


def collect_feedback(ranked) -> dict:
    """
    Asks the user which movies they liked/disliked and whether they want
    to add extra interest keywords. Returns a structured feedback dict.
    """
    print_heading("USER FEEDBACK")

    if ranked is None or ranked.empty:
        print("No recommendations to give feedback on yet. Generate some first.")
        return {"disliked": [], "extra_keywords": []}

    print("Current recommendations:")
    for idx, row in ranked.iterrows():
        print(f"  {idx + 1}. {row['title']}")

    disliked_raw = input(
        "\nEnter numbers of movies you DON'T want (comma separated, or press Enter to skip): "
    ).strip()
    disliked_titles = []
    if disliked_raw:
        for token in disliked_raw.split(","):
            token = token.strip()
            if token.isdigit():
                pos = int(token) - 1
                if 0 <= pos < len(ranked):
                    disliked_titles.append(ranked.iloc[pos]["title"])

    extra_raw = input(
        "Any additional interests/keywords to refine results? (comma separated, or Enter to skip): "
    ).strip()
    extra_keywords = [k.strip() for k in extra_raw.split(",") if k.strip()]

    return {"disliked": disliked_titles, "extra_keywords": extra_keywords}


def refine_analysis(analysis: dict, feedback: dict) -> dict:
    """Merges feedback keywords into the existing preference analysis."""
    updated = dict(analysis)
    if feedback.get("extra_keywords"):
        updated["search_terms"] = list(analysis["search_terms"]) + feedback["extra_keywords"]
        updated["secondary_interests"] = list(analysis["secondary_interests"]) + feedback["extra_keywords"]
    return updated


def display_refined(ranked):
    """Prints the refined recommendation list."""
    print_heading("REFINED RECOMMENDATIONS")
    if ranked.empty:
        print("No refined recommendations could be generated. Try different keywords.")
        return
    for idx, row in ranked.iterrows():
        print(f"{idx + 1}. {row['title']}  |  Suitability Score: {row['suitability_score']:.2f}/100")
