import gymnasium as gym
from gymnasium.utils import EzPickle

class Snake(gym.Env, EzPickle):

    metadata = {
        'render.modes': ['human'],
        "render_fps": 50,
    }

    def __init__(self):
        # These are required
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(32, 32, 3), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(4)

        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass


