# cl-pos-graphs
Graphing user positions for Osmosis CL pools


## Grab pool position data
`osmosisd q concentratedliquidity liquidity-per-tick-range <poolid> -o json > <poolid>.json`

## Generate graph from data
`python3 graph-3d.py ./data/<poolid>.json ./data/graphs/<poolid>.png`
