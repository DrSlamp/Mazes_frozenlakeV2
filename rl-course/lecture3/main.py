import os
# RobotBattery-v0, FrozenLake-v1, FrozenLake-v2 , RobotBaterry-v0
import gym
import gym_environments
import time
from agent import MonteCarlo


# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

def train(env, agent, episodes):
    for _ in range(episodes):
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation)
            new_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(observation, action, reward, terminated)
            observation = new_observation


def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = True, False
    while not (terminated or truncated):
        action = agent.get_best_action(observation)
        observation, _, terminated, truncated, _ = env.step(action)
        
        env.render()
        time.sleep(40)


if __name__ == "__main__":
    env = gym.make("FrozenLake-v2", render_mode="human")
    
    agent = MonteCarlo(
        env.observation_space.n, env.action_space.n, gamma=0.9, epsilon=0.9 
      
    )

    train(env, agent, episodes=10)
    agent.render()

    play(env, agent)

    env.close()


