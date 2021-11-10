import pytest
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrence_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({'from': account, 'value': entrence_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrence_fee
    tx2 = fund_me.withdraw({'from': account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip('only for local testing')
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({'from': bad_actor})
