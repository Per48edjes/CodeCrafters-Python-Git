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
            _, output = decomp_data.split(b"\x00", 1)

            print(b'output: ' + output)
            # sys.stdout.buffer.write(output)
        # we have the tree object now and need to parse the output to just get 
        # the file and folder names. the filename is prefaced by a space and succeeded by a null byte
        # can discard the sha
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
