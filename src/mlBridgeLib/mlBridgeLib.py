# todo:
# use infer_types() or convert_dtypes() in _InsertScoringColumns instead of explicitly stating?
# make into class?
# create a class, move loose statements into __init__()
# implement assert statements that check function args for correctness, tuple count and len.
# remove unused functions.
# change functions that require dataframe to use list (series) instead.
# move dataframe functions to another source file?
# remove dependencies on: np, sklearn
# create validation functions for DDmakes, Hands, LoTT, HCP, dtypes, Vul, Dealer, Score, etc.


import numpy as np
import pandas as pd
import os
import pathlib
from collections import defaultdict
from sklearn import preprocessing
import matplotlib.pyplot as plt
from IPython.display import display  # needed for VSCode


# declare module read-only variables
CDHS = 'CDHS' # string ordered by suit rank - low to high
CDHSN = CDHS+'N' # string ordered by strain
NSHDC = 'NSHDC' # order by highest score value. useful for idxmax(). coincidentally reverse of CDHSN.
SHDC = 'SHDC' # string ordered by suit rank - high to low
NSEW = 'NSEW' # string ordered by partnership direction
NESW = 'NESW' # string ordered by order of bidding/playing direction
NWSE = 'NWSE' # string ordered by order of bidding/playing direction but with EW swapped
direction_order = NESW
NS_EW = ['NS','EW'] # list of partnership directions
suit_order = CDHS
ranked_suit = 'AKQJT98765432' # card denominations - high to low
ranked_suit_rev = reversed(ranked_suit) # card denominations - low to high
ranked_suit_dict = {c:n for n,c in enumerate(ranked_suit)}
max_bidding_level = 7
tricks_in_a_book = 6
vul_syms = ['None','N_S','E_W','Both']
vul_directions = [[],[0,2],[1,3],[0,1,2,3]]
contract_types = ['Pass','Partial','Game','SSlam','GSlam']
dealer_d = {'N':0, 'E':1, 'S':2, 'W':3}
vul_d = {'None':0, 'Both':1, 'N_S':2, 'E_W':3} # dds vul encoding is weird
allContracts = [(0,'Pass')]+[(l+1,s) for l in range(0,7) for s in CDHSN]
allHigherContracts_d = {c:allContracts[n+1:] for n,c in enumerate(allContracts)}
suit_names_d = {'S':'Spades','H':'Hearts','D':'Diamonds','C':'Clubs','N':'No-Trump'}

def pd_options_display():
    # display options overrides
    pd.options.display.max_columns = 0
    pd.options.display.max_colwidth = 100
    pd.options.display.min_rows = 500
    pd.options.display.max_rows = 50 # 0
    pd.options.display.precision = 2
    pd.options.display.float_format = '{:.2f}'.format

    # Don't wrap repr(DataFrame) across additional lines
    pd.options.display.expand_frame_repr = False
    #pd.set_option("display.expand_frame_repr", False)


def sort_suit(s):
    return '' if s == '' else ''.join(sorted(s,key=lambda c: ranked_suit_dict[c]))


def sort_hand(h):
    return [sort_suit(s) for s in h]


# Create a board_record_string from hand.
def HandToBoardRecordString(hand):
    return ''.join([s+c for h in [hand[0],hand[3],hand[1],hand[2]] for s,c in zip('SHDC',h)])


# Create a tuple of suit lengths per direction (NESW).
# todo: assert that every suit has 13 cards
def SuitLengths(h):
    return tuple(tuple(len(hhh) for hhh in hh) for hh in h)


# Create a tuple of suit lengths per direction (NESW).
# todo: assert that every suit has 13 cards
def CombinedSuitLengths(h):
    t = SuitLengths(h)
    return tuple(tuple(sp1+sp2 for sp1,sp2 in zip(h1,h2)) for h1,h2 in [[t[0],t[2]],[t[1],t[3]]])


# Create a tuple of combined suit lengths (NS, EW) sorted by largest to smallest
#def SortedSuitLengthTuples(h):
#    t = CombinedSuitLengths(h)
#    return tuple((t[i],i,'SHDC'[i]) for (v, i) in sorted([(v, i) for (i, v) in enumerate(t)],reverse=True))


# convert hand tuple into PBN
def HandToPBN(hand):
    return 'N:'+' '.join('.'.join([hh for hh in h]) for h in hand)
# create list of PBNs from Hands (list of tuple of tuples)
def HandsToPBN(hands):
    pbns = []
    for hand in hands:
        pbns.append(HandToPBN(hand))
    return pbns

# Create tuple of suit lengths per partnership (NS, EW)
#def CombinedSuitLengthTuples(t):
#    return tuple([tuple([sn+ss for sn,ss in zip(t[0],t[2])]),tuple([se+sw for se,sw in zip(t[1],t[3])])])


