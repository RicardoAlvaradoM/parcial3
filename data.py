import json

class data:
    data = []

    def read(self):
        with open('data/data.json','r') as file:
            data = json.load(file)
            self.data = data['Items']

    def getDescripcion(self):
        des =[]
        for row in self.data:
            descrip = row['Description']
            if descrip not in des:
                des.append(descrip)
        return des
    
    def getUnitId(self):
        unit = []
        for row in self.data:
            ids = row['UnitId']
            if ids not in unit:
                unit.append(ids)
        return unit
    
    def getLocation(self,Description, UnitId):
        infoLocation = []
        for row in self.data:
            opc1= row['Description']
            opc2= row['UnitId']
            if opc1 == Description and opc2 == UnitId:
                infoLocation.append([opc1, row['LocalTimestamp'], row['Location']])
        return infoLocation