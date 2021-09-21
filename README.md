# Houdini Shader Converter
## Overview
*This tool as of **v0.1** only allows converting Mantra shaders to a appropriate 3rd party shader. (See Compatibility List)*

This tool allows the convertion of shaders from parameters specified inside external JSON files found in the Bindings Folder.
![HouShaderConvHeader](https://github.com/SideswipeeZ/houdini-shader-converter/blob/main/git/ui_cap.png)
## Installation
*This tool can exist for both Python2 and Python 3 Builds of Houdini in the same Folder. (Tested in 18.5)*
### Manual Install

To install the Tool using Manual Instructions, Extract the **echopr** and **packages** folders into your Houdini Documents folder (This Folder contains the houdini.env file.)

Then Create a Shelf tool with the following:

Options:
Name: **Shader_Converter_echopr**
Label: **Shader Converter 0.1**
Icon: **hicon:/SVGIcons.index?COP2_aidenoise.svg**

Code:
```
import shader_conv_echopr as shaderConv

shaderConvWin = shaderConv.ShaderConv()
shaderConvWin.resize(360,500)
shaderConvWin.show()

 ```

### Auto Installer (Windows)
To install the tool on Windows using the Auto-Installer, Simply download the executable binary from **Releases** and follow the instructions.

## Function
To use this tool Simply select the Shader from the dropdown menu you want to convert to: Then select the appropriate shader(s) from Houdini's Network View then Finally Click Convert.

By Default the location to create the new shader is specified inside of the JSON files, However you can override the location by selecting a **Material Network** from the Houdini Network View and Clicking **Set Override**. This allows you to set the target Material Network to be the new place to create the new shaders to.
To reset the override Material Network, simply click **Reset Override**, this will reset the setting to use the default location specified inside of the JSON file.

## Editing JSON Parameters
If you want to edit/add/remove parameters to a shader you can do so by editing the **shader_binds** and **shader_maps** objects inside of the JSON file for each specified shader. 

Each object name must match between all shaders to convert, however the value can be different.

The JSON File contains 3 lists of objects:
* **shader_details**
	* This contains details for the shader for the UI elements and meta data for nodes needed to create a texture node and container vopnet.
	

* **shader_binds**
	* This contains details for the shader for the paramter conversion. These have been sorted into lists for ease of readablilty.
	* Shader parameters here can be added/changed as long as the object name remains consistant with other JSON shader parameter names.

* **shader_maps**
	* This contains parameters for locating shader texture maps.
	*  Shader parameters here can be added/changed as long as the object name remains consistant with other JSON shader parameter names.

### Adding Shaders
You can also create new shader support for another render engine as long as you follow the template that you can obtain from the template.json file or an of the other json files.


# Future Plans
* Allow support for any shader to shader conversion
* Add more support for parameters inside of JSON files from Default install.

# Licence
MIT
