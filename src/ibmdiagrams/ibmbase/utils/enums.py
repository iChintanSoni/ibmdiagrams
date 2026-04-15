# @file enums.py
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

"""Centralized Enum definitions for ibmdiagrams.

This module consolidates all Enum classes used throughout the project
to avoid duplication and ensure consistency.
"""

from enum import Enum


# Provider and Mode Enums
class Providers(Enum):
    """Cloud provider types."""
    ANY = 'any'
    IBM = 'ibm'


class RunMode(Enum):
    """Application run modes."""
    BATCH = 'batch'
    GUI = 'gui'
    WEB = 'web'


# Input/Output Type Enums
class InputTypes(Enum):
    """Supported input file types."""
    PYTHON = 'python'
    RIAS = 'rias'
    JSON = 'json'
    YAML = 'yaml'
    Terraform = 'terraform'


class OutputFormats(Enum):
    """Supported output file formats."""
    JPG = 'JPG'
    PDF = 'PDF'
    PNG = 'PNG'
    SVG = 'SVG'
    XML = 'XML'


# Label and Code Type Enums
class LabelTypes(Enum):
    """Label display types."""
    CUSTOM = 'CUSTOM'
    GENERAL = 'GENERAL'


class CodeTypes(Enum):
    """Code generation types."""
    DRAWIO = 'DRAWIO'
    PYTHON = 'PYTHON'


# Direction and Alternate Enums
class Directions(Enum):
    """Diagram layout directions."""
    LR = 'LR'  # Left to Right
    TB = 'TB'  # Top to Bottom


class Alternates(Enum):
    """Fill color alternation patterns."""
    WHITE = 'WHITE'  # white-to-light
    LIGHT = 'LIGHT'  # light-to-white
    NONE = 'NONE'    # all transparent
    USER = 'USER'    # all user-defined


# Font Enums
class FontNames(Enum):
    """Supported IBM Plex font families."""
    IBM_PLEX_SANS = 'IBM Plex Sans'
    IBM_PLEX_SANS_ARABIC = 'IBM Plex Sans Arabic'
    IBM_PLEX_SANS_DEVANAGARI = 'IBM Plex Sans Devanagari'
    IBM_PLEX_SANS_HEBREW = 'IBM Plex Sans Hebrew'
    IBM_PLEX_SANS_JP = 'IBM Plex Sans JP'
    IBM_PLEX_SANS_KR = 'IBM Plex Sans KR'
    IBM_PLEX_SANS_THAI = 'IBM Plex Sans Thai'


# Region Enums
class Regions(Enum):
    """IBM Cloud regions."""
    ALL = 'all'
    GERMANY = 'eu-de'
    OSAKA = 'jp-osa'
    SAOPAULO = 'br-sao'
    SYDNEY = 'au-syd'
    TOKYO = 'jp-tok'
    TORONTO = 'ca-tor'
    UNITEDKINGDOM = 'eu-gb'
    USEAST = 'us-east'
    USSOUTH = 'us-south'


# Shape Type Enums
class ItemTypes(Enum):
    """Item shape types (collapsed layout)."""
    ACTOR = 'ACTOR'
    PNODE = 'PRESCRIBED NODE'


class GroupTypes(Enum):
    """Group shape types (expanded layout)."""
    EPNODE = 'PRESCRIBED NODE EXPANDED'
    PLOC = 'PRESCRIBED LOCATION'
    GPLOC = 'GENERIC PRESCRIBED LOCATION'
    ZONE = 'ZONE'
    GZONE = 'GENERIC ZONE'


# Connector Enums
class ConnectorArrows(Enum):
    """Connector arrow types."""
    NONE = 'NONE'
    BLOCK = 'BLOCK'
    DIAMOND = 'DIAMOND'
    OVAL = 'OVAL'


class ConnectorStyles(Enum):
    """Connector line styles."""
    SOLID = 'SOLID'
    DASHED = 'DASHED'
    LONGDASHED = 'LONGDASHED'
    DOTTED = 'DOTTED'
    DOUBLE = 'DOUBLE'
    TUNNEL = 'TUNNEL'


class ExtendedConnectorStyles(Enum):
    """Extended connector style definitions for customization."""
    SOLID_LINE = 'dashed=0;'
    DASHED_LINE = 'dashed=1;'
    NO_ARROW = 'endArrow=none;'
    SINGLE_ARROW = 'endArrow=block;endFill=1;'
    DOUBLE_ARROW = 'endArrow=block;endFill=1;startArrow=block;startFill=1;'


__all__ = [
    # Provider and Mode
    "Providers",
    "RunMode",
    # Input/Output
    "InputTypes",
    "OutputFormats",
    # Labels and Code
    "LabelTypes",
    "CodeTypes",
    # Layout
    "Directions",
    "Alternates",
    # Fonts
    "FontNames",
    # Regions
    "Regions",
    # Shapes
    "ItemTypes",
    "GroupTypes",
    # Connectors
    "ConnectorArrows",
    "ConnectorStyles",
    "ExtendedConnectorStyles",
]

# Made with Bob
