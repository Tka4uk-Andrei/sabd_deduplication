from dataclasses import dataclass
import hashlib
from operator import truediv
from platform import node
from re import L
import sqlite3 as sl
import os
import sys
import time

HASH_FUNCTION_NONE = "None"
HASH_FUNCTION_MD5 = "MD5"

DATA_PATH = "data"
SEGMENT_SIZE = 10
ZIPPED_DATA_CELL_SIZE = 8
HASH_FUNCTION_IN_USE = HASH_FUNCTION_NONE
FOLDER_WITH_COMPRESED_DATA = "compressed_data"
FOLDER_WITH_DECOMPRESED_DATA = "decompressed_data"
BD_FILE_NAME = "hashes.db"


@dataclass
class DataNode():
    id : int
    hash : str
    hash_val : str
    rep_count : int


# def data_node_adapter(vehicle):
#     return f"{vehicle.id};{vehicle.hash};{vehicle.hash_val};{vehicle.rep_count}".encode("utf-8")

# sl.register_adapter(DataNode, data_node_adapter)


def get_file_names_in_folder(relative_folder_path : str):
    return os.listdir(relative_folder_path)


def get_hash_for_segment(byte_slice : bytes, hash_function : str) -> bytes:
    if (hash_function == HASH_FUNCTION_NONE):
        return byte_slice.hex()
    elif (hash_function == HASH_FUNCTION_MD5):
        return hashlib.md5().hexdigest()
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


def save_compresed_data_file(relative_file_path : str, block_ids : list, 
                             zipped_data_cell_size : int):
    with open(relative_file_path + ".bin", "wb") as f:
        for elem in block_ids:
            f.write(elem.to_bytes(zipped_data_cell_size, byteorder='big'))


def read_compresed_data_file(relative_file_path : str,
                             id_dict, zipped_data_cell_size : int):
    hash_arr = []
    with open(relative_file_path + ".bin", "rb") as f:
        file_bytes = f.read()
        file_bytes_len = len(file_bytes)
        for i in range(0, file_bytes_len, zipped_data_cell_size):
            hash_id = int.from_bytes(file_bytes[i:i+zipped_data_cell_size], byteorder='big')
            hash_arr.append(bytes.fromhex(id_dict[hash_id].hash_val))
    return hash_arr


def get_data_from_bd(cur):
    cur.execute("SELECT * FROM hash_table;")
    nodes = []
    for node in cur.fetchall():
        nodes.append(DataNode(node[0], node[1], node[2], node[3]))
    return nodes


def insert_hashes_into_bd(cur, conn, values):
    """_summary_

    Args:
        cur (_type_): _description_
        conn (_type_): _description_
        values (_type_): _description_
    """

    for val in values:
        cur.execute("INSERT INTO hash_table VALUES(?,?,?,?)",
                    (val.id, val.hash, val.hash_val, val.rep_count))
    conn.commit()


def update_hashes_in_bd(cur, conn, values):
    for val in values:
        cur.execute("Update hash_table set rep_count = ? where id = ?",
                    (val.rep_count, val.id))
    conn.commit()


def compress_data():
    """_summary_ compress data
    """

    # connect to bd
    conn = sl.connect(BD_FILE_NAME)
    cur = conn.cursor()

    # establish bd if not exist
    cur.execute("""CREATE TABLE IF NOT EXISTS hash_table(
        id INT PRIMARY KEY,
        hash TEXT,
        hash_val TEXT,
        rep_count INT
    );""")
    conn.commit()

    # work with files
    files = get_file_names_in_folder(DATA_PATH)
    prev_hash_dict_len = 0
    for file in files:
        start_ts = time.time()
        reused_nodes = 0
        dublicated_nodes = 0
        # get data from bd
        bd_hashes = {}
        hash_dict = {}
        for data in get_data_from_bd(cur):
            bd_hashes[data.hash] = data
        hash_dict_len = len(bd_hashes)
        # compress file
        print(f"Compress file: {file}")
        bin_arr = binary_file_read(DATA_PATH + "/" + file)
        segmented_arr = get_segmented_sequence(bin_arr, SEGMENT_SIZE)
        hashed_data_seq = []
        for seg in segmented_arr:
            hash = get_hash_for_segment(seg, HASH_FUNCTION_IN_USE)
            if (bd_hashes.get(hash) != None):
                bd_hashes[hash].rep_count += 1
                hashed_data_seq.append(bd_hashes[hash].id)
                reused_nodes += 1
                dublicated_nodes += 1
            elif (hash_dict.get(hash) == None):
                data_note = DataNode(hash_dict_len, hash, seg.hex(), 1)
                hash_dict[hash] = data_note
                hash_dict_len += 1
                hashed_data_seq.append(hash_dict[hash].id)
            else :
                hash_dict[hash].rep_count += 1
                hashed_data_seq.append(hash_dict[hash].id)
                dublicated_nodes += 1
        if ((1 << (ZIPPED_DATA_CELL_SIZE * 8)) - 1 < hash_dict_len):
            print(f"ZIPPED_DATA_CELL_SIZE could hold only " \
                  f"{(1 << (ZIPPED_DATA_CELL_SIZE * 8)) - 1} items current amount " \
                  f"of unique_hashes is {hash_dict_len}")
            exit(-1)
        save_compresed_data_file(FOLDER_WITH_COMPRESED_DATA + "/" + file, hashed_data_seq,
                                 ZIPPED_DATA_CELL_SIZE)

        # save data to db
        insert_hashes_into_bd(cur, conn, hash_dict.values())
        update_hashes_in_bd(cur, conn, bd_hashes.values())

        end_ts = time.time()
        print(f"Nodes increased by   : {hash_dict_len - prev_hash_dict_len}")
        print(f"Hashes from prev try : {reused_nodes}")
        print(f"Dublicated hashes    : {dublicated_nodes}")
        print(f"Process time         : {end_ts - start_ts}")
        prev_hash_dict_len = hash_dict_len



    conn.close()


# def decompress_data():
def decompress_data():

    # connect to bd
    conn = sl.connect(BD_FILE_NAME)
    cur = conn.cursor()

    # Check that table exists
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='hash_table';")

    if cur.fetchone()[0] != 1 : {
        exit(-1)
    }

    # get data from bd
    id_dict = {}
    for data in get_data_from_bd(cur):
        id_dict[data.id] = data

    for file in get_file_names_in_folder(FOLDER_WITH_COMPRESED_DATA):
        start_ts = time.time()
        print(f"Decompress file: {file}")
        data_arr = read_compresed_data_file(FOLDER_WITH_COMPRESED_DATA + "/" + file[0:-4], 
                                            id_dict, ZIPPED_DATA_CELL_SIZE)
        binary_file_write(FOLDER_WITH_DECOMPRESED_DATA + "/" + file[0:-4], data_arr)
        end_ts = time.time()
        print(f"Process time         : {end_ts - start_ts}")


if __name__ == "__main__":

    c_flag = 1
    d_flag = 1

    if len(sys.argv) == 1:
        if sys.argv[0] == "-c":
            d_flag = 0
        elif sys.argv[0] == "-d":
            c_flag = 0

    if c_flag == 1:
        compress_data()

    if d_flag == 1:
        decompress_data()
