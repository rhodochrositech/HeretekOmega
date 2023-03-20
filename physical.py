import csv
import random
import re


def remove_nonnumeric(s):
    return re.sub(r'\D', '', s)
def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9-]', ' ', text)
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
        self.weapons = 'weapons'
        Model.ModelList.append(self)
    
    def __str__(self):
        return str(self.getStats())
    
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
    def getStats(self):
        return [self.ID, self.line, self.name,
                self.movement, self.weaponSkill, self.ballisticSkill,
                self.strength, self.toughness, self.wounds,
                self.attacks, self.leadership, self.save,
                self.cost, self.weapons, self.base]
def createModels():
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
def loadWeapons():
    with open('Datasheets_wargear.csv',newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            headers = next(reader)
            print([header+str(index) for index,header in enumerate(headers)],)
            count = 0
            while 1:
                try:
                    count+=1
                except Exception as err:
                    print(count,'weapons have been loaded.')
                    print(err)
                    break


if __name__ == '__main__':
    createModels()
    #loadWeapons()
    for i in range(30):
        print(Model.getModelList(i))