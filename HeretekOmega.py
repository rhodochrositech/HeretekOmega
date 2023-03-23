# REVIEW: Why is this the case? Shouldn't we be "using" p whenever we call
# a method specific to Model() or Unit()?


def calculate_damage(attacker, attacked):
    # TODO: Change this when we add guns.
    skill = attacker.getWeaponSkill()
    strength = attacker.getStrength()
    attacks = 1
    # TODO: Change this to something like attacker.getDamage() and write this method
    # which should be dependent on weapon.

    damage = 1
    toughness = attacked.getToughness()
    # Calculate ratio to hit
    # DONE: Refactor this to reflect new model representation
    if skill >= 7:
        hit_ratio = 1
    elif skill <= 1:
        hit_ratio = 1 / 6
    else:
        hit_ratio = (7 - skill) / 6
    # print("|Chance to hit:", hit_ratio)
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
    # print("|Chance to wound:", wound_ratio)
    # print("|Attacks:", attacks)

    # Calculate average damage
    avg_damage = (attacks * hit_ratio * damage) * wound_ratio

    return avg_damage


def attackSpace(squad):
    # Convert each creature with multiple attacks into
    # imaginary "component creatures" with only one attack
    # and otherwise identical stats, to preserve utility
    # of calculate_damage
    space = []
    for model in squad.getModels():
        for i in range(model.getAttacks()):
            virtualModel = model
            virtualModel.setAttacks(1)
            space += [virtualModel]
    return space


def modelPoints(m):
    # DONE: Refactor this to account for new model format.
    return m.getCost()


def unitSpace(unit):
    sortedUnit = unit
    sortedUnit.setModels(sorted(unit.getModels(), key=modelPoints, reverse=True))
    i = 0
    outputSpace = []
    while i < len(sortedUnit.getModels()):
        currentSubUnit = sortedUnit.createSubUnit(i, 0, i + 1)
        tranch = currentSubUnit.cumulativeModel()
        outputSpace += [tranch]
        i += 1
    return outputSpace


def enemyHealth(e):
    # DONE: Change enemyHealth to reflect refactoring of models.
    # Note: "wounds" are health
    return e.getWounds()


class DamageKeyGivenEnemy:
    # When instantiated on a bg, acts as a function which maps
    # unit -> (damage done by unit to bg).
    def __init__(self, bg):
        self.bg = bg

    def key(self, fg):
        return calculate_damage(fg, self.bg)


def optimumAssignment(friendlies, enemies):
    friendlyAttacks = attackSpace(friendlies)
    enemyTargets = unitSpace(enemies)
    print("This is friendly attacks")
    print(friendlyAttacks)
    print()
    print("this is enemyTargets")
    print(friendlyAttacks)

    # Here we are going to represent the assignment as a dict, whose
    # keys are the attacks, and values are the enemies each key will
    # target.

    # Initialize this dict as everyone attacking the first enemy to begin with.
    noTargets = []
    for i in friendlyAttacks:
        noTargets += [enemyTargets[0]]
    target = dict(zip(friendlyAttacks, noTargets))

    # Sort enemies by health, weakest first.
    enemiesByHealth = sorted(enemyTargets, key=enemyHealth, reverse=True)
    i = 0
    while i < len(enemiesByHealth):
        currentEnemy = enemiesByHealth[i]
        # TODO: Handle the case where some attacks are never assigned
        # REVIEW: Suppose a1 and a2 are assigned to e1, and a1, a2, and a3
        # get assigned to e2 in the next iteration, but a3
        # on its own is enough to kill a3. We could have killed
        # both e1 and e2, but instead are "overkilling" e2.
        #
        # Instantiate the key on the current enemy.
        currentDamage = DamageKeyGivenEnemy(currentEnemy)

        # Create a new list which is the list of friendly units sorted by
        # how much damage they do to the ith enemy, weakest first.
        friendlyAttacksByDamage = sorted(
            friendlyAttacks, key=currentDamage.key, reverse=True
        )

        j = 0
        damageDone = 0
        while j < len(friendlyAttacksByDamage) and damageDone < enemyHealth(
            currentEnemy
        ):
            damageDone += currentDamage.key(friendlyAttacksByDamage[j])
            j += 1

        # If we can kill the ith enemy, assign him as the target of the 0-j
        # friendlyAttacks iff he is worth more points than the sum of points
        # of their previous targets.
        if damageDone >= enemyHealth(currentEnemy):

            # Get the list of previous targets as a set to remove duplicates.
            previousTargets = set([])
            for attack in friendlyAttacksByDamage[0 : j + 1]:
                previousTargets.add(target[attack])

            # Sum the value of their previous targets.
            previousPoints = 0
            for target in previousTargets:
                previousPoints += modelPoints(target)

            # If we gain more points by attacking the currentEnemy.
            if previousPoints < modelPoints(currentEnemy):
                for k in range(0, j + 1):
                    # If we actually need this attack to kill the
                    # higher priority currentEnemy, reassign it.
                    # Otherwise, do nothing- our cause is better
                    # forwarded by having it attack another enemy,
                    # even if it will not kill it.
                    #
                    # Since not reassigning an attack will only
                    # effectively decrease previousPoints, the
                    # outer condition is still valid.
                    if damageDone - currentDamage.key(
                        friendlyAttacksByDamage[k]
                    ) < enemyHealth(currentEnemy):
                        target[attack] = currentEnemy

        # If the previousPoints condition is not met, or we have
        # finished the sub-loop, we have assigned profitably.
        i += 1
    return target
