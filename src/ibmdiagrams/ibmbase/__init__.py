# @file __init__.py
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

# Import from new locations and re-export for backward compatibility
from .builders.build import Build
from .builders.shapes import Shapes
from .builders.types import Types
from .core.common import Common
from .core.options import Options
from .core.properties import Properties
from .core.messages import Messages
from .composers.compose import Compose
from .composers.composejson import ComposeJSON
from .loaders.load import Load
from .loaders.loadjson import LoadJSON
from .loaders.opsjson import OpsJson
from .loaders.icons import Icons
from .elements.elements import Elements
from .resources import Resources
from .utils.utils import randomid
from .utils import enums, constants
from .utils.colors import Colors

__all__ = [
    "Build",
    "Shapes",
    "Types",
    "Common",
    "Options",
    "Properties",
    "Messages",
    "Compose",
    "ComposeJSON",
    "Load",
    "LoadJSON",
    "OpsJson",
    "Icons",
    "Elements",
    "Resources",
    "randomid",
    "enums",
    "constants",
    "Colors",
]
