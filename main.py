# EcoSim is allowed to be used as an economy model in any game or project as long as you have explicit permission from the creator. DM import_laziness on Discord if you would like to ask for permission.
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt

# Agent classes

class Consumer(Agent):
    def __init__(self, unique_id, model, wealth):
        super().__init__(unique_id, model)
        self.wealth = wealth

    def step(self):
        self.buy_goods()

    def buy_goods(self):
        if self.wealth > 0:
            producer = random.choice(self.model.schedule.agents)
            if isinstance(producer, Producer) and producer.goods > 0:
                price = producer.price
                if self.wealth >= price:
                    producer.goods -= 1
                    self.wealth -= price
                    producer.wealth += price

class Producer(Agent):
    def __init__(self, unique_id, model, goods, price):
        super().__init__(unique_id, model)
        self.goods = goods
        self.price = price
        self.wealth = 0

    def step(self):
        self.produce_goods()

    def produce_goods(self):
        self.goods += 1

# Model class

class Economy(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            if i % 2 == 0:
                a = Consumer(i, self, wealth=random.randint(10, 50))
            else:
                a = Producer(i, self, goods=random.randint(5, 20), price=random.uniform(1, 10))
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Wealth": "wealth"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Visualization

def visualize_economy(model):
    agent_wealth = [a.wealth for a in model.schedule.agents if isinstance(a, Consumer)]
    plt.hist(agent_wealth, bins=range(0, 60, 5))
    plt.xlabel("Wealth")
    plt.ylabel("Number of Consumers")
    plt.title("Distribution of Wealth Among Consumers")
    plt.show()

# Run the model

model = Economy(N=50, width=10, height=10)
for i in range(100):
    model.step()

visualize_economy(model)

# Collecting data

wealth_data = model.datacollector.get_agent_vars_dataframe()
print(wealth_data.tail())
