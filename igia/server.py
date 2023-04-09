"""
Configure visualization elements and instantiate a server
"""

from mesa import visualization as vs
from .model import TraderModel

NUM_CEILS = 20
SIZE_PIXEL_X = 860
SIZE_PIXEL_Y = 400

model_kwargs = {
    "num_agents": vs.NumberInput(
        name="Traders",
        value=10,
        description="Number of traders",
    ),
    "height": NUM_CEILS,
    "width": NUM_CEILS,
}


def circle_portrayal_example(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "Pink",
        "Name": agent.name,
        "Wealth": agent.wealth,
        "Layer": 0,
    }

    if agent.stocks > 15:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1

    elif agent.stocks < 15:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2

    return portrayal


canvas_element = vs.CanvasGrid(
    circle_portrayal_example, NUM_CEILS, NUM_CEILS, SIZE_PIXEL_X, SIZE_PIXEL_Y
)
chart_element = vs.ChartModule(
    [
        {"Label": "Performers", "Color": "green"},
        {"Label": "Mid Performers", "Color": "orange"},
        {"Label": "Non Performers", "Color": "red"},
    ],
    data_collector_name="datacollector",
)


server = vs.ModularServer(
    TraderModel,
    [canvas_element, chart_element],
    "Igia",
    model_kwargs,
)
