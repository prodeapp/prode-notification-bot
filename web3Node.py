# -*- coding: utf-8 -*-
"""
"""

import json

from web3 import Web3
from web3._utils.events import get_event_data

from telegram import sendNewAnswer, sendNewMarket


PRODE_MARKET_FACTORY_ADDRESS = "0x67d3673CF19a6b0Ad70D76b4e9C6f715177eb48b"
PRODE_MARKET_FACTORY_ABI = json.load(open('abis/MarketFactory.json',
                                          'r')
                                     )['abi']
PRODE_MARKET_ABI = json.load(open('abis/Market.json', 'r'))['abi']
REALITY_3_0_ABI = json.load(open('abis/RealityETH_v3_0.json', 'r'))['abi']
REALITY_3_0_ADDRESS = "0xE78996A233895bE74a66F451f1019cA9734205cc"


class web3NodeHTTP():
    # web3_node_url = os.environ.get('WEB3_ENDPOINT')
    # if web3_node_url is None:
    #     raise Exception("WEB3_ENDPOINT enviromental variable not found")
    web3_node_url = 'https://rpc.gnosischain.com/'
    web3 = Web3(Web3.HTTPProvider(web3_node_url))

    @classmethod
    def getTransaction(cls, tx_hash):
        return cls.web3.eth.getTransaction(tx_hash)


class ProdeMarketHTTP(web3NodeHTTP):
    def __init__(self, address):
        super().__init__()

        self.mf_abi = PRODE_MARKET_FACTORY_ABI
        self.mf_address = address
        self.mf_contract = self.web3.eth.contract(address=self.mf_address,
                                                  abi=self.mf_abi)
        self.real_abi = REALITY_3_0_ABI
        self.real_address = REALITY_3_0_ADDRESS
        self.real_contract = self.web3.eth.contract(address=self.real_address,
                                                    abi=self.real_abi)
        self.lastBlock = self.web3.eth.blockNumber
        print('Last Block in this chain: ', self.lastBlock)

    def _getMarketContract(self, address):
        return self.web3.eth.contract(address=address, abi=PRODE_MARKET_ABI)

    @staticmethod
    def handle_event(event, event_template):
        try:
            result = get_event_data(event_template.web3.codec,
                                    event_template._get_event_abi(),
                                    event)
            return True, result
        except Exception as e:
            print(e)
            return False, None

    def _MarketFactoryEvents(self, _from, _to):
        # MarketFactory Events
        events = self.web3.eth.get_logs({
            'fromBlock': _from,
            'toBlock': _to,
            'address': self.mf_address})
        for event in events:
            if event['topics'][0].hex() == Web3.keccak(
                    text="NewMarket(address,bytes32,address)").hex():
                suc, res = self.handle_event(
                    event=event,
                    event_template=self.mf_contract.events.NewMarket)
                if suc:
                    market_address = res['args']['market']
                    marketInfo = self.getMarketInfo(market_address)
                    # print(f'New Market!: {marketInfo[3]}')
                    sendNewMarket(marketInfo[3], market_address)

    def _RealityEvents(self, _from, _to):
        # Reality Events
        events = self.web3.eth.get_logs({
            'fromBlock': _from,
            'toBlock': _to,
            'address': self.real_address})
        for event in events:
            if event['topics'][0].hex() == Web3.keccak(
                    text=("LogNewAnswer(bytes32,bytes32,bytes32,address,"
                          "uint256,uint256,bool)")).hex():
                suc, res = self.handle_event(
                    event=event,
                    event_template=self.real_contract.events.LogNewAnswer)
                if suc:
                    questionId = res['args']['question_id'].hex()
                    answer = res['args']['answer'].hex()
                    question = questionId
                    marketInfo = ['', '', '111', '']
                    market_address = '0x0000'
                    bond = Web3.fromWei(res['args']['bond'], 'ether')
                    if self._isProdeQuestion(questionId):
                        print(f'New Answer!: {answer} for {questionId}')
                        sendNewAnswer(marketInfo, market_address,
                                      question, answer, bond)

    def getMarketInfo(self, address):
        market_contract = self._getMarketContract(address)
        marketInfo = market_contract.functions.marketInfo().call()
        return marketInfo

    def main(self, startBlock):
        if startBlock:
            fromBlock = startBlock
            self.lastBlock = startBlock
        else:
            fromBlock = self.lastBlock
        chainBN = self.web3.eth.blockNumber
        toBlock = chainBN \
            if chainBN < fromBlock + 1000 \
            else fromBlock + 1000
        if toBlock < fromBlock:
            print("The starting block is bigger than last chain block "
                  f"{chainBN}")
            return
        while self.lastBlock < chainBN:
            print(f'from {fromBlock} | To {toBlock}')
            self._MarketFactoryEvents(fromBlock, toBlock)
            # self._RealityEvents(fromBlock, toBlock)
            self.lastBlock = toBlock
            fromBlock = toBlock + 1
            toBlock = chainBN \
                if chainBN < toBlock + 1000 \
                else toBlock + 1000


if __name__ == '__main__':
    # print(Web3.keccak(text="LogNewAnswer(bytes32,bytes32,bytes32,address,uint256,uint256,bool)").hex())
    pmf = ProdeMarketHTTP(PRODE_MARKET_FACTORY_ADDRESS)
    pmf.main(24042482)
