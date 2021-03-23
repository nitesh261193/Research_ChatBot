from rasa_core.agent import Agent
from rasa_core.policies import MemoizationPolicy, KerasPolicy
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.training_data import load_data


def train():
    training_data = load_data("nlu.md")
    trainer = Trainer(config.load("config.yml"))

    trainer.train(training_data)
    trainer.persist("./models/nlu", fixed_model_name="current")

    agent = Agent('domain.yml', policies=[MemoizationPolicy(), KerasPolicy()])

    training_data = agent.load_data('stories.md')

    agent.train(
        training_data,
        validation_split=0.0,
        epochs=100
    )

    agent.persist('models/dialogue')


if __name__ == '__main__':
    train()
