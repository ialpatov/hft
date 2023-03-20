from typing import List, Optional, Tuple, Union, Dict

import numpy as np
import pandas as pd

from simulator import MdUpdate, Order, OwnTrade, Sim, update_best_positions


class StoikovStrategy:
    '''
        This strategy places ask and bid order every `delay` nanoseconds.
        If the order has not been executed within `hold_time` nanoseconds, it is canceled.
    '''
    def __init__(self, delay: float, hold_time: Optional[float], t_start: float, t_end: float,
                 sigma: float, gamma: float, k: float) -> None:
        '''
        Args:
            delay(float): delay between orders in nanoseconds
            hold_time(Optional[float]): holding time in nanoseconds
            t_start(float): time of first update of our data
            t_end(float): end time of our data (correspondent to T time in Stoikov paper)
            sigma(float): volatility from initial time to the end time
            gamma(float): risk-aversity
            k(float): exponent for Poisson rate lambda
        '''
        self.delay = delay
        if hold_time is None:
            hold_time = max(delay * 5, pd.Timedelta(10, 's').delta)
        self.hold_time = hold_time
        self.t_start = t_start
        self.t_end = t_end
        self.sigma = sigma
        self.gamma = gamma
        self.k = k

    def run(self, sim: Sim ) ->\
        Tuple[ List[OwnTrade], List[MdUpdate], List[ Union[OwnTrade, MdUpdate] ], List[Order] ]:
        '''
        This function runs simulation

        Args:
            sim(Sim): simulator
        Returns:
            trades_list(List[OwnTrade]): list of our executed trades
            md_list(List[MdUpdate]): list of market data received by strategy
            updates_list( List[ Union[OwnTrade, MdUpdate] ] ): list of all updates
            received by strategy(market data and information about executed trades)
            all_orders(List[Order]): list of all placed orders
        '''

        #market data list
        md_list:List[MdUpdate] = []
        #executed trades list
        trades_list:List[OwnTrade] = []
        #all updates list
        updates_list = []
        #current best positions
        best_bid = 0
        best_ask = 0

        # current inventory (correspondent to state variable 'q' in Stoikov paper)
        inventory = 0

        # last order timestamp
        prev_time = -np.inf
        # orders that have not been executed/canceled yet
        ongoing_orders: Dict[int, Order] = {}
        all_orders = []

        while True:
            # get update from simulator
            receive_ts, updates = sim.tick()
            if updates is None:
                break
            # save updates
            updates_list += updates
            for update in updates:
                # update best position
                if isinstance(update, MdUpdate):
                    best_bid, best_ask = update_best_positions(best_bid, best_ask, update)
                    md_list.append(update)
                elif isinstance(update, OwnTrade):
                    trades_list.append(update)
                    trade = update
                    # update positions
                    if trade.side == 'BID':
                        inventory += trade.size
                    elif trade.side == 'ASK':
                        inventory -= trade.size

                    # delete executed trades from the dict
                    if update.order_id in ongoing_orders.keys():
                        ongoing_orders.pop(update.order_id)
                else: 
                    assert False, 'invalid type of update!'

            if receive_ts - prev_time >= self.delay:
                prev_time = receive_ts
                # calculate reservation price and spread
                mid_price = 0.5*(best_ask + best_bid)
                time_spread = (self.t_end - receive_ts)/(self.t_end - self.t_start)
                reservation_price = mid_price - inventory * self.gamma * self.sigma**2 * time_spread
                spread = self.gamma * self.sigma**2 * time_spread + 2 * np.log(1 + self.gamma/self.k) / self.gamma
                # place order
                bid_order = sim.place_order(receive_ts, 0.001, 'BID', reservation_price - 0.5*spread)
                ask_order = sim.place_order(receive_ts, 0.001, 'ASK', reservation_price + 0.5*spread)
                ongoing_orders[bid_order.order_id] = bid_order
                ongoing_orders[ask_order.order_id] = ask_order

                all_orders += [bid_order, ask_order]
            
            to_cancel = []
            for ID, order in ongoing_orders.items():
                if order.place_ts < receive_ts - self.hold_time:
                    sim.cancel_order( receive_ts, ID )
                    to_cancel.append(ID)
            for ID in to_cancel:
                ongoing_orders.pop(ID)
            
                
        return trades_list, md_list, updates_list, all_orders
