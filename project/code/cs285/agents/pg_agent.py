import numpy as np

from .base_agent import BaseAgent
from cs285.policies.MLP_policy import MLPPolicyPG
from cs285.infrastructure.replay_buffer import ReplayBuffer
from cs285.infrastructure.utils import normalize

class PGAgent(BaseAgent):
    def __init__(self, env, agent_params):
        super(PGAgent, self).__init__()

        # init vars
        self.env = env
        self.agent_params = agent_params
        self.gamma = self.agent_params['gamma']
        self.standardize_advantages = self.agent_params['standardize_advantages']
        self.nn_baseline = self.agent_params['nn_baseline']
        self.reward_to_go = self.agent_params['reward_to_go']

        # actor/policy
        self.actor = MLPPolicyPG(
            self.agent_params['ac_dim'],
            self.agent_params['ob_dim'],
            self.agent_params['n_layers'],
            self.agent_params['size'],
            discrete=self.agent_params['discrete'],
            learning_rate=self.agent_params['learning_rate'],
            nn_baseline=self.agent_params['nn_baseline'],
            normal=self.agent_params['normal']
        )

        # replay buffer
        self.replay_buffer = ReplayBuffer(1000000)

    def train(self, obs, acs, rews_list, next_obs, terminals):

        """
            Training a PG agent refers to updating its actor using the given observations/actions
            and the calculated qvals/advantages that come from the seen rewards.
        """

        # step 1: calculate q values of each (s_t, a_t) point, using rewards (r_0, ..., r_t, ..., r_T)
        q_values = self.calculate_q_vals(rews_list)

        # step 2: calculate advantages that correspond to each (s_t, a_t) point
        advantage_values = self.estimate_advantage(obs, q_values)

        # step 3: use all datapoints (s_t, a_t, q_t, adv_t) to update the PG actor/policy
        log = self.actor.update(obs, acs, advantage_values, qvals=q_values)
        return log

    def calculate_q_vals(self, rewards_list):

        """
            Monte Carlo estimation of the Q function.
        """

        # Case 1: trajectory-based PG
        # Estimate Q^{pi}(s_t, a_t) by the total discounted reward summed over entire trajectory
        if not self.reward_to_go:

            # For each point (s_t, a_t), associate its value as being the discounted sum of rewards over the full trajectory
            # In other words: value of (s_t, a_t) = sum_{t'=0}^T gamma^t' r_{t'}
            q_values = np.concatenate([self._discounted_return(r) for r in rewards_list])

        # Case 2: reward-to-go PG
        # Estimate Q^{pi}(s_t, a_t) by the discounted sum of rewards starting from t
        else:

            # For each point (s_t, a_t), associate its value as being the discounted sum of rewards over the full trajectory
            # In other words: value of (s_t, a_t) = sum_{t'=t}^T gamma^(t'-t) * r_{t'}
            q_values = np.concatenate([self._discounted_cumsum(r) for r in rewards_list])

        return q_values

    def estimate_advantage(self, obs, q_values):

        """
            Computes advantages by (possibly) subtracting a baseline from the estimated Q values
        """

        # Estimate the advantage as [Q-b], when nn_baseline is True,
        # by querying the neural network that you're using to learn the baseline
        if self.nn_baseline:
            b_n = self.actor.run_baseline_prediction(obs)
            assert b_n.ndim == q_values.ndim
            b_n = b_n * np.std(q_values) + np.mean(q_values)
            adv_n = q_values - b_n

        # Else, just set the advantage to [Q]
        else:
            adv_n = q_values.copy()

        # Normalize the resulting advantages
        if self.standardize_advantages:
            adv_n = normalize(adv_n, np.mean(adv_n), np.std(adv_n))

        return adv_n

    #####################################################
    #####################################################

    def add_to_replay_buffer(self, paths):
        self.replay_buffer.add_rollouts(paths)

    def sample(self, batch_size):
        return self.replay_buffer.sample_recent_data(batch_size, concat_rew=False)

    #####################################################
    ################## HELPER FUNCTIONS #################
    #####################################################

    def _discounted_return(self, rewards):
        """
            Helper function

            Input: list of rewards {r_0, r_1, ..., r_t', ... r_T} from a single rollout of length T

            Output: list where each index t contains sum_{t'=0}^T gamma^t' r_{t'}
                note that all entries of this output are equivalent
                because each sum is from 0 to T (and doesnt involve t)
        """

        # create a list of indices (t'): from 0 to T
        indices = np.arange(len(rewards))

        # create a list where the entry at each index (t') is gamma^(t')
        discounts = self.gamma ** indices

        # create a list where the entry at each index (t') is gamma^(t') * r_{t'}
        discounted_rewards = discounts * rewards

        # scalar: sum_{t'=0}^T gamma^(t') * r_{t'}
        sum_of_discounted_rewards = sum(discounted_rewards)

        # list where each entry t contains the same thing
        # it contains sum_{t'=0}^T gamma^t' r_{t'}
        list_of_discounted_returns = np.ones_like(rewards) * sum_of_discounted_rewards

        return list_of_discounted_returns

    def _discounted_cumsum(self, rewards):
        """
            Helper function which
            -takes a list of rewards {r_0, r_1, ..., r_t', ... r_T},
            -and returns a list where the entry in each index t' is sum_{t'=t}^T gamma^(t'-t) * r_{t'}
        """

        all_discounted_cumsums = []

        # for loop over steps (t) of the given rollout
        for start_time_index in range(len(rewards)):
            # create a list of indices (t'): goes from t to T
            indices = np.arange(start_time_index, len(rewards))

            # create a list of indices (t'-t)
            indices_adjusted = indices - start_time_index

            # create a list where the entry at each index (t') is gamma^(t'-t)
            discounts = self.gamma ** (indices_adjusted)  # each entry is gamma^(t'-t)

            # create a list where the entry at each index (t') is gamma^(t'-t) * r_{t'}
            discounted_rtg = discounts * rewards[start_time_index:]

            # scalar: sum_{t'=t}^T gamma^(t'-t) * r_{t'}
            sum_discounted_rtg = sum(discounted_rtg)
            all_discounted_cumsums.append(sum_discounted_rtg)

        list_of_discounted_cumsums = np.array(all_discounted_cumsums)
        return list_of_discounted_cumsums

