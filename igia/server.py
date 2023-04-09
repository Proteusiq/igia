"""
Configure visualization elements and instantiate a server
"""

from .model import TraderModel, TraderAgent  # noqa

import mesa


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
        portrayal["Layer"] = 0
    elif agent.stocks < 15:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 20, 20, 500, 500
)
chart_element = mesa.visualization.ChartModule([{"Label": "Performers", "Color": "green"},
                                                {"Label": "Non Performers", "Color": "red"},
                                                ],
                                               data_collector_name="datacollector",)

model_kwargs = {"num_agents": 10, "width": 10, "height": 10}

server = mesa.visualization.ModularServer(
    TraderModel,
    [canvas_element, chart_element],
    "Igia",
    model_kwargs,
)
