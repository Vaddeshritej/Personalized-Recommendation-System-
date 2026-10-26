"""
explanation_module.py
Generates a short natural-language explanation for each ranked movie
by querying the local Ollama model.
"""

import pandas as pd

from utils import print_heading, query_ollama


def generate_explanations(ranked: pd.DataFrame, profile: dict, analysis: dict) -> dict:
    """
    Calls Ollama once per movie to explain why it fits the user.
    Returns a dict of {title: explanation_text}.
    """
    explanations = {}
    if ranked.empty:
        return explanations

    for _, row in ranked.iterrows():
        genres = ", ".join(row["genres_list"]) if row["genres_list"] else "unknown genres"
        overview = row["overview"][:300] if isinstance(row["overview"], str) else ""

        movie_prompt = (
            f"User profile: interests={analysis['primary_interest']}, "
            f"goal={analysis['goal']}, preferred category={analysis['preferred_category']}. "
            f"Movie: '{row['title']}' (Genres: {genres}). "
            f"Overview: {overview} "
            f"In 2 short sentences, explain why this movie suits the user."
        )
        explanations[row["title"]] = query_ollama(movie_prompt)

    return explanations


def display_explanations(explanations: dict):
    """Prints each movie's explanation under the EXPLANATIONS heading."""
    print_heading("EXPLANATIONS")
    if not explanations:
        print("No explanations available yet. Generate recommendations first.")
        return
    for title, text in explanations.items():
        print(f"\n{title}:")
        print(f"  {text}")
