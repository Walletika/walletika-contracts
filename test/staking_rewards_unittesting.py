import os
import unittest
os.chdir('..')


# Configuration
contract_name = "StakingRewards"
constructor_args = ()
contract_file_name = "StakingRewards.sol"
debugging = True


# Deployment
from deploy import w3, run
contract = run(contract_name, constructor_args, contract_file_name)
wtk_token = run("WalletikaToken", constructor_args, "Token.sol")
tst_token = run("WalletikaToken", constructor_args, "Token.sol")


def function_name(text: str):
    print(f"[ + ] Start for: {text}")


# Testing
class MyTestCase(unittest.TestCase):
    def test1_initial_details(self):
        function_name('initial_details')

        # Task
        owner = contract.functions.owner().call()
        smart_chef_factory = contract.functions.SMART_CHEF_FACTORY().call()
        has_user_limit = contract.functions.hasUserLimit().call()
        locked_to_end = contract.functions.lockedToEnd().call()
        is_initialized = contract.functions.isInitialized().call()
        is_paused = contract.functions.paused().call()
        last_pause_time = contract.functions.lastPauseTime().call()
        acc_token_per_share = contract.functions.accTokenPerShare().call()
        bonus_end_block = contract.functions.bonusEndBlock().call()
        start_block = contract.functions.startBlock().call()
        last_reward_block = contract.functions.lastRewardBlock().call()
        pool_limit_per_user = contract.functions.poolLimitPerUser().call()
        reward_per_block = contract.functions.rewardPerBlock().call()
        precision_factor = contract.functions.PRECISION_FACTOR().call()
        reward_token = contract.functions.rewardToken().call()
        staked_token = contract.functions.stakedToken().call()
        total_supply = contract.functions.totalSupply().call()
        reward_supply = 0   # contract.functions.rewardSupply().call()
        balance_of = contract.functions.balanceOf(owner).call()
        pending_reward = 0  # contract.functions.pendingReward(owner).call()

        # Debugging
        if debugging:
            print(f"""
            owner: {owner}
            smart_chef_factory: {smart_chef_factory}
            has_user_limit: {has_user_limit}
            locked_to_end: {locked_to_end}
            is_initialized: {is_initialized}
            is_paused: {is_paused}
            last_pause_time: {last_pause_time}
            acc_token_per_share: {acc_token_per_share}
            bonus_end_block: {bonus_end_block}
            start_block: {start_block}
            last_reward_block: {last_reward_block}
            pool_limit_per_user: {pool_limit_per_user}
            reward_per_block: {reward_per_block}
            precision_factor: {precision_factor}
            reward_token: {reward_token}
            staked_token: {staked_token}
            total_supply: {total_supply}
            reward_supply: {reward_supply}
            balance_of: {balance_of}
            pending_reward: {pending_reward}
            """)

        # Test
        self.assertEqual(owner, w3.eth.default_account)
        self.assertEqual(smart_chef_factory, w3.eth.default_account)
        self.assertFalse(has_user_limit)
        self.assertFalse(locked_to_end)
        self.assertFalse(is_initialized)
        self.assertFalse(is_paused)
        self.assertAlmostEqual(last_pause_time, 0)
        self.assertAlmostEqual(acc_token_per_share, 0)
        self.assertAlmostEqual(bonus_end_block, 0)
        self.assertAlmostEqual(start_block, 0)
        self.assertAlmostEqual(last_reward_block, 0)
        self.assertAlmostEqual(pool_limit_per_user, 0)
        self.assertAlmostEqual(reward_per_block, 0)
        self.assertAlmostEqual(precision_factor, 0)
        self.assertEqual(reward_token, "0x0000000000000000000000000000000000000000")
        self.assertEqual(staked_token, "0x0000000000000000000000000000000000000000")
        self.assertAlmostEqual(total_supply, 0)
        self.assertAlmostEqual(reward_supply, 0)
        self.assertAlmostEqual(balance_of, 0)
        self.assertAlmostEqual(pending_reward, 0)

    def test2_initialize(self):
        function_name('initialize')

        # Settings
        owner = w3.eth.default_account
        # w3.eth.default_account = w3.eth.accounts[1]     # test initialize by without factory address
        reward_token_decimal = tst_token.functions.decimals().call()
        reward_amount = 1000000 * 10 ** reward_token_decimal
        _stakedToken = wtk_token.address
        _rewardToken = tst_token.address
        _rewardPerBlock = 100000 * 10 ** reward_token_decimal
        _startBlock = w3.eth.block_number + 10
        _bonusEndBlock = _startBlock + 10
        _poolLimitPerUser = 1000 * 10 ** reward_token_decimal
        _lockedToEnd = True
        _admin = owner

        # Task
        contract.functions.initialize(
            _stakedToken, _rewardToken, _rewardPerBlock, _startBlock,
            _bonusEndBlock, _poolLimitPerUser, _lockedToEnd, _admin
        ).transact()
        has_user_limit = contract.functions.hasUserLimit().call()
        locked_to_end = contract.functions.lockedToEnd().call()
        is_initialized = contract.functions.isInitialized().call()
        bonus_end_block = contract.functions.bonusEndBlock().call()
        start_block = contract.functions.startBlock().call()
        last_reward_block = contract.functions.lastRewardBlock().call()
        pool_limit_per_user = contract.functions.poolLimitPerUser().call()
        reward_per_block = contract.functions.rewardPerBlock().call()
        precision_factor = contract.functions.PRECISION_FACTOR().call()
        reward_token = contract.functions.rewardToken().call()
        staked_token = contract.functions.stakedToken().call()
        pending_reward = contract.functions.pendingReward(owner).call()
        reward_supply = contract.functions.rewardSupply().call()
        tst_token.functions.transfer(contract.address, reward_amount).transact()
        reward_supply_expected = contract.functions.rewardSupply().call()

        # Debugging
        if debugging:
            print(f"""
            has_user_limit: {has_user_limit}
            locked_to_end: {locked_to_end}
            is_initialized: {is_initialized}
            bonus_end_block: {bonus_end_block}
            start_block: {start_block}
            last_reward_block: {last_reward_block}
            pool_limit_per_user: {pool_limit_per_user}
            reward_per_block: {reward_per_block}
            precision_factor: {precision_factor}
            reward_token: {reward_token}
            staked_token: {staked_token}
            pending_reward: {pending_reward}
            reward_supply: {reward_supply}
            reward_supply_expected: {reward_supply_expected}
            """)

        # Test
        self.assertEqual(has_user_limit, _poolLimitPerUser > 0)
        self.assertEqual(locked_to_end, _lockedToEnd)
        self.assertTrue(is_initialized)
        self.assertAlmostEqual(bonus_end_block, _bonusEndBlock)
        self.assertAlmostEqual(start_block, _startBlock)
        self.assertAlmostEqual(last_reward_block, _startBlock)
        self.assertAlmostEqual(pool_limit_per_user, _poolLimitPerUser)
        self.assertAlmostEqual(reward_per_block, _rewardPerBlock)
        self.assertAlmostEqual(precision_factor, 10 ** (30 - reward_token_decimal))
        self.assertEqual(reward_token, _rewardToken)
        self.assertEqual(staked_token, _stakedToken)
        self.assertAlmostEqual(pending_reward, 0)
        self.assertAlmostEqual(reward_supply, 0)
        self.assertAlmostEqual(reward_supply_expected, reward_amount)

    def test3_deposit(self):
        function_name('deposit')

        # Settings
        owner = w3.eth.default_account
        user_address = w3.eth.default_account
        # w3.eth.default_account = w3.eth.accounts[1]     # test initialize by without factory address
        stake_token_decimal = wtk_token.functions.decimals().call()
        deposit_amount = 1000 * 10 ** stake_token_decimal
        reward_token_decimal = tst_token.functions.decimals().call()

        # Task
        start_block = contract.functions.startBlock().call()
        bonus_end_block = contract.functions.bonusEndBlock().call()
        acc_token_per_share = contract.functions.accTokenPerShare().call()
        last_reward_block = contract.functions.lastRewardBlock().call()
        wtk_token.functions.approve(contract.address, deposit_amount).transact()
        contract.functions.deposit(deposit_amount).transact()
        acc_token_per_share_after = contract.functions.accTokenPerShare().call()
        last_reward_block_after = contract.functions.lastRewardBlock().call()
        total_supply = contract.functions.totalSupply().call()
        my_staked_balance = contract.functions.balanceOf(user_address).call()
        pending_reward = 0

        # Debugging
        if debugging:
            print(f"""
            start_block: {start_block}
            bonus_end_block: {bonus_end_block}
            acc_token_per_share: {acc_token_per_share}
            acc_token_per_share_after: {acc_token_per_share_after}
            last_reward_block: {last_reward_block}
            last_reward_block_after: {last_reward_block_after}
            total_supply: {total_supply}
            my_staked_balance: {my_staked_balance}
            """)

        # Test
        self.assertLessEqual(start_block, bonus_end_block)
        self.assertLessEqual(acc_token_per_share, acc_token_per_share_after)
        self.assertLessEqual(last_reward_block, last_reward_block_after)
        self.assertAlmostEqual(my_staked_balance, deposit_amount)

        while w3.eth.block_number <= bonus_end_block:
            pending_reward = contract.functions.pendingReward(owner).call()
            self.__add_block()

            # Debugging
            if debugging:
                print(f"""
                active: {w3.eth.block_number >= start_block}
                block_number: {w3.eth.block_number}
                pending_reward: {pending_reward}
                """)

        self.assertAlmostEqual(pending_reward, contract.functions.rewardSupply().call())

    @staticmethod
    def __add_block():
        amount = 1 * 10 ** 18
        w3.eth.send_transaction({
            'from': w3.eth.default_account,
            'to': w3.eth.default_account,
            'value': amount
        })


if __name__ == '__main__':
    unittest.main()
