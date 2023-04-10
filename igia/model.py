from mesa import Model
from mesa import time, space
from mesa.datacollection import DataCollector

from mimesis import Person
from mimesis.locales import Locale

from .agent import TraderAgent



def performers(model):
    return sum(1 for agent in model.schedule.agents if agent.stocks > 15)


def middle_performers(model):
    return sum(1 for agent in model.schedule.agents if 12 <= agent.stocks <= 15)


def non_performers(model):
    return sum(1 for agent in model.schedule.agents if agent.stocks < 12)



class TraderModel(Model):
    """
    The model class holds the model-level attributes, manages the agents, and generally handles
    the global level of our model.

    There is only one model-level parameter: how many agents the model contains. When a new model
    is started, we want it to populate itself with the given number of agents.

    The scheduler is a special model component which controls the order in which agents are activated.
    """

    def __init__(self, num_agents, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = time.RandomActivation(self)
        self.grid = space.MultiGrid(width=width, height=height, torus=True)

        person = Person(Locale.EN)
        for _ in range(self.num_agents):
            agent = TraderAgent(person.username(), person.full_name(), self)
            self.schedule.add(agent)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # example data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Performers": performers,
                "Mid Performers": middle_performers,
                "Non Performers": non_performers,
            },
        )

        self.running = True

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.datacollector.collect(self)

        self.schedule.step()

        # 1 zero stocks
        if sum(1 for trader in self.schedule.agents if trader.stocks == 0) == 1:
            self.running = False