hcpd = {c:w for c,w in zip(ranked_suit,[4,3,2,1]+[0]*9)}
def HandsToHCP(hands):
    t = tuple(HandToHCP(hand) for hand in hands)
    assert sum(h[0] for h in t) == 40
    return t
def HandToHCP(hand):
    t = tuple(SuitToHCP(suit) for suit in hand)
    return sum(t),t
def SuitToHCP(suit):
    return sum(hcpd[c] for c in suit)


# Convert list of tupled hands to binary string.
def HandsLToBin(handsl):
    return [tuple(hand[0] for hand in HandsToBin(hands)) for hands in handsl]


# Convert list of hands, in binary string format, to One Hot Encoded list
def BinLToOHE(binl):
    return [tuple((int(i) for hand in hands for i in f'{hand[2:].zfill(52)}')) for hands in binl]


# Convert One Hot Encoded hands to tupled hands.
def OHEToHandsL(ohel):
    return [tuple(tuple(([''.join([ranked_suit[denom] for denom in range(13) if hands[hand+suit*13+denom]]) for suit in range(4)])) for hand in range(0,52*4,52)) for hands in ohel]


# Create column of binary encoded hands
wd = {c:1<<n for n,c in enumerate(ranked_suit_rev)}
def HandsToBin(hands):
    t = tuple(HandToBin(hand) for hand in hands)
    assert sum(tt[0] for tt in t) == (1<<(13*4))-1
    return tuple(tuple([bin(h[0]),tuple(bin(s) for s in h[1])]) for h in t)
def HandToBin(hand):
    t = tuple(SuitToBin(suit) for suit in hand)
    tsum = sum(h<<(n*13) for n,h in enumerate(reversed(t))) # order spades to clubs
    return tsum,t
def SuitToBin(suit):
    return sum([wd[c] for c in suit])


# Create column of hex encoded hands
def HandsToHex(hands):
    t = tuple(HandToHex(hand) for hand in hands)
    assert sum(tt[0] for tt in t) == (1<<(13*4))-1
    return tuple(tuple([hex(h[0]),tuple(hex(s) for s in h[1])]) for h in t)
def HandToHex(hand):
    t = tuple(SuitToHex(suit) for suit in hand)
    tsum = sum(h<<(n*13) for n,h in enumerate(reversed(t))) # order spades to clubs
    return tsum,t
def SuitToHex(suit):
    return sum([wd[c] for c in suit])


# Create column of Quick Trick values. Might be easier to do using binary encoded hands.
qtl = [(2,'AK'),(1.5,'AQ'),(1,'A'),(1,'KQ'),(0.5,'K')] # list of (quick tricks card combos, combo value)
qtls = sorted(qtl,reverse=True) # sort by quick trick value (most to least) to avoid ambiguity
def HandsToQT(hands):
    t = tuple(HandToQT(hand) for hand in hands)
    return sum(h[0] for h in t),t
def HandToQT(hand):
    t = tuple(SuitToQT(suit) for suit in hand)
    return sum(t),t
def SuitToQT(suit):
    # assumes suits are sorted by HCP value (most to least) (AKQJT...)
    for qt in qtls:
        if suit.startswith(qt[1]):
            return qt[0]
    return 0


def BoardNumberToDealer(bn):
    return 'NESW'[(bn-1) & 3]


