import random

#Possible Future Features: Holes, Height

def grid_count_bool(grid, test):
    count = 0
    for row in grid:
        for col in row:
            if col == test:
                count += 1
    return count

def c_count(state):
    return grid_count_bool(state.grid, "c")

def b_count(state):
    return grid_count_bool(state.grid, "b")

def stable(state):
    return 1

def max_height(state):
    for rind in range(len(state.grid)):
        for col in state.grid[rind]:
            if col != '_':
                return len(state.grid) - rind - 1
#for some reason "unstable" might be a bug in QLearningAgent
def weak_hole_count(state):
    count = 0
    grid = state.grid
    for row in range(1, len(grid) - 1):
        for col in range(len(grid[row])):
            if grid[row][col] == "_" and grid[row + 1][col] != "_" and grid[row - 1][col] != "_":
                count += 1
    return count

def c_cleared_reward(before, after):
    return c_count(before) - c_count(after)

features = []
class Player:
    def __init__(self, evaluator, numsteps=100, numtrails=1, epsilon=.05):
        self.evaluator = evaluator
        self.numsteps = numsteps
        self.numtrails = numtrails
        self.epsilon = epsilon

    def play_game(self, game):
        for i in range(self.numtrails):
            state = game.get_start_state()
            for _ in range(self.numsteps):
                if game.is_goal(state):
                    break
                succesor = self.pick_succesor(game, state)
                if succesor is None:
                    break
                self.evaluator.update(state, succesor)
                state = succesor[0]
            print("Trial: " + str(i) + "/" + str(self.numtrails))
            print("Game Done, End Board")
            print(state)
            print(self.evaluator)
        print("Trials done")
        print(self.evaluator)

    def pick_succesor(self, game, state):
        successors = game.get_successors(state)
        if successors == []:
            return None
        random.shuffle(successors)
        if random.random() < self.epsilon:
            return successors[0]
        values = list(map(lambda a: self.evaluator.value(a[0]) + a[2], successors))
        maxind = values.index(max(values))
        return successors[maxind]




class QFeatureAgent:
    def __init__(self, features, alpha= .000001, gamma = .96):
        self.features = features
        self.weights = dict()
        self.alpha = alpha
        self.gamma = gamma
        for feature in self.features:
            self.weights[feature] = 0.0

    def __repr__(self):
        return str(self.weights)

    def set_weight(self, func, val):
        self.weights[func] = val

    def value(self, state):
        total = 0
        for feature in self.features:
            total += self.weights[feature] * feature(state)
        return total

    #succesor tuple of (next state, action, reward)
    def update(self, original, successor):
        difference = successor[2] + self.gamma * self.value(successor[0]) - self.value(original)
        for feature in self.features:
            self.weights[feature] = self.weights[feature] + self.alpha * difference * feature(original)
        difference = difference + 0


#PROBLEM: Instability with max_hegiht and weak_hole_count,
# is it a bug or a consequence of how problem is set up, will investigate later
from simpletetris import CheeseGameLocked, Piece
tqfeature = QFeatureAgent([c_count, b_count, max_height, weak_hole_count, stable])
"Below I've listed where the values fall, as close as this is going to get, not good enough, need more"
tqfeature.set_weight(c_count,  0.29405214714047423)
tqfeature.set_weight(b_count, -0.3120097818120923)
tqfeature.set_weight(max_height, -0.673233201061796)
tqfeature.set_weight(weak_hole_count, -0.5826443124031087)
tqfeature.set_weight(stable, -2.1236049500924117)
tplayer = Player(tqfeature, 100, 1000)
game = CheeseGameLocked()
game.set_reward(c_cleared_reward)
tplayer.play_game(game)
