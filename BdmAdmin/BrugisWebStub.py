# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2016

@author: mvanasten
'''

import json

import requests

from PyQt4.QtCore import *
from warnings import catch_warnings
import settings as CONF 
import platform

class Stub(object):
    '''
    classdocs
    '''
    # states
    _brugis_dataflow_cout = "COUT" 
    _brugis_dataflow_cin = "CIN" 
    _brugis_dataflow_staging = "STAGING" 
    _brugis_dataflow_valid = "VALID"
    _brugis_dataflow_undefined = "UNDEFINED"
    
    _brugis_useraction_CHECKOUT = "CHECKOUT"
    _brugis_useraction_VALIDATE = "VALIDATE"
    _brugis_useraction_STAGING = "STAGING"
    _brugis_useraction_UNDOCHECKOUT = "UNDOCHECKOUT"
    _brugis_useraction_UNDOSTAGING = "UNDOSTAGING"
    _myVersion = "0.6" 
    
    _brugis_GEOMETRY_COLUMN = "GEOMETRY"
    
    _brugisEmailAdress = CONF._brugisEmailAdress
    _brugisSmtp = CONF._brugisSmtp
    

    _brugisAppServer = CONF._brugisAppServer
    _brugisWfsProxy = CONF._brugisWfsProxy
    
    _commandPath = CONF._commandPath
    _adminCommandPath = CONF._adminCommandPath
    
    _tokenPath = CONF._tokenPath
     
    _authUser = CONF._authUser
    _authPassword = CONF._authPassword  
    _authKey = ''
    _jkeyFunction = CONF._jkeyFunction

    def __init__(self, params):
        
        '''
        Constructor
        '''
    
 
    def getUserTableState(self, layername, authkey, uname):
        queryparams = "action={}&lname={}&uname={}&key={}".format('U_T_STATE', layername, uname, authkey)
        return self.getWebFunction(queryparams)
    
    def getUserActivityState(self, uname, authkey):
        queryparams = "action={}&uname={}&key={}".format('U_A_STATE', uname, authkey)
        return self.getWebFunction(queryparams)
    
    def getTableState(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_S_STATE', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def getTableStateCrea(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_S_STATECREA', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def getAllIntraTables(self, authkey):
        queryparams = "action={}&key={}".format('ALL_INTRATABLES', authkey)
        return self.getAdminFunction(queryparams)
    
    def getAllUserNames(self, authkey):
        queryparams = "action={}&key={}".format('ALL_USERNAMES', authkey)
        return self.getAdminFunction(queryparams)
    
    def getAllUserTables(self, uname, authkey):
        queryparams = "action={}&uname={}&key={}".format('ALL_USERTABLES', uname, authkey)
        return self.getWebFunction(queryparams)
    
    def doPk(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('DO_PK', layername, authkey)
        return self.getAdminFunction(queryparams)
    
    
    def getGeoKey(self, uname):
        queryparams = "action={}&uname={}".format('NEWKEY', uname)
        return self.getTokenFunction(queryparams)
   
    def getTableLastOwner(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_L_OWNER', layername, authkey)
        return self.getWebFunction(queryparams)
        
    def isTableAssigned(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_ASSIGNED', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def grantEdit(self, authkey):
        queryparams = "action={}&key={}".format('GRANT', authkey)
        return self.doAdminCommand(queryparams)
    
    def doRevokeEdit(self, authkey):
        queryparams = "action={}&key={}".format('REVOKE', authkey)
        return self.doAdminCommand(queryparams)
    
    def sendMail(self, subject, body, recipient, authkey):
        queryparams = "action={}&mail_message={}&mail_recipient={}&mail_subject={}&key={}".format('SEND_MAIL', body, recipient, subject, authkey)
        return self.doWebCommand(queryparams)

    def doBrugisEvent(self, lname, authkey, action, state, context, res, info):
        queryparams = "action={}&lname={}&key={}&trans={}&state={}&result={}&info={}&hname={}".format('EVENT',
                                                                                                      lname,
                                                                                                      authkey,
                                                                                                      action,
                                                                                                      state,
                                                                                                      res,
                                                                                                      info,
                                                                                                      platform.node())
        return self.doWebCommand(queryparams)

    # #
    # doCleanupOrphaned : remove references to table no more present in any databrugis schema
    # @code delete from brugis_qgisplugin_admin.tables_states where table_name not in ( select tablename from pg_tables );    
    # delete from brugis_qgisplugin_admin.user_rights where table_name not in ( select tablename from pg_tables );
    #
    def doCleanupOrphaned(self):
        queryparams = "action={}".format('CLEANUP_ORPHANED')
        return self.doWebCommand(queryparams)
    
  
    
    def tableModifDrop(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('M_DROP', layername, authkey)
        return self.doWebCommand(queryparams)

    def tableEditDrop(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('E_DROP', layername, authkey)
        return self.doWebCommand(queryparams)
                
    
    def doGetGeometryType(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('GEOTYPE', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def doTableDefaultAssignement(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('DEFAULT_ASSIGN', layername, authkey)
        return self.doAdminCommand(queryparams)
    
    def doValidateImport(self, layername, gtype, authkey):
        queryparams = "action={}&lname={}&gtype={}&key={}".format('IMPORT_VALIDATE', layername, gtype, authkey)
        return self.doAdminCommand(queryparams)
    
    def doTransfertAllCheckout(self, authkey):
        queryparams = "action={}&key={}".format('TRANSFCOUT', authkey)
        return self.doAdminCommand(queryparams)
    
    def doAssignUserLayer(self, layername, authkey, uname):
        queryparams = "action={}&lname={}&uname={}&key={}".format('ASSIGN_LAYER', layername, uname, authkey)
        return self.doAdminCommand(queryparams)
    
    
    def doRemoveUserRight(self, layername, authkey, uname):
        queryparams = "action={}&lname={}&uname={}&key={}".format('REMOVE_RIGHT', layername, uname, authkey)
        return self.doAdminCommand(queryparams)
    
    def doRemoveAllUserRight(self, authkey, uname):
        queryparams = "action={}&uname={}&key={}".format('REMOVE_ALL_RIGHT', uname, authkey)
        return self.doAdminCommand(queryparams)
    
    def doDeleteUser(self, authkey, uname):
        queryparams = "action={}&uname={}&key={}".format('DELETE_USER', uname, authkey)
        return self.doAdminCommand(queryparams)
    
    def doCreateUser(self, usrname, usermail, userpswd, authkey):
        queryparams = "action={}&uname={}&umail={}&upswd={}&key={}".format('CREATE_USER', usrname, usermail, userpswd, authkey)
        return self.doAdminCommand(queryparams)
    
    def doUpdateUser(self, usrname, usermail, userpswd, authkey):
        queryparams = "action={}&uname={}&umail={}&upswd={}&key={}".format('UPDATE_USER', usrname, usermail, userpswd, authkey)
        return self.doAdminCommand(queryparams)  
    
    def doCopyTableModifToEdit(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('COPY_ME', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def doResetGLock(self, authkey):
        queryparams = "action={}&key={}".format('RESET_G_LOCK', authkey)
        return self.doAdminCommand(queryparams)
    
    def doSetGLock(self, authkey):
        queryparams = "action={}&key={}".format('SET_G_LOCK', authkey)
        return self.doAdminCommand(queryparams)
    
    def doCheckGlobalLock(self, authkey):
        queryparams = "action={}&key={}".format('GET_G_LOCK', authkey)
        return self.getWebFunction(queryparams)
    
    def doCopyTableEditToModif(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('COPY_EM', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def doCopyTableIntraToEdit(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('COPY_IE', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def doSafeCopyTableModifIntra(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('SAFE_COPY_MI', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def doSafeCopyTableModifPublish(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('SAFE_COPY_PU', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def dogetUserLock(self, authkey):
        queryparams = "action={}&key={}".format('U_LOCK', authkey)
        return int(self.getWebFunctionSingl(queryparams))
    
    def getUserMail(self, uname, authkey):
        queryparams = "action={}&uname={}&key={}".format('U_MAIL', uname, authkey)
        return self.getWebFunctionSingl(queryparams)
    
    def getGeometryValid(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('IS_VALID', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def addGSLayer(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('ADD_GS_LAYER', layername, authkey)
        return self.getAdminFunction(queryparams)
    
    def removeGSLayer(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('REMOVE_GS_LAYER', layername, authkey)
        return self.getAdminFunction(queryparams)
    
    def doLockUserSession(self, authkey):
        queryparams = "action={}&key={}".format('L_U_SESSION', authkey)
        return self.doWebCommand(queryparams)
    
    def doUnLockUserSession(self, authkey):
        queryparams = "action={}&key={}".format('U_U_SESSION', authkey)
        return self.doWebCommand(queryparams)
    
    def doPkDefaultValue(self, lname, authkey):
        queryparams = "action={}&lname={&key={}}".format('PKDEFAULT', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def updateLayerStatus(self, layername, status, authkey="undefined"):
        queryparams = "action={}&lname={}&status={}&key={}".format('U_L_STATUS', layername, status, authkey)
        return self.doWebCommand(queryparams)
    
    def removeLayerStatus(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('R_L_STATUS', layername, authkey)
        return self.doWebCommand(queryparams)
    
    def resetCreationStatus(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('R_C_STATUS', layername, authkey)
        return self.doWebCommand(queryparams)
    
    def doCheckConsistency(self, authkey):
        queryparams = "action={}&key={}".format('C_CHECK', authkey)
        return self.getWebFunction(queryparams)
    
    def getAllNewTables(self, authkey):
        queryparams = "action={}&key={}".format('ALL_NEWTABLES', authkey)
        return self.getAdminFunction(queryparams)
    
    
    def authenticate(self, strusername, strpassword):
        self._authUser = strusername
        self._authPassword = strpassword  
        self.doDebugPrint( "authenticate {} {}".format(strusername, strpassword))
        queryparams = "action={}".format('KEEPALIVE')
        self.doDebugPrint( "authenticate {}".format(queryparams))
        return self.doWebCommand(queryparams)    
    

            
    def getWebFunction(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._commandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            return jData[self._jkeyFunction]
    
    def getAdminFunction(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._adminCommandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            return jData[self._jkeyFunction]
        
    def getTokenFunction(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._tokenPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            return jData[self._jkeyFunction]
    
    def getWebFunctionSingl(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._commandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            val = jData[self._jkeyFunction]
            return val
            
    
  
        
    def JsonToList(self, jdata):
        lst = list()
        for record in jdata:
            val = record
            lst.append(val)
        return lst
    
    # #
    # safeLen : safe (unicode, None) string len function 
    #
    def safeLen(self, ch):
        if ch is None:
            return 0
        try:
            if str(ch) == "NULL":
                return 0
            l = len(str(ch))
            return l
        except Exception, e :
            self.doDebugPrint("Safelen Not a valid string {}".format(e))
        return 0

    # #
    # doDebugPrint : print log message ( severe parameter to be used later)
    #
    def doDebugPrint(self, debugmsg, severe=False):
        try:
            print debugmsg.decode('utf8')
        except :
            pass
      

    

  
    
    def isUserEditGranted(self, authkey):
        queryparams = "action={}&key={}".format('IS_EDIT_GRANTED', authkey)
        count = self.getWebFunction(queryparams)
        try:
            count = int(self.getWebFunction(queryparams))
            return (count > 0)
        except :
            return False
        
    
    
    
    def doUserCommand(self, user, mail, password):
        url = "{}{}/users/".format(self._brugisAppServer, self._commandPath)
        resp = requests.post(url, auth=(self._authUser, self._authPassword), data={'user':user, 'email':mail, 'password':password})
        self.doDebugPrint(resp)
        if(resp.status_code < 400):
            return True
        else:
            return False
  
    
    def doCreateCustomSerial(self, layername):
        queryparams = "action={}&lname={}".format('PKDEFAULT', layername)
        return self.doWebCommand(queryparams)
     
    
    def getWebRessource(self, ressourcename, rfilter=None):
        if rfilter is None or len(rfilter) > 0:
            url = "{}{}?{}".format(self._brugisAppServer, ressourcename, rfilter)
        else:
            url = "{}{}".format(self._brugisAppServer, ressourcename)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            return json.loads(resp.content)
            
    def doWebCommand(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._commandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        self.doDebugPrint(resp)
        if(resp.status_code < 400):
            return True
        else:
            return False
    
    def doAdminCommand(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._adminCommandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        self.doDebugPrint(resp)
        if(resp.ok):
            return True
        else:
            return False
    
    def JsonToQstringList(self, jdata):
        lst = QStringList()
        for record in jdata:
            val = record
            lst.append(val)
        return lst    


