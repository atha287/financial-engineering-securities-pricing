import numpy as np

#arbitrage-free risk neutral pricing of various securities using the binomial model

'''
binomial tree constructor, from initial cost of a security (eg. stock)
i/p:
S0: initial stock/security value
n: no. of periods
u: up move multiplier
d: down move multiplier
c: dividend payout multiplier (use decimal value for a given percentage)
pnp: 'p' to give printed o/p, 'np' to return the list (to use for other purposes)
o/p:
returns binomial tree
'''
def binom_stock(S0, n, u, d, c, pnp):
    fin_tree = [[S0]]                         #initialize binom. tree; first entry is S0
    for t in range(1, n+1):                   #repeat for n periods (range(1, n+1) chosen as it is more useful here than range(0, n))
        x = []                                #empty list, will be filled with entries for each period
        for i in range(0, t):                 #in each period, create up and down moves from an entry in the previous period
            x.append((u+c)*fin_tree[t-1][i])  #append up move value to list
            x.append((d+c)*fin_tree[t-1][i])  #append down move value to list
        del x[2::2]                           #multiple entries up and down moves of consecutive entries in prev. period coincide; delete extra
        fin_tree.append(x)                    #append this period's list in the final tree
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({i:{0}{2}}) {np.around(np.array(fin_tree[i]), 4).tolist()}')
        return None
    else:
        return fin_tree

'''
binomial tree constructor, from final costs; futures bin. tree
i/p:
R: risk-free interest rate: R = (1 + r/100) where 'r' is the short-rate (fixed and deterministic)
o/p:
returns back-calculated bin. tree
'''
def binom_fut(S0, n, u, d, c, R, pnp):
    ST = binom_stock(S0, n, u, d, c, 'np')[-1]
    N, futs = len(ST), [ST]      #store length of last entry, initialize futs with ST (itself a list)
    q = (R-d-c)/(u-d)                    #calculate risk-neutral probabilities
    for t in range(0, n):                #repeat T times
        x = []                           #empty list for each period
        for i in range(1, N):            #number of back-calculations (y) to do in each period
            y = ((q * futs[t][i-1]) + ((1-q) * futs[t][i]))
            x.append(y)                  #append back-calculated vals to list
        N = N - 1                        #after calcs of each period, prev. period will need one less back-calc
        futs.append(x)                   #append current period list to final tree list
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({n-i:{0}{2}}) {np.around(np.array(futs[i]), 4).tolist()}')
        return None
    else:
        return futs

'''
options' binomial tree constructor, from final costs; options bin. tree
i/p:
cp: for call: 1, for put: -1
ameu: 'am' for american opt, 'eu' for european opt
K: strike price
und_sec: entire binomial tree of underlying security
o/p:
returns back-calculated options bin. tree
'''
def binom_opt(cp, ameu, K, und_sec, n, u, d, c, R, pnp):
    if len(und_sec[0]) == 1:    #stock and short-rate lattices are non-inverted trees; all others are inverted: invert non-inverted trees
        und_sec = und_sec[::-1]
    ST = und_sec[0]             #final vals of und_sec at maturity forms basis for comparing with strike
    comp = und_sec[1:]          #second-last to first entries of und_sec bin. tree needed for comparison in case of amer. put opt.
    N = len(ST)
    if cp == 1:                  #call condition
        opt = np.array(ST) - K
    else:                        #put condition
        opt = K - np.array(ST)
    opt[opt < 0] = 0             #neg vals become zero
    opts = [opt.tolist()]        #initiate options list
    q = (R-d-c)/(u-d)
    for t in range(0, n):
        x = []
        for i in range(1, N):
            y = ((q * opts[t][i-1]) + ((1-q) * opts[t][i])) / R
            if (cp == -1) and (ameu == 'am'):
                x.append(max(y, K - comp[t][i-1])) #compare back-calc. value with corresponding futs value, choose max
            else:
                x.append(y)
        N = N - 1
        opts.append(x)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({n-i:{0}{2}}) {np.around(np.array(opts[i]), 4).tolist()}')
        return None
    else:
        return opts
    
'''
constructs binomial tree for market interest rates (short rates) for fixed-income securities (eg. bond)
i/p:
r0: interest rate today (enter percentage value)
n: number of periods
u: up move multiplier
d: down move multiplier
pnp: 'p' to give printed o/p, 'np' to return the list (to use for other purposes)
o/p:
binomial tree for short rates
'''
#loop structure similar to binom_stock
def short_rate_lattice(r0, n, u, d, pnp): #srl for short henceforth
    fin_latt = [[r0]]
    for i in range(1, n+1):
        x = []
        for j in range(0, i):
            x.append(u*fin_latt[i-1][j])
            x.append(d*fin_latt[i-1][j])
        del x[2::2]
        fin_latt.append(x)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({i:{0}{2}}) {np.around(np.array(fin_latt[i]), 4).tolist()}')
        return None
    else:
        return fin_latt
    
