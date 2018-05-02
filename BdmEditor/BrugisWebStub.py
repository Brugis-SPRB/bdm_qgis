# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2016

@author: mvanasten
@warning: designed has a web replacement for Brugis shared.... But need some child class rework
'''

import json

import requests
import settings as CONF
import platform

from PyQt4.QtCore import *


class Stub(object):
    '''
    @summary: group all django interface and utility functions 
    @note:  path to django server and WFS authorization are defined here
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
    
    
    _commandPath = CONF._commandPath
    _adminCommandPath = CONF._adminCommandPath
    _tokenPath = CONF._tokenPath
    
    _authUser = CONF._authUser
    _authPassword = CONF._authPassword
    
    _brugisAppServer = CONF._brugisAppServer
    _brugisWfsProxy = CONF._brugisWfsProxy
    
    _jkeyFunction = 'functionvalue'

    def __init__(self, params):
        
        '''
        Constructor
        '''
    
   
    def getUserTableState(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('U_T_STATE', layername, authkey)
        return self.getWebFunction(queryparams)
 
    def getUserActivityState(self, uname, authkey):
        queryparams = "action={}&uname={}&key={".format('U_A_STATE', uname, authkey)
        return self.getWebFunction(queryparams)
    
    def getTableState(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_S_STATE', layername, authkey)
        return self.getWebFunction(queryparams)
    
    
    
    
    def getTableStateCrea(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_S_STATECREA', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def getAllIntraTables(self, authkey):
        queryparams = "action={}&key={}".format('ALL_INTRATABLES', authkey)
        return self.getWebFunction(queryparams)
    
    def getAllUserNames(self, authkey):
        queryparams = "action={}&key={}".format('GET_ALL_USERNAMES', authkey)
        return self.getWebFunction(queryparams)
    
    def getAllUserTables(self, authkey):
        queryparams = "action={}&key={}".format('GET_ALL_USERTABLES', authkey)
        return self.getWebFunction(queryparams)
    
    def getGeoKey(self, uname):
        queryparams = "action={}&uname={}".format('NEWKEY', uname)
        return self.getTokenFunction(queryparams)
    
    
    
    
    def getTableLastOwner(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_L_OWNER', layername, authkey)
        return self.getWebFunction(queryparams)
        
    def isTableAssigned(self, layername, authkey):
        queryparams = "action={}&lname={}&key={}".format('T_ASSIGNED', layername, authkey)
        return self.getWebFunction(queryparams)
    
    def doGrantEdit(self, authkey):
        queryparams = "action={}&key={}".format('GRANT', authkey)
        return self.doWebCommand(queryparams)
    
    def doRevokeEdit(self, authkey):
        queryparams = "action={}&key={}".format('REVOKE', authkey)
        return self.doWebCommand(queryparams)
    
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
        return self.getWebFunction(queryparams)
    
    def doTransfertAllCheckout(self, authkey):
        queryparams = "action={}&key={}".format('TRANSFCOUT', authkey)
        return self.doWebCommand(queryparams)
         
    
    def doCopyTableModifToEdit(self, lname, authkey):
        queryparams = "action={}&lname={}&key={}".format('COPY_ME', lname, authkey)
        return self.doWebCommand(queryparams)
    
    def doResetGLock(self, authkey):
        queryparams = "action={}&key={}".format('RESET_G_LOCK', authkey)
        return self.doWebCommand(queryparams)
    
    def doSetGLock(self, authkey):
        queryparams = "action={}&key={}".format('SET_G_LOCK', authkey)
        return self.doWebCommand(queryparams)
    
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
    
    def dogetUserLock(self, authkey):
        queryparams = "action={}&key={}".format('U_LOCK', authkey)
        res = self.getWebFunctionSingl(queryparams)
        if res is None:
            return 0
        else:
            return int(res)
    
    def getUserMail(self, authkey):
        queryparams = "action={}&key={}".format('U_MAIL', authkey)
        return self.getWebFunctionSingl(queryparams)
        
    def getLastError(self, authkey):
        queryparams = "action={}&key={}".format('LAST_ERROR', authkey)
        return self.getWebFunction(queryparams)
    
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
    
    def authenticate(self, strusername, strpassword):
        self._authUser = strusername
        self._authPassword = strpassword  
        queryparams = "action={}".format('KEEPALIVE')
        self.doDebugPrint("authenticate {}".format(queryparams))
        return self.doWebCommand(queryparams)    
    
    def getAdminFunction(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._adminCommandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            return jData[self._jkeyFunction]
    
    
    def getWebRessource(self, ressourcename, rfilter):
        if len(rfilter) > 0:
            url = "{}{}?{}".format(self._brugisAppServer, ressourcename, rfilter)
        else:
            url = "{}{}".format(self._brugisAppServer, ressourcename)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            return json.loads(resp.content)
            
    def getWebFunction(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._commandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.ok):
            jData = json.loads(resp.content)
            return jData[self._jkeyFunction]
        else:
            return ''

        
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
            
    def doWebCommand(self, queryparams):
        url = "{}{}?{}".format(self._brugisAppServer, self._commandPath, queryparams)
        resp = requests.get(url, auth=(self._authUser, self._authPassword))
        if(resp.status_code < 400):
            return True
        else:
            return False
    
  
        
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
            self.doDebugPrint("SafeLen Not a valid string {}".format(self.toString(e)))
        return 0

    # #
    # matchOne : return true is item contains one of the string of matchList
    #
    def matchOne(self, item, matchList):
        for m in matchList:
            if item.find(m) != -1:
                return True
        return False 

    # #
    # doDebugPrint : print log message ( severe parameter to be used later)
    #
    def doDebugPrint(self, debugmsg, severe=False):
        try:
            print debugmsg.decode('utf8')
        except:
            pass
        
    def toString(self,obj):
        try:
            return str(obj)
        except:
            return ''
