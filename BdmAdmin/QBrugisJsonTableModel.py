'''
Created on 26 oct. 2016

@author: mvanasten
'''

import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QBrugisJsonTableModel(QAbstractTableModel):
    '''
    classdocs
    '''


    def __init__(self, parent=None, *args):
        super(QBrugisJsonTableModel, self).__init__()
        self._datatabs = [[]]
        self._header = []
        
        '''
        Constructor
        '''
    
    def setJson(self, jdata, fields=None):
        self.beginResetModel()
        
        if fields ==None:            
            self._header = jdata[0].keys()
        else:
            self._header = fields
        row = 0
        
        w, h = len(self._header), len(jdata) 
        self._datatabs = [[0 for x in range(w)] for y in range(h)] 
        
        for record in jdata:
            col = 0
            for key in self._header:
                val = record[key]
                self._datatabs[row][col] = val
                col +=1
            row+= 1
        self.endResetModel()
        
    def clean(self):
        self.beginResetModel()
        self._datatabs = [[]]
        self._header = []        
        self.endResetModel()
        
    def setHorizontalLabels(self,lstLabels):
        col = 0
        if len(lstLabels) != len(self._header):
            return False
        for label in lstLabels:
            self.setHeaderData(col,Qt.Horizontal,label)
            col += 1
        return True
    
    def setJsonList(self, jdata, label):
        self.beginResetModel()
        self._header = label
        #print self._header
        row = 0
        
         
        self._datatabs = list() 
        
        
        for record in jdata:
            val = record
            self._datatabs.append(val)
            row+= 1
        self.endResetModel()
    
    def rowCount(self,parent):
        return len(self._datatabs)
        pass
    
    def columnCount(self,parent):
        return len(self._header)
        pass
    
    def data(self,index,role):
        if not index.isValid():
            return None
        
        if role != Qt.DisplayRole:
            return None
        return  self._datatabs[index.row()][index.column()]
    
    def setData(self, index, value, role):
        self._datatabs[index.row()][index.column()] = value
        self.datachanged()
        
        
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    
    def headerData(self, section, orientation,role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            #return QtCore.QVariant(self.headerdata[col])
            if section >= 0:
                print "self._header[section]{}".format(self._header[section])
                return self._header[section]
    
    def safelen(self, obj):
        if obj is None:
            return 0
        else:
            return len(obj)
        