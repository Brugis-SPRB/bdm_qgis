'''
Created on 26 oct. 2016

@author: mvanasten
'''

import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

##
# Json compatible implementation of QAbstractTableModel
class QBrugisJsonTableModel(QAbstractTableModel):
    '''
    classdocs
    '''


    def __init__(self, parent=None, *args):
        #def __init__(self, parent=None, *args): 
        super(QBrugisJsonTableModel, self).__init__()
        #QAbstractTableModel.__init__(self, params)
        self._datatabs = [[]]
        self._header = []
        
        '''
        Constructor
        '''
    
    def setHorizontalLabels(self,lstLabels):
        # check len(lstLabels) = len(self._header)
        if len(lstLabels) != len(self._header):
            return False
        col = 0
        for label in lstLabels:
            self.setHeaderData(col,Qt.Horizontal,label)
            col += 1
        return True
    
    ##
    # Fill table content with Json data
    #@param fields : list of expected fileds names ( skip other columns)
#     def setJson(self, jdata, fields=None):
#         if fields ==None:            
#             self._header = jdata[0].keys()
#         else:
#             self._header = fields
#         #print self._header
#         row = 0
#         
#         w, h = len(self._header), len(jdata)-1 
#         self._datatabs = [[0 for x in range(w)] for y in range(h)] 
#         
#         col = 0
#         for key in self._header:
#             self._datatabs[0][col] = key
#             col +=1
#         
#         for record in jdata:
#             col = 0
#             if row == 0:
#                 row+= 1
#                 continue
#             for key in self._header:
#                 val = record[key]
#                 self._datatabs[row-1][col] = val
#                 col +=1
#             row+= 1
#     
    
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
    
    
    
    
    
    ##
    # Fill table with one data column
    #@param label : column name
    def setJsonList(self, jdata, label):
        self._header = label
        #print self._header
        row = 0
        
        h = len(jdata)-1 
        self._datatabs = [h] 
        
        
        for record in jdata:
            col = 0
            if row == 0:
                row+= 1
                continue
            for key in self._header:
                val = record
                self._datatabs[row-1] = val
                col +=1
            row+= 1
        

   
    
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
    
    def clean(self):
        self.beginResetModel()
        self._datatabs = [[]]
        self._header = []        
        self.endResetModel()
    
    def headerData(self, section, orientation,role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._header[section]
        