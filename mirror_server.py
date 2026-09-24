import random

def generate_failure_interval(mtbf):
    return max(1, round(random.expovariate(1 / mtbf)))

def simulate_run(server_mtbf, run_number):
    servers = []

    for i, mtbf in enumerate(server_mtbf):
        server = {
            "id": f"S{i:02}",
            "mtbf": mtbf,
            "status": "UP",
            "next_failure": 0,
            "recovery_time": None,
            "uptime": 0,
            "downtime": 0,
            "failures": 0
        }

        server["next_failure"] = generate_failure_interval(mtbf)

        servers.append(server)

    current_time = 0

    print(f"\nSimulation Run {run_number}")

    # Print initial state
    print(f"{0:3}", end=" | ")

    for server in servers:
        print(f"{server['status']:4}", end=" | ")

    print()

    while True:
        event_times = []

        for server in servers:
            if server["status"] == "UP":
                event_times.append(server["next_failure"])
            else:
                event_times.append(server["recovery_time"])

        previous_time = current_time
        current_time = min(event_times)

        elapsed_time = current_time - previous_time

        # Add uptime/downtime for the elapsed interval
        for server in servers:
            if server["status"] == "UP":
                server["uptime"] += elapsed_time
            else:
                server["downtime"] += elapsed_time

        # Recover servers whose restoration completes now
        for server in servers:
            if (
                server["status"] == "DOWN"
                and server["recovery_time"] == current_time
            ):
                server["status"] = "UP"
                server["recovery_time"] = None

                server["next_failure"] = (
                    current_time
                    + generate_failure_interval(server["mtbf"])
                )

        # Fail servers whose failure occurs now
        for server in servers:
            if (
                server["status"] == "UP"
                and server["next_failure"] == current_time
            ):
                server["status"] = "DOWN"
                server["next_failure"] = None
                server["recovery_time"] = current_time + 2
                server["failures"] += 1

        # Print state after this event
        print(f"{current_time:3}", end=" | ")

        for server in servers:
            print(f"{server['status']:4}", end=" | ")

        print()

        # End simulation if every server is down
        if all(server["status"] == "DOWN" for server in servers):
            print(
                f"\nTotal system failure occurred at hour {current_time}."
            )
            break

    return current_time, servers

def main():
    print("Mirror Server Simulation")

    num_servers = int(input("Enter number of servers (2-5): "))

    while num_servers < 2 or num_servers > 5:
        print("Please enter a number between 2 and 5.")
        num_servers = int(input("Enter number of servers (2-5): "))

    print("\nServer Configuration")

    server_mtbf = []

    for i in range(num_servers):
        mtbf = random.randint(10, 20)
        server_mtbf.append(mtbf)

    for i, mtbf in enumerate(server_mtbf):
        print(f"S{i:02} | {mtbf} |")

    for run_number in range(1, 6):
        simulate_run(server_mtbf, run_number)
        
if __name__ == "__main__":
    main()