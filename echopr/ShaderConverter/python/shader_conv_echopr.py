import os, sys, hou, json, base64, re

root_path = hou.getenv("ShaderConv_echopr_PATH")

#Qt Import Block 
from Qt import QtCore, QtWidgets, QtCompat , QtGui 

#Class Creation
class ShaderConv(QtWidgets.QMainWindow):
    def __init__(self, parent=hou.qt.mainWindow()): # parent=hou.qt.mainWindow()
        super(ShaderConv, self).__init__(parent) #QtCore.Qt.WindowStaysOnTopHint
        #File Interface File goes here
        file_interface = os.path.join(root_path + "\\Assets\\GUI\\shaderConv.ui")
        self.mw = QtCompat.loadUi(file_interface)
        self.setCentralWidget(self.mw)

        self.setWindowTitle("Shader Converter") # Set Window Title
        self.setStyleSheet(hou.qt.styleSheet()) # Set Stylesheet
        
        #Header  Image (Base64)
        header64 = 'iVBORw0KGgoAAAANSUhEUgAAAWkAAACXCAYAAADXlKqTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFF2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDYgNzkuZGFiYWNiYiwgMjAyMS8wNC8xNC0wMDozOTo0NCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIyLjQgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMS0wOC0yOVQxNjowMjo1NCswMTowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjEtMDgtMjlUMTY6MDM6MzgrMDE6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjEtMDgtMjlUMTY6MDM6MzgrMDE6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6YzNiMTU1N2MtYmU0MS1i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'
        header_data = base64.b64decode(header64)
        header_pixmap = QtGui.QPixmap()
        header_pixmap.loadFromData(header_data)
        #Assign Pixmap to label
        self.mw.lbl_header.setPixmap(header_pixmap)
        
        self.clearFields() #Clear Fields
        self.loadInit() # Load Initial Code Binds
        
        #Set Button Bind to Convert Button
        self.mw.bttn_convert.clicked.connect(self.convertButton)
        
        self.mw.cmb_load1.currentIndexChanged.connect(self.changeButtonIcon)
        self.mw.cmb_load2.currentIndexChanged.connect(self.changeButtonIcon)
        
        self.mw.bttn_mat_override.clicked.connect(self.setOverrideMat)
        self.mw.bttn_mat_override_reset.clicked.connect(self.clearOverrideMat)
        
    def clearOverrideMat(self):
        self.mw.line_mat_override.clear()
        self.consoleOut("Cleared Override.")
        
    def setOverrideMat(self):
        selNode = hou.selectedNodes()[0]
        if selNode.isMaterialManager() == True:
            self.mw.line_mat_override.setText(selNode.path())
            self.consoleOut("Set Override.")
        else:
            self.consoleOut("ERROR: Please Select a Material Network.")
        
    def consoleOut(self,message):
        self.mw.lbl_console.setText(message)
        
    def clearFields(self):
        self.mw.cmb_load1.clear()
        self.mw.cmb_load2.clear()
        
    def getBindPath(self):
        return(os.path.join(root_path + "\\Assets\\Bindings"))
        
    def getTargetExt(self):
        return(".json")
        
    def changeButtonIcon(self,basename):
        icoPath = os.path.join(root_path + "\\Assets\\GUI\\icons")
        try:
            iconPix = QtGui.QIcon(os.path.join(icoPath + "\\" + basename.lower() + ".png"))
            return(iconPix)
        except:
            pass
        
    def loadInit(self):
        #bindPath = os.path.join(root_path + "\\Assets\\Bindings")
        self.consoleOut("Loading Items...")
        bindPath = self.getBindPath()
        target_ext = self.getTargetExt()
        indxx = 0
        for file in os.listdir(bindPath):
            if file.endswith(target_ext):
                #Save to List
                fbase_name = os.path.basename(file).split(".")[0].title()
                #print(fbase_name)
                self.mw.cmb_load1.addItem(fbase_name)
                self.mw.cmb_load2.addItem(fbase_name)

                iconData = self.changeButtonIcon(fbase_name)
                self.mw.cmb_load1.setItemIcon(indxx,iconData)
                self.mw.cmb_load2.setItemIcon(indxx,iconData)
                
                indxx += 1 #inc counter
        try:
            AllItems = [self.mw.cmb_load1.itemText(i) for i in range(self.mw.cmb_load1.count())]
            counter1 = 0
            for i in AllItems:
                if i == "Mantra":
                    self.mw.cmb_load1.setCurrentIndex(counter1)
                else:
                    counter1 += 1
            #self.mw.cmb_load1.setCurrentIndex(1)
        except:
            pass
        self.consoleOut("...")
        
    ############################################################
    def flatten_json(self,y):
        out = {}
    
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '-')
                    i += 1
            else:
                name1 = re.sub(r'^.*?-','',name) 
                out[name1[:-1]] = x
    
        flatten(y)
        return out
    ############################################################
    
    #Get Raw File Data
    def getFileData(self,filePath):
        fileOpen = open(filePath,)
        data = json.load(fileOpen)
        fileOpen.close()
        return(data)
        
    def getDictErrorMsg(self):
        return("NULL")
        
    #Get Shader Details from json obj
    def getShaderDetails(self,dataObj,indx,id2):
        metaLst = []
        dict_errormsg = self.getDictErrorMsg()
        for meta in dataObj['shader_details']: 
        
            shader_givenname = meta.get('shader_givenname',dict_errormsg)
            metaLst.append(shader_givenname)
            #print(shader_givenname)
            
            ver = meta.get('version',dict_errormsg)
            metaLst.append(ver)
            
            hou_node_name = meta.get('houdini_node_name',dict_errormsg)
            metaLst.append(hou_node_name)
            
            hou_container = meta.get('houdini_container',dict_errormsg)
            metaLst.append(hou_container)
            
            hou_shopLoc = meta.get('houdini_shader_location',dict_errormsg)
            metaLst.append(hou_shopLoc)
            
            hou_node_name1 = ""
            if hou_node_name1 == "" and hou_node_name!=dict_errormsg:
                if hou_container == "SELF":
                    hou_node_name1 = hou_node_name
                else:
                    hou_node_name1 = hou_container

                
            prefx = meta.get('prefix',dict_errormsg)
            metaLst.append(prefx)
                
            #Get Image Node Data
            img_node = meta.get('image_details',dict_errormsg)
            metaLst.append(img_node)
            
            if id2 == 1:
                return(hou_node_name1)
            elif indx == 0 or indx == 1:
                return(metaLst)
                
    #loads shaderbinds        
    def getShaderBinds(self,dataObj):
        temp_dict = {}
        for bindings in dataObj["shader_binds"]:
            temp_dict.update(bindings)
        return(temp_dict)
        
    #Get Shader Texture Maps
    def getShaderMaps(self,dataObj):
        map_dict = {}
        for maps in dataObj["shader_maps"]:
            map_dict.update(maps)
        return(map_dict)
        
    def getShaderImg(self,imgMeta):
        flatImgMeta = self.flatten_json(imgMeta)
        dict_errormsg = self.getDictErrorMsg()
        i_nodename = flatImgMeta.get("node_name",dict_errormsg)
        i_fileParm = flatImgMeta.get("filename_parm",dict_errormsg)
        iLst = [i_nodename,i_fileParm]
        return(iLst)
        
        
    #Create Shader
    def createShader(self,location,nType,container,ogShaderName,givenname,prefix):
        #Create Container First
        if container != "SELF":
            if self.mw.line_mat_override.text() == "":
                LOC = hou.node(location)
            else:
                LOC = hou.node(self.mw.line_mat_override.text())
            contNode = LOC.createNode(container)
            contNode.moveToGoodPosition()
            contNode.setName((prefix+"_"+ogShaderName),unique_name=True)
            #Get Output node first
            outNode = contNode.children()[0]
            #Create internalNode
            intNode = contNode.createNode(nType)
            #Connect material to int node
            outNode.setInput(0,intNode)
            #Move to good location
            outNode.moveToGoodPosition()
            return(intNode) # Returns the interoir node for easy access
            
        elif container == "SELF":
            #mantra node process
            if self.mw.line_mat_override.text() == "":
                LOC = hou.node(location)
            else:
                LOC = hou.node(self.mw.line_mat_override.text())
            contNode = LOC.createNode(nType)
            contNode.setName((prefix+"_"+ogShaderName),unique_name=True)
            contNode.moveToGoodPosition()
            return(contNode)
            
            
    def convertShader(self,shader,shaderbinds1,shaderbinds2,shader2_meta,container,maps1,maps2):
        #print("ConvertShader")
        shader_parms = [parm for parm in shader.parms() if not parm.isAtDefault()]
        
        if container == True:
            parentNode = shader.parent()
            nametopass = parentNode.name()
        else:
            nametopass = shader.name()
        
        #Flatten Shaders JSON Data
        #global shaderbinds1, shaderbinds2
        sb1 = self.flatten_json(shaderbinds1)
        sb2 = self.flatten_json(shaderbinds2)
        
        shader2 = self.createShader(shader2_meta[4],shader2_meta[2],shader2_meta[3],nametopass,shader2_meta[0],shader2_meta[5])
        
        #Parm Convertion
        for i in shader_parms:
            #print(i.name())
            for k1, v1 in sb1.items():
                if i.name() in v1 and len(i.name()) == len(v1):
                    #print("BOUND",v1)
                    #Check if settings exist in other shader
                    for k2, v2 in sb2.items():
                        if k1 in k2:
                            #print("BOUND2",v2)
                            #eval value from shader1 and copy to shader 2
                            shader2.parm(v2).set(i.eval())
            #Check for Maps.
            for mk1, mv1 in maps1.items():
                if i.name() in mv1 and len(i.name()) == len(mv1):
                    for mk2, mv2 in maps2.items():
                        if mk1 in mk2:
                            #Create Node if not self else set parm.
                            shader_img_meta = self.getShaderImg(shader2_meta[6])
                            if shader_img_meta[0] == "SELF": #This is Mainly for Mantra
                                enableParm = i.name().split("_")[0] + str(shader_img_meta[1])
                                if enableParm == "baseNormal_useTexture":
                                    enableParm = "baseBumpAndNormal_enable"
                                shader2.parm(enableParm).set(True)
                                shader2.parm(mv2).set(str(i.eval()))
                            else:
                                #Create image node and connect result to appropriate shader.
                                imgNode = shader2.parent().createNode(shader_img_meta[0])
                                imgNode.parm(shader_img_meta[1]).set(str(i.eval()))
                                #Connect Shader2 to imgNode
                                
                                #Find Inputs for Shaders
                                inputList = shader2.inputNames()
                                connection_Dict = {}
                                keys = range(len(inputList))
                                for r in keys:
                                    connection_Dict[r] = inputList[r]
                                new_dict = {value:key for (key,value) in connection_Dict.items()}
                                connection_Dict = new_dict
                                paramTarget = connection_Dict.get(mv2, self.getDictErrorMsg()) #dict_errormsg = self.getDictErrorMsg()
                                
                                #Set Input for Shader2 to paramtarget
                                shader2.setInput(paramTarget,imgNode)
                                imgNode.moveToGoodPosition()
                                imgNode.setName("IMG_" + mv2)
                    
                     
    def convertButton(self):
        self.consoleOut("Attempting to Convert from: " + self.mw.cmb_load1.currentText() + " To: " + self.mw.cmb_load2.currentText())
        fileLoc1 = os.path.join(self.getBindPath() + "\\" + self.mw.cmb_load1.currentText().lower() + self.getTargetExt())
        fileLoc2 = os.path.join(self.getBindPath() + "\\" + self.mw.cmb_load2.currentText().lower() + self.getTargetExt())
        
        #Globals
        file1_data = self.getFileData(fileLoc1)
        file2_data = self.getFileData(fileLoc2)
        dict_errormsg = self.getDictErrorMsg() #Dictionary Error Parm
        hou_node_name1 = self.getShaderDetails(file1_data,0,1) #Used for Node Selection Filter
        shader1_meta = self.getShaderDetails(file1_data,0,0)
        shader2_meta = self.getShaderDetails(file2_data,1,0)
        #Shader Binds
        shaderbinds1 = self.getShaderBinds(file1_data)
        shaderbinds2 = self.getShaderBinds(file2_data)
        #Shader Maps
        shaderMap1 = self.getShaderMaps(file1_data)
        shaderMap2 = self.getShaderMaps(file2_data)
        
        #Get Nodes to Convert
        selNodes = [node for node in hou.selectedNodes() if node.type().name()==hou_node_name1]
        lenNodes = []
        for node in selNodes:
            if len(node.children()) > 0:
                lenNodes.append(node)
        if len(lenNodes)>0:
            container = True
        else:
            container = False
            
        if container == True:
            newTarg = shader1_meta[2]
            nNodes = []
            for node in selNodes:
                for i in node.children():
                    if i.type().name()==newTarg:
                        nNodes.append(i)
            selNodes = nNodes
            
        if len(selNodes)>0:
            #process nodes
            #print("len>1")
            #Iterate over each node in selection and convert.
            for each in selNodes:
                self.convertShader(each,shaderbinds1,shaderbinds2,shader2_meta,container,shaderMap1,shaderMap2)
            self.consoleOut("Task Finished...")
        else:
            self.consoleOut("ERROR:No Valid Node(s) Detected.")
        
        
def createWindow():        
    #End Block
    try:
        shaderConvWin.close()
    except:
        pass
        
    shaderConvWin = ShaderConv()
    shaderConvWin.resize(360,500)
    shaderConvWin.show() 