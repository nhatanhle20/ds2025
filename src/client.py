from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def send_command(action, key=None, value=None):
    command = {
        "action": action,
        "key": key,
        "value": value,
        "client_rank": rank,
    }
    comm.send(command, dest=0, tag=0)
    response = comm.recv(source=0)
    return response

if __name__ == "__main__":
    while True:
        user_input = input("Enter command (e.g., SET key value): ").strip().split()
        if not user_input:
            continue
        action = user_input[0].upper()
        if action == "SET" and len(user_input) == 3:
            key, value = user_input[1], user_input[2]
            print(send_command(action="SET", key=key, value=value))
        elif action == "GET" and len(user_input) == 2:
            key = user_input[1]
            print(send_command(action="GET", key=key))
        elif action == "DELETE" and len(user_input) == 2:
            key = user_input[1]
            print(send_command(action="DELETE", key=key))
        elif action == "EXIT":
            break
        else:
            print("Invalid command.")