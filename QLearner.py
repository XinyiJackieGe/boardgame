import random

class Player():
    """A class that represents a player in the game"""
    
    def __init__(self, side):
        """
        Initialize a player with their coin type
        """
        self.side = side
        
    def complete_move(self):
        """
        A method to make a move and update any learning parameters if any
        """
        pass
    
    def get_side(self):
        """
        Return the coin type of the player
        """
        return self.side
    
    def set_side(self, side):
        """
        Set the coin type of a player
        """
        self.side = side
        
    
    
class QLearningPlayer(Player):
    """A class that represents an AI using Q-learning algorithm"""
    
    def __init__(self, side, epsilon=0.1, alpha=0.3, gamma=0.9):
        """
        Initialize a Q-learner with parameters epsilon, alpha and gamma
        and its coin type
        """
        Player.__init__(self, side)
        self.q = {}
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards 
        
    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 10
        return self.q.get((state, action))  
    
    def getWholeQ(self):  
        return self.q
        
    def choose_action(self, state, actions):
        """
        Return an action based on the best move recommendation by the current
        Q-Table with a epsilon chance of trying out a new move
        """
        current_state = state
        
        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]
    
    def learn(self, game, actions, chosen_action):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the maximum future reward
        based on the resulting state due to the chosen action
        """
        rewards = game.get_reward()
        if self.side == 'X':
            reward = rewards[0]
        else:
            reward = rewards[1]
        prev_state = game.get_prev_state()
        prev = self.getQ(prev_state, chosen_action)
        result_state = game.get_state()
        if actions:
            maxqnew = max([self.getQ(result_state, a) for a in actions])
        else:
            maxqnew = 0
        self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)    
        
    def complete_move(self, game):
        """
        Move the coin and decide which slot to drop it in and learn from the
        chosen move
        """
        game_over = False
        actions = game.get_available_moves(self.side)
        state = game.get_state()
        if actions:
            chosen_action = self.choose_action(state, actions)
            game.make_move(chosen_action[0][0], chosen_action[0][1], chosen_action[1])
            actions = game.get_available_moves(self.side)
            self.learn(game, actions, chosen_action)
        
        game_over = game.game_finish(self.side)
        return game_over
