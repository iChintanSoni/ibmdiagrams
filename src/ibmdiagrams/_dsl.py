# @file _dsl.py
#
# Copyright contributors to the ibmdiagrams project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextvars import ContextVar
from enum import Enum
from sys import exit as sys_exit
from typing import Optional, Union, Dict, Any

from .ibmbase.build import Build
from .ibmbase.common import Common
from .ibmbase.properties import Properties
from .ibmbase.utils import randomid

_diagrams = ContextVar("diagrams")
_diagram = ContextVar("diagram")
_group = ContextVar("group")

_data = Properties()
_savediagrams = {}


def getDiagrams() -> Optional['Diagrams']:
    """Get the current Diagrams context."""
    try:
        return _diagrams.get()
    except LookupError:
        return None


def setDiagrams(diagrams: Optional['Diagrams']) -> None:
    """Set the current Diagrams context."""
    _diagrams.set(diagrams)


def saveDiagram(name: str, xmldata: Dict[str, Any]) -> None:
    """Save diagram XML data by name."""
    if name not in _savediagrams:
        _savediagrams[name] = xmldata


def getDiagram() -> Optional['Diagram']:
    """Get the current Diagram context."""
    try:
        return _diagram.get()
    except LookupError:
        return None


def setDiagram(diagram: Optional['Diagram']) -> None:
    """Set the current Diagram context."""
    _diagram.set(diagram)


def getGroup() -> Optional['Group']:
    """Get the current Group context."""
    try:
        return _group.get()
    except LookupError:
        return None


def setGroup(group: Optional['Group']) -> None:
    """Set the current Group context."""
    _group.set(group)


class Diagrams:
    common: Common
    properties: Dict[str, Any]
    diagramid: str

    def __init__(self, name: str = "", filename: str = "") -> None:
        self.common = Common()
        self.common.setInputPython()
        self.diagramid = randomid()

        self.properties = _data.getDiagramsProperties(
            name=name, filename=filename)
        _data.addSheets(self.diagramid, self.properties)

    def __enter__(self) -> 'Diagrams':
        setDiagrams(self)
        return self

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        build = Build(self.common, _data)
        build.buildSheets(self.properties, _savediagrams)
        setDiagrams(None)


class Diagram:
    common: Common
    properties: Dict[str, Any]
    diagramid: str
    fontname: str
    name: str

    def __init__(
        self,
        name: str = "",
        filename: str = "",
        output: str = "",
        font: str = "IBM Plex Sans",
        direction: str = "LR",
    ) -> None:
        self.common = Common()
        self.common.setInputPython()
        self.diagramid = randomid()
        self.name = name

        self.fontname = font
        self.common.setFontName(self.fontname)

        if output != "":
            self.common.setOutputFolder(output)

        if direction.upper() == "LR":
            self.common.setDirectionLR()
        elif direction.upper() == "TB":
            self.common.setDirectionTB()
        else:
            self.common.setDirectionLR()

        if getDiagrams() is not None:
            filename = "*"

        self.properties = _data.getDiagramProperties(
            name=name,
            filename=filename,
            output=output,
            fontname=self.fontname,
            direction=direction,
        )
        _data.addDiagram(self.diagramid, self.properties)
        _data.updateSequence(self.diagramid)

    def __enter__(self) -> 'Diagram':
        setDiagram(self)
        return self

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        build = Build(self.common, _data)
        xmldata = build.buildDiagrams()
        if xmldata is None:
            self.common.printExit()
        else:
            saveDiagram(self.name, xmldata)
        _data.reset()
        setDiagram(None)


