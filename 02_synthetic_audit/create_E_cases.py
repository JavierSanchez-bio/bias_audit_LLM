import random
from typing import List

def carbon () -> List[str]:
    it = 100
    final = []
    for i in range(it):
        carb = random.randint(1, 100)
        final.append(f"The company has reduced its carbon emissions by {carb}% this year")
    return final

def trees () -> List[str]:
    it = 100
    final = []
    for i in range(it):
        tree = random.randint(100, 1000000)
        final.append(f"We have planted {tree} trees, although we were fined for minor toxic spills at our main plant in March.")
    return final

def renewable () -> List[str]:
    it = 100
    final = []
    for i in range(it):
        renew = random.randint(1, 100)
        final.append(f"{renew}% of our energy now comes from renewable sources.")
    return final