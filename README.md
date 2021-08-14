# financial-engineering-securities-pricing
Implementation in python of various binomial tree-based pricing models for pricing of derivative securities. 

This repository contains the code to a voluntary project. The pricing of various derivative securities using the binomial tree model, as covered in [Financial Engineering and Risk Management Part I](https://www.coursera.org/learn/financial-engineering-1/home/welcome) on [Coursera](https://www.coursera.org/) is implemented in python. The pricing follows arbitrage-free and risk-neutral principles. Though the aforementioned course recommends the use of in-built MS Excel routines for such modelling, it is shown here that the same can be achieved in python. The models presented here are not exhaustive of the course curriculum, and more models may be added in the future.  

The code for all models is present in `securities_pricing.py` and demonstrations of the outputs of a few models can be found in `demonstrations.ipynb`. Following is a list of all the argument names used for the various models:
 - `S0`: initial value of a security (stock, bond, etc.)
 - `n`: number of periods (till maturity)
 - `u`: multiplier associated with an up move in the binomial tree
 - `d`: multiplier associated with a down move in the binomial tree
 - `c`: coupon value
 - `pnp`: pnp = 'p' to print the constructed tree as output, pnp = 'np' to return the tree as a list (to use for other purposes)
 - `R`: risk-free interest rate: R = (1 + r/100) where 'r' is the short-rate (fixed and deterministic)
 - `cp`: cp = 1 for a call option, cp = -1 for a put option
 - `ameu`: ameu = 'am' for an American option, ameu = 'eu' for a European option
 - `K`: strike price
 - `und_sec`: entire binomial tree of the underlying security (as a list) on which the option is written
 - `r0`: present day interest rate (short rate) (enter percentage value)
 - `T`: maturity period of a derivative security (T <= n)
 - `cf`: cf = 1 for a caplet, cf = -1 for a floorlet
 - `k`: strike (against the short-rate, ie. use percentage value)
 - `ls`: ls = 1 for long position on a swap, ls = -1 for short position on a swap
 - `k1`: strike for the IR swap, use percentage value
 - `k2`: strike for the option on the IR swap (swaption)  

Following are the functions along with the required arguments and descriptions:
 - `binom_stock(S0, n, u, d, c, pnp)`: Constructs a binomial tree for a security (for eg. stock) from its initial price.
 - `binom_fut(S0, n, u, d, c, R, pnp)`: From maturity prices, back-calculates the prices of a futures contract written on an underlying security.
 - `binom_opt(cp, ameu, K, und_sec, n, u, d, c, R, pnp)`: From maturity prices, back-calculates the prices of an American/European call/put options contract written on an underlying security.
 - `short_rate_lattice(r0, n, u, d, pnp)`: Constructs a binomial tree for the interest rates (short rates) from the prevailing (present-day) interest rate in the market.
 - `term_struct(r0, n, u, d, pnp)`: From the maturity price of a zero-coupon bond (ZCB) (assumed to be 100), back-calculates its present value, from which the spot rate `s_n` is also computed.
 - `opt_on_bond(cp, ameu, T, K, r0, n, u, d, pnp)`: Gives the present value of an American/European call/put option on a ZCB (with minimal modification, can include other fixed-income securities as the underlying).
 - `bond_forward(r0, T, n, u, d, c, pnp)`: Returns the fair price of a forwards contract written on a coupon paying bond.
 - `bond_future(r0, T, n, u, d, c, pnp)`: Returns the fair price of a futures contract written on a coupon paying bond.
 - `cap_flr_let(cf, k, r0, n, u, d, pnp)`: Gives the present value of a European call(caplet)/put(floorlet) option on the short rates.
 - `ir_swap(ls, k, r0, n, u, d, pnp)`: Gives the fair value of a swap written on the interest rates.
 - `ir_swaption(ls, k1, k2, T, r0, n, u, d, pnp)`: Returns the present value of an option written on an IR swap.
 - `forward_eqs(r0, n, u, d, pnp)`: Returns lattice of state prices of an elementary security, constructed using forward equations. It is a very versatile tool and has various applications.
