# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BdmAdmin
                                 A QGIS plugin
 BdmAdmin
                              -------------------
        begin                : 2015-10-05
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Michel Van Asten GIM
        email                : michelvanasten@yahoo.fr
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
import os.path
import re

from BdmAdmin_dialog import BdmAdminDialog
from BrugisWebStub import Stub
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from PyQt4.QtSql import *
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
    QgsSingleSymbolRendererV2,
    QgsFillSymbolV2,
    QgsCoordinateReferenceSystem)
import resources


# Initialize Qt resources from file resources.py
# Import the code for the dialog
# from BrugisShared import PlCommon
class BdmAdmin(Stub):
    """QGIS Plugin Implementation."""
    
    _adminuser = ""
    _mailrequestor = ""
    
    _firstRun = True 
    
    
    
    _authKey = ''
    
    
    
    # utility..... used to increment default userID
    _pseudocounter = 0
    
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
            'BdmAdmin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BdmAdminDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&BdmAdmin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BdmAdmin')
        self.toolbar.setObjectName(u'BdmAdmin')
        


        
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
        return QCoreApplication.translate('BdmAdmin', message)


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

        
        icon_path = ':/plugins/BdmAdmin/BdmAdmin.ico'
        self.add_action(
            icon_path,
            text=self.tr(u'BdmAdmin'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&BdmAdmin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        print "run !!!!"
        
        authorized_version = [21803, 21811, 21813, 21816]
        
        # Retrieve QGIS version number
        v = QGis.QGIS_VERSION_INT 
        self.doDebugPrint(str(v))
        
        if v in authorized_version:
            if self._firstRun:
                QObject.connect(self.dlg.pushButton_DoLogin, SIGNAL("clicked()"), self.doLogin)
                QObject.connect(self.dlg.comboBox_Users , SIGNAL("currentIndexChanged(int)"), self.doUserRightsSelectionChanged);
                QObject.connect(self.dlg.pushButton_AssignLayer, SIGNAL("clicked()"), self.doAssignLayer)
                QObject.connect(self.dlg.pushButton_RemoveLayer, SIGNAL("clicked()"), self.doRemoveLayer)
                QObject.connect(self.dlg.pushButton_RemoveAllLayers, SIGNAL("clicked()"), self.doRemoveAllLayer)
                QObject.connect(self.dlg.comboBox_UsersAdmin , SIGNAL("currentIndexChanged(int)"), self.doUserAdminSelectionChanged);
                QObject.connect(self.dlg.pushButton_NewUser, SIGNAL("clicked()"), self.doNewUser)
                QObject.connect(self.dlg.pushButton_SaveUser, SIGNAL("clicked()"), self.doSaveUser)
                QObject.connect(self.dlg.pushButton_RemoveUser, SIGNAL("clicked()"), self.doRemoveUser)
                QObject.connect(self.dlg.comboBox_MngtUsers , SIGNAL("currentIndexChanged(int)"), self.doUserMngtSelectionChanged)
                QObject.connect(self.dlg.pushButton_ToProduction , SIGNAL("clicked()"), self.doToIntra)
                QObject.connect(self.dlg.pushButton_Cancel , SIGNAL("clicked()"), self.doCancelCheckOut)
                QObject.connect(self.dlg.pushButton_TakeControl , SIGNAL("clicked()"), self.doTakeControl)
                QObject.connect(self.dlg.pushButton_GrantEdit , SIGNAL("clicked()"), self.doGrantEdit)
                QObject.connect(self.dlg.pushButton_Orphaned, SIGNAL("clicked()"), self.doCleanupOrphaned)
                QObject.connect(self.dlg.pushButton_ImportNew, SIGNAL("clicked()"), self.doImportNewTable)
                QObject.connect(self.dlg.pushButton_CreateIndex, SIGNAL("clicked()"), self.doCreateCustomSerial)
                QObject.connect(self.dlg.pushButton_UndoStaging, SIGNAL("clicked()"), self.doUndoStaging)
                icon_path = ':/plugins/BdmAdmin/BdmAdmin.ico'
                
                app_icon = QIcon(icon_path)
                self.dlg.setWindowIcon(app_icon)  
                
                self._firstRun = False
        else:
            
            self.doNotify("unsupported version {}".format(str(v)))
            
        # show the dialog
        
        self.dlg.show()
        
        self.dlg.activateWindow()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass



    def doLogin(self):
        """(UI) Adapt UI according to the result of checkUserPassword function"""
        tLogin = self.dlg.pushButton_DoLogin.text()
        if (tLogin == "LogOut"):
            self.dlg.lineEdit_User.setText("")
            self.dlg.lineEdit_Password.setText("")
            self.dlg.pushButton_DoLogin.setText("Login")
            
            
            self.dlg.lineEdit_MngtPassword.setText("")
            self.dlg.lineEdit_MngtUser.setText("")
            self.dlg.lineEdit_MngEmail.setText("")
            
            self.doClearAllCombo()
            self.doClearAllViews()
            
            self.dlg.groupBox_Users.setDisabled(True)
            self.dlg.groupBox_Rights.setDisabled(True)
            self.dlg.groupBox_Admin.setDisabled(True)
            
            self._authUser = ""
            
        else:
            usr = self.dlg.lineEdit_User.text()
            pswd = self.dlg.lineEdit_Password.text()
            self.checkUserPassword(usr, pswd)
            
 
        
    # #
    # doUserRightsSelectionChanged : (UI) refresh QTableView Assigned_layers according to the selected user
    # @param idx index of the selected user in the list
    #     
    def doUserRightsSelectionChanged(self, idx):
        username = self.dlg.comboBox_Users.itemText(idx)     
        model = QBrugisJsonTableModel()
        jdata = self.getAllUserTables(username, self._authKey)
        model.setJsonList(jdata, "table_name")
            
        view = self.dlg.listView_Assigned_layers
        view.setModel(model)
        view.show()

    
    # # 
    # doUserAdminSelectionChanged : (UI) refresh QTableView AdminLayers according to the selected user
    # @param idx index of the selected user in the list
    #             
    def doUserAdminSelectionChanged(self, idx):
        username = self.dlg.comboBox_UsersAdmin.itemText(idx)     
        
        model = QBrugisJsonTableModel()
        jdata = self.getWebRessource('usertablestates', "uname={}".format(username))
        states = jdata[u'results']
        view = self.dlg.tableView_AdminLayers
        # print states
        if len(states) == 0:
            model.clean()
            view.setModel(model)        
            view.show()
            return 
        else:
            expectedfields = ['table_name', 'state']
            model.setJson(states, expectedfields)
            
            
            model.setHeaderData(0, Qt.Horizontal, "table_name")
            model.setHeaderData(1, Qt.Horizontal, "state")
            
            
            
            view.setModel(model)
            
            view.setColumnWidth(0, 230)
            view.setColumnWidth(1, 91)
            view.show()


    # #
    # doRefreshAdminLayers : (UI) Requery tables_states and populate AdminLayers QTableView
    #
    def doRefreshAdminLayers(self, username):          
        model = QBrugisJsonTableModel()
        jdata = self.getWebRessource('usertablestates', "uname={}".format(username))
        states = jdata[u'results']
        # print states
        if len(states) == 0:
            return 
        expectedfields = ['table_name', 'state']
        model.setJson(states, expectedfields)
        
        
        model.setHeaderData(0, Qt.Horizontal, "table_name")
        model.setHeaderData(1, Qt.Horizontal, "state")
        
        
        view = self.dlg.tableView_AdminLayers
        view.setModel(model)
        
        view.setColumnWidth(0, 230)
        view.setColumnWidth(1, 91)
        view.show()  

    
    # #
    # doUserMngtSelectionChanged : (UI) Ajust user editable info to match changes of selected user 
    #
    def doUserMngtSelectionChanged(self, idx):
        
        username = self.dlg.comboBox_MngtUsers.itemText(idx) 	
        
        jdata = self.getWebRessource('userinfos', "username={}".format(username))
        uinfo = jdata[u'results']
        # print states
        if len(uinfo) == 0:
            return 
        for record in uinfo:
            self.dlg.lineEdit_MngtPassword.setText(record[u'userpswd'])
            self.dlg.lineEdit_MngtUser.setText(record[u'username'])
            self.dlg.lineEdit_MngEmail.setText(record[u'usermail'])
            self.dlg.lineEdit_MngEmail.setEnabled(True)
            self.dlg.lineEdit_MngtUser.setEnabled(False)
            


     
    
       
        
    # #
    # checkUserPassword : simple authentication function 
    # perequisite : user is admin ( name match %_adm_%)
    #
    def checkUserPassword(self, usrname, pswd):
        if usrname.find('_adm_') == -1:
            self.doNotify("Only admin users are allowed to log in") 
            return "nok"		
        auth = self.authenticate(usrname, pswd)
        self.doDebugPrint("auth {}".format(auth))
        self._authKey = self.getGeoKey(usrname)
        if auth == True:
            # enable user interface
            self.dlg.groupBox_Users.setEnabled(True)
            self.dlg.groupBox_Rights.setEnabled(True)
            self.dlg.groupBox_Admin.setEnabled(True)
            self.dlg.pushButton_DoLogin.setText("LogOut")
            
            self.fillInAllLayersTable()
            self.fillInComboUsers()
            self._adminuser = usrname   
            self.activateGrantButtons()     
            
            # avoid multiple login
            self.dlg.lineEdit_Info.setText("")             
            return "ok" 
        else:
            self.doNotify("Invalid user and (or) password") 
            return "nok"
    
    

    



    

    # #
    # fillInUsersTable : (UI) Fill in user table
    #
    def fillInUsersTable(self, database):
        model = QBrugisJsonTableModel()
        jdata = self.getWebRessource('users')
        
        # expected fields ( and order)
        expectedfields = ['user_name', 'table_name', 'UserRights']
    
        
        states = jdata[u'results']
        # print states
        if len(states) == 0:
            return 
        model.setJson(states, expectedfields)
    
        
        view = self.dlg.tableView_UserRights
        view.setModel(model)
        numRows = model.rowCount()
        self.doDebugPrint("numRows " + str(numRows))
        model.setHeaderData(0, Qt.Horizontal, "username")
        model.setHeaderData(1, Qt.Horizontal, "userrole")
        model.setHeaderData(2, Qt.Horizontal, "userpassword")
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)		
        
        
        view.setColumnWidth(0, 81)
        view.setColumnWidth(1, 160)
        view.setColumnWidth(2, 100)
        
        view.show()

    # #
    # fillInUsersTable : (UI) Fill list of all available table (for editing)
    # @code select tablename from pg_tables where not tablename like 'PUB%' and schemaname = 'brugis_intra' order by UPPER(tablename) ;
    #
    def fillInAllLayersTable(self):
        
        model = QBrugisJsonTableModel()
        jdata = self.getAllIntraTables(self._authKey)
        
        
        model.setJsonList(jdata, "atttables")
        view = self.dlg.listView_AllLyers
        view.setModel(model)
        
        view.show()


    # #
    # fillInComboUsers (UI) Requery users and fill in all user comboboxes 
    #
    def fillInComboUsers(self):
        jdata = self.getAllUserNames(self._authKey)
        lst = self.JsonToList(jdata)
        
        self.dlg.comboBox_Users.clear()
        self.dlg.comboBox_UsersAdmin.clear()
        self.dlg.comboBox_MngtUsers.clear()
        for uname in lst:
            self.dlg.comboBox_Users.addItem(uname[0])
            self.dlg.comboBox_UsersAdmin.addItem(uname[0])
            self.dlg.comboBox_MngtUsers.addItem(uname[0])
        self.dlg.comboBox_Users.show()	
        self.dlg.comboBox_UsersAdmin.show()	
        self.dlg.comboBox_MngtUsers.show()
        
        
    # #
    # doAssignLayer : assign right on selected user and table
    # -# create entry in user_rights table
    # -# update assigned layers list content (UI)
    #
    def doAssignLayer(self):
        self.doDebugPrint("doAssignLayer")
        # retrieve user
        usrname = self.dlg.comboBox_Users.currentText()
        # retrieve layer
        view = self.dlg.listView_AllLyers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            self.doDebugPrint("doAssignLayer  modelIndexList > 0")
            iIndex = modelIndexList[0]
            
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            
            self.doAssignUserLayer(layername, self._authKey, usrname)
            self.doDebugPrint("doAssignLayer  2")
    
            model = QBrugisJsonTableModel()
            jdata = self.getAllUserTables(usrname, self._authKey)
            model.setJsonList(jdata, "table_name")
            
            viewa = self.dlg.listView_Assigned_layers
            viewa.setModel(model)
            viewa.show()
            
            gstate = self.getTableState(layername, self._authKey)
            if gstate == self._brugis_dataflow_cin :
                self.updateLayerStatus(layername, self._brugis_dataflow_cin, self._adminuser)    
            self.doNotify("table {} assigned to {}".format(layername,usrname))    
            


    # #
    # doRemoveLayer : Remove assigned layer based on user selection (combobox)
    # prerequisite The table must be checked in by the relevant user
    # #
    def doRemoveLayer(self):
        # retrieve user
        self.doNotify("")
        usr = self.dlg.comboBox_Users.currentText()
        # retrieve layer
        view = self.dlg.listView_Assigned_layers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            state = self.getUserTableState(layername, self._authKey, usr)
            
            if not (state == self._brugis_dataflow_cin or state == self._brugis_dataflow_undefined):
                self.doNotify("invalid operation (layer not checked in)")
                return
            self.doRemoveUserRight(layername, self._authKey, usr)
            
            if not self.isTableAssigned(layername, self._authKey):
                self.removeLayerStatus(layername, self._authKey)
            
            model = QBrugisJsonTableModel()
            
            jdata = self.getAllUserTables(usr, self._authKey)
            model.setJsonList(jdata, "table_name")
            view = self.dlg.listView_Assigned_layers
            view.setModel(model)
            view.show()
            self.doNotify("table {} is no more assigned to {}".format(layername,usr))
            

    # #
    # doNotify : (UI) Fill in notification text box "lineEdit_Info"
    # #
    def doNotify(self, strMessage):
        self.dlg.lineEdit_Info.setText(strMessage)
        self.doDebugPrint(strMessage, True)
    
    
   
          
    
    # #
    # doRemoveAllLayer : Remove all the layers assigned to a specific user
    # prerequisite : layer must be checked in by the user
    # #
    def doRemoveAllLayer(self):
        self.doNotify("")
        # retrieve user
        usr = self.dlg.comboBox_Users.currentText()
         
        self.doRemoveAllUserRight(self._authKey, usr) 
        
        model = QBrugisJsonTableModel()
            
        jdata = self.getAllUserTables(usr, self._authKey)
        model.setJsonList(jdata, "table_name")
            
                        
        view = self.dlg.listView_Assigned_layers
        view.setModel(model)
        view.show()
        

    

    
        
    
    # #
    # doNewUser : (UI) Set default values for new user
    # #
    def doNewUser(self):
        self.dlg.lineEdit_MngtUser.setText("newuser_" + str(self._pseudocounter))
        self.dlg.lineEdit_MngtPassword.setText("newpswd")
        self.dlg.lineEdit_MngEmail.setText("newuser_" + str(self._pseudocounter) + "@sprb.irisnet.be")		
        self.dlg.lineEdit_MngtUser.setEnabled(True)          
        self.dlg.lineEdit_MngEmail.setEnabled(True)
        self._pseudocounter = self._pseudocounter + 1


   
    
    # #
    # User : remove the user from database if
    # 1° user <> admin
    # 2° No open action exist for this user
    # #
    def doRemoveUser(self):
        lEdit = self.dlg.lineEdit_MngtUser
        username = lEdit.text()
        # check that any layer is checkout by user
        if username.find('_adm_') >= 0:
            self.doNotify('Cannot remove admin user')
        else:    
            if self.getUserActivityState(username, self._authKey) == self._brugis_dataflow_cin :
                if self.doAskUser(u"L'utilisateur sera définitivement supprimé", "Veuillez confirmer"):
                    self.DeleteUser(username)
                    self.doBrugisEvent('undefined', 
                                       self._authKey, 
                                       "DELETE USER",
                                       "GLOBAL", 
                                       "BdmAdmin",
                                       "NOK", 
                                       "target : {}".format(username) )
                
            else:
                self.doNotify("Open action(s) for this user")
                
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
    # doDeleteUser : delete user related entries
    # delete entry in tables_states, user_rights and users
    # #
    def DeleteUser(self, username):
        self.doRemoveAllUserRight(self._authKey, username)
        self.doDeleteUser(self._authKey, username)
        self.fillInComboUsers()
        self.doNotify("User {} removed".format(username))
            
        
        
  
        
    # #
    # doSaveUser : Store username\password in brugis_admin.users table
    # prerequisite | 
    #   -# password len >= 3 
    #   -# not username contains '_adm_'
    #   -# email len >= 5 
    #   -# email match @code re.match('[a-zA-Z0-9]+@[a-zA-Z]+[.][a-zA-Z]+',lEditEmail.text())
    # #
    def doSaveUser(self):
        lEdit = self.dlg.lineEdit_MngtUser
        lEditPswd = self.dlg.lineEdit_MngtPassword
        lEditEmail = self.dlg.lineEdit_MngEmail
        
        
        if len(lEditPswd.text()) < 3 :
            self.doNotify("invalid password len must be >= 3")
            return 
        
        if len(lEditEmail.text()) < 5 :
            self.doNotify("invalid email len must be >= 3")
            return 
        
        res = re.match('[a-zA-Z0-9]+@[a-zA-Z]+[.][a-zA-Z]+', lEditEmail.text())
        
        if (res is None):            
            self.doNotify("invalid email format")
            return 
        
        if  lEdit.isEnabled():
            if lEdit.text().find('_adm_') >= 0:
                self.doNotify("invalid username, only one admin user is allowed")
                return
            else:        
                self.doCreateUser(lEdit.text(), lEditEmail.text(), lEditPswd.text(), self._authKey)
                lEdit.setEnabled(False)
                self.doNotify("user created")
                self.dlg.comboBox_Users.addItem(lEdit.text())
                self.dlg.comboBox_UsersAdmin.addItem(lEdit.text())
                self.dlg.comboBox_MngtUsers.addItem(lEdit.text())
                self.doBrugisEvent('undefined', 
                                   self._authKey, 
                                   "CREATE USER",
                                   "GLOBAL", 
                                   "BdmAdmin", 
                                   "OK", 
                                   "target : {}".format(lEdit.text()) )
                
        else:
            self.doUpdateUser(lEdit.text(), lEditEmail.text(), lEditPswd.text(), self._authKey)                            
            self.doNotify("user updated")
            self.doBrugisEvent('undefined', 
                               self._authKey, 
                               "UPDATE USER", 
                               "GLOBAL", 
                               "BdmAdmin",    
                               "OK", 
                               "target : {}".format(lEdit.text()) )
        #self.fillInComboUsers()
       
    # #
    # doImportNewTable : Integration procedure for new tables 
    # - get the list of all the table wich exist in bugis_edittmp and not in brugis_intra
    # - for each tables in the liste 
    #    -# check if geometrytype of GEOMETRY is MULTIPOINT/MULTIPOLYGON/MULTILINESTRING... If not abort the procedure
    #    -# assigned user rights to adminuser ( with statecrea)
    #    -# add entry in tables_states
    #
    def doImportNewTable(self):  
        # Retrieve new table         
        ntablesList = self.getAllNewTables(self._authKey) 
        
        for tbl in ntablesList:
            # check table structure
            gtype = self.doGetGeometryType(tbl, self._authKey) 
            
            if(gtype != "MULTIPOINT" and gtype != "MULTIPOLYGON" and gtype != "MULTILINESTRING"):
                errMsg = "Invalid GEOMETRY TYPE {}".format(gtype)
                self.doBrugisEvent(tbl, 
                                   self._authKey, 
                                   "IMPORT NEW TABLE", 
                                   "GLOBAL", 
                                   "BdmAdmin",
                                   "NOK", 
                                   errMsg)
                self.doNotify(errMsg)
                continue              
            
            self.doValidateImport(tbl, gtype, self._authKey)
            self.doTableDefaultAssignement(tbl, self._authKey) 
            #self.resetCreationStatus(tbl, self._authKey)
            self.doBrugisEvent(tbl, 
                               self._authKey, 
                               "IMPORT NEW TABLE", 
                               "GLOBAL", 
                               "BdmAdmin",  
                               "OK", 
                               "")
        
        
    #===========================================================================
    # doCreateCustomSerial
    # To be used with newly created tables ( stateCrea == NEW ) condition is tested in the function
    # 1° create the new sequence to be used to fill in ID field
    # 2° Create the ID fields
    # 3° Set sequence to max value of ID field
    # 4° Set ID field default value to nextval of sequence
    #===========================================================================
    def doCreateCustomSerial(self):
        view = self.dlg.tableView_AdminLayers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            stCrea = self.getTableStateCrea(layername, self._authKey)
            
            if stCrea != "NEW":
                self.doNotify("invalid operation (stateCrea <> NEW)")
                return
            
            self.doPk(layername, self._authKey)
            
        

    # #
    # doToIntra : Check if layer is in staging state if ok copy the table, copy constraints, drop table in modif
    # and update layer status
    #
    def doToIntra(self):
        view = self.dlg.tableView_AdminLayers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            usr = self.dlg.comboBox_UsersAdmin.currentText()
            state = self.getUserTableState(layername, self._authKey, usr)
            self.doDebugPrint( "ToIntra 1" ) 
            if state != self._brugis_dataflow_staging:
                self.doNotify("invalid operation (state <> STAGING)")
                return
            username = self.getTableLastOwner(layername, self._authKey)
            self.doDebugPrint( "ToIntra 2")
            ##################################################
            # Table is copied to Intra AND Publish to ensure Workflow consistency !!!!!
            self.doSafeCopyTableModifIntra(layername, self._authKey)
            self.doSafeCopyTableModifPublish(layername, self._authKey)
            self.doDebugPrint( "ToIntra 3" )
            ##################################################
            # Table is dropped from modif !!!!!
            self.tableModifDrop(layername, self._authKey)
            self.updateLayerStatus(layername, self._brugis_dataflow_cin, self._adminuser)
            self.resetCreationStatus(layername, self._authKey)
            self.doDebugPrint("ToIntra 4")
            self.refreshAdminLayers(usr, view)
            usermail = self.getUserMail(username) 
            self.send_mail("Notification Brugis", "La publication de la couche {} est prise en compte. Elle est immédiatement effective dans Brugis".format(layername) , usermail)
            self.send_mail("Notification Brugis", "La publication de la couche {} est notifiee a {}".format(layername, username) , self._brugisEmailAdress)
            self.doDebugPrint("ToIntra 5")
            self.fillInAllLayersTable()
            self.doBrugisEvent(layername, 
                               self._authKey, 
                               "TO_INTRA", 
                               self._brugis_dataflow_staging, 
                               "BdmAdmin", 
                               "OK", 
                               "")
            
            


            

    # #
    # doCancelCheckOut :  Check if table table state is VALID or COUT and if exist in brugis_intra 
    # if ok check out = drop the table and change status
    #
    def doCancelCheckOut(self):
        view = self.dlg.tableView_AdminLayers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            state = self.getTableState(layername, self._authKey)
            statecrea = self.getTableStateCrea(layername, self._authKey)
            if state != self._brugis_dataflow_cout:
                self.doNotify("invalid operation, state <> COUT ")
                return
            if statecrea == "NEW":
                self.doNotify("invalid operation (statecrea == NEW) ")
                return
            # undo checkout.... for table that previously exit in intra
            if self.tableExist(self._devSchema_intra, layername, self._authKey) != True :
                self.doBrugisEvent(layername, 
                               self._authKey, 
                               "UNDO_CHECKOUT", 
                               self._brugis_dataflow_cout, 
                               "BdmAdmin", 
                               "NOK", 
                               "Table does'nt exist in brugis_intra")
                self.doNotify("invalid operation table does'nt exist in brugis_intra")
                return
            self.tableEditDrop(self._devSchema_edit, layername, self._authKey)
            self.removeGSLayer(layername, self._authKey)
            self.updateLayerStatus(layername, self._brugis_dataflow_cin, self._authKey)
            self.doBrugisEvent(layername, 
                               self._authKey, 
                               "UNDO_CHECKOUT", 
                               self._brugis_dataflow_cout, 
                               "BdmAdmin", 
                               "OK", 
                               "")
            
            usr = self.dlg.comboBox_UsersAdmin.currentText()
            self.refreshAdminLayers(usr, view)
            self.doNotify("Cancel Checkout done " + layername)    

    # #
    # doTakeControl : Revoke restricted right from brugis_editor on brugis_edittmp schema
    # Transfer all checkout from specific users to admin user
    #
    def doTakeControl(self):
        self.doRevokeEdit(self._authKey)                  
        self.doSetGLock(self._authKey)
        
        self.activateGrantButtons()
        self.doBrugisEvent("undefined", 
                           self._authKey, 
                           "TAKE_CONTROL", 
                           "GLOBAL", 
                           "BdmAdmin", 
                           "OK", 
                           "")
        self.doDebugPrint("Grant revoked")

    
    # #
    # doGrantEdit Grant brugis_editor restricted edition rights on brugis_edittmp schema
    #
    def doGrantEdit(self):
        self.grantEdit(self._authKey)
        self.doResetGLock(self._authKey)
        
        self.activateGrantButtons()
        
        self.doBrugisEvent("undefined", 
                           self._authKey, 
                           "GRANT_EDIT", 
                           "GLOBAL", 
                           "BdmAdmin", 
                           "OK", 
                           "")
        self.doDebugPrint("Granted")
        
   
    # #
    # doClearAllCombo : cleanup content of all the comboxes
    #
    def doClearAllCombo(self):
        self.dlg.comboBox_Users.clear()
        self.dlg.comboBox_UsersAdmin.clear()
        self.dlg.comboBox_MngtUsers.clear()
        self.dlg.comboBox_Users.show()    
        self.dlg.comboBox_UsersAdmin.show()    
        self.dlg.comboBox_MngtUsers.show()
    
    
    def doClearAllViews(self):
        self.doClearView(self.dlg.listView_AllLyers)
        self.doClearView(self.dlg.listView_Assigned_layers)
        self.doClearView(self.dlg.tableView_AdminLayers)
        
        
    def doClearView(self, view):        
        model = QBrugisJsonTableModel()
        view.setModel(model)
        view.show()
        pass
        
    # #
    # doUndoStaging : remove table from brugis_modif, restore table in edit schema and update layer status
    #
    def doUndoStaging(self):
        view = self.dlg.tableView_AdminLayers
        modelIndexList = view.selectedIndexes()
        if len(modelIndexList) > 0:
            iIndex = modelIndexList[0]
            rowIndex = iIndex.row()
            layername = iIndex.sibling(rowIndex, 0).data()
            state = self.getTableState(layername, self._authKey)
            if state != self._brugis_dataflow_staging:
                self.doNotify("invalid operation (state <> STAGING)")
                return  
            self.doCopyTableModifToEdit(layername, self._authKey)
            self.tableModifDrop(layername, self._authKey)
            self.updateLayerStatus(layername, self._brugis_dataflow_cout, self._authKey)
            usr = self.dlg.comboBox_UsersAdmin.currentText()
            self.refreshAdminLayers(usr, view)
            self.doGrantEdit(self._authKey)
            self.doBrugisEvent(layername, 
                               self._authKey, 
                               "UNDO_STAGING", 
                               self._brugis_dataflow_staging, 
                               "BdmAdmin", 
                               "OK", 
                               "")
            
    
   
    
            
    # #
    # refreshAdminLayers : (UI) Requery and refresh content of AdminLayers QTableView
    # #
    def refreshAdminLayers(self, username, view):
        # usrname = self.dlg.comboBox_Users.itemText(idx)     
        model = QBrugisJsonTableModel()
        jdata = self.getWebRessource('UserTableStates', "uname={}".format(username))
        
        # expected fields ( and order)
        expectedfields = ['table_name', 'state']
    
        
        states = jdata[u'results']
        if len(states) == 0:
            model.clean(self)
            view.setModel(model)
            return 
        else:
            model.setJson(states, expectedfields)
         
        
            model.setHeaderData(0, Qt.Horizontal, "table_name")
            model.setHeaderData(1, Qt.Horizontal, "state")
        
            self.dlg.tableView_AdminLayers
            view.setModel(model)
        
            view.setColumnWidth(0, 230)
            view.setColumnWidth(1, 91)
        
        view.show()
        
        
    
        
    def activateGrantButtons(self):
        if self.isUserEditGranted(self._authKey):
            self.dlg.pushButton_TakeControl.setEnabled(True)
            self.dlg.pushButton_GrantEdit.setDisabled(True)
        else:
            self.dlg.pushButton_TakeControl.setDisabled(True)
            self.dlg.pushButton_GrantEdit.setEnabled(True)
        
