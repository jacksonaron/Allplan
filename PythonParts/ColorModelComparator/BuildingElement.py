"""
BuildingElement for ColorModelComparator PythonPart
Using Allplan color constants
"""

class BuildingElement:
    """Building element containing the parameter properties."""
    
    def __init__(self):
        self.Tolerance = ControlPropertyFloat(0.001)
        # Use Allplan color IDs instead of RGB
        self.Color1ID = ControlPropertyInt(1)  # Red = 1
        self.Color2ID = ControlPropertyInt(3)  # Cyan = 3
        self.Color1Name = ControlPropertyString("Existing")
        self.Color2Name = ControlPropertyString("Proposed")


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
