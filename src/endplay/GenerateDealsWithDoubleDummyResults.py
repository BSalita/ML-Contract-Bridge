# Generate hands, with constraints, and their double dummy results.

# Contains example code to:
# 1. Calculate distribution points.
# 2. Function to handle constraint.
# 3. Specifying a predeal string.
# 4. Generate multiple deals.
# 5. Calculate double dummy for all deals.
# 6. Create tuples of double dummy results for future processing (direction (rows) by suit (columns)).
# 7. Display hand, double dummy results

from endplay.dealer import generate_deals
from endplay.types import Deal
from endplay.dds import calc_all_tables
from endplay.evaluate import hcp

def dist_points_suit(suit, points=[3,2,1]+[0]*10):
    return points[len(suit)]

def dist_points(hand):
    return sum([dist_points_suit(suit) for suit in [hand.clubs, hand.diamonds, hand.hearts, hand.spades]])
        
def constraints(deal):
    points = hcp(deal.west)+dist_points(deal.west)-dist_points_suit(deal.west.spades)
    return points >= 13 and points <= 15 and len(deal.west.spades) <= 4 and len(deal.west.hearts) >= 5 and len(deal.west.diamonds) < 5 and len(deal.west.clubs) < 5

predeal = Deal('N:... AK962.Q86.J.9743 ... ...')
swapping = 0 # either 0 (no swapping), 2 (swapping EW) or 3 (swapping EWS)
show_progress = False
produce = 10
seed = None # or any int
max_attempts = 1000
env = dict()
strict = True

d = generate_deals(
    constraints,
    predeal=predeal,
    swapping=swapping,
    show_progress=show_progress,
    produce=produce,
    seed=seed,
    max_attempts=max_attempts,
    env=env,
    strict=strict
    )

d_t = tuple(d) # create a tuple before the storage goes wonky
tables = calc_all_tables(d_t)
t_t = (tt._data.resTable for tt in tables)
for ii,(dd,sd,tt) in enumerate(zip(d_t,t_t,tables)):
    print(f"Deal: {ii+1}")
    dd.pprint()
    print()
    tt.pprint()
    print(tuple(tuple(sd[suit][direction] for suit in [3,2,1,0,4]) for direction in [0,2,3,1]))
    print()