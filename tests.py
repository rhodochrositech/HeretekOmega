import physical as p
import HeretekOmega as h

unit = []
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        # print(model.getStats())
        unit.append(model)
unit.append(unit[1])
unit.append(unit[1])
unit.append(unit[1])
VanguardUnit = p.Unit(1, unit)
EvilVanguardUnit = p.Unit(2, unit)
print(VanguardUnit.getModels())
print(EvilVanguardUnit.getModels())
# BUG: both of these return empty

# h.optimumAssignment(friendlies=VanguardUnit, enemies=EvilVanguardUnit)
