from mpi4py import MPI
import os

# Initialize MPI communication
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the file to transfer and the chunk size
filename = "example.txt"
chunk_size = 1024  # Chunk size in bytes

if rank == 0:
    # Master process: read file and distribute chunks
    try:
        with open(filename, 'rb') as file:
            file_content = file.read()
        file_size = len(file_content)
        print(f"File size: {file_size} bytes")

        # Distribute chunks to worker processes
        for i in range(1, size):
            start_index = (i - 1) * chunk_size
            end_index = min(start_index + chunk_size, file_size)
            comm.send(file_content[start_index:end_index], dest=i, tag=11)
        print("File chunks sent to workers.")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        for i in range(1, size):
            comm.send(None, dest=i, tag=11)

else:
    # Worker processes: receive chunks and save to file
    chunk = comm.recv(source=0, tag=11)
    if chunk is not None:
        with open(f"received_chunk_{rank}.txt", 'wb') as file:
            file.write(chunk)
        print(f"Process {rank} received and saved chunk.")
    else:
        print(f"Process {rank} received no data.")

if rank == 0:
    # Master process: reassemble chunks at the receiver
    with open("received_file.txt", 'wb') as output_file:
        for i in range(1, size):
            try:
                with open(f"received_chunk_{i}.txt", 'rb') as input_file:
                    output_file.write(input_file.read())
            except FileNotFoundError:
                print(f"Error: Chunk from process {i} not found.")
    print("File reassembled successfully.")
