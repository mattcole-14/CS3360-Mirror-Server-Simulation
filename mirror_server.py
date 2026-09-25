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

    #table header
    header = "    | " + " | ".join(
        f"{server['id']:4}" for server in servers
    ) + " |"

    print(header)
    print("-" * len(header))

    #initial state at 0
    print(
        f"{0:3} | "
        + " | ".join(
            f"{server['status']:4}" for server in servers
        )
        + " |"
    )

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

        # uptime/downtime
        for server in servers:
            if server["status"] == "UP":
                server["uptime"] += elapsed_time
            else:
                server["downtime"] += elapsed_time

        # recover servers 
        for server in servers:
            if (
                server["status"] == "DOWN"
                and server["recovery_time"] == current_time
            ):
                server["status"] = "UP"
                server["recovery_time"] = None

                server["next_failure"] = (
                    current_time
                    + generate_failure_interval(server["mtbf"]))

        # fail servers
        for server in servers:
            if (
                server["status"] == "UP"
                and server["next_failure"] == current_time
            ):
                server["status"] = "DOWN"
                server["next_failure"] = None
                server["recovery_time"] = current_time + 2
                server["failures"] += 1

        # print state change
        print(
            f"{current_time:3} | "
            + " | ".join(
                f"{server['status']:4}" for server in servers
            )
            + " |")

        # end sim when all servers are down
        if all(server["status"] == "DOWN" for server in servers):
            break

    return current_time, servers


def main():
    num_servers = int(input("Enter number of servers (2-5): "))

    while num_servers < 2 or num_servers > 5:
        print("Please enter a number between 2 and 5.")
        num_servers = int(input("Enter number of servers (2-5): "))

    server_mtbf = []

    for i in range(num_servers):
        mtbf = random.randint(10, 20)
        server_mtbf.append(mtbf)

    # print configuration
    print("\nServer Configuration")
    
    for i, mtbf in enumerate(server_mtbf):
        print(f"S{i:02} | {mtbf} |")

    # run same configuration 5 times
    run_results = []
    system_failure_times = []

    for run_number in range(1, 6):
        failure_time, servers = simulate_run(
            server_mtbf,
            run_number
        )

        system_failure_times.append(failure_time)
        run_results.append(servers)

    # final stats
    print("\nFinal Statistics")
    print(
        "Server | Avg Uptime | Avg Downtime | Availability | MTBF"
    )
    print(
        "--------------------------------------------------------"
    )

    for i in range(num_servers):
        total_uptime = 0
        total_downtime = 0
        total_failures = 0

        for run in run_results:
            total_uptime += run[i]["uptime"]
            total_downtime += run[i]["downtime"]
            total_failures += run[i]["failures"]

        avg_uptime = total_uptime / 5
        avg_downtime = total_downtime / 5

        total_time = total_uptime + total_downtime

        if total_time > 0:
            availability = total_uptime / total_time * 100
        else:
            availability = 0

        if total_failures > 0:
            experimental_mtbf = total_uptime / total_failures
        else:
            experimental_mtbf = 0

        print(
            f"S{i:02}    | "
            f"{avg_uptime:10.2f} | "
            f"{avg_downtime:12.2f} | "
            f"{availability:11.2f}% | "
            f"{experimental_mtbf:.2f}"
        )

    average_failure_time = sum(system_failure_times) / 5

    print(
        f"\nAverage time until total system failure: "
        f"{average_failure_time:.2f} hours"
    )


if __name__ == "__main__":
    main()