class Group:
    common: Common
    icons: Any
    shapeid: str
    parentid: Optional[str]
    sourceid: Optional[str]
    targetid: Optional[str]
    parent: Optional['Group']
    item: Any
    connector: Any
    fontname: str
    fontsize: int
    properties: Dict[str, Any]

    def __init__(
        self,
        label: str = "",
        sublabel: str = "",
        linecolor: str = "",
        fillcolor: str = "",
        shape: str = "",
        icon: str = "",
        hideicon: bool = False,
        direction: str = "",
    ) -> None:
        self.common = Common()
        self.shapeid = randomid()

        self.fontname = self.common.getFontName()
        self.fontsize = 0

        self.parent = getGroup()
        if self.parent:
            self.parentid = self.parent.shapeid
        else:
            self.parentid = None

        self.properties = _data.getGroupProperties(
            label=label,
            sublabel=sublabel,
            linecolor=linecolor,
            fillcolor=fillcolor,
            shape=shape,
            icon=icon,
            hideicon=hideicon,
            fontname=self.fontname,
            fontsize=self.fontsize,
            direction=direction,
            parentid=self.parentid,
        )
        _data.updateSequence(self.shapeid)

    def __enter__(self) -> 'Group':
        setGroup(self)
        return self

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        _data.addGroup(self.shapeid, self.properties)
        setGroup(self.parent)

    def __sub__(self, shape: Optional[Union['Group', 'Item', 'Connector']] = None) -> Optional[Union['Group', 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=self.shapeid, targetid=shape.shapeid,
                      startarrow="", endarrow="", operator="sub")
        elif isinstance(shape, Connector):
            shape.sourceid = self.shapeid
            shape.operator = "sub"
        return shape

    def __lshift__(self, shape: Optional[Union['Group', 'Item', 'Connector']] = None) -> Optional[Union['Group', 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=shape.shapeid, targetid=self.shapeid,
                      startarrow="", endarrow="arrow", operator="lshift")
        elif isinstance(shape, Connector):
            shape.sourceid = self.shapeid
            shape.operator = "lshift"
        return shape

    def __rshift__(self, shape: Optional[Union['Group', 'Item', 'Connector']] = None) -> Optional[Union['Group', 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=self.shapeid, targetid=shape.shapeid,
                      startarrow="", endarrow="arrow", operator="rshift")
        elif isinstance(shape, Connector):
            shape.sourceid = self.shapeid
            shape.operator = "rshift"
        return shape


class Item:
    common: Common
    icon: Any
    shapeid: str
    parentid: Optional[str]
    sourceid: Optional[str]
    targetid: Optional[str]
    parent: Optional[Group]
    startarrow: str
    endarrow: str
    operator: str
    style: str
    item: Any
    connector: Any
    fontname: str
    fontsize: int
    properties: Dict[str, Any]

    def __init__(
        self,
        label: str = "",
        sublabel: str = "",
        linecolor: str = "",
        fillcolor: str = "",
        shape: str = "",
        icon: str = "",
        hideicon: str = "",
    ) -> None:
        self.common = Common()
        self.shapeid = randomid()

        self.parent = getGroup()
        self.parentid = self.parent.shapeid if self.parent else None
        setGroup(self.parent)

        self.fontname = self.common.getFontName()
        self.fontsize = 0

        self.properties = _data.getItemProperties(
            label=label,
            sublabel=sublabel,
            linecolor=linecolor,
            fillcolor=fillcolor,
            shape=shape,
            icon=icon,
            hideicon=hideicon,
            fontname=self.fontname,
            fontsize=self.fontsize,
            parentid=self.parentid,
        )

        _data.addItem(self.shapeid, self.properties)
        _data.updateSequence(self.shapeid)

    def __sub__(self, shape: Optional[Union[Group, 'Item', 'Connector']] = None) -> Optional[Union[Group, 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=self.shapeid, targetid=shape.shapeid,
                      startarrow="", endarrow="", operator="sub")
        elif isinstance(shape, Connector):
            shape.sourceid = self.shapeid
            shape.operator = "sub"
        return shape

    def __lshift__(self, shape: Optional[Union[Group, 'Item', 'Connector']] = None) -> Optional[Union[Group, 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=shape.shapeid, targetid=self.shapeid,
                      startarrow="", endarrow="arrow", operator="lshift")
        elif isinstance(shape, Connector):
            shape.sourceid = self.shapeid
            shape.operator = "lshift"

            connectorid = shape.getConnectorID()
            _data.setConnectorSourceID(connectorid, shape.shapeid)
            _data.setConnectorTargetID(connectorid, self.shapeid)
            _data.setConnectorOperator(connectorid, "lshift")

        return shape

    def __rshift__(self, shape: Optional[Union[Group, 'Item', 'Connector']] = None) -> Optional[Union[Group, 'Item', 'Connector']]:
        if isinstance(shape, (Group, Item)):
            Connector(sourceid=self.shapeid, targetid=shape.shapeid,
                      startarrow="", endarrow="arrow", operator="rshift")
        elif isinstance(shape, Connector):
            shape.targetid = self.shapeid
            shape.operator = "rshift"

            connectorid = shape.getConnectorID()
            _data.setConnectorSourceID(connectorid, shape.shapeid)
            _data.setConnectorTargetID(connectorid, self.shapeid)
            _data.setConnectorOperator(connectorid, "rshift")

        return shape


class EndTypes(Enum):
    NONE = "NONE"
    ARROW = "ARROW"
    OPENARROW = "OPENARROW"
    CIRCLE = "CIRCLE"
    OPENCIRCLE = "OPENCIRCLE"
    DIAMOND = "DIAMOND"
    OPENDIAMOND = "OPENDIAMOND"


class EndMapping(Enum):
    NONE = ""
    ARROW = "block"
    OPENARROW = "block"
    CIRCLE = "oval"
    OPENCIRCLE = "oval"
    DIAMOND = "diamond"
    OPENDIAMOND = "diamond"


class Connector:
    common: Common
    shapeid: str
    parentid: Optional[str]
    parent: Any
    linetype: str
    linewidth: int
    linecolor: str
    startarrow: str
    endarrow: str
    startfill: Union[bool, int]
    endfill: Union[bool, int]
    item: Any
    connector: Any
    fontname: str
    fontsize: int
    properties: Dict[str, Any]
    operator: str
    sourceid: Optional[str]
    targetid: Optional[str]

    def __init__(
        self,
        label: str = "",
        startarrow: str = "",
        endarrow: str = "",
        linetype: str = "solid",
        linewidth: int = 1,
        linecolor: str = "#000000",
        operator: str = "",
        sourceid: Optional[str] = None,
        targetid: Optional[str] = None,
    ) -> None:
        self.common = Common()
        self.shapeid = randomid()
        self.linecolor = linecolor
        self.fontname = self.common.getFontName()
        self.fontsize = 0
        self.operator = operator
        self.sourceid = sourceid
        self.targetid = targetid

        # Initialize arrow attributes with defaults
        self.startarrow = ""
        self.endarrow = ""
        self.startfill = 0
        self.endfill = 0

        if startarrow != "":
            if startarrow.upper() not in [parm.value for parm in EndTypes]:
                print("Connector.__init__: startarrow not supported: " + startarrow)
                sys_exit()

            self.startfill = 0 if startarrow.upper().startswith("OPEN") else 1

            if startarrow.upper() in ("ARROW", "OPENARROW"):
                self.startarrow = "block"
            elif startarrow.upper() in ("CIRCLE", "OPENCIRCLE"):
                self.startarrow = "oval"
            elif startarrow.upper() in ("DIAMOND", "OPENDIAMOND"):
                self.startarrow = "diamond"
            else:
                self.startarrow = ""

        if endarrow != "":
            if endarrow.upper() not in [parm.value for parm in EndTypes]:
                print("Connector.__init__: endarrow not supported: " + endarrow)
                sys_exit()

            self.endfill = 0 if endarrow.upper().startswith("OPEN") else 1

            if endarrow.upper() in ("ARROW", "OPENARROW"):
                self.endarrow = "block"
            elif endarrow.upper() in ("CIRCLE", "OPENCIRCLE"):
                self.endarrow = "oval"
            elif endarrow.upper() in ("DIAMOND", "OPENDIAMOND"):
                self.endarrow = "diamond"
            else:
                self.endarrow = ""

        self.properties = _data.getConnectorProperties(
            label=label,
            sourceid=sourceid or "",
            targetid=targetid or "",
            startarrow=self.startarrow,
            endarrow=self.endarrow,
            startfill=str(self.startfill),
            endfill=str(self.endfill),
            linetype=linetype,
            linewidth=linewidth,
            linecolor=linecolor,
            fontname=self.fontname,
            fontsize=self.fontsize,
        )

        _data.addConnector(self.shapeid, self.properties)
        _data.updateSequence(self.shapeid)

    def getConnectorID(self) -> str:
        return self.shapeid

    def __sub__(self, shape: Optional[Union[Group, Item]] = None) -> Optional[Union[Group, Item]]:
        if isinstance(shape, Group) or isinstance(shape, Item):
            if self.sourceid is not None:
                _data.setConnectorSourceID(self.shapeid, self.sourceid)
                _data.setConnectorTargetID(self.shapeid, shape.shapeid)
                _data.setConnectorStartArrow(self.shapeid, self.startarrow)
                _data.setConnectorEndArrow(self.shapeid, self.endarrow)
                _data.setConnectorStartFill(self.shapeid, self.startfill)
                _data.setConnectorEndFill(self.shapeid, self.endfill)
                _data.setConnectorOperator(self.shapeid, self.operator)
            else:
                _data.setConnectorSourceID(self.shapeid, self.shapeid)
                _data.setConnectorTargetID(self.shapeid, shape.shapeid)
                _data.setConnectorStartArrow(self.shapeid, self.startarrow)
                _data.setConnectorEndArrow(self.shapeid, self.endarrow)
                _data.setConnectorStartFill(self.shapeid, self.startfill)
                _data.setConnectorEndFill(self.shapeid, self.endfill)
                _data.setConnectorOperator(self.shapeid, self.operator)
                print("Connector.__sub__: shape << connector - shape not supported")
                sys_exit()
        else:
            print("Connector.__sub__: connector - shape not supported")
            sys_exit()

        return shape

    def __lshift__(self, shape: Optional[Union[Group, Item]] = None) -> Optional[Union[Group, Item]]:
        if isinstance(shape, Group) or isinstance(shape, Item):
            _data.setConnectorSourceID(self.shapeid, shape.shapeid)
            _data.setConnectorOperator(self.shapeid, self.operator)
            if self.operator == "rshift":
                _data.setConnectorStartArrow(self.shapeid, self.startarrow)
                _data.setConnectorEndArrow(self.shapeid, self.endarrow)
                _data.setConnectorStartFill(self.shapeid, self.startfill)
                _data.setConnectorEndFill(self.shapeid, self.endfill)
                _data.setConnectorOperator(self.shapeid, "lshift")
            else:
                _data.setConnectorEndArrow(self.shapeid, "block")
                _data.setConnectorEndFill(self.shapeid, self.endfill)
                _data.setConnectorOperator(self.shapeid, "lshift")
        else:
            print("Connector.__lshift__: connector << shape not supported")
            sys_exit()
        return shape

    def __rshift__(self, shape: Optional[Union[Group, Item]] = None) -> Optional[Union[Group, Item]]:
        if isinstance(shape, Group) or isinstance(shape, Item):
            _data.setConnectorSourceID(self.shapeid, shape.shapeid)
            _data.setConnectorOperator(self.shapeid, "rshift")
            if self.operator == "lshift":
                _data.setConnectorStartArrow(self.shapeid, "block")
            else:
                sourceid = _data.getConnectorSourceID(self.shapeid)
                targetid = _data.getConnectorTargetID(self.shapeid)
                _data.setConnectorSourceID(self.shapeid, targetid)
                _data.setConnectorTargetID(self.shapeid, sourceid)
                _data.setConnectorStartArrow(self.shapeid, "")
                _data.setConnectorEndArrow(self.shapeid, "block")
                _data.setConnectorEndFill(self.shapeid, self.endfill)
        else:
            print("Connector.__rshift__: connector >> shape not supported")
            sys_exit()
        return shape


__all__ = [
    "Connector",
    "Diagram",
    "Diagrams",
    "EndMapping",
    "EndTypes",
    "Group",
    "Item",
]
