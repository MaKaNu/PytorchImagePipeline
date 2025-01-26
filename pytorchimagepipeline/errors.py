"""Error handling for pytorch image pipeline.

This module implements error handling for configuration, registry and execution of the pipeline.

Copyright (C) 2025 Matti Kaupenjohann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorCode(Enum):
    CONFIG_MISSING = ("CFG001", "Configuration file not found")
    CONFIG_PERMISSION = ("CFG002", "Permission of config is not correct")
    CONFIG_INVALID = ("CFG003", "Configuration toml is invalid")
    CONFIG_SECTION = ("CFG004", "Missing required configuration section")
    REGISTRY_INVALID = ("REG001", "Class is not valid [Permance | PipelineProcess]")
    REGISTRY_PARAM = ("REG002", "Provided params for object are invalid.")
    INST_TYPE = ("INS001", "Type not definded for process or permanence")
    INSTANTIATION_FAILURE = ("INS001", "Object instantiation failed")
    PROCESS_EXECUTION = ("PROC001", "")
    PARAM_VALIDATION = ("PARAM001", "Invalid parameter configuration")
    PERMA_KEY = ("PERMA001", "Invalid Permanence object")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


## PIPELINE
@dataclass
class BuilderError(RuntimeError):
    error_value: Any

    def __post_init__(self, error_code: ErrorCode) -> None:  # type: ignore  # noqa: PGH003
        self.error_code = error_code

    def __str__(self) -> str:
        return f"[{self.error_code.code}]: {self.error_code.message}: {self.error_value}"


class ConfigNotFoundError(BuilderError):
    """Raised when the builder configuration file does not exists"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.CONFIG_MISSING)


class ConfigPermissionError(BuilderError):
    """Raised when the builder configuration file does not exists"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.CONFIG_PERMISSION)


class ConfigInvalidTomlError(BuilderError):
    """Raised when the configuration file is not valid toml"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.CONFIG_INVALID)


class ConfigSectionError(BuilderError):
    """Raised for config section missing"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.CONFIG_SECTION)


class RegistryError(BuilderError):
    """Raised for class registration issues"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.REGISTRY_INVALID)


class RegistryParamError(BuilderError):
    """Raised for class instatioation with wrong params"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.REGISTRY_PARAM)


class InstTypeError(BuilderError):
    """Raised when type in config not set"""

    def __post_init__(self) -> None:
        super().__post_init__(ErrorCode.INST_TYPE)


## Execution
class ExecutionError(Exception):
    """Raised during process execution failures"""

    def __init__(self, process: str, error: Exception):
        error_code = ErrorCode.PROCESS_EXECUTION
        super().__init__(f"[{error_code.code}]: Process {process} failed with {error}")


## PERMANENCE
class PermanenceError(RuntimeError):
    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
        super().__init__(f"[{error_code.code}]: raised without further context")


class PermanenceKeyError(PermanenceError):
    def __init__(self, error_code: ErrorCode, key: str) -> None:
        self.key = key
        super().__init__(error_code)

    def __str__(self) -> str:
        return f"[{self.error_code.code}]: {self.error_code.message} -> {self.key}"
