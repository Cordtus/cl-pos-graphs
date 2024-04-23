# Concentrated Liquidity Positions, Graphed

---

Fully interactive [in terminal]. Generates a 3-d plot chart showing the general spread, depth and concentration of liquidity positions by calling `liquidity_per_tick_range`.


Option to export chart image [`png` format] and/or `CSV` file to `./data/` in the same directory the script is run from.
Optional block height [leave blank for default - latest height]


If you have issues like HTTP errors, try changing the node the script uses. There is a REST/LCD URL at the top of the script you can change for another endpoint.
See `[https://cosmos.directory/osmosis/nodes]` for other public nodes

```
# Constants
default_url = "https://rest-osmosis.ecostake.com:443"
```

See [`https://cosmos.directory/osmosis/nodes`] for other public nodes

---

### setup

#### Install dependencies
Requires python/python3 + pip/pip3

##### Install python packages
`pip3 install -r requirements.txt`
<br>




