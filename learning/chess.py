import gym
import gym_chessven

import tensorflow as tf
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

policy_kwargs = dict(act_fun=tf.nn.tanh, net_arch=[64, 64, 64, 64])
env = make_vec_env('gym_chessven:chessven-v0', n_envs=4)
model = PPO2("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
print(model.get_parameter_list())
#model = PPO2(MlpPolicy, env, verbose=1)v2
#model = PPO2(MlpLstmPolicy, env, verbose=1)v2
#model = PPO2.load("ppo2_chess_mlp_v2", env)
model.learn(total_timesteps=2000000)
model.save("ppo2_chess_mlp_v3")

del model # r
