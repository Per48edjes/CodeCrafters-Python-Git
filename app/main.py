import sys
import os
import zlib


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
            _, output = decomp_data.split(b'\x00')
            sys.stdout.buffer.write(output)

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
