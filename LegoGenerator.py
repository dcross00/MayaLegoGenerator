import maya.cmds as cmds

class LegoMakerUI:
    def __init__(self):
        self.window = cmds.window(title="LEGO Maker", menuBar=True, width=300)
        self.create_ui()

    def create_ui(self):
        cmds.columnLayout("Square Blocks")
        cmds.separator(h=10)
        cmds.intSliderGrp("blockWidth", label="Block Width", field=True, min=1, max=10, v=4)
        cmds.intSliderGrp("blockDepth", label="Block Depth", field=True, min=1, max=10, v=2)
        cmds.optionMenu("ColourChoice", label="Colour Choice")
        for color in ["Red", "Blue", "Green", "Yellow", "Orange", "Pink", "Brown"]:
            cmds.menuItem(label=color)
        cmds.separator(h=10)
        cmds.button(label="Create Block", c=self.create_block)
        cmds.separator(h=10)
        cmds.showWindow(self.window)

    def create_block(self, *args):
        # Get parameters from UI
        width = cmds.intSliderGrp("blockWidth", q=True, v=True)
        depth = cmds.intSliderGrp("blockDepth", q=True, v=True)
        color = cmds.optionMenu("ColourChoice", q=True, v=True)  

        # Create block
        lego_block = LegoBlock(width, depth, color)
        lego_block.create()

class LegoBlock:
    def __init__(self, width, depth, color):
        self.width = width
        self.depth = depth
        self.color = color

    def create(self):
        sizeY = 0.96
        sizeX = self.width * 0.8
        sizeZ = self.depth * 0.8

        # Main block
        block = cmds.polyCube(h=sizeY, w=sizeX, d=sizeZ, sx=self.width, sz=self.depth)
        cmds.setAttr(block[0] + ".overrideEnabled", 1)

        # Apply color to block
        self.apply_color(block)

        # Create studs
        for i in range(self.width):
            for j in range(self.depth):
                nub = cmds.polyCylinder(r=0.25, h=0.2)
                cmds.move((sizeY/2.0 + 0.1), moveY=True, a=True)
                cmds.move((-sizeX/2.0 + (i+0.5) * 0.8), moveX=True, a=True)
                cmds.move((-sizeZ/2.0 + (j+0.5) * 0.8), moveZ=True, a=True)
                block = cmds.polyCBoolOp(block[0], nub[0], op=1, ch=False)

        # Remove Bottom
        tmp = cmds.polyCube(h=sizeY, w=sizeX-0.12*2, d=sizeZ-0.12*2, sx=self.width-1, sz=self.depth-1)
        cmds.move(-0.1, moveY=True)
        block = cmds.polyCBoolOp(block[0], tmp[0], op=2, ch=False)

        # Create inner nubs
        for i in range(self.width-1):
            for j in range(self.depth-1):
                nub = cmds.polyCylinder(r=0.3255, h=sizeY, sx=10)
                center = cmds.polyCylinder(r=0.25, h=1, sx=10)
                nub = cmds.polyCBoolOp(nub[0], center[0], op=2, caching=False, ch=False)
                cmds.move((-0.05), moveY=True, a=True)
                cmds.move((-sizeX/2.0 + (i+1) * 0.8), moveX=True, a=True)
                cmds.move((-sizeZ/2.0 + (j+1) * 0.8), moveZ=True, a=True)
                block = cmds.polyCBoolOp(block[0], nub[0], op=1, ch=False)

    def apply_color(self, block):
        rgb_values = {    
            "Red": (0.5, 0, 0),
            "Blue": (0, 0.34, 0.65),
            "Green": (0, 0.48, 0.15),
            "Yellow": (0.9, 0.7, 0),
            "Orange": (0.9, 0.3, 0.09),
            "Pink": (0.9, 0.55, 0.7),
            "Brown": (0.2, 0.1, 0.05),
        }

        rgb = rgb_values.get(self.color, (0, 0, 0))

        myShader = cmds.shadingNode('lambert', asShader=True)
        cmds.setAttr(myShader + '.color', rgb[0], rgb[1], rgb[2], type='double3')
        cmds.select(block[0])
        cmds.hyperShade(assign=myShader)
        cmds.delete(ch=True)

# Entry point
if __name__ == "__main__":
    LegoMakerUI()