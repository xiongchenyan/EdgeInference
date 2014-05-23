'''
Created on May 22, 2014
check whether an object has sufficient information
the sufficient is defined via ObjInforRichC
input: fb dump
output: ObjInforC.dump
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools/')
site.addsitedir('/bos/usr0/cx/PyCode/EdgeInference/')


from FreebaseDump.FbDumpReader import *
from FreebaseDump.FbDumpBasic import *

from cxBase.base import cxConf,cxBaseC


class ObjInforRichC(object):
    def Init(self):
        self.ObjId = ""
        self.HasDesp = 0
        self.NumOfType = 0
        self.HasNotable = 0
        self.HasName = 0
        self.HasAlias = 0
        self.NumOfAttDomain = 0
        self.NumOfAtt = 0
        self.NumOfNeighbor = 0
        
    def __init__(self,data = ""):
        self.Init()
        if "" != data:
            if type(data) == str:
                self.loads(data)
            if type(data) == list:
                self.Extract(data)
        
        
    def dumps(self):
        res = self.ObjId
        res += "\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d" %(self.HasDesp,
                                                    self.NumOfType,
                                                    self.HasNotable,
                                                    self.HasName,
                                                    self.HasAlias,
                                                    self.NumOfAttDomain,
                                                    self.NumOfAtt,
                                                    self.NumOfNeighbor)
        return res
    
    
    def loads(self,line):
        vCol = line.strip().split('\t')
        self.ObjId = vCol[0]
        self.HasDesp = int(vCol[1])
        self.NumOfType = int(vCol[2])
        self.HasNotable = int(vCol[3])
        self.HasName = int(vCol[4])
        self.HasAlias = int(vCol[5])
        self.NumOfAttDomain = int(vCol[6])
        self.NumOfAtt = int(vCol[7])
        self.NumOfNeighbor = int(vCol[8])
        
        return True
    
    def Extract(self,lvCol):
        #lvCol is the dump for a obj
        if [] == lvCol:
            return False
        
        ObjId = GetId(lvCol[0][0])
        if "" == ObjId:
            return False
        
        self.ObjId = ObjId
        self.HasDesp = self.CheckDesp(lvCol)
        self.NumOfType = self.CheckType(lvCol)
        self.HasNotable = self.CheckNotable(lvCol)
        self.HasName = self.CheckName(lvCol)
        self.HasAlias = self.CheckAlias(lvCol)
        self.NumOfAttDomain = self.CheckAttDomain(lvCol)
        self.NumOfAtt = self.CheckAtt(lvCol)
        self.NumOfNeighbor = self.CheckNeighbor(lvCol)
        return True
    
    
    def CheckDesp(self,lvCol):
        if "" != GetDesp(lvCol):
            return 1
        return 0
    
    def CheckType(self,lvCol):
        cnt = 0
        for vCol in lvCol:
            if "" != GetType(vCol):
                cnt +=1
        return cnt
    
    def CheckNotable(self,lvCol):
        if "" != GetNotableType(lvCol):
            return 1
        return 0
    
    def CheckName(self,lvCol):
        if "" != GetName(lvCol):
            return 1
        return 0
    
    def CheckAlias(self,lvCol):
        for vCol in lvCol:
            if "" != GetAlias(vCol):
                return 1
        return 0
    
    def CheckAttDomain(self,lvCol):
        lDomain = []
        for vCol in lvCol:
            domain = GetDomain(vCol[1])
            if not domain in lDomain:
                lDomain.append(domain)
        return len(lDomain)
    
    def CheckAtt(self,lvCol):
        return len(lvCol)
    
    def CheckNeighbor(self,lvCol):
        cnt = 0
        for vCol in lvCol:
            if IsId(vCol[2]):
                cnt += 1
        return cnt
        
        
        
class FbObjInforRichJudgerC(cxBaseC):
    def Init(self):
        self.FbIn = ""
        self.OutName = ""
        
    @staticmethod
    def ShowConf():
        print "fbdumpin\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FbIn = conf.GetConf('fbdumpin')
        self.OutName = conf.GetConf('out')
        
        
    def Process(self):
        FbReader = FbDumpReaderC()
        FbReader.open(self.FbIn)
        out = open(self.OutName,'w')
        cnt = 0
        for lvCol in FbReader:
            cnt += 1
            if 0 == (cnt % 1000):
                print "read [%d] obj" %(cnt)
            ObjInfor = ObjInforRichC(lvCol)
            if ObjInfor.HasName & ObjInfor.HasDesp:
                print >>out, ObjInfor.dumps()      
        
        FbReader.close()    
        
        
        
        
import sys

if 2 != len(sys.argv):
    print "conf"
    FbObjInforRichJudgerC.ShowConf()
    sys.exit()
    
Judger = FbObjInforRichJudgerC(sys.argv[1])    
Judger.Process()

print "done"