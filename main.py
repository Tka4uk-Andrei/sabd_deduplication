HASH_FUNCTION = "None"

def get_file_names_in_folder(relative_folder_path : str) -> list[str]:
    return relative_folder_path + "/test.txt"



def get_hash_for_segment(byte_arr : bytes, )


# todo segmented read?
def binary_file_read(relative_file_path : str) -> bytes:
    """
        Read file in binary format, return byte array which file consists of
    """
    ret_arr = []
    with open(relative_file_path, "rb") as f:
        ret_arr = f.read()
    return ret_arr


bin_arr = binary_file_read(get_file_names_in_folder("test_data"))
