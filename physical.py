import csv
import random
import re


def remove_nonnumeric(s):
    return re.sub(r'\D', '', s)
def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9-]', ' ', text)

class Unit:
    UnitList = []
    def __init__(self, UID, subUID = False, models=[]):
        self.UID = UID
        self.subUID = subUID
        self.models = models
        Unit.UnitList.append(self)

    @staticmethod
    def cleanSubUnits():
        index = 0
        for unit in Unit.UnitList:
            if unit.getSubUID():
                Unit.UnitList.pop(index)
            index+=1

    def getUID(self):
        return self.UID
    def getSubUID(self):
        return self.subUID
    def getModels(self):
        return self.models

    def createSubUnit(self, subUID, begin, end):
        Unit(self.UID, subUID, self.models[begin:end])
    def cumulative_model(self):
        return False
    #createSubUnit(self, [int1,int2])


class Model:
    #TODO: ADD IN WEAPONS CATEGORY LIST
    ModelList = []
    #datasheet_id,line,name,M,WS,BS,S,T,W,A,Ld,Sv,Cost
    def __init__(self, ID, line, name, movement, weaponSkill, ballisticSkill, strength, toughness, wounds, attacks, leadership, save, cost, base,):
        self.ID = ID
        self.line = line
        self.name = remove_non_alphanumeric(name)
        self.movement = movement
        self.weaponSkill = remove_nonnumeric(weaponSkill)
        self.ballisticSkill = remove_nonnumeric(ballisticSkill)
        self.strength = strength
        self.toughness = toughness
        self.wounds = wounds
        self.attacks = attacks
        self.leadership = leadership
        self.save = remove_nonnumeric(save)
        self.cost = cost
        self.base = base
        self.weapons = []
        Model.ModelList.append(self)

    
    def __str__(self):
        return str(self.getStats(clean = True))
    
    @staticmethod
    def getModelList(index = 'False'):
        try:
            if index != 'False':
                return Model.ModelList[index]
            return Model.ModelList
        except Exception as err:
            print('non-index given for getModelList')
            return(err)
        

    def getID(self):
        return self.ID
    def getLine(self):
        return self.line
    def getName(self):
        return self.name    
    def getMovement(self):
        return self.movement
    def getWeaponSkill(self):
        return self.weaponSkill
    def getBallisticSkill(self):
        return self.ballisticSkill
    def getStrength(self):
        return self.strength
    def getToughness(self):
        return self.toughness 
    def getWounds(self):
        return self.wounds 
    def getAttacks(self):
        return self.attacks
    def getLeadership(self):
        return self.leadership
    def getSave(self):
        return self.save
    def getCost(self):
        return self.cost
    def getBase(self):
        return self.base
    def getWeapons(self):
        return self.weapons
    def addWeapons(self, weapon):
        self.weapons.append(weapon)
    def getStats(self, clean=False):
        if not clean:
            return [self.ID, self.line, self.name,
                    self.movement, self.weaponSkill, self.ballisticSkill,
                    self.strength, self.toughness, self.wounds,
                    self.attacks, self.leadership, self.save,
                    self.cost, self.weapons, self.base]
        else:
            stats = [self.ID, self.line, self.name,
                    self.movement, self.weaponSkill, self.ballisticSkill,
                    self.strength, self.toughness, self.wounds,
                    self.attacks, self.leadership, self.save,
                    self.cost]
            for weapon in self.weapons:
                stats.append(weapon.getName())
            stats.append(self.base)
            return stats

