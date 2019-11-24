nanonis_format_dict = {
    "big endian float 32": ">f4",
    "little endian float 32": "<f4",
    "big endian float 64": ">f8",
    "little endian float 64": "<f8",
}

end_tags = dict(grid=":HEADER_END:\r\n", scan=":SCANIT_END:\n", spec="[DATA]")
suffix_map = {".3ds": "grid", ".sxm": "scan", ".dat": "spec"}
