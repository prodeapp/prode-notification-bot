# -*- coding: utf-8 -*-
"""
"""

import json

from web3 import Web3
from web3._utils.events import get_event_data

from telegram import sendNewMarket


PRODE_MARKET_FACTORY_ADDRESS = "0x67d3673CF19a6b0Ad70D76b4e9C6f715177eb48b"
PRODE_MARKET_FACTORY_ABI = json.load(open('abis/MarketFactory.json',
                                          'r')
                                     )['abi']
PRODE_MARKET_ABI = json.load(open('abis/Market.json', 'r'))['abi']


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
        self.address = address
        self.abi = PRODE_MARKET_FACTORY_ABI
        self.contract = self.web3.eth.contract(address=self.address,
                                               abi=self.abi)
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
        while self.lastBlock < chainBN:
            print(f'from {fromBlock} | To {toBlock} | Address {self.address}')
            events = self.web3.eth.get_logs({
                'fromBlock': fromBlock,
                'toBlock': toBlock,
                'address': self.address})
            for event in events:
                if event['topics'][0].hex() == Web3.keccak(
                        text="NewMarket(address,bytes32,address)").hex():
                    suc, res = self.handle_event(
                        event=event,
                        event_template=self.contract.events.NewMarket)
                    if suc:
                        market_address = res['args']['market']
                        marketInfo = self.getMarketInfo(market_address)
                        print(f'New Market!: {marketInfo[3]}')
                        sendNewMarket(marketInfo, market_address)

            self.lastBlock = toBlock
            fromBlock = toBlock + 1
            toBlock = chainBN \
                if chainBN < toBlock + 1000 \
                else toBlock + 1000


if __name__ == '__main__':
    pmf = ProdeMarketHTTP(PRODE_MARKET_FACTORY_ADDRESS)
    pmf.main(24042482)
