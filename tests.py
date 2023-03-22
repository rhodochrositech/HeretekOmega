import physical as p
import HeretekOmega as h



VanguardUnit = p.Unit(1)
#EvilVanguardUnit = p.Unit(2)
for model in p.Model.getModelList():
    if "ii Vanguard" in model.getName():
        print('adding ', model.getName())
        VanguardUnit.addModel(model)
        #EvilVanguardUnit.addModel(model)
        
print('Normal')
for model in VanguardUnit.getModels():
    print(model.getName())
print('Evil')
#for model in EvilVanguardUnit.getModels():
    #print(model.getName())
# BUG: both of these return empty

# h.optimumAssignment(friendlies=VanguardUnit, enemies=EvilVanguardUnit)
