import tensorflow as tf
import csv
import re

# Load the Datasheets.csv file into a dictionary
datasheets = {}


def calculate_damage(skill, strength, toughness, attacks, damage=1):
    print()
    # Calculate ratio to hit
    # TODO: Refactor this to reflect new model representation
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
    # convert each creature with multiple attacks into
    # imaginary "component creatures" with only one attack
    # and otherwise identical stats, to preserve utility
    # of calculate_damage
    space = []
    for creature in squad:
        for i in range(megadict[creature].values()[3]):
            space += [megadict[creature].values()[0:3] + [1]]
    return space


def enemyHealth(e):
    # TODO: Change enemyHealth to reflect refactoring of models
    return e[8]


class DamageKeyGivenEnemy:
    # when instantiated on a bg, acts as a function which maps
    # unit -> (damage done by unit to bg)
    def __init__(self, bg):
        self.bg = bg

    def key(self, fg):
        return calculate_damage(fg, bg)


def optimumAssignment(self, friendlies, enemies):
    # figure out which of your guys should shoot which of the bad guys
    # so that you get the most points possible
    #
    # some assumptions: for any enemy e, e[9] is the points the enemy is worth

    # see the definition of friendlyAttacks
    friendlyAttacks = attackSpace(friendlies)

    # here we are going to represent the assignment as a dict, whose
    # keys are the attacks, and values are the enemies each key will
    # target.
    #
    # initialize this dict as everyone attacking the first enemy to begin with
    noTargets = []
    for i in friendlyAttacks:
        noTargets += [enemies[0]]
    target = dict(zip(friendlyAttacks, noTargets))

    # sort enemies by health, weakest first
    enemiesByHealth = enemies.sort(reverse=True, key=enemyHealth)
    i = 0
    while i < len(enemiesByHealth):
        currentEnemy = enemiesByHealth[i]
        # DONE: remember to update i!!!!
        # clocking out for tonight [2023-03-09 Thu 21:05].
        # clocking out [2023-03-20 Mon 5:55]
        # TODO: Add check to this loop
        # TODO: Handle the case where some attacks are never assigned
        # REVIEW: suppose a1 and a2 are assigned to e1, and a1, a2, and a3
        # get assigned to e2 in the next iteration, but a3
        # on its own is enough to kill a3. we could have killed
        # both e1 and e2, but instead are "overkilling" e2.
        #
        # instantiate the key on the current enemy
        currentDamage = DamageKeyGivenEnemy(currentEnemy)

        # create a new list which is the list of friendly units sorted by
        # how much damage they do to the ith enemy, weakest first
        friendlyAttacksByDamage = friendlyAttacks.sort(
            reverse=True, key=currentDamage.key
        )

        j = 0
        damageDone = 0
        while j < len(friendlyAttacksByDamage) and damageDone < enemyHealth(
            currentEnemy
        ):
            damageDone += currentDamage.key(friendlyAttacksByDamage[j])
            j += 1

        # if we can kill the ith enemy, assign him as the target of the 0-j
        # friendlyAttacks iff he is worth more points than the sum of points
        # of their previous targets.
        if damageDone >= enemyHealth(currentEnemy):

            # get the list of previous targets as a set to remove duplicates
            previousTargets = set([])
            for attack in friendlyAttacksByDamage[0 : j + 1]:
                previousTargets.add(target[attack])

            # sum the value of their previous targets
            previousPoints = 0
            for target in previousTargets:
                previousPoints += target[9]

            # if we gain more points by attacking the currentEnemy
            if previousPoints < currentEnemy[9]:
                for k in range(0, j + 1):
                    # if we actually need this attack to kill the
                    # higher priority currentEnemy, reassign it.
                    # otherwise, do nothing- our cause is better
                    # forwarded by having it attack another enemy,
                    # even if it will not kill it
                    #
                    # Since not reassigning an attack will only
                    # effectively decrease previousPoints, the
                    # outer condition is still valid.
                    if damageDone - currentDamage.key(
                        friendlyAttacksByDamage[k]
                    ) < enemyHealth(currentEnemy):
                        target[attack] = currentEnemy

        # if the previousPoints condition is not met, or we have
        # finished the sub-loop, we have reassigned profitably,
        i += 1
