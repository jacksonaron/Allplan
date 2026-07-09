<?xml version="1.0" encoding="utf-8"?>
<PythonPart xmlns="http://www.nemetschek.com/Allplan/PythonPart/1.0">
  <Name>Color Model Comparator</Name>
  <Description>Compare 3D models by Allplan color ID (1=Red, 2=Yellow, 3=Cyan, 4=Green, etc.). Double-click to run.</Description>
  <Author>Your Name</Author>
  <Version>1.0</Version>
  <Date>2024-12-19</Date>
  <MinAllplanVersion>2026</MinAllplanVersion>
  <MaxAllplanVersion>2026</MaxAllplanVersion>
  <PythonFile>ColorModelComparator.py</PythonFile>
  <Icon>None</Icon>
  <TaskArea>Modeling</TaskArea>
  <Startable>true</Startable>
  <Palette>
    <Name>Color Model Comparator</Name>
    <Description>Compare models by Allplan color ID and highlight missing elements</Description>
    <Width>350</Width>
    <Height>300</Height>
    <ControlProperties>
      <ControlProperty>
        <Name>Tolerance</Name>
        <Description>Comparison tolerance in meters</Description>
        <Type>Float</Type>
        <DefaultValue>0.001</DefaultValue>
        <MinValue>0.0</MinValue>
        <MaxValue>1.0</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color1ID</Name>
        <Description>First color ID (1=Red, 2=Yellow, 3=Cyan, 4=Green, 5=Magenta, 6=Blue)</Description>
        <Type>Integer</Type>
        <DefaultValue>1</DefaultValue>
        <MinValue>1</MinValue>
        <MaxValue>16</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2ID</Name>
        <Description>Second color ID (1=Red, 2=Yellow, 3=Cyan, 4=Green, 5=Magenta, 6=Blue)</Description>
        <Type>Integer</Type>
        <DefaultValue>3</DefaultValue>
        <MinValue>1</MinValue>
        <MaxValue>16</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color1Name</Name>
        <Description>Name for first color set (e.g., Existing)</Description>
        <Type>String</Type>
        <DefaultValue>Existing</DefaultValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2Name</Name>
        <Description>Name for second color set (e.g., Proposed)</Description>
        <Type>String</Type>
        <DefaultValue>Proposed</DefaultValue>
      </ControlProperty>
    </ControlProperties>
  </Palette>
</PythonPart>
