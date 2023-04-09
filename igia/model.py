from mesa import Agent, Model
from mesa import time, space
from mesa.datacollection import DataCollector

from mimesis import Person
from mimesis.locales import Locale


def performers(model):
    
    return sum(1 for agent in model.schedule.agents if agent.stocks > 15)
    

def non_performers(model):

    return sum(1 for agent in model.schedule.agents if agent.stocks < 15)


class TraderAgent(Agent):  # noqa
    """
    An agent
    """

    def __init__(self, unique_id, name, model):
        """
        Customize the agent
        """
        self.unique_id = unique_id
        self.name = name
        super().__init__(unique_id, model)

        self.stocks = 15
        self._worth = 1

    @property  
    def wealth(self):
        return self.stocks * self._worth
    
    @wealth.setter
    def wealth(self, value):
        raise ValueError(f"Agent's wealth is {self.wealth} and cannot be changed!")
    
    @property
    def worth(self):
        return self._worth
    
    @worth.setter
    def worth(self, value):
        self._worth = value

    def step(self):
        """
        Modify this method to change what an individual agent will do during each step.
        Can include logic based on neighbors states.
        """
        # print(f"hello, I am {self.name} with ID {self.unique_id}")

        self.exchange()
        self.move()

    def move(self):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
        )

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def exchange(self):
        if self.stocks == 0:
            return
        
        # any trader
        # other_trader = self.random.choice(self.model.schedule.agents)

        # traders on the same cell
        other_traders = self.model.grid.get_cell_list_contents([self.pos])

        # no trader in the same cell
        if len(other_traders) == 0:
            return

        other_trader = self.random.choice(other_traders)

        print(f"Hello, I am {self.name} with {self.stocks} stocks"
             f" I am giving 1 stock to {other_trader.name} with {other_trader.stocks} stocks")
        
        other_trader.stocks += 1
        self.stocks -= 1



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
            model_reporters={"Performers": performers,
                             "Non Performers": non_performers}, 
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
