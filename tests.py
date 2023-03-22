#!/usr/bin/env python3
import physical as p
import HeretekOmega as heretek


unit = []
for model in Model.getModelList():
        if 'ii Vanguard' in model.getName():
            #print(model.getStats())
            unit.append(model)
unit.append(unit[1])
unit.append(unit[1])
unit.append(unit[1])
VanguardUnit = Unit(1,unit)
EvilVanguardUnit = Unit(2,unit)
print(VanguardUnit)
print(EvilVanguardUnit)
