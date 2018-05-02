# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BrugisDataAccess
                                 A QGIS plugin
 Allow safe and controlled modifications on Brugis Data
                              -------------------
        begin                : 2015-09-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Michel Van Asten GIM
        email                : michelvanasten@gim.be
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject
import ConfigParser
import os.path
import string
import random


from BdmEditor_dialog import BdmEditorDialog
from BrugisWebStub import Stub
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon, QAbstractItemView, QItemSelectionModel, QMessageBox, QMenu, QCursor, QApplication 
from PyQt4.QtSql import *
from PyQt4.QtXml import QDomDocument
from QBrugisJsonTableModel import QBrugisJsonTableModel 
from qgis.core import (
    QgsMapLayer,
    QgsGeometry,
    QgsMapLayerRegistry,
    QgsFeature,
    QgsFeatureRequest,
    QgsRectangle,
    QgsPoint,
    QgsField,
    QgsFields,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QGis,
    QgsProject,
    QgsSingleSymbolRendererV2,
    QgsFillSymbolV2,
    QgsCoordinateReferenceSystem,
    QgsDataSourceURI,
    QgsMessageLog)
import resources_rc


# Initialize Qt resources from file resources.py
# Import the code for the dialog
# from BrugisShared import PlCommon
class BdmEditor(Stub):
    """QGIS Plugin Implementation."""
    _firstRun = True 
    # Database parameters
    _authUser = ""
    # databrugis_dev ||  databrugis
    _devEditUser = "brugis_editor"
    _devEditPassword = "editorbg"
    _authKey = ''
    _brugisLayerPrefix = ["BRUGISEDIT" , "BRUGISERRORS"]
    
    # _myversion = "0.6" 
     
       
    _uiTimer = QTimer()
    
    def __init__(self, iface):
        """Constructor.
        
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BdmEditor{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BdmEditorDialog()
        # Bind the event handlers
        # self.dlg.pushButton_checkOut.clicked.connect(self.test())
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&BdmEditor')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BdmEditor')
        self.toolbar.setObjectName(u'BdmEditor')
        self.read_init()
        self._lockpluggin = 0
        
        # Qgis Plugin::version ( )

    def read_init(self):

        required_metadata = [
            'name',
            'description',
            'version',
            'qgisMinimumVersion',
            'email',
            'author']

        
        basepath = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(basepath, 'metadata.txt')
        
        # file_path = os.path.abspath(os.path.join(
        #    os.path.dirname(__file__), os.pardir,
        #    'metadata.txt'))
        
        parser = ConfigParser.ConfigParser()
        # parser.optionxform = str
        parser.read(file_path)
        
        self._myVersion = parser.get('general', 'version')
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BdmEditor', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        
        #self.menu = QMenu( "&Brugis", self.iface.mainWindow().menuBar() )
        #actions = self.iface.mainWindow().menuBar().actions()
        #lastAction = actions[-1]
        #self.iface.mainWindow().menuBar().insertMenu( lastAction, self.menu )

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)
        
        

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/BdmEditor/BdmEditor.ico'
        self.add_action(
            icon_path,
            text=self.tr(u'BdmEditor'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        


    def unload(self):
        self.doDebugPrint("------------------UNLOAD----------------")
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.doUnLockUserSession(self._authKey)
        
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&BdmEditor'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Bind the event handlers
        self.dlg.activateWindow()
        
        self.doDebugPrint("HERE")
        
        authorized_version = [21813, 21816, 21817, 21818]
        
        v = QGis.QGIS_VERSION_INT
        self.doDebugPrint(str(v))
        
        
        if v in authorized_version:
            if self._firstRun:
                QObject.connect(self.dlg.pushButton_checkOut, SIGNAL("clicked()"), self.doCheckOut)
                QObject.connect(self.dlg.pushButton_LogIn, SIGNAL("clicked()"), self.doLogin)
                QObject.connect(self.dlg.pushButton_Staging, SIGNAL("clicked()"), self.doStaging)
                QObject.connect(self.dlg.pushButton_UndoStaging, SIGNAL("clicked()"), self.doUndoStaging)
                QObject.connect(self.dlg.pushButton_Free, SIGNAL("clicked()"), self.doCancel)
                QObject.connect(self.dlg.pushButton_Validate, SIGNAL("clicked()"), self.doValidate)
                QObject.connect(self._uiTimer, SIGNAL("timeout()"), self.doUIRefresh)
                
                
                self.dlg.label_Version.setText(self._myVersion)
                icon_path = ':/plugins/BdmEditor/BdmEditor.ico'
                
                app_icon = QIcon(icon_path)
                self.dlg.setWindowIcon(app_icon)                
                
                self._firstRun = False
        else:
            self.dlg.label_Version.setText("unsupported version {}".format(str(v)))


        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        
    
    def doUIRefresh(self):
        self.doDebugPrint("doUIRefresh")
        self.doRefrehStatesTable()
        
    def doLogin(self, clicked=False):
        self.doDebugPrint("Enter Login")
        tLogin = self.dlg.pushButton_LogIn.text()
        self.doDebugPrint("-doLogin 1")
        if (tLogin == "LogOut"):
            self.doUnLockUserSession(self._authKey)
            self.doDebugPrint("-doLogin 2")
            self.dlg.lineEdit_User.setText("")
            self.dlg.lineEdit_Password.setText("")
            self.dlg.pushButton_LogIn.setText("Login")
            self.dlg.groupBox_Editions.setDisabled(True)
            self._authUser = ""
            self.doCleanupProjectBeforeLeave(None)
            self.dlg.textEdit_Result.setText("")
            self.doCleanStatesTable()
            self._uiTimer.stop()
            self.doAjustUItoSelection()
            return 
        
        # Retrieve User/password
        # if ok enable graphical components
        usr = self.dlg.lineEdit_User.text()
        pswd = self.dlg.lineEdit_Password.text()
        self.doDebugPrint("-doLogin 1-1 {} {}".format(usr, pswd))
        if self.checkUserPassword(usr, pswd) == "ok":
            self.doDebugPrint("-doLogin 1-2")
            self.dlg.groupBox_Editions.setEnabled(True)	
            self._authUser = usr
            self.dlg.pushButton_LogIn.setText("LogOut")
            self._uiTimer.start(13000)
            self.doAjustUItoSelection()
            return	            
        else:
            self.dlg.groupBox_Editions.setDisabled(True)
                    
        
        

    def checkUserPassword(self, usrname, pswd):
        self.doDebugPrint("checkUserPassword 1")
        
        self.doDebugPrint("before authenticate")
        
        auth = self.authenticate(usrname, pswd)
        self.doDebugPrint("after authenticate")
        self._authKey = self.getGeoKey(usrname)
        self.doDebugPrint( self._authKey )
        self.doDebugPrint("auth {}".format(auth))
        if auth == True:
            self.doDebugPrint("checkUserPassword 2-1")
            sessionlock = self.dogetUserLock(self._authKey)
            if (sessionlock < 1):                
                self.fillInTableStates(self._authKey)
                self.doDebugPrint("checkUserPassword 2-1-1")
                self.doLockUserSession(self._authKey)
                self.doDebugPrint("checkUserPassword 2-2-1")
                self.doNotify("")
                # consistency between tables_states and schema content
                self.doCheckConsistency(self._authKey)
                return "ok" 
            else:
                self.doBrugisEvent("", self._authKey, "login", "", "BdmEditor", "NOK", "user already logged in")                                
                self.doNotify("user already logged in")
                return "user already logged in"
        else:
            self.doNotify("invalid user and (or) password")
            return "nok"

    

            


    # #
    # fillInTableStates : (UI)
    #
    def fillInTableStates(self, username=None):
        # model = QSqlQueryModel()
        #QApplication.setOverrideCursor(Qt.WaitCursor)
        model = QBrugisJsonTableModel()
        if username == None:
            view = self.dlg.tableView_editables_layers
            model.clean()
            view.setModel(model)
            view.show()
            return
        jdata = self.getWebRessource('usertablestates', "uname={}".format(username))
        
        # expected fields ( and order)
        expectedfields = ['table_name', 'uname', 'state', 'schema']
    
        
        states = jdata[u'results']
        if len(states) == 0:
            return 
        model.setJson(states, expectedfields)
        
        #QApplication.restoreOverrideCursor()
        
        view = self.dlg.tableView_editables_layers
        view.setModel(model)
        view.setColumnWidth(0, 160)
        view.setColumnWidth(1, 80)
        view.setColumnWidth(2, 40)
        view.setColumnWidth(3, 80)
        
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        selectionModel = view.selectionModel()
        selectionModel.selectionChanged.connect(self.doAjustUItoSelection)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.show()
        
  
        
    # #
    # doNotifyAppendLine : insert message in notification textbox
    #    
    def doNotify(self, usermessage):
        self.dlg.textEdit_Result.setText(usermessage)
        self.doDebugPrint(usermessage, True)


    # #
    # doNotifyAppendLine : append message to notification textbox
    #
    def doNotifyAppendLine(self, usermessage):
        self.dlg.textEdit_Result.append(usermessage)
        self.doDebugPrint(usermessage, True)
    
              
    
    
    # #
    # doCheckOut : Checkout the table... Or only editable if already checkout
    #
    def doCheckOut(self):
        
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0] 				
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            # _schemaname = self._devSchema_intra
            state = self.getTableState(layername, self._authKey)
            statecrea = self.getTableStateCrea(layername, self._authKey)
            if self.doCheckGlobalLock(self._authKey):
                self.doNotify("Checkout blocked by administrator")
                self.doBrugisEvent(layername, self._authKey, self._brugis_useraction_CHECKOUT, state, "BdmEditor", "NOK", "Checkout blocked by administrator")
                return
            
            if state == self._brugis_dataflow_staging :
                self.doNotify("Layer in staging, edition refused")
                self.doBrugisEvent(layername, self._authKey, self._brugis_useraction_CHECKOUT, state, "BdmEditor", "NOK", "Layer in staging, edition refused")
                return
            
            if state != self._brugis_dataflow_cin or statecrea == "NEW":
                self.doNotify("Layer already checkout")
                self.doBrugisEvent(layername, self._authKey, self._brugis_useraction_CHECKOUT, state, "BdmEditor", "NOK", "Layer already checkout")
                self.doGrantEdit(self._authKey)
            else:
                self.doNotify("{} checked out".format(layername))
                self.doCopyTableIntraToEdit(layername, self._authKey)
                self.doGrantEdit(self._authKey)
                self.updateLayerStatus(layername, self._brugis_dataflow_cout, self._authKey)
                self.doRefrehStatesTable()
                self.doBrugisEvent(layername, self._authKey, self._brugis_useraction_CHECKOUT, state, "BdmEditor", "OK", "")
            
            self.addGSLayer(layername, self._authKey)
            self.addEditableLayerToMap(layername)
            
            
    
            

    def doGetSelectedRow(self):
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        self.doDebugPrint("doGetSelectedRow")
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]                 
            rowIndex = iIndex.row()
            self.doDebugPrint("rowindex {}".format(rowIndex))
            return rowIndex
        else:
            return -1
    
        
    # #
    # doAjustUItoSelection : Make UI consistent with actions available for selected layer
    #
    def doAjustUItoSelection(self):
        self.doDebugPrint("doAjustUItoSelection")
        # disable all buttons
        self.dlg.pushButton_checkOut.setDisabled(True)
        self.dlg.pushButton_Free.setDisabled(True)
        self.dlg.pushButton_Staging.setDisabled(True)
        self.dlg.pushButton_UndoStaging.setDisabled(True)
        self.dlg.pushButton_Validate.setDisabled(True)
        view = self.dlg.tableView_editables_layers
        # retrieve selected line in the table... No selection means no action
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]                 
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            self.doDebugPrint( "A_UI 1 {}".format(layername))
            # _schemaname = self._devSchema_intra
            # state owner... Who made the last action 
            stateowner = iIndex.sibling(rowIndex, 1).data()
            # state ... The workflow state
            self.doDebugPrint( "A_UI 2 {}".format(stateowner))
            state = self.getTableState(layername, self._authKey)
            self.doDebugPrint( "A_UI 3 {}".format(state))
            # statecrea ... The creation state ( related to newly created tables)
            statecrea = self.getTableStateCrea(layername, self._authKey)
            # if state is checkedin... stateowner is not relevant !    
            if state == self._brugis_dataflow_cin:
                self.dlg.pushButton_checkOut.setEnabled(True)
                pass
            elif stateowner == self._authUser:        
                if state == self._brugis_dataflow_cout:
                    self.dlg.pushButton_checkOut.setEnabled(True)
                    self.dlg.pushButton_Staging.setEnabled(True)
                    self.dlg.pushButton_Validate.setEnabled(True)
                    if self.safeLen(statecrea) < 1:
                        self.dlg.pushButton_Free.setEnabled(True)                
                elif state == self._brugis_dataflow_staging:
                    self.dlg.pushButton_UndoStaging.setEnabled(True)                
                else:
                    pass

    

                

    # #
    # doRefrehStatesTable : If exist, retrieve the selected line... Redo the query to states table... restore the selected line 
    #
    def doRefrehStatesTable(self):
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        # Retrieve initial selected layer.
        selrow = -1
        iIndex = None
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]                 
            selrow = iIndex.row()        
        self.fillInTableStates(self._authUser)
        # Restore selected layer
        if selrow > 0:
            view.setSelectionBehavior(QAbstractItemView.SelectRows)
            
            view.selectRow(selrow)
            
        self.doAjustUItoSelection()
            
    # #
    # doFakeRefrehStatesTable : (UI) ... Tricky.force TableStates cleanup
    #
    def doCleanStatesTable(self):
        self.fillInTableStates()        
    
    
    def doValidate(self):
        layername = 'undefined'
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]                 
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            msg = self.getGeometryValid(layername, self._authKey)
            if len(msg) > 0:
                self.doNotify(msg)
                return False
            else:
                self.doNotify('Validation succeed')
                return True
        else:
            return False    
        
    # doStaging : Layer is submitted to staging...  
    #
    def doStaging(self):
        if self._lockpluggin > 0 :
            self.doNotify("Layer in edition, action refused")
            return     
        layername = 'undefined'
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]                 
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
        else:
            return
        
        state = self.getTableState(layername, self._authKey)
        if (state != self._brugis_dataflow_cout):
            self.doNotify("Invalid state, layer must be checked out")
            self.doBrugisEvent(layername, 
                               self._authKey, 
                               self._brugis_useraction_STAGING, 
                               state, 
                               "BdmEditor", 
                               "NOK", 
                               "Invalid operation (validation failure)")
            return
        if self.doCheckGlobalLock(self._authKey):
            self.doNotify("Action blocked by administrator")
            self.doBrugisEvent(layername, 
                               self._authKey,  
                               self.__brugis_useraction_STAGING, 
                               state, 
                               "BdmEditor", 
                               "NOK", 
                               "Action blocked by administrator")
            return
        
        if not self.doValidate():
            self.doBrugisEvent(layername, 
                               self._authKey,  
                               self.__brugis_useraction_STAGING, 
                               state, 
                               "BdmEditor", 
                               "NOK", 
                               "Invalid operation (Validation failure)")
            return
            
        self.doCopyTableEditToModif(layername, self._authKey)
        self.updateLayerStatus(layername, self._brugis_dataflow_staging, self._authKey)
        self.doBrugisEvent(layername, 
                           self._authKey,  
                           self._brugis_useraction_STAGING, 
                           state, 
                           "BdmEditor", 
                           "OK", 
                           "")
        self.doRefrehStatesTable()  
        self.doCleanupSingleTable(layername)  
        
        self.removeGSLayer(layername,self._authKey)    
        usermail = self.getUserMail(self._authKey) 
        self.sendMail("Notification Bdm (Version:{})".format(self._myVersion), "Couche {} envoyee en staging pour validation dans les 24 heures. N'oubliez pas de demander ensuite la publication".format(layername) , usermail, self._authKey)
        self.sendMail("Notification Bdm (Version:{})".format(self._myVersion), "Couche {} envoyee en staging par {}".format(layername, self._authUser) , self._brugisEmailAdress, self._authKey)
        self.doNotify("{} copied to staging".format(layername))
            

    
    # #
    # doUndoStaging : remove table from brugis_modif, restore table in edit schema and update layer status
    #
    def doUndoStaging(self):
        if self._lockpluggin > 0 :
            self.doNotify("Layer in edition, action refused")
            return 
        
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            state = self.getUserTableState(layername, self._authKey)
            if state != self._brugis_dataflow_staging:
                self.doNotify("invalid operation ({} <> STAGING) for layer {}".format(state,layername))
                return  
            if self.doAskUser(u"Les données publiées seront supprimées de l'envirronement de validation", "Veuillez confirmer votre choix"):
                self.doCopyTableModifToEdit(layername, self._authKey)
                
                self.updateLayerStatus(layername, self._brugis_dataflow_cout, self._authKey)
                self.doBrugisEvent(layername, 
                                   self._authKey,  
                                   self._brugis_useraction_UNDOSTAGING, 
                                   state, 
                                   "BdmEditor", 
                                   "OK", 
                                   "")
        
                self.doRefrehStatesTable()
                self.doGrantEdit(self._authKey)
                
    # #
    # doCancel : Discard current edition
    #
    def doCancel(self):
        view = self.dlg.tableView_editables_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0] 				
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            _schemaname = iIndex.sibling(rowIndex, 1).data()
            state = self.getUserTableState(layername, self._authKey)
            statecrea = self.getTableStateCrea(layername, self._authKey)
            if statecrea == "NEW":
                self.doNotify(u"Invalid operation (statecrea == NEW)")
                self.doBrugisEvent(layername, 
                                   self._authKey,  
                                   self._brugis_useraction_UNDOCHECKOUT, 
                                   state, 
                                   "BdmEditor", 
                                   "NOK", 
                                   "Invalid operation (statecrea == NEW)")                
                return
            if (state != self._brugis_dataflow_cout and state != self._brugis_dataflow_cin):
                self.doNotify(u"Invalid operation ( state <> COUT | CIN )")
                self.doBrugisEvent(layername, 
                                   self._authKey,  
                                   self._brugis_useraction_UNDOCHECKOUT, 
                                   state, 
                                   "BdmEditor", 
                                   "NOK", 
                                   "Invalid operation ( state <> COUT | CIN )")                
                return
            if self.doAskUser(u"Les données de la couche ne seront plus éditables", "Veuillez confirmer votre choix"):            
                self.doCleanupSingleTable(layername)
                if self.doCheckGlobalLock(self._authKey):
                    self.doNotify("Action blocked by administrator")
                    self.doBrugisEvent(layername, 
                                       self._authKey,  
                                       self._brugis_useraction_UNDOCHECKOUT, 
                                       state, 
                                       "BdmEditor", 
                                       "NOK", 
                                       "Action blocked by administrator")
                    return
                self.removeGSLayer(layername, self._authKey)
                self.tableEditDrop(layername, self._authKey)
                self.doNotify("undo {} checkout".format(layername))
                self.updateLayerStatus(layername, self._brugis_dataflow_cin, self._authKey)
                self.doBrugisEvent(layername, 
                                   self._authKey,  
                                   self._brugis_useraction_UNDOCHECKOUT, 
                                   self._brugis_dataflow_cout, 
                                   "BdmEditor", 
                                   "OK", 
                                   "")
                self.doRefrehStatesTable()
            else:
                self.doNotify(u"Canceled by user")
                
                
          
     
    
        
    # #
    # addEditableLayerToMap : (UI) Add layer to the the map, make ID field not editable
    #
    def addEditableLayerToMap(self, layername):
        maplayers = QgsMapLayerRegistry.instance().mapLayers()
        
        fullname = "BRUGISEDITTEMP:{}".format(layername)
        easyname = self.formatBrugisLayerName(layername)
        for k, layer in maplayers.iteritems():
            if layer.name() == easyname:
                return
                
        #uri = '{}{}/?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME={}&SRSNAME=urn:ogc:def:crs:EPSG:31370'.format(self._brugisWfsProxy, self._authKey, fullname)
        
        #uri = '{}{}/?SERVICE=WFS&VERSION=1.0.0&TYPENAME={}&SRSNAME=urn:ogc:def:crs:EPSG:31370'.format(self._brugisWfsProxy, self._authKey, fullname)
        
        
        #####################################Ê
        ## add random part in the url to ensure cache is not used for getCapabilities...
        uri = '{}{}/{}/?SERVICE=WFS&VERSION=1.0.0&TYPENAME={}&SRSNAME=urn:ogc:def:crs:EPSG:31370'.format(self._brugisWfsProxy, self._authKey, self.id_generator(), fullname)
        
        #uri = 'monhos?SERVICE=WFS&VERSION=1.0.0&TYPENAME=monnamespace:macouche&SRSNAME=urn:ogc:def:crs:EPSG:31370'.format(self._brugisWfsProxy, self._authKey, fullname)
        
        
        #uri = '{}{}/?SERVICE=WFS&REQUEST=GetFeature&TYPENAME={}&SRSNAME=EPSG:31370'.format(self._brugisWfsProxy, self._authKey, fullname)
       
        
        vlayer = QgsVectorLayer(uri, easyname, "WFS")
        
        #####################################Ê
        ## Just to ensure first getCapabilities call is done 
        dp = vlayer.dataProvider()
        dp.forceReload()          
        dp.clearMinMaxCache()
        cp = dp.capabilitiesString()
        
        
        
        self.doHiddenField(vlayer, False)
        
        reg = QgsMapLayerRegistry.instance()
        ml = reg.addMapLayer(vlayer, True)
        
        # check that ml is not null
        if ml is None:
            errmsg = self.getLastError(self._authKey)
            try:
                self.doNotify("couche non disponible \n {}".format(errmsg.decode('utf8')))
            except:
                self.doNotify("couche non disponible \n {}".format(layername))
            return 
        
        ml.editingStarted.connect(self.brugisLayerStartEditing)
        ml.editingStopped.connect(self.brugisLayerStopEditing)
        
        # Editing map layer should 
        
        
        # In order to avoid consistency errors related to layer life cycle Brugis layers cannot remain in the project
        # This decision ensure that the reference to the layer will be removed from project before saving it
        self.doDebugPrint("connect writeProject")
        proj = QgsProject.instance()
        # connect custom cleanup to WriteProject signal
        QObject.connect(proj, SIGNAL("writeProject( QDomDocument & )"), self.doCleanupProjectBeforeLeave)            
        self.doDebugPrint("after connect")
        
        return ml
    
    def formatBrugisLayerName(self, layername):
        return "BRUGISEDIT_{}".format(layername)
        
    # #
    # doCleanupProjectBeforeLeave :  check all layers and remove any reference to Brugis layers
    #
    def doCleanupProjectBeforeLeave(self, doc):
        self.doDebugPrint("doCleanupProjectBeforeLeave")
        maplayers = QgsMapLayerRegistry.instance().mapLayers()        
        
        llist = []    
        for k, layer in maplayers.iteritems():
            ln = layer.name()
            if self.matchOne(ln, self._brugisLayerPrefix):
                llist.append(k)
        
        QgsMapLayerRegistry.instance().removeMapLayers(llist)        
        self.doDebugPrint("after doCleanupProjectBeforeLeave")    
    
    # #
    # doHiddenField : (UI) hide all or only "ID" field of the layer 
    #
    def doHiddenField(self, qLayer, allfiels=True):
        lf = qLayer.pendingFields()
        if allfiels:            
            for (k, field) in lf.iteritems():
                qLayer.setEditType(k, QgsVectorLayer.Hidden)
        else:
            idx = lf.indexFromName("ID")
            qLayer.setEditType(idx, QgsVectorLayer.Hidden)

    def brugisLayerStartEditing(self):
        self._lockpluggin += 1 
        pass
    
    def brugisLayerStopEditing(self):
        self._lockpluggin -= 1
        pass  
    
    # #
    # doAskUser : (UI) Display OK_Cancel Message box to capture user decision
    #
    def doAskUser(self, warningmessage, acknoledgemessage):
        msgBox = QMessageBox() 
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(warningmessage)
        msgBox.setInformativeText(acknoledgemessage)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel);
        userAnswer = msgBox.exec_()
        if userAnswer == QMessageBox.Ok :
            return True
        else :
            return False
    
    # #
    # doCleanupSingleTable : Remove any reference to this specific Brugis layer
    #
    def doCleanupSingleTable(self, tablename):
        maplayers = QgsMapLayerRegistry.instance().mapLayers()        
        
        llist = []    
        for k, layer in maplayers.iteritems():
            ln = layer.name()
            if ln.find(tablename) == -1:
                continue
            # if ln.find("BRUGIS EDIT") != -1 or ln.find("BRUGIS ERRORS") != -1 :
            if self.matchOne(ln, self._brugisLayerPrefix):
                llist.append(k)
        
        QgsMapLayerRegistry.instance().removeMapLayers(llist)        
    
    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    
def wait_cursor():
    try:
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    except:
        pass