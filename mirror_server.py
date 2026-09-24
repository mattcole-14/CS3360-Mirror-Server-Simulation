import random

def generate_failure_interval(mtbf):
    return max(1, round(random.expovariate(1 / mtbf)))

def main():
    print("Mirror Server Simulation")

    num_servers = int(input("Enter number of servers (2-5): "))

    while num_servers < 2 or num_servers > 5:
        print("Please enter a number between 2 and 5.")
        num_servers = int(input("Enter number of servers (2-5): "))

    print("\nServer Configuration")

    servers = []

    for i in range(num_servers):
        server = {
            "id": f"S{i:02}",
            "mtbf": random.randint(10, 20),
            "status": "UP",
            "next_failure": 0,
            "recovery_time": None,
            "uptime": 0,
            "downtime": 0,
            "failures": 0
        }

        server["next_failure"] = generate_failure_interval(server["mtbf"])

        servers.append(server)

    for server in servers:
        print(
            f"{server['id']} | MTBF: {server['mtbf']} | "
            f"First failure: {server['next_failure']}"
        )

    current_time = 0

    print("\nSimulation Run")

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

        for server in servers:
            if server["status"] == "UP":
                server["uptime"] += elapsed_time
            else:
                server["downtime"] += elapsed_time

        # Recover servers whose restoration finishes now
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

        # Print the state after this event
        print(f"{current_time:3}", end=" | ")

        for server in servers:
            print(f"{server['status']:4}", end=" | ")

        print()

        # Stop if every server is down
        if all(server["status"] == "DOWN" for server in servers):
            print(
                f"\nTotal system failure occurred at hour {current_time}."
            )
            break

    print("\nStatistics")

    for server in servers:
        total_time = server["uptime"] + server["downtime"]

        if total_time > 0:
            availability = server["uptime"] / total_time * 100
        else:
            availability = 0

        if server["failures"] > 0:
            experimental_mtbf = server["uptime"] / server["failures"]
        else:
            experimental_mtbf = 0

        print(
            f"{server['id']} | "
            f"Uptime: {server['uptime']} | "
            f"Downtime: {server['downtime']} | "
            f"Availability: {availability:.2f}% | "
            f"MTBF: {experimental_mtbf:.2f}"
        )


if __name__ == "__main__":
    main()