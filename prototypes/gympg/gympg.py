import gym


def main():
    env = gym.make("CartPole-v0")

    num_episodes = 5
    max_tries = 1000
    
    for i in range(num_episodes):
        observation = env.reset()
        score = 0

        for _ in range(max_tries):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            
            score += reward
            
            if done: break
        
        print(f"{i}: {done=}, {score=}")
    
    env.close()


if __name__ == "__main__":
    main()
