import physical as p
import HeretekOmega as h


staticModelList = []
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        staticModelList.append(model)

        # NewUnit = p.Squad(3)
        # for model in p.Model.getModelList():
        #     if "Onager" in model.getName() or "Boy" in model.getName():
        #         NewUnit.addModel(model)

VanguardUnit = []
Evil = []

for model in staticModelList:
    print("adding ", model.getName())
    VanguardUnit.append(model.copyModel())
    VanguardUnit.append(model.copyModel())
    VanguardUnit.append(model.copyModel())
for model in staticModelList:
    print("adding ", model.getName())
    Evil.append(model.copyModel())
squad1 = p.Squad(UID=1, models=VanguardUnit)
squad2 = p.Squad(UID=2, models=Evil)

print(squad1.getModels())
print(squad2.getModels())
x = h.optimumAssignment(friendlies=squad1, enemies=squad2)

for attack, target in x.items():
    print(attack.getName(), "attacks", target)
