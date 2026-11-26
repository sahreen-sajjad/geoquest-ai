from langgraph.graph import StateGraph, START, END

from backend.workflows.game_state import GameState
from backend.agents.quiz_agent import generate_quiz
from backend.agents.hint_agent import generate_hint
from backend.agents.evaluation_agent import evaluate_answer
from backend.agents.training_agent import recommend_training
from backend.storage.player_store import load_player, save_player
from backend.workflows.adaptive_difficulty import get_difficulty
from backend.agents.image_quiz_agent import generate_image_quiz


def route_action(state):

    if state["action"] == "quiz":
        if state["mode"] == "Street View":
            return "image_quiz"

    return state["action"]

builder = StateGraph(GameState)

builder.add_node("quiz_agent", generate_quiz)
builder.add_node("hint_agent", generate_hint)
builder.add_node("evaluation_agent", evaluate_answer)
builder.add_node("training_agent", recommend_training)
builder.add_node("image_quiz_agent", generate_image_quiz)

builder.add_conditional_edges(
    START,
    route_action,
    {
        "quiz": "quiz_agent",
        "image_quiz": "image_quiz_agent",
        "hint": "hint_agent",
        "evaluate":"evaluation_agent"
    }
)

builder.add_edge("quiz_agent", END)
builder.add_edge("hint_agent", END)
builder.add_edge("evaluation_agent", "training_agent")
builder.add_edge("training_agent", END)
builder.add_edge("image_quiz_agent", END)

game_graph = builder.compile()

if __name__ == "__main__":

    state = load_player()

    while True:

        state["action"] = "quiz"
        state["mode"] = "Landscape"
        state["difficulty"] = get_difficulty(
            state["history"]
        )

        state = game_graph.invoke(state)

        print("\n" + "=" * 50)
        print("Round:", state["round_number"])
        print("Difficulty:", state["difficulty"])
        print("Total score:", state["score"])
        print("=" * 50)

        print("\nQuestion:", state["question"])

        for option in state["options"]:
            print("-", option)

        while True:

            answer = input(
                "\nEnter answer, 'hint' or 'quit': "
            ).strip()

            if answer.lower() == "quit":
                save_player(state)
                raise SystemExit

            if answer.lower() == "hint":

                if state["hints_used"] >= 3:
                    print("No more hints available.")
                    continue

                state["action"] = "hint"
                state = game_graph.invoke(state)

                print("Hint:", state["hints"][-1])
                continue

            valid_answers = [
                option.casefold()
                for option in state["options"]
            ]

            if answer.casefold() not in valid_answers:
                print("Please select a valid option.")
                continue

            state["action"] = "evaluate"
            state["player_answer"] = answer

            state = game_graph.invoke(state)

            print("\nCorrect:", state["is_correct"])
            print("Answer:", state["correct_answer"])
            print("Total score:", state["score"])
            print("Feedback:", state["feedback"])

            print("\nTraining Recommendation:")
            print(state["training_recommendation"])

            state["round_number"] += 1

            save_player(state)

            break

        play_again = input(
            "\nPlay another round? (y/n): "
        )

        if play_again.strip().lower() != "y":
            break