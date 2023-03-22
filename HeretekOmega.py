# REVIEW: Why is this the case? Shouldn't we be "using" p whenever we call
# a method specific to Model() or Unit()?
import physical as p


def calculate_damage(attacker, attacked):
    skill = attacker.getSkill()
    strength = attacker.getStrength()
    attacks = 1
    damage = attacker.getDamage()
    toughness = attacked.getToughness()
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
    # DONE: E999 SyntaxError: positional argument follows keyword argument no idea what this is
    # p.Unit(unit.UID, unit.subUID, unit.models.sort(reverse=True, modelPoints))

    sortedUnit = unit
    sortedUnit.setModels(unit.getModels().sort(modelPoints, reverse=True))
    i = 0
    outputSpace = []
    while i < len(sortedUnit.models):
        currentSubUnit = sortedUnit.subUnit(i, 0, i + 1)
        tranch = currentSubUnit.cumulative()
        outputSpace += [tranch]
        i += 1


def enemyHealth(e):
    # DONE: Change enemyHealth to reflect refactoring of models.
    # Note: "wounds" are health
    return e.getHealth()


class DamageKeyGivenEnemy:
    # When instantiated on a bg, acts as a function which maps
    # unit -> (damage done by unit to bg).
    def __init__(self, bg):
        self.bg = bg

    def key(self, fg):
        return calculate_damage(fg, self.bg)


def optimumAssignment(self, friendlies, enemies):
    # Figure out which of your guys should shoot which of the bad guys
    # so that you get the most points possible.
    #
    # Some assumptions: for any enemy e, e[9] is the points the enemy is worth.
    # DONE: Refactor this so enemyPoints is a method called on e.
    # TODO: Write and implement some tests.

    # See the definition of friendlyAttacks.
    friendlyAttacks = attackSpace(friendlies)

    # Here we are going to represent the assignment as a dict, whose
    # keys are the attacks, and values are the enemies each key will
    # target.
    #
    # Initialize this dict as everyone attacking the first enemy to begin with.
    noTargets = []
    for i in friendlyAttacks:
        noTargets += [enemies[0]]
    target = dict(zip(friendlyAttacks, noTargets))

    # Sort enemies by health, weakest first.
    enemiesByHealth = enemies.sort(reverse=True, key=enemyHealth)
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
