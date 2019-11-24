default_op = lambda x: x.strip('"').split(";")
no_op = lambda x: x.pop() if len(x) == 1 else x


def clean_metadata(bytestr):
    raw = bytestr.decode("utf-8").strip("\r\n").split("\r\n")
    raw_dict = dict(item.split("=") for item in raw)
    return {key: default_op(val) for key, val in raw_dict.items()}


metadata_to_dtypes = {
    "grid": {
        "Grid dim": lambda x: list(map(int, x.pop().split(" x "))),
        "Grid settings": lambda x: list(map(float, x)),
        "Sweep Signal": no_op,
        "Fixed parameters": no_op,
        "Experiment parameters": no_op,
        "# Parameters (4 byte)": lambda x: int(no_op(x)),
        "Experiment size (bytes)": lambda x: int(no_op(x)),
        "Points": lambda x: int(no_op(x)),
        "Channels": no_op,
    }
}
metadata_dtype = {"grid": {"Grid dim": float,}}

