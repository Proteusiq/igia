from mesa import Agent

class TraderAgent(Agent):
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
        all_traders = self.model.grid.get_cell_list_contents([self.pos])

        # no trader in the same cell
        if len(all_traders) < 2:
            return 

        other_traders = [agent for agent in all_traders if agent.unique_id != self.unique_id]
        other_trader = self.random.choice(other_traders)

        print(
            f"Hello, I am {self.name} with {self.stocks} stocks"
            f" I am giving 1 stock to {other_trader.name} with {other_trader.stocks} stocks"
        )

        other_trader.stocks += 1
        self.stocks -= 1