'''
back-calculated binomial tree for zero-cooupon bond (zcb) prices (starting from 100 at maturity), and the spot rate 's_n' corresponding to zcb maturity period 'n'
'''
#loop structure similar to bin_fut
def term_struct(r0, n, u, d, pnp):
    srl = short_rate_lattice(r0, n, u, d, 'np')[::-1]
    N = len(srl[0])
    z = [(100*np.ones(n+1)).tolist()]     #zcb maturity value set to 100
    for t in range(0, n):
        x = []
        for i in range(1, N):
            y = 0.5 * (z[t][i-1] + z[t][i]) / (1 + (0.01 * srl[t+1][i-1]))
            x.append(y)
        N = N - 1
        z.append(x)
    s_n = ((100 / z[-1][0]) ** (1/n)) - 1  #calculate spot rate from present value of zcb
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({n-i:{0}{2}}) {np.around(np.array(z[i]), 4).tolist()}')
        print(f's_{n} = {(100*s_n):.4f}%')
        return None
    else:
        return [s_n, z]
    
'''
back-calculated bin. tree to give present value (t = 0 value in the tree) of a call/put amer./euro. option on a zcb (minimal modification of code can allow modelling an option on other fixed-income securities)
i/p:
T: maturity period of a derivative security
'''
#loop structure same as bin_opt but with T (maturity of opt) <= n (maturity of bond)
def opt_on_bond(cp, ameu, T, K, r0, n, u, d, pnp):  #oob henceforth
    srl = short_rate_lattice(r0, n, u, d, 'np')
    z = term_struct(r0, n, u, d, 'np')[1]
    ssrl = srl[T::-1]
    N = len(ssrl[0])
    if cp == 1: #call
        zz = np.array(z[n-T]) - K    #n-T selects the correct period of option maturity
    else:  #put
        zz = K - np.array(z[n-T])
    zz[zz < 0] = 0
    zz = [zz.tolist()]
    z_new = z[n-T:]
    for t in range(0, T):
        x = []
        for i in range(1, N):
            y = 0.5 * (zz[t][i-1] + zz[t][i]) / (1 + (0.01 * ssrl[t+1][i-1]))  #ssrl first row not relevant, so start from +1 row
            if (cp == -1) and (ameu == 'am'):
                x.append(max(y, K - z_new[t+1][i-1]))
            else:
                x.append(y)
        N = N - 1
        zz.append(x)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, T+1):
            print(f'({T-i:{0}{2}}) {np.around(np.array(zz[i]), 4).tolist()}')
        return None
    else:
        return zz
    
'''
gives the fair price of a forward written on a bond. Maturity of of forward 'T' <= maturity of bond 'n'. Coupon value added bond is discounted to 'T', bond values at 'T' form the maturity prices of the forward, which is then discounted to t=0 without adding coupons (coupons apply only to the underlying bond, not the forward).
i/p:
c: coupon payment percentage (use percentage value)
'''
#nominal price assumed 100; if different multiply final answer by number of units of 100
def bond_forward(r0, T, n, u, d, c, pnp):
    srl = short_rate_lattice(r0, n, u, d, 'np')[::-1]
    z = term_struct(r0, n, u, d, 'np')[1]
    z_new = [(np.array(z[0]) + c).tolist()]
    nn = len(z_new[-1])
    for i in range(0, n-1-T):
        x = []
        for j in range(1, nn):
            y = (0.5 * (z_new[i][j-1] + z_new[i][j]) / (1 + (0.01 * srl[i+1][j-1]))) + c
            x.append(y)
        nn = nn - 1
        z_new.append(x)
    N = len(z_new[-1])
    for t in range(n-1-T, n):
        xx = []
        for i in range(1, N):
            yy = 0.5 * (z_new[t][i-1] + z_new[t][i]) / (1 + (0.01 * srl[t+1][i-1]))
            xx.append(yy)
        N = N - 1
        z_new.append(xx)
    g_0 = z_new[-1][0] / (term_struct(r0, T, u, d, 'np')[1][-1][0] / 100)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({n-i:{0}{2}}) {np.around(np.array(z_new[i]), 4).tolist()}')
        print(f'G_0 = {g_0:.4f}')
        return None
    else:
        return [g_0, z_new]
    
'''
previously constructed forwards bin. tree is used to arrive at the maturity prices of a futures contract written on the same bond. Risk-neutral pricing to t=0 of these maturity prices give the fair value of the contract.
'''
def bond_future(r0, T, n, u, d, c, pnp):
    z_new = bond_forward(r0, T, n, u, d, c, 'np')[1][:n-T+1]
    N = len(z_new[-1])
    for t in range(n-T, n):
        xx = []
        for i in range(1, N):
            yy = 0.5 * (z_new[t][i-1] + z_new[t][i])
            xx.append(yy)
        N = N - 1
        z_new.append(xx)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({n-i:{0}{2}}) {np.around(np.array(z_new[i]), 4).tolist()}')
        return None
    else:
        return z_new
    