class WeaponConnection:
    WeaponconnList = []

    @staticmethod
    def getWeaponconnList(index = 'False'):
        try:
            if index != 'False':
                return WeaponConnection.WeaponconnList[index]
            return WeaponConnection.WeaponconnList
        except Exception as err:
            print('non-index given for getWeaponconnList')
            return(err)

    def __init__(self, DID, line, wargear_id,cost,is_index_wargear,model,is_upgrade):
        self.DID = DID
        self.line = line
        self.wargear_id = wargear_id
        self.cost = cost
        self.is_index_wargear = is_index_wargear
        self.model = model
        self.is_upgrade = is_upgrade
        WeaponConnection.WeaponconnList.append(self)
    def getDID(self):
        return self.DID
    def getLine(self):
        return self.line
    def getWargear_id(self):
        return self.wargear_id
    def getCost(self):
        return self.cost
    def getIs_index_wargear(self):
        return self.is_index_wargear
    def getModel(self):
        return self.model
    def getIs_upgrade(self):
        return self.is_upgrade
    
    def getStats(self):
        return [self.DID, self.line, self.wargear_id,
                self.cost, self.is_index_wargear, self.model,
                self.is_upgrade]
    def __str__(self):
        return str(self.getStats())

class Weapon:
    WeaponList = []

    @staticmethod
    def getWeaponList(index = 'False'):
        try:
            if index != 'False':
                return Weapon.WeaponList[index]
            return Weapon.WeaponList
        except Exception as err:
            print('non-index given for getWeaponList')
            return(err)
    def __init__(self, wargear_id, line, name, range, type, strength, ap, damage, abilities):
        self.wargear_id = wargear_id
        self.line = line
        self.name = name
        self.range = range
        self.type = type
        self.strength = strength
        self.ap = ap
        self.damage = damage
        self.abilities = abilities
        Weapon.WeaponList.append(self)
    
    def getWargear_id(self):
        return self.wargear_id
    def getLine(self):
        return self.line
    def getName(self):
        return self.name
    def getRange(self):
        return self.range
    def getType(self):
        return self.type
    def getStrength(self):
        return self.strength
    def getAP(self):
        return self.ap
    def getDamage(self):
        return self.damage
    def getAbilities(self):
        return self.abilities
    def getStats(self):
        return [self.wargear_id, self.line, self.name,
                self.range, self.type, self.strength,
                self.ap, self.damage, self.abilities]
    def __str__(self):
        return str(self.getStats())


def loadModels():
    with open('Datasheets_models.csv',newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            headers = next(reader)
            #print([header+str(index) for index,header in enumerate(headers)],)
            count = 0
            while 1:
                try:
                    row = next(reader)
                    Model(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[16])
                    count += 1
                except Exception as err:
                    print(count,'models have been loaded.')
                    print(err)
                    break
def loadWeaponConnection():
    with open('Datasheets_wargear.csv',newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            headers = next(reader)
            #print([header+str(index) for index,header in enumerate(headers)],)
            count = 0
            while 1:
                try:
                    row = next(reader)
                    WeaponConnection(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    count+=1
                except Exception as err:
                    print(count,'weapons have been loaded.')
                    print(err)
                    break

def loadWeapons():
    with open('Wargear_list.csv',newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            headers = next(reader)
            #print([header+str(index) for index,header in enumerate(headers)],)
            count = 0
            while 1:
                try:
                    row = next(reader)
                    Weapon(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    count+=1
                except Exception as err:
                    print(count,'weapons have been loaded.')
                    print(err)
                    break

def populateWeapons():
    for model in Model.getModelList():
        for weaponconn in WeaponConnection.getWeaponconnList():
            if model.getID() == weaponconn.getDID():
                for weapon in Weapon.getWeaponList():
                    if weapon.getWargear_id() == weaponconn.getWargear_id():
                        model.addWeapons(weapon)


loadModels()
loadWeapons()
loadWeaponConnection()
populateWeapons()
if __name__ == '__main__':
    unit = []
    
    for i in range(5):
        print(Model.getModelList(i))
    for i in range(10):
        print(WeaponConnection.getWeaponconnList(i))
    for model in Model.getModelList():
        if 'ii Vanguard' in model.getName():
            #print(model.getStats())
            unit.append(model)
    #print(unit)
    for model in unit:
        print(model)
    