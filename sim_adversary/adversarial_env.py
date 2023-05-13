import gym
from gym import spaces
import numpy as np

DEFAULT_QUALITY = 1

def mbps_to_bps(mbps):
    return mbps * 125000



# Go step by step.
# Define your state first
# Define your action functions first
# Define how your state changes for an action

# THEN INVOLVE GYM
# Flow:
# Agent provides Bw and duration for first chunk - default quality
# Environment downloads chunk in that much time and returns state:
# State Includes:
# Blah
#


class AdversarialEnv(gym.Env):
    """Adversarial Environment to generate traces in which pensieve performs poorly"""
    metadata = {'render.modes': ['human']}

    def __init__(self, bw=(0.8, 4.8)):
        super(AdversarialEnv, self).__init__()
        
        self.bw_lo = bw[0]
        self.bw_hi = bw[1]
        self.state_dim = 1 # just bitrate for now
        
        self.last_bitrate = DEFAULT_QUALITY
        
        # Define action and observation space
        self.action_space = spaces.Box(low=[0.8, 0], high=[4.8, 24])  # 23.95 seconds to download largest chunk at lowest bitrate
        # Example for using image as input:
        self.dict_space = {
            "bitrate": spaces.Discrete(6)
        }
        self.observation_space = spaces.Dict(self.dict_space)
        
        
    def observe_state(self):
        obs = [self.last_bitrate]
        return obs
        

    # environment downloads the next chunk 
    def step(self, action):
        network_bw, duration = action
        obs = self.observe_state()
        reward, done, info = (0,0,0)
        return obs, reward, done, info
    
    def reset(self):
        self.last_bitrate = DEFAULT_QUALITY
        obs = [self.last_bitrate]
        return obs  # reward, done, info can't be included
    
    def render(self, mode='human'):
        pass
    
    def close (self):
        pass