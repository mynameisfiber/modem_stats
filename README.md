# Modem Stats

> Optimum insisted my connection was fine... I thought otherwise

[**CLICK HERE TO SEE THE GOODS**](./Modem Analysis.ipynb)

This repo will scrape stats from an Arris modem, as well as do speed tests,
every minute. The included jupyter notebook does some stats on the collected
information to give you a sense on how good/bad your connection is.

My problem was with a bad cable coming in which was leading to high signal
noise for some frequencies. I'm not sure how useful this will be for other
problems, but it's worth a shot!

## Installation

Install the requirements listed in the `requirements.txt` and then run
`get_data.sh` (modify this script to point to a different IP if your arris modem
happens to have a different address).

Let this script run for a while in order to collect some data, then open up
the included jupyter notebook and run all cells. This should give you more than
enough ammo for your next call to customer support.