def BoardNumberToVul(bn):
    bn -= 1
    return range(bn//4, bn//4+4)[bn & 3] & 3


# create column of LoTT
def LoTT(ddmakes,lengths):
    #print(ddmakes,lengths)
    maxnsl = []
    maxewl = []
    for nsidx,(nmakes,smakes) in enumerate(zip(ddmakes[0][:4],ddmakes[2][:4])):
        nsmax = max(nmakes,smakes)
        maxnsl.append((lengths[0][3-nsidx],nsmax,nsidx)) # 3- because lengths are SHDC and ddmakes are CDHSN
    for ewidx,(emakes,wmakes) in enumerate(zip(ddmakes[1][:4],ddmakes[3][:4])):
        ewmax = max(emakes,wmakes)
        maxewl.append((lengths[1][3-ewidx],ewmax,ewidx)) # 3- because lengths are SHDC and ddmakes are CDHSN
    sorted_maxnsl = sorted(maxnsl,reverse=True)
    sorted_maxewl = sorted(maxewl,reverse=True)
    maxlen = sorted_maxnsl[0][0]+sorted_maxewl[0][0]
    maxmake = sorted_maxnsl[0][1]+sorted_maxewl[0][1]
    return (maxmake,maxlen,maxmake-maxlen)


def ContractType(tricks,suit):
    if tricks < 7:
        ct = 'Pass'
    elif tricks == 12:
        ct = 'SSlam'
    elif tricks == 13:
        ct = 'GSlam'
    elif suit in 'CD' and tricks in range(11,12):
        ct = 'Game'
    elif suit in 'HS' and tricks in range(10,12):
        ct = 'Game'
    elif suit in 'N' and tricks in range(9,12):
        ct = 'Game'
    else:
        ct = 'Partial'
    return ct


def CategorifyContractType(ddmakes):
    contract_types_d = defaultdict(list)
    for dd in ddmakes:
        for direction,nesw in zip(NS_EW,dd): # todo: using NS_EW instead of NESW for now. switch to NESW?
            for suit,tricks in zip(CDHSN,nesw):
                assert tricks is not None
                ct = ContractType(tricks,suit)
                contract_types_d['_'.join(['CT',direction,suit])].append(ct) # estimators don't like categorical dtype
    return contract_types_d


# convert vul to boolean based on direction
def DirectionToVul(vul, direction):
    return direction in vul_directions[vul_syms.index(vul)]


def DirectionSymToDealer(direction_symbol):
    return list(NESW).index(direction_symbol) # using NSEW index because of score()


def StrainSymToValue(strain_symbol):
    return list(CDHSN).index(strain_symbol) # using CDHSN index because of score()


# Create list of tuples of (score, (level, strain), direction, result). Useful for calculating Pars.
# todo: rewrite into two defs; looping, core logic
def DDmakesToScores(ddmakes,vuls):
    scoresl = []
    for ddmakes,vul in zip(ddmakes,vuls):
        directionsl = []
        for direction in range(len(NESW)):
            # todo: add to mlBridgeLib
            v =  DirectionToVul(vul,direction)
            strainl = []
            for strain, tricks in enumerate(ddmakes[direction]): # cycle through all strains
                highest_make_level = tricks-1-tricks_in_a_book
                for level in range(max(highest_make_level,0), max_bidding_level):
                    result = highest_make_level-level
                    s = score(level, strain, result < 0, 0, v, result)
                    strainl.append((s,(level,strain),direction,result))
            # stable sort by contract then score
            sorted_direction = sorted(sorted(strainl,key=lambda k:k[1]),reverse=True,key=lambda k:k[0])
            directionsl.append(sorted_direction)
        scoresl.append(directionsl)
    return scoresl


# Convert score tuples into Par.
# todo: rewrite into two defs; looping, core logic
# todo: Is this still working? Compare against dds generated pars.
def ScoresToPar(scoresl):
    par_scoresll = []
    for directionsl in scoresl: # [scoresl[0]]:
        par_scoresl = [(0,(0,0),0,0)]
        direction = 0
        while(True):
            d_ew = direction & 1
            #print(directionsl[direction])
            for par_score in directionsl[direction]: # for each possible remaining bid
                if par_scoresl[0][1] < par_score[1]: # bid is sufficient
                    #print("suff:",par_scoresl[0],par_score)
                    psl_ew = par_scoresl[0][2] & 1
                    #print(direction,d_ew,ps_ew,((direction ^ ps_ew) & 1),((d_ew ^ ps_ew) & 1))
                    assert ((direction ^ psl_ew) & 1) == ((d_ew ^ psl_ew) & 1)
                    opponents = d_ew != psl_ew
                    assert (d_ew != psl_ew) == opponents
                    if opponents:
                        #print("oppo:",-par_scoresl[0][0],par_score[0],d_ew,ps_ew)
                        if -par_scoresl[0][0] <= par_score[0]: # bidder was opponent, improved score is a sacrifice
                            par_scoresl.insert(0,par_score)
                            #error
                            #break
                        else:
                            break
                    else:
                        if par_scoresl[0][0] <= par_score[0]: # bidder was partnership, take improved score
                            #print("same:",par_scoresl[0][0],par_score[0],len(par_scoresl))
                            par_scoresl.insert(0,par_score)
                            #break
                        else:
                            break
            direction = (direction+1) % len(NESW)
            #print(direction,par_scoresl[0][2])
            if direction == par_scoresl[0][2]: # bidding is over when new direction is last bidder
                break
        parl = []
        score = par_scoresl[0][0]
        psl_ew = par_scoresl[0][2] & 1
        par_scores_formatted = (-score if psl_ew else score,parl)
        for par_score in par_scoresl:
            ps_ew = par_score[2] & 1
            if len(parl) > 0 and (score != par_score[0] or psl_ew != ps_ew): # only use final score in same direction
                break
            result = par_score[3]
            par = tuple((par_score[1][0]+1,CDHSN[par_score[1][1]],'*' if result < 0 else '',['NS','EW'][ps_ew],result))
            parl.insert(0,par)
        #display(par_scores_formatted)
        par_scoresll.append(par_scores_formatted)
    return par_scoresll


# todo: don't pass row. pass only necessary values
#def LoTT(r):
#    t = []
#    for d in range(0,2):
#        max_suit_length_tuple = r['Suit_Lengths_Sorted'][d][0]
#        suit_length, suit_idx, suit_char = max_suit_length_tuple
#        dd_makes_suit_idx = 3-suit_idx
#        dd_makes = r['DDmakes'][d][dd_makes_suit_idx],r['DDmakes'][d+2][dd_makes_suit_idx]
#        variance = suit_length-dd_makes[0],suit_length-dd_makes[1]
#        t.append(tuple([suit_char,suit_length,dd_makes,variance]))
#    return tuple(t)


def FilterBoards(df, cn=None, vul=None, direction=None, suit=None, contractType=None, doubles=None):
    # optionally filter dataframe's rows
    if not cn is None:
        # only allow this club number e.g. not subclubs 108571/267096
        df = df[df['Key'].str.startswith(cn)]
    if not vul is None:
        # one of the following: 'None','NS','EW','Both'
        if vul == 'None':
            df = df[~(df['Vul_NS'] | df['Vul_EW'])]  # neither NS, EW
        elif vul == 'NS':
            df = df[df['Vul_NS']]  # only NS
        elif vul == 'EW':
            df = df[df['Vul_EW']]  # only EW
        elif vul == 'Both':
            df = df[df['Vul_NS'] & df['Vul_NS']]  # only Both
        else:
            print(f'FilterBoards: Error: Invalid vul:{vul}')
    if not direction is None:
        # either 'NS','EW' # Single direction is problematic so using NS, EW
        df = df[df['Par_Dir'] == direction]
    if not suit is None:
        df = df[df['Par_Suit'].isin(suit)]  # ['CDHSN']
    if not contractType is None:
        # ['Pass',Partial','Game','SSlam','GSlam']
        df = df[df['Par_Type'].isin(contractType)]
    if not doubles is None:
        # ['','*','**'] # Par scores only are down if they're sacrifices
        df = df[df['Par_Double'].isin(doubles)]
    df.reset_index(drop=True, inplace=True)
    return df


# adapted (MIT license) from https://github.com/jfklorenz/Bridge-Scoring/blob/master/features/score.js
# ================================================================
# Scoring
def score(level, suit, double, declarer, vulnerability, result):
    assert level in range(0, 7), f'ValueError: level {level} is invalid'
    assert suit in range(0, 5), f'ValueError: suit {suit} is invalid'
    assert double in range(0, 3), f'ValueError: double {double} is invalid'
    assert declarer in range(
        0, 4), f'ValueError: declarer {declarer} is invalid'
    assert vulnerability in range(
        0, 2), f'ValueError: vulnerability {vulnerability} is invalid'
    assert result in range(-13, 7), f'ValueError: result {result} is invalid'

    # Contract Points
    points_contract = [
        [[20, 40, 80], [20, 40, 80]],
        [[20, 40, 80], [20, 40, 80]],
        [[30, 60, 120], [30, 60, 120]],
        [[30, 60, 120], [30, 60, 120]],
        [[40, 80, 160], [30, 60, 120]]
    ]

    # Overtrick Points
    overtrick = [
        [[20, 100, 200], [20, 200, 400]],
        [[20, 100, 200], [20, 200, 400]],
        [[30, 100, 200], [30, 200, 400]],
        [[30, 100, 200], [30, 200, 400]],
        [[30, 100, 200], [30, 200, 400]]
    ]

    # Undertrick Points
    undertricks = [
        [[50, 50, 50, 50], [100, 200, 200, 300], [200, 400, 400, 600]],
        [[100, 100, 100, 100], [200, 300, 300, 300], [400, 600, 600, 600]]
    ]

    # Bonus Points
    bonus_game = [[50, 50], [300, 500]]
    bonus_slam = [[500, 750], [1000, 1500]]
    bonus_double = [0, 50, 100]

    if result >= 0:
        points = points_contract[suit][0][double] + \
            level * points_contract[suit][1][double]

        points += bonus_game[points >= 100][vulnerability]

        if level >= 5:
            points += bonus_slam[level - 5][vulnerability]

        points += bonus_double[double] + result * \
            overtrick[suit][vulnerability][double]

    else:
        points = -sum([undertricks[vulnerability][double][min(i, 3)]
                       for i in range(0, -result)])

    return points if declarer < 2 else -points  # negate points if EW

# ================================================================


# create some helpful scoring dicts
# de-cumsum set scores
def ScoreUnderTricks(level, suit, double, declarer, vulnerability):
    l = [score(level, suit, double, declarer, vulnerability, result)
         for result in list(range(-7-level, 0))]
    return [s-ss for s, ss in zip(l, l[1:]+[0])]+[0]*(7-level)


# de-cumsum make scores
def ScoreOverTricks(level, suit, double, declarer, vulnerability):
    l = [score(level, suit, double, declarer, vulnerability, result)
         for result in list(range(0, 7-level))]
    return [0]*(7+level)+[s-ss for s, ss in zip(l, [0]+l[:-1])]


def ScoreDicts():
    # Returns 3 dicts useful for scoring. Each dict expects a tuple: (level, suit, vulnerability, double, declarer)
    # Examples:
    #   scoresd[(0,0,0,0,0)] return [-350, -300, -250, -200, -150, -100, -50, 70, 90, 110, 130, 150, 170, 190]
    #   makeScoresd[(0,0,0,0,0)] return [0, 0, 0, 0, 0, 0, 0, 70, 20, 20, 20, 20, 20, 20]
    #   setScoresd[(0,0,0,0,0)] return [-50, -50, -50, -50, -50, -50, -50, 0, 0, 0, 0, 0, 0, 0]    
    scoresd = {(level, suit, vulnerability, double, declarer): [score(level, suit, double, declarer, vulnerability, result) for result in list(range(-7-level, 0))+list(
        range(0, 7-level))] for declarer in range(0, 4) for level in range(0, 7) for suit in range(0, 5) for double in range(0, 3) for vulnerability in range(0, 2)}
    assert sum([len(v) != 14 for v in scoresd.values()]) == 0
    # display(scoresd)
    setScoresd = {(level, suit, vulnerability, double, declarer): ScoreUnderTricks(level, suit, double, declarer, vulnerability)
                  for declarer in range(0, 4) for level in range(0, 7) for suit in range(0, 5) for double in range(0, 3) for vulnerability in range(0, 2)}
    # display(setScoresd)
    assert sum([len(v) != 14 for v in setScoresd.values()]) == 0
    makeScoresd = {(level, suit, vulnerability, double, declarer): ScoreOverTricks(level, suit, double, declarer, vulnerability)
                   for declarer in range(0, 4) for level in range(0, 7) for suit in range(0, 5) for double in range(0, 3) for vulnerability in range(0, 2)}
    # display(makeScoresd)
    assert sum([len(v) != 14 for v in makeScoresd.values()]) == 0
    return scoresd, setScoresd, makeScoresd


# insert Actual and Predicted as leftmost columns for easier viewing.
# default column creation is rightmost
def MakeColName(prefix, name, suit, direction):
    if name != '':
        name = '_'+name
    if suit != '':
        suit = '_'+suit
    if direction != '':
        direction = '_'+direction
    return prefix+name+suit+direction


def MakeSuitCols(prefix, suit, direction):
    return ['_'.join([prefix, suit, direction])+str(n).zfill(2) for n in range(0, 14)]


def AssignToColumn(df, name, values, dtype=None):
    df[name] = values
    if dtype is not None:
        df[name] = df[name].astype(dtype)  # float doesn't support pd.NA
    return df[name]


def AssignToColumnLoc(df, bexpr, name, values, dtype=None):
    df.loc[bexpr, name] = values
    if dtype is not None:
        df[name] = df[name].astype(dtype)  # float doesn't support pd.NA
    return df.loc[bexpr, name]


def InsertTcgColumns(df, dep_vars, prefix, tcgd, tcg299d):
    dep_var, new_dep_var, suit, direction, double = dep_vars
    # colnum = len(df.columns)-1 # todo: subtract one until colnum+1 is adjusted in inserts
    # create TCG_Key for indexing into tcgd to obtain common game data. TCG_Key has no direction.
    bnotna = df[MakeColName(prefix, 'Score', suit, direction)].notna()
    # todo: Is this the best place for replace('E2A','A')?
    AssignToColumn(df, MakeColName(prefix, 'TCG_Key', suit, direction), df.loc[bnotna, 'EventBoard'].str.replace(
        'E2A', 'A').str.cat(df.loc[bnotna, MakeColName(prefix, 'Score', suit, direction)].astype(int).map(str), sep='_'), 'string')
    # TCG stuff returns NS MP, never EW.
    tcgns = GetTcgMPs(tcgd, df[MakeColName(
        prefix, 'TCG_Key', suit, direction)])
    tcg299ns = GetTcgMPs(
        tcg299d, df[MakeColName(prefix, 'TCG_Key', suit, direction)])
    if direction == '' or direction == 'NS':
        AssignToColumn(df, MakeColName(
            prefix, 'TCG_MP', suit, 'NS'), tcgns, 'float')
        AssignToColumn(df, MakeColName(
            prefix, 'TCG299_MP', suit, 'NS'), tcg299ns, 'float')
    if direction == '' or direction == 'EW':
        tcgew = [1-mp for mp in tcgns]
        tcg299ew = [1-mp for mp in tcg299ns]
        AssignToColumn(df, MakeColName(
            prefix, 'TCG_MP', suit, 'EW'), tcgew, 'float')
        AssignToColumn(df, MakeColName(
            prefix, 'TCG299_MP', suit, 'EW'), tcg299ew, 'float')
    return


def FormatBid(df, prefix, dep_vars):
    dep_var, new_dep_var, suit, direction, double = dep_vars
    # alternative: if MakeColName(prefix, 'Dir', suit, direction) in df.columns
    if direction == '':
        nsew = df[MakeColName(prefix, 'Dir', suit, direction)]
    else:
        nsew = direction
    return df[MakeColName(prefix, 'Level', suit, direction)].map(
        str)+df[MakeColName(prefix, 'Suit', suit, direction)]+df[MakeColName(prefix, 'Double', suit, direction)]+' '+nsew+' '+(df[MakeColName(prefix, 'Result', suit, direction)].map(str))


def InsertScoringColumnsPar(df, dep_vars, prefix):
    # df has 'Level' but not 'Tricks'
    dep_var, new_dep_var, suit, direction, double = dep_vars
    values = df[MakeColName(prefix, 'Level', suit, direction)]
    assert all(values <= 7), [v for v in values if v > 7]
    AssignToColumnLoc(df, values > 0, MakeColName(
        prefix, 'Tricks', suit, direction), values+6, 'Int8')
    return InsertScoringColumns(df, dep_vars, prefix)


def InsertScoringColumnsTricks(df, dep_vars, prefix):
    # df has 'Tricks' but not 'Level'
    dep_var, new_dep_var, suit, direction, double = dep_vars
    values = df[MakeColName(prefix, 'Tricks', suit, direction)]
    assert all(values >= 0) and all(values <= 13), [v for v in values if v < 0 or v > 13]
    AssignToColumnLoc(df, values > 6, MakeColName(
        prefix, 'Level', suit, direction), values-6, 'Int8')
    return InsertScoringColumnsSDR(df, dep_vars, prefix)


def InsertScoringColumnsSDR(df, dep_vars, prefix):
    dep_var, new_dep_var, suit, direction, double = dep_vars
    AssignToColumn(df, MakeColName(
        prefix, 'Suit', suit, direction), suit, 'string')
    AssignToColumn(df, MakeColName(prefix, 'Double',
                                   suit, direction), double, 'string')
    AssignToColumn(df, MakeColName(prefix, 'Result', suit, direction),
                   df[dep_var]-df[MakeColName(prefix, 'Tricks', suit, direction)], 'Int8')
    return InsertScoringColumns(df, dep_vars, prefix)


def InsertScoringColumns(df, dep_vars, prefix):
    dep_var, new_dep_var, suit, direction, double = dep_vars
    AssignToColumnLoc(df, df[MakeColName(prefix, 'Tricks', suit, direction)] >= 7, MakeColName(
        prefix, 'Bid', suit, direction), FormatBid(df, prefix, dep_vars), 'string')
    AssignToColumnLoc(df, df[MakeColName(prefix, 'Tricks', suit, direction)] < 7, MakeColName(
        prefix, 'Bid', suit, direction), 'Pass', 'string')  # not worth a bid

    # Calculate contract type
    AssignToColumn(df, MakeColName(
        prefix, 'Type', suit, direction), 'Pass', 'string')
    AssignToColumnLoc(df, df[MakeColName(prefix, 'Level', suit, direction)] > 0, MakeColName(
        prefix, 'Type', suit, direction), 'Partial', 'string')
    AssignToColumnLoc(df, (df[MakeColName(prefix, 'Suit', suit, direction)].isin(['C', 'D'])) & (
        df[MakeColName(prefix, 'Level', suit, direction)] >= 5), MakeColName(prefix, 'Type', suit, direction), 'Game', 'string')
    AssignToColumnLoc(df, (df[MakeColName(prefix, 'Suit', suit, direction)].isin(['H', 'S'])) & (
        df[MakeColName(prefix, 'Level', suit, direction)] >= 4), MakeColName(prefix, 'Type', suit, direction), 'Game', 'string')
    AssignToColumnLoc(df, (df[MakeColName(prefix, 'Suit', suit, direction)] == 'N') & (df[MakeColName(
        prefix, 'Level', suit, direction)] >= 3), MakeColName(prefix, 'Type', suit, direction), 'Game', 'string')
    AssignToColumnLoc(df, df[MakeColName(prefix, 'Level', suit, direction)] >= 6, MakeColName(
        prefix, 'Type', suit, direction), 'SSlam', 'string')
    AssignToColumnLoc(df, df[MakeColName(prefix, 'Level', suit, direction)] == 7, MakeColName(
        prefix, 'Type', suit, direction), 'GSlam', 'string')

    # Calculate Score
    scoresl = []
    for i, r in df.iterrows():
        s = r[MakeColName(prefix, 'Level', suit, direction)]
        if s is not pd.NA:  # Level is a dtype that supports pd.NA (int8)
            if s > 0:
                # Calculate vulnerability
                if direction == '':
                    idirection = list('NSEW').index(
                        r[MakeColName(prefix, 'Dir', suit, direction)][0])
                else:
                    idirection = list('NSEW').index(direction[0])
                vul = [r['Vul_NS'], r['Vul_NS'],
                       r['Vul_EW'], r['Vul_EW']][idirection]
                s = score(
                    s-1,
                    list('CDHSN').index(
                        r[MakeColName(prefix, 'Suit', suit, direction)]),
                    len(r[MakeColName(prefix, 'Double', suit, direction)]),
                    idirection,
                    vul,
                    r[MakeColName(prefix, 'Result', suit, direction)]
                )
            else:
                s = pd.NA
        scoresl.append(s)
    AssignToColumn(df, MakeColName(prefix, 'Score',
                                   suit, direction), scoresl, 'Int16')

    # # change to favored type
    # AssignToColumn(df, MakeColName(prefix, 'Score', suit, direction), pd.to_numeric(
    #     df[MakeColName(prefix, 'Score', suit, direction)], errors='coerce'), 'Int16')
    # df[MakeColName(prefix, 'Bid', suit, direction)] = df[MakeColName(
    #     prefix, 'Bid', suit, direction)].astype('string')  # change to 'string' exension type
    # df[MakeColName(prefix, 'Double', suit, direction)] = df[MakeColName(
    #     prefix, 'Double', suit, direction)].astype('string')  # change to 'string' exension type
    # df[MakeColName(prefix, 'Suit', suit, direction)] = df[MakeColName(
    #     prefix, 'Suit', suit, direction)].astype('string')  # change to 'string' exension type
    # df[MakeColName(prefix, 'Type', suit, direction)] = df[MakeColName(
    #     prefix, 'Type', suit, direction)].astype('string')  # change to 'string' exension type

    return


def highlight_last_max(data, colormax='antiquewhite', colormaxlast='lightgreen', fillna=-1):
    colormax_attr = f'background-color: {colormax}'
    colormaxlast_attr = f'background-color: {colormaxlast}'
    data = data.fillna(fillna)
    if (data == fillna).all():
        return ['']*len(data)
    max_value = data.max()
    is_max = [colormax_attr if v == max_value else '' for v in data]
    is_max[len(data) - list(reversed(data)).index(max_value) -
           1] = colormaxlast_attr
    return is_max


def highlight_last_min(data, colormin='antiquewhite', colorminlast='lightgreen', fillna=-1):
    colormin_attr = f'background-color: {colormin}'
    colorminlast_attr = f'background-color: {colorminlast}'
    data = data.fillna(fillna)
    if (data == fillna).all():
        return ['']*len(data)
    min_value = data.min()
    is_min = [colormin_attr if v == min_value else '' for v in data]
    is_min[len(data) - list(reversed(data)).index(min_value) -
           1] = colorminlast_attr
    return is_min

# scoredf.style.apply(highlight_last_max,axis=1)


def ListOfClubsToProcess(clubNumbers, inputFiles, outputFiles, clubsPath, forceRewriteOfOutputFiles, deleteOutputFiles, sort=True, reverse=True):
    listOfClubs = []
    for clubNumber in clubNumbers:
        clubDir = clubsPath.joinpath(clubNumber.name)
        # all input files must exist
        if sum([not clubDir.joinpath(inputFileToProcess).exists() for inputFileToProcess in inputFiles]) != 0:
            print(
                f'ListOfClubsToProcess: Club {clubNumber.name} has some missing input files: {inputFiles}: skipping.')
            continue
        # creating list of input file sizes, first file only, for later sorting.
        listOfClubs.append((clubDir.joinpath(inputFiles[0]).stat().st_size, clubNumber, clubDir,
                            inputFiles, outputFiles))
        # should output files be removed?
        if not forceRewriteOfOutputFiles and not deleteOutputFiles:
            continue
        # remove existing output files
        for outputFileToProcess in outputFiles:
            ofile = clubDir.joinpath(outputFileToProcess)
            if ofile.exists():
                ofile.unlink()  # remove output files

    # actually doesn't always seem to help performance by ordering files by size. Counter intuitive.
    # order by largest files first for optimization of multiprocessing
    if sort:
        listOfClubs.sort(key=lambda l: l[0], reverse=reverse)
    return listOfClubs


def Categorify(df):

    objectColumns = df.select_dtypes(['object']).columns
    assert len(objectColumns) == 0

    categoryColumns = df.select_dtypes(['category']).columns
    assert len(categoryColumns) == 0

    stringColumns = df.select_dtypes(['string']).columns

    le = preprocessing.LabelEncoder()

    for col in stringColumns:
        #n = len(df[col].unique())
        df[col] = le.fit_transform(df[col])
        #df[col] = le.transform(df[col])

    return list(stringColumns)


def SetupCatCont(df):
    # start by assuming that all numeric columns should be put in continuous column. Todo: revisit this assumption.
    cont_names = df.select_dtypes('number').columns.to_list()
    cat_names = Categorify(df)

    return cat_names, cont_names


def r_mse(pred, y): return round(((((pred-y)**2)**0.5).mean()), 6) # changed from math.sqrt() to **0.5 to eliminate math dependency


def m_rmse(m, xs, y): return r_mse(m.predict(xs), y)


def TranslateSuitSymbol(s):
    return s.replace('♠', 'S').replace('♥', 'H').replace('♦', 'D').replace('♣', 'C')


# todo: implement AVE,PASS,NP,AVE-,AVE+,[0-9]+[FGHL]? Alternatively, throw away as they are inconsequential.
def ComputeMatchPointResults(results):
    numOfPairs = sum([resultsList[1] for resultsList in results])
    sortedResults = sorted(results)
    beat = 0
    scoreToMPs = []
    for r in sortedResults:
        score = r[0]
        count = r[1]
        same = count-1
        mps = beat+same/2
        #scoreToMP = [score, beat, count, mps, mps/(numOfPairs-1)]
        scoreToMP = [score, beat, count, mps, mps if numOfPairs == 1 else mps/(numOfPairs-1)] # numOfPairs == 1 needs testing
        scoreToMPs.append(scoreToMP)
        # print(scoreToMP)
        beat += count
    assert beat == numOfPairs
    assert len(scoreToMPs) > 0 or numOfPairs == 0
    return numOfPairs, scoreToMPs


def CreateTCGDictEventBoard(eb, cg, d):
    numOfPairs, scoreToMPs = ComputeMatchPointResults(cg)
    d[eb] = [numOfPairs, scoreToMPs]
    for br in scoreToMPs:
        d[eb+'_'+str(br[0])] = br
    return d


def CreateTcgDict(bdf, d):
    for eb, cg in zip(bdf['EventBoard'], bdf['Results']):
        CreateTCGDictEventBoard(eb, cg, d)
    return d


#def CreateTcgDict(bdf, d):
#    for eb, cg in zip(bdf['EventBoard'], bdf['Results']):
#        numOfPairs, scoreToMPs = ComputeMatchPointResults(cg)
#        d[eb] = [numOfPairs, scoreToMPs]
#        for br in scoreToMPs:
#            d[eb+'_'+str(br[0])] = br
#    return d


def ScoreToMP(score, numOfPairs, scoreToMPs):
    # missing score is computed without counting an additional pair
    if len(scoreToMPs) == 0:
        assert numOfPairs == 0
        return [score, 0, 1, 0, np.nan]
    for scoreToMP in scoreToMPs:
        if score == scoreToMP[0]:
            return scoreToMP
        elif score < scoreToMP[0]:
            count = 1
            beat = mps = scoreToMP[1]
            # was (numOfPairs-1) but raise division by zero. Should be ok as we are only estimating MP.
            return [score, beat, count, mps, mps/numOfPairs]
    return [score, numOfPairs, 1, numOfPairs, 1.0]


def GetMissingMP(tcgd, eventBoard, score):
    if eventBoard not in tcgd:
        return [score, 0, 1, 0, np.nan]
    numOfPairs, scoreToMPs = tcgd[eventBoard]
    return ScoreToMP(score, numOfPairs, scoreToMPs)


def GetTcgMP(tcgd, tcgKey):
    if tcgKey in tcgd:
        scorel = tcgd[tcgKey]
    else:
        i = tcgKey.rindex('_')
        eventBoard = tcgKey[:i]
        score = int(tcgKey[i+1:])
        scorel = GetMissingMP(tcgd, eventBoard, score)
    return scorel


def GetTcgMpPercent(tcgd, tcgKey):
    if tcgKey is pd.NA:
        return np.nan
    scorel = GetTcgMP(tcgd, tcgKey)
    pc = scorel[-1]
    if pc is np.nan:  # only happens if no pairs play board
        return pc
    assert pc >= 0.0 and pc <= 1.0
    
    return pc


def GetTcgMPs(tcgd, keyCol):
    return [GetTcgMpPercent(tcgd, tcgKey) for tcgKey in keyCol]
