# import statements
import os
from OCC.Extend.DataExchange import read_step_file, write_stl_file


def convert(input_file: str, output_file: str, mode: str = "stp-2-stl"):
    """
    Description:
    ============
        Convert function that converts various file formats to other.
        The function just call pythonocc in the backend.

        Default mode is converting step files to stl files.

    Parameters:
    ===========
        mode:str
            - "stp-2stl"
        input_file:str
            file of a given format
        stl_file:str
            file of required output format

    Return:
    =======
        Output file type selcted or Error
    """
    if os.path.exists(input_file):
        # Read the input file
        if mode == "stp-2-stl":
            shape = read_step_file(input_file)
        else:
            raise NotImplementedError(
                "No other filr format method implemented!")
    else:
        raise FileNotFoundError("Could not find the input file.")

    try:
        # Write the STL file
        write_stl_file(shape, output_file)
    except:
        raise IOError(
            "Failed to write the corresponding STL file from the provided STEP file.")
