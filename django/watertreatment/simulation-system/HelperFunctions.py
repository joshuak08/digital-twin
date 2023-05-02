import FilterSnapshotter
import FilterSystem


def basic_simulation(average_flow, average_tss, sim_length, testing):

    # sim_length is given in seconds, each round is a second, so conversion is direct
    rounds = sim_length

    # make and run the simulation, defaults to each round being a second, and snapshotting every round
    snapshotter = FilterSnapshotter.FilterSnapshotter(testing)
    system = FilterSystem.FilterSystem(
        1, average_flow, average_tss, snapshotter, rounds, 5, True)
    system.simulate()

    # write results to a database
    table_name = snapshotter.to_database()

    # return the name of the table to be used by the server
    return table_name


def initial_particulate_simulation(average_flow, average_tss, sim_length, initial_particulates, testing):

    # sim_length is given in seconds, each round is a second, so conversion is direct
    rounds = sim_length

    # make the simulation, using basic 1 snapshot per 5 rounds, 1 second rounds
    snapshotter = FilterSnapshotter.FilterSnapshotter(testing)
    system = FilterSystem.FilterSystem(
        1, average_flow, average_tss, snapshotter, rounds, 5, True)

    # set initial values to those specified in parameters
    filter = 0
    for i in system.components:
        if i.type == "Filter":
            i.particulate_mass = initial_particulates[filter]
            filter += 1

    # run the simulation
    system.simulate()

    # write results to a database
    table_name = snapshotter.to_database()

    # return the name of the table to be used by the server
    return table_name
