# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.10.4, generator: @autorest/python@6.32.2)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import


from ._models import (  # type: ignore
    BodyAuthGetOidcToken,
    BodyAuthGetOidcTokenGrantType,
    GroupInfo,
    HTTPValidationError,
    HeartbeatData,
    InitiateDeviceFlowResponse,
    InsertedJob,
    JobCommand,
    JobSearchParams,
    JobSearchParamsSearchItem,
    JobStatusUpdate,
    JobSummaryParams,
    JobSummaryParamsSearchItem,
    Metadata,
    OpenIDConfiguration,
    SandboxDownloadResponse,
    SandboxInfo,
    SandboxUploadResponse,
    ScalarSearchSpec,
    ScalarSearchSpecValue,
    SetJobStatusReturn,
    SetJobStatusReturnSuccess,
    SortSpec,
    SupportInfo,
    TokenResponse,
    UserInfoResponse,
    VOInfo,
    ValidationError,
    ValidationErrorLocItem,
    VectorSearchSpec,
    VectorSearchSpecValues,
)

from ._enums import (  # type: ignore
    ChecksumAlgorithm,
    JobStatus,
    SandboxFormat,
    SandboxType,
    ScalarSearchOperator,
    SortDirection,
    VectorSearchOperator,
)
from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "BodyAuthGetOidcToken",
    "BodyAuthGetOidcTokenGrantType",
    "GroupInfo",
    "HTTPValidationError",
    "HeartbeatData",
    "InitiateDeviceFlowResponse",
    "InsertedJob",
    "JobCommand",
    "JobSearchParams",
    "JobSearchParamsSearchItem",
    "JobStatusUpdate",
    "JobSummaryParams",
    "JobSummaryParamsSearchItem",
    "Metadata",
    "OpenIDConfiguration",
    "SandboxDownloadResponse",
    "SandboxInfo",
    "SandboxUploadResponse",
    "ScalarSearchSpec",
    "ScalarSearchSpecValue",
    "SetJobStatusReturn",
    "SetJobStatusReturnSuccess",
    "SortSpec",
    "SupportInfo",
    "TokenResponse",
    "UserInfoResponse",
    "VOInfo",
    "ValidationError",
    "ValidationErrorLocItem",
    "VectorSearchSpec",
    "VectorSearchSpecValues",
    "ChecksumAlgorithm",
    "JobStatus",
    "SandboxFormat",
    "SandboxType",
    "ScalarSearchOperator",
    "SortDirection",
    "VectorSearchOperator",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
if TYPE_CHECKING:
    __all__.extend(
        [
            "DeviceFlowErrorResponse",
        ]
    )
