import random

# Possible Future Features: Holes, Height


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


def w_something(state):
    total = 0
    r = 1.05
    grid = state.grid
    for rind in range(len(grid)):
        count = 0
        for col in grid[rind]:
            if col != "_":
                count += 1
        total += count * (r ** rind)
    return total / 70


def stable(state):
    return 1


def max_height(state):
    for rind in range(len(state.grid)):
        for col in state.grid[rind]:
            if col != "_":
                return len(state.grid) - rind - 1


# for some reason "unstable" might be a bug in QLearningAgent
def weak_hole_count(state):
    count = 0
    grid = state.grid
    for row in range(1, len(grid) - 1):
        for col in range(len(grid[row])):
            if (
                grid[row][col] == "_"
                and grid[row + 1][col] != "_"
                and grid[row - 1][col] != "_"
            ):
                count += 1
    return count


def weaker_hole_count(state):
    count = 0
    grid = state.grid
    for row in range(1, len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "_" and grid[row - 1][col] != "_":
                count += 1
    return count


# takado8 on github use this
def bumpiness(state):
    firstblock = []
    grid = state.grid
    for col in range(len(grid[0])):
        count = 0
        for row in range(len(grid)):
            if grid[row][col] != "_":
                break
            count += 1
        firstblock += [count]

    bump = 0
    for i in range(len(firstblock) - 1):
        bump += abs(firstblock[i + 1] - firstblock[i])
    return bump


def c_cleared_reward(before, after):
    return c_count(before) - c_count(after)


def any_cleared_reward(before, after):
    return 3 + grid_count_bool(after.grid, "_") - grid_count_bool(before.grid, "_")


def c_open(state):
    return state.top_row().count("c")


features = []


class Player:
    pass

    def __init__(self, evaluator, numsteps=100, numtrails=1, epsilon=0.05):
        self.evaluator = evaluator
        self.numsteps = numsteps
        self.numtrails = numtrails
        self.epsilon = epsilon

    def play_game(self, game):
        averagereward = 20.0
        successcount = 0
        for i in range(self.numtrails):
            totalreward = 0
            state = game.get_start_state()
            for _ in range(self.numsteps):
                if game.is_goal(state):
                    successcount += 1
                    break
                succesor = self.pick_succesor(game, state)
                if succesor is None:
                    break
                self.evaluator.update(state, succesor)
                totalreward += succesor[2]
                # print(state)
                state = succesor[0]
            print("Trial: " + str(i) + "/" + str(self.numtrails))
            print("Game Done, End Board")
            print(state)
            print(self.evaluator)
            averagereward = totalreward / (i + 1) + averagereward * (i) / (i + 1)
        print("Trials done")
        print(self.evaluator)
        print("Average: " + str(averagereward))
        print("SuccessCount: " + str(successcount))

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
    def __init__(self, features, alpha=0.00001, gamma=0.96):
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

    # succesor tuple of (next state, action, reward)
    def update(self, original, successor):
        difference = (
            successor[2] + self.gamma * self.value(successor[0]) - self.value(original)
        )
        for feature in self.features:
            self.weights[feature] = self.weights[
                feature
            ] + self.alpha * difference * feature(original)
        difference = difference + 0


# PROBLEM: Instability with max_hegiht and weak_hole_count,
# is it a bug or a consequence of how problem is set up, will investigate later
from simpletetris import CheeseGameLocked, Piece

tqfeature = QFeatureAgent(
    [c_count, b_count, max_height, weaker_hole_count, bumpiness, w_something, stable]
)
"Below I've listed where the values fall, as close as this is going to get, not good enough, need more"
"Note that below numbers are on top are for 100 (basically until it can't)"
" moves which due to suboptimality changes numbers, perhaps lower trials"
"more accurate"
# tqfeature.set_weight(c_count, 1.6)
# tqfeature.set_weight(b_count, 0.5)
# tqfeature.set_weight(max_height, -.25)
# tqfeature.set_weight(weaker_hole_count, -1.7)
# tqfeature.set_weight(bumpiness, -.15)
# tqfeature.set_weight(w_something, 1)
# tqfeature.set_weight(stable, 0)

tqfeature.set_weight(c_count, 0.5)
tqfeature.set_weight(b_count, -0.035)
tqfeature.set_weight(max_height, -0.35)
tqfeature.set_weight(weaker_hole_count, -1.85)
tqfeature.set_weight(bumpiness, -0.1)
tqfeature.set_weight(w_something, 0.94)
tqfeature.set_weight(stable, 0)
tplayer = Player(tqfeature, 10000, 1000, 0.005)
game = CheeseGameLocked(10, 20, 1, 9)
game.set_reward(c_cleared_reward)
tplayer.play_game(game)
