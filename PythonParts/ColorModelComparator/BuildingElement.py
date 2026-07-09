"""
BuildingElement for ColorModelComparator PythonPart
"""

class BuildingElement:
    """Building element containing the parameter properties."""
    
    def __init__(self):
        self.Tolerance = ControlPropertyFloat(0.001)
        self.Color1Red = ControlPropertyInt(255)
        self.Color1Green = ControlPropertyInt(0)
        self.Color1Blue = ControlPropertyInt(0)
        self.Color2Red = ControlPropertyInt(0)
        self.Color2Green = ControlPropertyInt(255)
        self.Color2Blue = ControlPropertyInt(0)
        self.Color1Name = ControlPropertyString("Existing")
        self.Color2Name = ControlPropertyString("Proposed")
        self.RunComparison = ControlPropertyBool(False)


class ControlPropertyFloat:
    """Control property for float values."""
    
    def __init__(self, value):
        self.value = value


class ControlPropertyInt:
    """Control property for integer values."""
    
    def __init__(self, value):
        self.value = value


class ControlPropertyString:
    """Control property for string values."""
    
    def __init__(self, value):
        self.value = value


class ControlPropertyBool:
    """Control property for boolean values."""
    
    def __init__(self, value):
        self.value = value
