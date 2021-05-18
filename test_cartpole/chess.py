import gym
import gym_chessven
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

env = make_vec_env('gym_chessven:chessven-v0', n_envs=4)
#model = PPO2(MlpPolicy, env, verbose=1)
model = PPO2.load("ppo2_chess_black", env)
model.learn(total_timesteps=1000000 )
model.save("ppo2_chess_black")

del model # r
