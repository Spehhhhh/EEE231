class Component():

    #PLEASE init itself when create a new node or arc
    #Active property shows the Node/Arc is visible or not
    #PLEASE contact Zehao Liu if you have any problem of Component Class

    def __init__(self):
        Component.NodeCount = 0
        Component.ArcCount = 0
        Component.NodeCopyCount = 0
        Component.ArcCopyCount = 0

    def Node_Generate(NodeClass,Num,X,Y):
    #please change 'NodeClass' to the ACTUAL NODE CLASS NAME in code 
        Component.NodeCount = Component.NodeCount + 1
        NodeClass.Num(Component.NodeCount) = Num
        NodeClass.Active(Component.NodeCount) = 1
        NodeClass.PosX(Component.NodeCount) = X
        NodeClass.PosY(Component.NodeCount) = Y
        return NodeClass

    def Arc_Generate(ArcClass,Num,Connect1,Connect2):
    #please change 'ArcClass' to the ACTUAL ARC CLASS NAME in code 
        Component.ArcCount = Component.ArcCount + 1
        ArcClass.Num(Component.ArcCount) = Num
        ArcClass.Active(Component.ArcCount) = 1
        ArcClass.ConnectionHead(Component.ArcCount) = Connect1
        ArcClass.ConnectionTail(Component.ArcCount) = Connect2
        return ArcClass

    def Node_Delete(NodeClass,Num):
    #please change 'NodeClass' to the ACTUAL NODE CLASS NAME in code 
        for i in range(1,Component.NodeCount):
            if NodeCount(i) = Num
                NodeClass.Active(i) = 0
        return NodeClass

    def Arc_Delete(ArcClass,Num):
    #please change 'NodeClass' to the ACTUAL NODE CLASS NAME in code
        for i in range(1,Component.ArcCount):
            if ArcCount(i) = Num
                ArcClass.Active(i) = 0
        return ArcClass

    #2021.5.9 update*******************************
    def Node_Copy (NodeClass, Num):
        #please change 'NodeClass' to the ACTUAL NODE CLASS NAME in code
        Coponent.NodeCopyCount = ChosenNodeClass.Num(Num)
        return Component.NodeCopyCount

    def Node_Paste (X,Y):
        #please change 'NodeClass' to the ACTUAL NODE CLASS NAME in code
        Component.NodeCount =Component.NodeCount + 1
        NodeClass.Num(Component.NodeCount) = Component.NodeCount
        NodeClass.PosX(Component.NodeCount) = X
        NodeClass.PosY(Component.NodeCount) = Y
        #Color
        #NodeClass.Color(Component.NodeCount) =
            #NodeClass.Color(Coponent.NodeCopyCount)

        #Size
        #NodeClass.Size(Component.NodeCount) =
            #NodeClass.Size(Coponent.NodeCopyCount)

        #Shape
        #NodeClass.Shape(Component.NodeCount) =
            #NodeClass.Shape(Coponent.NodeCopyCount)
        #PLEASE change the 'commented code' to what is should be IN THE NODE CLASS
        return NodeClass

    def Arc_Copy (ChosenArcClass, Num):
        #please change 'ArcClass' to the ACTUAL ARC CLASS NAME in code
        Coponent.ArcCopyCount = ChosenArcClass.Num(Num)
        return Component.ArcCopyCount

    def Arc_Paste (X,Y):
        #please change 'ArcClass' to the ACTUAL ARC CLASS NAME in code
        Component.ArcCount = Component.ArcCount + 1
        ArcClass.Num(Component.ArcCount) = Component.ArcCount
        ArcClass.PosX(Component.ArcCount) = X
        ArcClass.PosY(Component.ArcCount) = Y
        #Color
        #ArcClass.Color(Component.ArcCount) =
            #ArcClass.Color(Coponent.ArcCopyCount)

        #Size
        #ArcClass.Size(Component.ArcCount) =
            #ArcClass.Size(Coponent.ArcCopyCount)

        #Shape
        #ArcClass.Shape(Component.ArcCount) =
            #ArcClass.Shape(Coponent.ArcCopyCount)
        #PLEASE change the 'commented code' to what is should be IN THE ARC CLASS
        return ArcClass
