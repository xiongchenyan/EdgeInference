'''
Created on May 22, 2014
count edge (between obj id) in Freebase
input :fb dump
output: edge cnt
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



class FbEdgeCounterC(cxBaseC):
    def Init(self):
        self.FbDumpIn = ""
        self.OutName = ""
        self.hEdge = {}
    @staticmethod
    def ShowConf():
        print "dumpin\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FbDumpIn = conf.GetConf('dumpin')
        self.OutName = conf.GetConf('out')
        
        
    def ProcessOneObj(self,lvCol):
        for vCol in lvCol:
            if (not IsId(vCol[0])) | (not IsId(vCol[2])):
                continue
            edge = DiscardPrefix(vCol[1])
            if not edge in self.hEdge:
                self.hEdge[edge] = 1
            else:
                self.hEdge[edge] += 1
        return True
    
    
    def dump(self):
        out = open(self.OutName,'w')        
        l = self.hEdge.items()
        l.sort(key=lambda item: item[1],reverse = True)
        
        for item in l:
            print >>out, item[0] + "\t%d" %(item[1])
        out.close()
        return True
    
    
    def Process(self):
        FbReader = FbDumpReaderC()
        FbReader.open(self.FbDumpIn)
        cnt = 0
        for lvCol in FbReader:
            cnt += 1
            if 0 == (cnt % 1000):
                print "processed [%d] obj [%d] edge met" %(cnt,len(self.hEdge))
            self.ProcessOneObj(lvCol)
        
        print "dumping"    
        self.dump()
        FbReader.close()
        print "done"
        return True


import sys

if 2 != len(sys.argv):
    print "conf"
    FbEdgeCounterC.ShowConf()
    sys.exit()
    
EdgeCounter = FbEdgeCounterC(sys.argv[1])

EdgeCounter.Process()

        