from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    raise Exception("Client cannot run on rank 0 (Primary Server)")

# Function to send commands
def send_command(action, key=None, value=None):
    command = {
        "action": action,
        "key": key,
        "value": value,
        "client_rank": rank,
    }
    comm.send(command, dest=0, tag=0)  # Send to Primary Server
    response = comm.recv(source=0)  # Receive response
    return response

# Client interaction
if __name__ == "__main__":
    print("[Client] Connected to the server")

    while True:
        print("\nCommands: SET key value, GET key, DELETE key, EXIT")
        user_input = input("Enter command: ").strip().split()
        if not user_input:
            continue

        action = user_input[0].upper()
        if action == "EXIT":
            print("Exiting client.")
            break
        elif action == "SET" and len(user_input) == 3:
            key, value = user_input[1], user_input[2]
            response = send_command(action="SET", key=key, value=value)
            print(f"Response: {response}")
        elif action == "GET" and len(user_input) == 2:
            key = user_input[1]
            response = send_command(action="GET", key=key)
            print(f"Response: {response}")
        elif action == "DELETE" and len(user_input) == 2:
            key = user_input[1]
            response = send_command(action="DELETE", key=key)
            print(f"Response: {response}")
        else:
            print("Invalid command. Try again.")
