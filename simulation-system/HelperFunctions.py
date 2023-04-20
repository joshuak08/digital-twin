import FilterSnapshotter
import FilterSystem


def basic_simulation(average_flow, average_tss, sim_length):

    # sim_length is given in seconds, each round is a second, so conversion is direct
    rounds = sim_length

    # make and run the simulation, defaults to each round being a second, and snapshotting every round
    snapshotter = FilterSnapshotter.FilterSnapshotter()
    system = FilterSystem.FilterSystem(1, average_flow, average_tss, snapshotter, rounds, 1, True)
    system.simulate()

    # write results to a database
    table_name = snapshotter.to_database()

    # return the name of the table to be used by the server
    return table_name  