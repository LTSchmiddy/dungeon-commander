import random

import re
from collections import namedtuple

from dungeonsheets.exceptions import DiceError

dice_re = re.compile('(\d+)d(\d+)', flags=re.I)
Dice = namedtuple('Dice', ('num', 'faces'))

digits = "0123456789"

def read_dice_str(dice_str: str):
    """Interpret a D&D dice string, eg. 3d10.

    Returns
    -------
    dice : tuple
      A named tuple with the scheme (num, faces), so '3d10' return
      (num=3, faces=10)

    """
    match = dice_re.match(dice_str)
    if match is None:
        raise DiceError(f"Cannot interpret dice string {dice_str}")
    dice = Dice(num=int(match.group(1)),
                faces=int(match.group(2)))
    return dice

def read_dice_str_safe(dice_str: str) -> Dice:
    """Interpret a D&D dice string, eg. 3d10.

    Returns
    -------
    dice : tuple
      A named tuple with the scheme (num, faces), so '3d10' return
      (num=3, faces=10)

    """
    match = dice_re.match(dice_str)
    if match is None:
        return None
    dice = Dice(num=int(match.group(1)),
                faces=int(match.group(2)))
    return dice

def roll_dice(p_dice: Dice):
    total = 0
    for i in range(0, p_dice.num):
        total += random.randint(1, p_dice.faces)

    return total


def parse_dice(exp: str) -> str:
    outstr = ""
    c_pos = 0
    dstr = ""

    while c_pos < len(exp) + 1:
        if c_pos == len(exp) or exp[c_pos] not in (digits + "d"):

            dice_check = read_dice_str_safe(dstr)
            # print(dice_check)
            if dice_check is not None:
                outstr += str(roll_dice(dice_check))
            else:
                outstr += dstr

            if c_pos == len(exp):
                break

            # outstr += exp[c_pos]
            if exp[c_pos] in (digits + "d"):
                dstr = exp[c_pos]
            else:
                dstr = ""
                outstr += exp[c_pos]

            c_pos += 1

            # print(f"dstr={dstr}")
            # print(f"outstr={outstr}")
            continue

        dstr += exp[c_pos]
        c_pos += 1

        # print(f"dstr={dstr}")
    # print(f"outstr={outstr}")

    return outstr

def eval_dice(dice_str: str):
    return eval(parse_dice(dice_str))