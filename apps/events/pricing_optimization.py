import numpy as np
import random

class DynamicPricingRL:
    def __init__(self, event, alpha=0.1, gamma=0.9, epsilon=0.2):
        """
        Initialize the dynamic pricing model for an event.
        Parameters:
        - event: Event object from the models
        - alpha: Learning rate (how fast the model updates)
        - gamma: Discount factor (how much future rewards are considered)
        - epsilon: Exploration rate (probability to explore versus exploit)
        """
        self.event = event
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Initialize states (remaining slots, time to event)
        self.states = self.get_states()

        # Actions: list of price adjustments
        self.actions = [-5, 0, 5, 10]  # Adjust price by -5, 0, 5, 10
        self.q_table = self.initialize_q_table()

    def get_states(self):
        """ Define the states based on available slots and days to the event."""
        remaining_slots = self.event.available_slots
        days_to_event = (self.event.start_datetime - self.get_current_time()).days
        return (remaining_slots, days_to_event)

    def get_current_time(self):
        """ Get the current time (useful for testing and getting real-time). """
        from django.utils import timezone
        return timezone.now()

    def initialize_q_table(self):
        """ Initialize Q-table where the state-action pairs will be stored."""
        remaining_slots = self.event.available_slots
        days_to_event = (self.event.start_datetime - self.get_current_time()).days

        # States as tuples (remaining slots, days to event)
        states = [(r, d) for r in range(remaining_slots + 1) for d in range(days_to_event + 1)]
        q_table = {}
        for state in states:
            q_table[state] = {action: 0 for action in self.actions}
        return q_table

    def choose_action(self, state):
        """ Epsilon-greedy policy to choose an action (price adjustment). """
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Explore: random action
        else:
            return max(self.q_table[state], key=self.q_table[state].get)  # Exploit: best action

    def update_q_table(self, state, action, reward, next_state):
        """ Q-learning update rule. """
        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def simulate_step(self, demand):
        """ Simulate one step of the reinforcement learning process. """
        current_state = self.get_states()

        # Choose an action (price adjustment)
        action = self.choose_action(current_state)
        self.event.dynamic_price = max(0, self.event.price + action)  # Adjust price but keep non-negative
        self.event.save()

        # Simulate reward: higher demand = higher reward
        reward = self.calculate_reward(demand)

        # Move to the next state (after some time passes)
        next_state = self.get_states()

        # Update the Q-table based on the action and reward
        self.update_q_table(current_state, action, reward, next_state)

    def calculate_reward(self, demand):
        """
        Calculate the reward based on demand and price.
        Higher demand and lower remaining slots yield higher reward.
        """
        remaining_slots = self.event.available_slots
        if demand > remaining_slots:
            return -10  # Negative reward if there are no enough slots
        else:
            return demand  # Reward is proportional to demand

    def run_simulation(self, demand_over_time):
        """ Run the entire reinforcement learning simulation over time. """
        for demand in demand_over_time:
            self.simulate_step(demand)
            # In a real-world application, you can loop through actual participation data.

        # Return the optimized price at the end of simulation
        return self.event.dynamic_price
