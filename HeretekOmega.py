import tensorflow as tf
import csv
import re

# Load the Datasheets.csv file into a dictionary
datasheets = {}


def calculate_damage(skill, strength, toughness, attacks, damage=1):
    print()
    # Calculate ratio to hit
    if skill >= 7:
        hit_ratio = 1
    elif skill <= 1:
        hit_ratio = 1 / 6
    else:
        hit_ratio = (7 - skill) / 6
    print("|Chance to hit:", hit_ratio)
    wound_ratio = "a"

    # Calculate ratio to wound
    if strength * 2 <= toughness:
        wound_ratio = 1 / 6
    elif strength < toughness:
        wound_ratio = 2 / 6
    elif strength == toughness:
        wound_ratio = 3 / 6
    elif strength > toughness:
        wound_ratio = 4 / 6
    elif strength >= toughness * 2:
        wound_ratio = 5 / 6
    print("|Chance to wound:", wound_ratio)
    print("|Attacks:", attacks)

    # Calculate average damage
    avg_damage = (attacks * hit_ratio * damage) * wound_ratio

    return avg_damage


def remove_nonnumeric(s):
    return re.sub(r"\D", "", s)


def fight(attacker_name, defender_name):
    print()
    print("----")
    print("|Skill, Strength, Toughness, Attacks")
    sel_attack = megadict[attacker_name].values()
    attacker = []
    for val in sel_attack:
        attacker.append(int(remove_nonnumeric(val)))
    print("|Attacker:", attacker_name, attacker)
    sel_defender = megadict[defender_name].values()
    defender = []
    for val in sel_defender:
        defender.append(int(remove_nonnumeric(val)))
    print("|Defender:", defender_name, defender)
    result = calculate_damage(attacker[0], attacker[1], defender[2], attacker[3])
    print("|Average damage: ", result)
    print("----")
    return result


with open("cleandata.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    # print(headers)
    count = 0
    megadict = {}
    while 1:
        try:
            count += 1
            row = next(reader)
            # if row[2] in megadict:
            # print('duplicate',row[2])
            megadict[row[2]] = {
                "skill": row[4],
                "strength": row[6],
                "toughness": row[7],
                "attacks": row[9],
            }
        except:
            # print(count)
            break
    print(len(megadict), "units have been loaded.")
    # print(megadict['Rough Rider'])

    fight("Skitarii Vanguard", "Rough Rider")
    fight("Rough Rider", "Skitarii Vanguard")
    fight("Skitarii Vanguard", "Shock Trooper")
    fight("Shock Trooper", "Skitarii Ranger")
    fight("Ironstrider Ballistarius", "Skitarii Ranger")
    fight("Skitarii Ranger", "Ironstrider Ballistarius")
    print(megadict["Kastelan Robot"].values())
    print(megadict["Redemptor Dreadnought"].values())

friendlies = ["Skitarii Vanguard", "Rough Rider"]
enemies = [
    megadict["Ironstrider Ballistarius"].values(),
    megadict["Skitarii Ranger"].values(),
]


def attackSpace(squad):
    space = []
    for creature in squad:
        # convert each creature with multiple attacks into
        # imaginary "component creatures" with only one attack
        # and otherwise identical stats, to preserve utility
        # of calculate_damage
        for i in range(megadict[creature].values()[3]):
            space += [megadict[creature].values()[0:3] + [1]]
    return space


def enemyHealth(e):
    return e[8]


class DamageKeyGivenEnemy:
    def __init__(self, bg):
        self.bg = bg

    def damage(self, fg):
        return calculate_damage(fg, bg)


# inspo:
# So basically, you start with the weakest enemies, and assign your weakest units to them. Go down the list like this, until one of these things happens:
#
# If you reach a higher priority enemy that you can kill with these units (including units you've already assigned!!!), you want to pull units off the low value targets and reassign to the higher value target. The condition for this can be some function of the priority difference between the high value target and the priority of the units you would have killed instead, but no longer can.
#
# If you reach a unit you can't kill with these units, you should stop going through the list, because they are ordered by their health and will only get tougher.
# [7:03 PM]
# The idea here is that you are passing on low value target kills to  "pay" for the cost of a high priority high health target
# [7:04 PM]
# So when you reassign units, you will start with the first units you assigned (who are killing low health low priority targets) (edited)
# [7:06 PM]
# After you "steal" a unit from an earlier assignment, you might have to fix the first portion of the solution. An easy way to do that would be to run the algorithm again on just that part of the solution, although there is surely a better way.
# [7:07 PM]
# does any of that make sense?
#
friendlyAttacks = attackSpace(friendlies)
scenario = []
for i in range(enemies):
    scenario += [[]]
enemiesByHealth = enemies.sort(reverse=True, key=enemyHealth)
i = 0
while i < len(enemiesByHealth):
    # remember to update i!!!!
    # clocking out for tonight [2023-03-09 Thu 21:05].
    # TODO: Add check to this loop
    currentDamage = DamageKeyGivenEnemy(enemiesByHealth[i])
    friendlyAttacksByDamage = friendlyAttacks.sort(
        reverse=True, key=currentDamage.damage
    )
    j = 0
    damageDone = 0
    while j < len(friendlyAttacksByDamage) and damageDone < enemiesByHealth[i][8]:
        damageDone += currentDamage.damage(friendlyAttacksByDamage[j])
        scenario[i] += [friendlyAttacksByDamage[j]]
        j += 1
    # if the loop terminates because we have used up all of our troops,
    # hail-mary all of the troops at that enemy
    if j == len(friendlyAttacksByDamage):
        scenario[i] += friendlyAttacksByDamage()
    i += 1
