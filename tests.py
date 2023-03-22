import physical as p
import HeretekOmega as h



VanguardUnit = p.Squad(1)
EvilVanguardUnit = p.Squad(2)
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        print('adding ', model.getName())
        VanguardUnit.addModel(model)
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        print('adding ', model.getName())
        EvilVanguardUnit.addModel(model)


NewUnit = p.Squad(3)
for model in p.Model.getModelList():
    if "Onager" in model.getName():
        NewUnit.addModel(model)

print('Normal')
for model in VanguardUnit.getModels():
    print(model.getName())
print('Evil')
for model in EvilVanguardUnit.getModels():
    print(model.getName())
print('Tank')
for model in NewUnit.getModels():
    print(model.getName())
# BUG: both of these return empty

# h.optimumAssignment(friendlies=VanguardUnit, enemies=EvilVanguardUnit)
