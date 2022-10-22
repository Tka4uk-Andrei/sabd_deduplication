import hashlib
import sqlite3 as sl
import os


HASH_FUNCTION_NONE = "None"
HASH_FUNCTION_MD5 = "MD5"

DATA_PATH = "test_data"
SEGMENT_SIZE = 4
HASH_FUNCTION_IN_USE = HASH_FUNCTION_NONE
FOLDER_WITH_COMPRESED_DATA = "compressed_data"
FOLDER_WITH_DECOMPRESED_DATA = "decompressed_data"


def get_file_names_in_folder(relative_folder_path : str):
    return os.listdir(relative_folder_path)


def get_hash_for_segment(byte_slice : bytes, hash_function : str) -> bytes:
    if (hash_function == HASH_FUNCTION_NONE):
        return byte_slice
    elif (hash_function == HASH_FUNCTION_MD5):
        return str.encode(hashlib.md5().hexdigest())
    else:
        print("FAILED: get_hash_for_segment()")
        exit(-1)


def get_segmented_sequence(byte_arr : bytes, seg_size : int):
    segmented_arr = []
    input_len = len(byte_arr)
    for seg_start in range(0, input_len, seg_size):
        segmented_arr.append(byte_arr[seg_start:min(seg_start + seg_size, input_len)])
    return segmented_arr


def binary_file_read(relative_file_path : str) -> bytes:
    """
        Read file in binary format, return byte array which file consists of
    """
    ret_arr = []
    with open(relative_file_path, "rb") as f:
        ret_arr = f.read()
    return ret_arr


def binary_file_write(relative_file_path : str, hash_arr):
    with open(relative_file_path, "wb") as f:
        for hash in hash_arr:
            f.write(hash)


def save_compresed_data_file(relative_file_path : str, compresed_data):
    with open(relative_file_path + ".txt", "w") as f:
        for elem in compresed_data:
            f.write(str(elem) + '\n')


def read_compresed_data_file(relative_file_path : str):
    byte_arr = []
    with open(relative_file_path + ".txt", "r") as f:
        for line in f.readlines():
            print(line)
            print(bytearray(line))
    return byte_arr


def insert_hashes_into_bd(cur, conn, data_arr):
    """_summary_

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
        data_arr (_type_): _description_
    """
    for data in data_arr:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", data)
    conn.commit()


def compress_data():
    """_summary_ compress data
    """
    files = get_file_names_in_folder(DATA_PATH)
    for file in files:
        print(f"Read file: {file}")
        bin_arr = binary_file_read(DATA_PATH + "/" + file)
        segmented_arr = get_segmented_sequence(bin_arr, SEGMENT_SIZE)
        hashes = []
        for seg in segmented_arr:
            hashes.append(get_hash_for_segment(seg, HASH_FUNCTION_IN_USE))
        save_compresed_data_file(FOLDER_WITH_COMPRESED_DATA + "/" + file, hashes)


def decompress_data():
    for file in get_file_names_in_folder(FOLDER_WITH_COMPRESED_DATA):
        read_compresed_data_file(FOLDER_WITH_COMPRESED_DATA + "/" + file[0:-4])
        # binary_file_write()




if __name__ == "__main__":

    compress_data()

    # decompress_data()

    # decompress data
    # binary_file_write(FOLDER_WITH_DECOMPRESED_DATA + "/" + file, hashes)




# conn = sl.connect('my-test.db')
# cur = conn.cursor()

# cur.execute("""CREATE TABLE IF NOT EXISTS hash_table(
#    hashId INT PRIMARY KEY,
#    hash TEXT,
#    hashValue TEXT,
#    repCount INT);
# """)



# conn.commit()




# cur.execute("""INSERT INTO users(userid, fname, lname, gender) 
#    VALUES('00001', 'Alex', 'Smith', 'male');""")
# conn.commit()

# cur.execute("SELECT * FROM users;")
# one_result = cur.fetchone()
# print(one_result)