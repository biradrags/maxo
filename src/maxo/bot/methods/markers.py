from unihttp.markers import (
    Body as UniBody,
    File as UniFile,
    Form as UniForm,
    Header as UniHeader,
    Path as UniPath,
    Query as UniQuery,
)

Body = UniBody
Path = UniPath
Query = UniQuery
Header = UniHeader
File = UniFile
Form = UniForm


__all__ = (
    "Body",
    "File",
    "Form",
    "Header",
    "Path",
    "Query",
)
