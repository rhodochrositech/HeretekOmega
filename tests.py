import physical as p
import HeretekOmega as h


VanguardUnit = p.Squad(UID=1)
EvilVanguardUnit = p.Squad(UID=2)
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        print("adding ", model.getName())
        VanguardUnit.addModel(model)
        VanguardUnit.addModel(model)
        VanguardUnit.addModel(model)
        VanguardUnit.addModel(model)
        EvilVanguardUnit.addModel(model)

# NewUnit = p.Squad(3)
# for model in p.Model.getModelList():
#     if "Onager" in model.getName() or "Boy" in model.getName():
#         NewUnit.addModel(model)

print(VanguardUnit.getModels())
print(EvilVanguardUnit.getModels())
x = h.optimumAssignment(friendlies=VanguardUnit, enemies=EvilVanguardUnit)

for attack, target in x.items():
    print(attack.getName(), "attacks", target.getName())
