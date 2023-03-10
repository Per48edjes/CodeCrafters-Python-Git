import os
import sys
import zlib
from hashlib import sha1


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")

    elif command == "cat-file":
        # need to check valid flag
        if sys.argv[2] == "-p":
            blob_sha = sys.argv[3]
            dir_sha, blob_sha = blob_sha[:2], blob_sha[2:]

        # get object from .git/objects
        # print(os.listdir(".git/objects"))
        filename = os.path.join(f".git/objects/{dir_sha}", blob_sha)
        with open(filename, "rb") as b:
            data = b.read()
            decomp_data = zlib.decompress(data)
            _, output = decomp_data.split(b"\x00")
            sys.stdout.buffer.write(output)

    elif command == "hash-object":
        # need to check valid flag
        if sys.argv[2] == "-w":
            filename = sys.argv[3]

            # TODO: Figure out whether binary or not (and treat accordingly)?

            # Hashing file contents
            with open(filename, "rb") as f:
                # "blob" + space + number of bytes + nullbyte + contents
                contents = f.read()
                contents = b"".join(
                    [
                        b"blob",
                        b" ",
                        bytes(f"{len(contents)}", encoding="utf-8"),
                        b"\x00",
                        contents,
                    ]
                )
                sha = sha1(contents).hexdigest().strip()

            # Create directory and object
            dir_sha, blob_sha = sha[:2], sha[2:]
            # Q: Would we need to check whether directory exists or not first?
            if not (os.path.exists(f".git/objects/{dir_sha}") and os.path.isdir(f".git/objects/{dir_sha}")):
                os.mkdir(f".git/objects/{dir_sha}")
            
            filename = os.path.join(f".git/objects/{dir_sha}", blob_sha)


            # TODO: Compress(?) and write the file
            with open(filename, "wb") as f:
                f.write(zlib.compress(contents))

            print(sha)

    elif command == "ls-tree":
        """
        format of tree object:
        tree [content size]\0[Entries having references to other trees and blobs]
        
        format each entry with references to other trees and blobs:
        [mode] [file/folder name]\0[SHA-1 of referencing blob or tree]
        """

        # need to check valid flag
        if sys.argv[2] == "--name-only":
            full_sha = sys.argv[3]
            dir_sha, tree_sha = full_sha[:2], full_sha[2:]

        filename = os.path.join(f".git/objects/{dir_sha}", tree_sha)

        with open(filename, "rb") as b:
            data = b.read()
            decomp_data = zlib.decompress(data)
            _, treedata = decomp_data.split(b"\x00", 1)

            res = []
            while treedata:
                # we don't need the mode
                _, treedata = treedata.split(b' ', 1)
                entry, treedata = treedata.split(b'\x00', 1)
                res.append(entry)
                # the next 20 bytes are the hash
                treedata = treedata[20:]

            sys.stdout.buffer.write(b"\n".join(res)+b"\n")



    elif command == "write-tree":
        
        # list out the contents of the repo root(?)


        # 1. os.scandir() object containing metadata + strings of the directory's entries
        # as objects, that have a "name" field -- extract these names

        # write these contents into a tree object (in the format prescribed
        # above)

        # Open Hypothesis: do we need to recurse into each tree to contruct the
        # tree object which then gets hashed / provides the hash enclosed in the
        # parent tree object?
        # 2. 

        # test by using our ls-tree function




    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
