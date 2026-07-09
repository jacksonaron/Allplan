<?xml version="1.0" encoding="utf-8"?>
<PythonPart xmlns="http://www.nemetschek.com/Allplan/PythonPart/1.0">
  <Name>Color Model Comparator</Name>
  <Description>Compare 3D models by color across all open drawing files. Double-click to run comparison and highlight missing elements.</Description>
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
    <Description>Compare models by color and highlight missing elements</Description>
    <Width>350</Width>
    <Height>250</Height>
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
        <Name>Color1Red</Name>
        <Description>First color - Red component</Description>
        <Type>Integer</Type>
        <DefaultValue>255</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color1Green</Name>
        <Description>First color - Green component</Description>
        <Type>Integer</Type>
        <DefaultValue>0</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color1Blue</Name>
        <Description>First color - Blue component</Description>
        <Type>Integer</Type>
        <DefaultValue>0</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2Red</Name>
        <Description>Second color - Red component</Description>
        <Type>Integer</Type>
        <DefaultValue>0</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2Green</Name>
        <Description>Second color - Green component</Description>
        <Type>Integer</Type>
        <DefaultValue>255</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2Blue</Name>
        <Description>Second color - Blue component</Description>
        <Type>Integer</Type>
        <DefaultValue>0</DefaultValue>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color1Name</Name>
        <Description>Name for first color set</Description>
        <Type>String</Type>
        <DefaultValue>Existing</DefaultValue>
      </ControlProperty>
      <ControlProperty>
        <Name>Color2Name</Name>
        <Description>Name for second color set</Description>
        <Type>String</Type>
        <DefaultValue>Proposed</DefaultValue>
      </ControlProperty>
    </ControlProperties>
  </Palette>
</PythonPart>
