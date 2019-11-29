default_op = lambda x: x.strip('"').split(";")
pop_op = (
    lambda x: x[0] if len(x) == 1 and isinstance(x, list) else x
)  # return only element from sequence else sequence
no_op = lambda x: x


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
        "# Parameters (4 byte)": lambda x: int(pop_op(x)),
        "Experiment size (bytes)": lambda x: int(pop_op(x)),
        "Points": lambda x: int(pop_op(x)),
        "Channels": no_op,
    }
}
metadata_dtype = {"grid": {"Grid dim": float,}}

