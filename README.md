# High Frequency Market Making: Optimal Quoting

This project is a part of the [CMF education](https://vk.com/cmf_russia).  Other CMF projects can be found at the [my Github](https://github.com/ialpatov/).

#### -- Project Status: Canceled

## Project Intro/Objective
The purpose of this project is to build market making strategy based on scientific papers.

### Technologies
* Python
* Pandas, Numpy
* Jupyter

## Project Description
This project is an introduction to high frequency trading (HFT) and to market making strategies. First, the EDA of market data was performed. Then all students had to build exchange simulator and the simulator of trader with the simplest random choice trading strategy. After that each group of students analyzed a set of articles on HFT and built own strategies based on these articles. 

## Files 

[hft1_Alpatov](https://github.com/ialpatov/hft/blob/main/hft1_Alpatov.ipynb) - the first homework on the project with EDA of market data of Binance BTC-USDT orderbook and tradebook.

[hft2_Alpatov_final](https://github.com/ialpatov/hft/blob/main/hft2_Alpatov_final.ipynb) - the second homework with the simulator of the exchange (latencies included) and the simulator of trader implementing random choice trading strategy.

[Stoikov strategy/stoikov_strategy](https://github.com/ialpatov/hft/blob/main/Stoikov%20strategy/stoikov_strategy.py) - the strategy build based on Avellaneda-Stoikov article [2].

[Stoikov strategy/strategy_run](https://github.com/ialpatov/hft/blob/main/Stoikov%20strategy/strategy_run.ipynb) - notebook for Stoikov strategy run.

[Cont article research/prepare_vols](https://github.com/ialpatov/hft/blob/main/Cont%20article%20research/prepare_vols.ipynb) - market data research based on Cont article [3], obtaining the distribution of the best level of the orderbook after the mid-price change.

[Cont article research/get_p1_ups](https://github.com/ialpatov/hft/blob/main/Cont%20article%20research/get_p1_ups.ipynb) - the second part of the research based on Cont article [3], obtaining _p1_ups_ - the matrix of probabilities that the next price move is an increase and _p_cont_ - the probability of two successive price
changes in the same direction.

__References:__

[1] Aldridge I. __High-Frequency Trading : A Practical Guide to Algorithmic Strategies and Trading Systems__. 2nd ed. Hoboken New Jersey: John Wiley & Sons; 2013.

[2] Avellaneda M. & Stoikov S. __High Frequency Trading in a Limit Order Book__. Quantitative Finance. 8. 217-224. 10.1080/14697680701381228; 2008. 

[3] Cont R. & de Larrard A. __Price Dynamics in a Markovian Limit Order Market__. SIAM Journal on Financial Mathematics, Society for Industrial and Applied Mathematics, 4 (1), pp.1-25. 10.1137/110856605; 2013.