'''
modelling caplets and floorlets: similar to euro. call and put (respectively) options on the short-rates
instead of recording t=n nodes on the tree, it is more appropriate to use (for a caplet) (r_(n-1) - k)/(1 + r_(n-1)) at t=n-1 to account for the values of nodes at t=6. This is in contrast to binom_opt because interest rates were deterministic there, whereas here they are not.
i/p:
cf: 1 for a caplet, -1 for a floorlet
k: strike (use percentage value)
'''
def cap_flr_let(cf, k, r0, n, u, d, pnp):
    srl = short_rate_lattice(r0, n-1, u, d, 'np')[::-1]
    if cf == 1:
        x = np.array(srl[0]) - k
    else:
        x = k - np.array(srl[0])
    x[x < 0] = 0
    x = 0.01 * x / (1 + (0.01 * np.array(srl[0])))
    fin = [x.tolist()]
    N = len(fin[0])
    for t in range(1, n):
        xx = []
        for i in range(1, N):
            y = 0.5 * (fin[t-1][i-1] + fin[t-1][i]) / (1 + (0.01 * srl[t][i-1]))
            xx.append(y)
        N = N - 1
        fin.append(xx)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n):
            print(f'({n-1-i:{0}{2}}) {np.around(np.array(fin[i]), 4).tolist()}')
        return None
    else:
        return fin
    
'''
returns the bin. tree for an IR swap. As with caplets and floorlets, discounted values for nodes at t=n-1 are used for values of nodes at t=n
i/p:
ls: 1 for a long position, -1 for a short position
'''
def ir_swap(ls, k, r0, n, u, d, pnp):
    srl = short_rate_lattice(r0, n-1, u, d, 'np')[::-1]
    if ls == 1:
        x = np.array(srl[0]) - k
    else:
        x = k - np.array(srl[0])
    x = 0.01 * x / (1 + (0.01 * np.array(srl[0])))
    fin = [x.tolist()]
    N = len(fin[0])
    for t in range(1, n):
        xx = []
        for i in range(1, N):
            if ls == 1:
                y = ((0.5 * (fin[t-1][i-1] + fin[t-1][i])) + (0.01 * (srl[t][i-1] - k))) / (1 + (0.01 * srl[t][i-1]))
            else:
                y = ((0.5 * (fin[t-1][i-1] + fin[t-1][i])) + (0.01 * (k - srl[t][i-1]))) / (1 + (0.01 * srl[t][i-1]))
            xx.append(y)
        N = N - 1
        fin.append(xx)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n):
            print(f'({n-1-i:{0}{2}}) {np.around(np.array(fin[i]), 4).tolist()}')
        return None
    else:
        return fin
    
'''
returns the bin. tree for a swaption (a euro. call option on an IR swap). As before,  discounted values for nodes at t=n-1 are used for values of nodes at t=n
i/p:
k1: strike for the underlying swap (enter percentage value)
k2: strike for the option (usually 0) (enter percentage value)
'''
def ir_swaption(ls, k1, k2, T, r0, n, u, d, pnp):
    swap = ir_swap(ls, k1, r0, n, u, d, 'np')
    x = np.array(swap[n-1-T]) - (0.01 * k2)
    x[x < 0] = 0
    fin = [x.tolist()]
    N = len(fin[0])
    srl = short_rate_lattice(r0, T-1, u, d, 'np')[::-1]
    for t in range(1, T+1):
        xx = []
        for i in range(1, N):
            y = 0.5 * (fin[t-1][i-1] + fin[t-1][i]) / (1 + (0.01 * srl[t-1][i-1]))
            xx.append(y)
        N = N - 1
        fin.append(xx)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, T+1):
            print(f'({T-i:{0}{2}}) {np.around(np.array(fin[i]), 4).tolist()}')
        return None
    else:
        return fin
    
'''
returns lattice of state prices of an elementary security, constructed using forward equations. very versatile tool; has various applications.
'''
def forward_eqs(r0, n, u, d, pnp):
    srl = short_rate_lattice(r0, u, d, n, 'np')
    p00 = 1
    fin_tree = [[p00]]
    for t in range(1, n+1):
        x = [0.5 * fin_tree[t-1][0] / (1 + (0.01 * srl[t-1][0]))]
        for i in range(1, t):
            y = (0.5 * fin_tree[t-1][i-1] / (1 + (0.01 * srl[t-1][i-1]))) + (0.5 * fin_tree[t-1][i] / (1 + (0.01 * srl[t-1][i])))
            x.append(y)
        x.append(0.5 * fin_tree[t-1][-1] / (1 + (0.01 * srl[t-1][-1])))
        fin_tree.append(x)
    if pnp == 'p':
        print(' t   Binomial tree nodes')
        for i in range(0, n+1):
            print(f'({i:{0}{2}}) {np.around(np.array(fin_tree[i]), 6).tolist()}')
        return None
    else:
        return fin_tree