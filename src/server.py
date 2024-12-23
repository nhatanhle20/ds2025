from mpi4py import MPI
import json
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Simulating a small cluster
PRIMARY_SERVER = 0
BACKUP_SERVERS = list(range(1, size))

# Key-Value store
kv_store = {}

# Periodic checkpointing to a file
def save_checkpoint():
    with open(f"checkpoint_{rank}.json", "w") as f:
        json.dump(kv_store, f)

def load_checkpoint():
    try:
        with open(f"checkpoint_{rank}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Replicate to backup servers
def replicate_to_backups():
    for backup in BACKUP_SERVERS:
        comm.send(kv_store, dest=backup, tag=1)

if rank == PRIMARY_SERVER:
    print(f"[Server {rank}] Running as Primary Server")
    kv_store = load_checkpoint()

    while True:
        # Receive a command from any client
        command = comm.recv(source=MPI.ANY_SOURCE, tag=0)
        action = command["action"]
        key = command.get("key")
        value = command.get("value")

        if action == "SET":
            kv_store[key] = value
            replicate_to_backups()
            save_checkpoint()
            comm.send({"status": "OK"}, dest=command["client_rank"])

        elif action == "GET":
            result = kv_store.get(key, "Key not found")
            comm.send({"status": "OK", "value": result}, dest=command["client_rank"])

        elif action == "DELETE":
            if key in kv_store:
                del kv_store[key]
                replicate_to_backups()
                save_checkpoint()
                comm.send({"status": "OK"}, dest=command["client_rank"])
            else:
                comm.send({"status": "Key not found"}, dest=command["client_rank"])
else:
    print(f"[Server {rank}] Running as Backup Server")
    while True:
        # Receive replicated data
        kv_store = comm.recv(source=PRIMARY_SERVER, tag=1)
        print(f"[Backup {rank}] Updated store: {kv_store}")
