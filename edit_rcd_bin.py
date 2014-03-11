#!/usr/bin/env python
#
# Author: Justin Grant
# Original Author: Farhan Ahmad
# Description: This patches the iTunes launch commands in the rcd binary to 
#        open Spotify instead. This program is expected to be executed by the
#         provided Patch.command driver.
#
# Note: The closing and reopening of the mmap instead of using resize()
# is do to a bug in python on unix derivates leading resize() to fail. 
# (http://mail.python.org/pipermail/python-bugs-list/2003-May/017446.html)
#
import mmap
import sys
import os.path

def deleteFromMmap(f, mmap_in, position, size):
    starting_offset = position+size
    map_size = len(mmap_in)
    block_size = map_size-starting_offset
    new_map_size = map_size-size

    mmap_in.move(position,starting_offset,block_size)
    mmap_in.flush()
    mmap_in.close()
    f.truncate(new_map_size)

    # return the new mmap due to python bug
    return mmap.mmap(f.fileno(),0)

def insertIntoMmap(f, mmap_in, offset, data):
    data_length = len(data)
    mmap_in_size = len(mmap_in)
    new_map_size = mmap_in_size + data_length
    destination_offset = offset+data_length
    block_size = mmap_in_size-offset
    end_data_block = offset + data_length

    # flush the mmap due to python bug and to recreate at correct size
    mmap_in.flush()
    mmap_in.close()

    # write dummy data to the end of the file (just to extend the size)
    f.seek(os.SEEK_END)
    f.write(data)
    f.seek(offset)

    # create a new map, and shift the block
    mmap_in = mmap.mmap(f.fileno(), 0)
    new_mmap_in_size = len(mmap_in)
    mmap_in.move(destination_offset,offset,block_size)
    
    # insert the new data
    mmap_in[offset:end_data_block] = data

    return mmap.mmap(f.fileno(),0)

def findAndReplace(string_to_find, string_to_use, fname_backup):
    instances = []
    start = 0
    if not os.path.isfile(fname_backup):
        print "'%s' is not a valid file." % rcd_filepath
        sys.exit(2)
    with open(rcd_filepath, "a+b") as f:
        f.seek(os.SEEK_SET)
        map = mmap.mmap(f.fileno(), 0)
        while True:
            found_at = map.find(string_to_find, start)
            if found_at == -1:
                break
            map = deleteFromMmap(f, map, found_at, len(string_to_find))
            map = insertIntoMmap(f, map, found_at, string_to_use)
            start = found_at
        map.flush()
        map.close()


# Check args
if len(sys.argv) != 2:
    print "%s rcd_filepath" % sys.argv[0]
    sys.exit(1)

rcd_filepath = sys.argv[1]

# Fix binary
string_to_find = 'tell application id "com.apple.iTunes" to launch'
string_to_use = 'tell application id "com.spotify.client" to launch'
findAndReplace(string_to_find,string_to_use,rcd_filepath)

sys.exit(0)   # Return successful status.
