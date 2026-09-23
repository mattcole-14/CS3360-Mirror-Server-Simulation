import random


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
            "recovery_time": None
        }

        server["next_failure"] = max(
            1,
            round(random.expovariate(1 / server["mtbf"]))
        )

        servers.append(server)

    for server in servers:
        print(
            f"{server['id']} | MTBF: {server['mtbf']} | "
            f"First failure: {server['next_failure']}"
        )

    current_time = 0

    next_event_time = min(server["next_failure"] for server in servers)
    current_time = next_event_time

    for server in servers:
        if server["next_failure"] == current_time:
            server["status"] = "DOWN"
            server["recovery_time"] = current_time + 2

    print(f"\nFirst event occurs at hour {current_time}")

    for server in servers:
        print(f"{server['id']} | {server['status']}")


if __name__ == "__main__":
    main()