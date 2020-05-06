import wandb
from wandb.keras import WandbCallback
wandb.init(project="minesweeper")
from minesweeper import Agent
import numpy as np
from board import Env
from utils import plotLearning
import tensorflow as tf

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    env= Env(20,20,0,0,0.3);
    lr = 0.001
    n_games = 1000
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr,input_dims=(9,),n_actions=8, mem_size=1000000, batch_size=64,epsilon_end=0.01)
    scores = []
    eps_history = []
    maxx=0
    print("Training started")
    for i in range(n_games):
        done = False
        score = 0
        #env.printBoard()
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action)
            score += reward
            if(score>maxx):
                maxx=score
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score,
        'max so far %.2f' %maxx,
        'average_score %.2f' % avg_score,
        'epsilon %.2f' % agent.epsilon)
    print("Training complete")
    print()
    print("start playing")
    for i in range(10):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action)
            score += reward
            if(score>maxx):
                maxx=score
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
        env.printGrid()
        print("total moves taken: ",env.getTotalMoves())
        print("total number of mines: ",env.getTotalMines())
        print("no. of mines destroyed: ",env.getMinesDestroyed())

    filename = 'mineSweeper_tf2.png'
    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
