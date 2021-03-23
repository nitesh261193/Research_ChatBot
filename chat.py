import random
import warnings

from rasa_core.agent import Agent
from rasa_nlu.model import Interpreter

import feedback
import history
from voicechat import speak, record_audio

warnings.filterwarnings("ignore")

Out_of_context_query_response = ["I am not able to understand what you are saying. you can ask about me ",
                                 "Your query is not on my slots. Could you please be specific like about me  ?",
                                 "Pls talk something else, couldn't get you clearly. ask regarding me",
                                 "Don't know much about it "]

After_feedback_query_response = ["Thanks for correcting me. ",
                                 "I'll update my information in next session. thanks a lot",
                                 "I'll consider this info. Thanks a lot"]


def random_response(response):
    index_response = random.randint(0, len(response) - 1)
    return response[index_response]


def return_index_of_element_in_list(intents_list, intent):
    if len(intents_list) == 0:
        raise RuntimeError("intents_list can't be empty")

    for i in range(len(intents_list) - 1, -1, -1):
        if intents_list[i] == intent:
            return i


def format_history_response(history_response):
    # todo implement
    return f'Hi.. I am Trump - Bot Assistant : We talked about: {history_response}\nHow can I help you today?'


def chat():
    model_directory = r"models/nlu/default/current"
    interpreter = Interpreter.load(model_dir=model_directory)
    agent = Agent.load('models/dialogue', interpreter=model_directory)
    intent_saved = []
    response_save_list = []

    with history.HistorySaver() as history_saver:
        response = "May I know your first name please?"
        history_saver.update_bot_response(response)
        # speak(response)
        print(response)
        while True:
            # a = record_audio()
            a = yield
            if not a.strip():
                continue

            history_saver.update_user_response(a)
            history_response = history_saver.get_history_based_response(a)
            if history_response:
                response = format_history_response(history_response)
                history_saver.update_bot_response(response)
                print(response)
                yield response
                # speak(response)
            else:
                response = "Hi.. I am Trump - Bot Assistant : We are talking for the first time. It's exciting!"
                history_saver.update_user_response(response)
                print(response)
                yield response
                # speak(response , s.loud)
            break

        while True:
            # a = record_audio()
            a = yield
            if not a.strip():
                continue

            history_saver.update_user_response(a)
            if a == 'stop':
                break

            if len(intent_saved) > 1 and intent_saved[-1] in "improvement":
                response = random_response(After_feedback_query_response)
                response_save_list.append(response)
                history_saver.update_bot_response(response)
                print(response)
                yield response
                # speak(response)
                intent_saved.append("custom")

                index = return_index_of_element_in_list(intent_saved, "improvement")
                if not index:
                    raise RuntimeError("This should not happen")

                save_improvement = intent_saved[index - 1]
                incorrect_response = response_save_list[index - 1]
                correct_answer = a
                print(
                    f"Will update intent:[{save_improvement}] having response:[{incorrect_response}] to [{correct_answer}]")
                yield f"Will update intent:[{save_improvement}] having response:[{incorrect_response}] to [{correct_answer}]"
                feedback.update_feed_back(save_improvement, incorrect_response, correct_answer)
            else:
                if interpreter.parse(a).get("intent")["confidence"] < 0.25:
                    response = random_response(Out_of_context_query_response)
                    history_saver.update_bot_response(response)
                    print(response)
                    yield response
                    # speak(response)
                    continue

                responses = agent.handle_message(a)
                for response in responses:
                    history_saver.update_bot_response(response["text"])
                    response_save_list.append(response["text"])
                    print(response["text"])
                    yield response["text"]
                    # speak(response["text"])
                    intent_saved.append(interpreter.parse(a).get("intent").get("name"))


if __name__ == '__main__':
    feedback.improve_using_feedback()
    chat()
