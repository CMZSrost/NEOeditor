import numpy as np
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class gameDB:
    def __init__(self, type):
        self.type = type
        self.column = ['modid', 'modstr']
        self.column.extend(self.getcolumn(type))
        self.map = dict(zip(self.column, range(len(self.column))))
        self.data = np.array([], dtype=str)

    def getcolumn(self, type):
        if type == 'encounters':
            return ['id', 'strName', 'strDesc', 'strImg', 'nTreasureID', 'nRemoveTreasureID', 'aConditions',
                    'aPreConditions', 'fPrice', 'aResponses', 'aMinimapHexes', 'bRemoveCreatures', 'bRemoveUsed',
                    'nItemsID', 'nCreatureID', 'ptCreatureHex', 'ptTeleport', 'ptEditor', 'nType', 'fLootChance',
                    'fAccidentChance', 'fCreatureChance', 'vAccidents', 'vLoot']
        elif type == 'encountertriggers':
            return ['id', 'strName', 'nEncounterID', 'fChance', 'bLocBased', 'bDateBased', 'bHexBased', 'bUnique',
                    'bAIPassable', 'aArea', 'dateMin', 'dateMax', 'aHexTypes']
        elif type == 'factions':
            return ['id', 'strName', 'dictFactions']
        elif type == 'forbiddenhexes':
            return ['id', 'nX', 'nY', 'strName']
        elif type == 'gamevars':
            return ['strName', 'strType', 'strValue']
        elif type == 'headlines':
            return ['id', 'strHeadline']
        elif type == 'hextypes':
            return ['id', 'strName', 'strDesc', 'nTerrainCost', 'nVizLimiter', 'nVizIncrease', 'nTreasureID',
                    'bPassable', 'nScavengeInitialID', 'nScavengeItemsIDPerHour', 'nCampItems', 'vLightLevels',
                    'nDefaultCampID', 'nMinRange', 'nMaxRange', 'vCondIDs']
        elif type == 'ingredients':
            return ['nID', 'strName', 'strRequiredProps', 'strForbidProps']
        elif type == 'itemprops':
            return ['nID', 'strPropertyName']
        elif type == 'itemtypes':
            return ['id', 'nGroupID', 'nSubgroupID', 'strName', 'strDesc', 'strDescAlt', 'nCondID', 'vImageList',
                    'vSpriteList', 'vImageUsage', 'fWeight', 'fMonetaryValue', 'fMonetaryValueAlt', 'fDurability',
                    'fDegradePerHour', 'fEquipDegradePerHour', 'fDegradePerUse', 'vDegradeTreasureIDs',
                    'aEquipConditions', 'aPossessConditions', 'aUseConditions', 'aCapacities', 'vEquipSlots',
                    'vUseSlots', 'bSocketLocked', 'vProperties', 'aContentIDs', 'nFormatID', 'nTreasureID',
                    'nComponentID', 'bMirrored', 'nSlotDepth', 'strChargeProfiles', 'aAttackModes', 'nStackLimit',
                    'aSwitchIDs', 'aSounds']
        elif type == 'maps':
            return ['id', 'strName', 'strDef']
        elif type == 'recipes':
            return ['nID', 'strName', 'strSecretName', 'strTools', 'strConsumed', 'strDestroyed', 'nTreasureID',
                    'fHours', 'nReverse', 'nHiddenID', 'bIdentify', 'bTransferComponents', 'vAlsoTry',
                    'nTempTreasureID', 'bDegradeOutput', 'strType', 'bScrap']
        elif type == 'treasuretable':
            return ['id', 'strName', 'aTreasures', 'bNested', 'bSuppress', 'bIdentify']
        elif type == 'attackmodes':
            return ["id", "strName", "strNotes", "nRange", "fDamageCut", "fDamageBlunt", "strChargeProfiles",
                    "nPenetration", "nType", "strSnd", "bTransfer", "vAttackerConditions", "strIMG", "fMorale",
                    "strWieldPhrase", "vAttackPhrases"]
        elif type == 'barterhexes':
            return ['id', 'nX', 'nY', 'bBuys', 'nRestockTreasureID']
        elif type == 'battlemoves':
            return ['id', 'strID', 'strName', 'strNotes', 'strSuccess', 'strFail', 'strPopUp', 'vChanceType',
                    'vUsConditions', 'vThemConditions', 'vPairConditions', 'vUsFailConditions', 'vThemFailConditions',
                    'vPairFailConditions', 'vUsPreConditions', 'vThemPreConditions', 'nSeeThem', 'nSeeUs',
                    'bAllOutOfRange', 'bInAttackRange', 'nMinCharges', 'nMinRange', 'nMaxRange', 'nAttackModeType',
                    'vHexTypes', 'fChance', 'fPriority', 'fDetect', 'fOrder', 'fFatigue', 'bApproach', 'bOffense',
                    'bFallBack', 'bRetreat', 'bPosition', 'bPassive']
        elif type == 'camptypes':
            return ['id', 'strDesc', 'vImageList', 'aCapacities', 'nTreasureID', 'm_fAlertness', 'm_fVisibility',
                    'WetTempAdjustMod', 'm_fHealPerHourMod', 'fSleepQuality']
        elif type == 'chargeprofiles':
            return ['nID', 'strName', 'strItemID', 'fPerUse', 'fPerHour', 'fPerHourEquipped', 'fPerHex', 'bDegrade']
        elif type == 'conditions':
            return ['id', 'strName', 'strDesc', 'aFieldNames', 'aModifiers', 'aEffects', 'bFatal', 'vIDNext',
                    'fDuration', 'bPermanent', 'vChanceNext', 'bStackable', 'bDisplay', 'bDisplayOther',
                    'bDisplayGameOver', 'nColor', 'bResetTimer', 'bRemoveAll', 'bRemovePostCombat', 'nTransferRange',
                    'aThresholds']
        elif type == 'containertypes':
            return ['id', 'strName']
        elif type == 'creatures':
            return ['id', 'strName', 'strNamePublic', 'strNotes', 'strImg', 'vEncounterIDs', 'nMovesPerTurn',
                    'nTreasureID', 'nFaction', 'vAttackModes', 'vBaseConditions', 'nCorpseID', 'vActivities']
        elif type == 'creaturesources':
            return ['id', 'strName', 'nX', 'nY', 'nCreatureID', 'nMin', 'nMax', 'fWeight']
        elif type == 'datafiles':
            return ['id', 'strName', 'strDesc', 'fValue', 'strImg']
        elif type == 'dmcplaces':
            return ['id', 'strImg', 'nEncounterID', 'nX', 'nY']

    def setupTable(self, table: QTableWidget):
        if table.rowCount() != 0:
            return
        table.setColumnCount(len(self.column))
        table.setHorizontalHeaderLabels(self.column)
        self.table = table
        self.loadData()

    def __setitem__(self, key, value):
        if isinstance(key, tuple) and isinstance(key[0], int) and len(key) == 2:
            column = key[1]
            if isinstance(column, str):
                column = self.column.index(column)
            if column == -1 or key[0] < 0:
                return None
            if key[0] >= self.data.shape[0]:
                self.data = np.append(self.data, np.zeros((1, len(self.column))), axis=0)
                self.table.setRowCount(self.data.shape[0])
            self.data[key[0]][column] = value
            self.table.setItem(key[0], column, QTableWidgetItem(str(value)))
        elif isinstance(key, int) and isinstance(value, list) and len(value) == len(self.column):
            if key < 0:
                return None
            if key >= self.data.shape[0]:
                self.data = np.append(self.data, np.zeros((1, len(self.column))), axis=0)
                self.table.setRowCount(self.data.shape[0])
            self.data[key] = value
            for i in range(len(value)):
                self.table.setItem(key, i, QTableWidgetItem(str(value[i])))

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            column = key[1]
            if isinstance(column, str):
                column = self.column.index(column)
            if column != -1 and 0 <= key[0] <= self.data.shape[0]:
                return self.data[key[0]][column]
        elif isinstance(key, int):
            if 0 <= key <= self.data.shape[0]:
                return self.data[key]
        return None

    def loadData(self):
        if hasattr(self, 'table'):
            self.table.setRowCount(self.data.shape[0])
            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

    def __len__(self):
        return self.data.shape[0]

    def shape(self):
        return self.data.shape
