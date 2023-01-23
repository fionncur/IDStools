def read_ids(scenario_file_path):

    import os, imas, yaml

    testmode = 0
    # Initial values of time slice and beam index
    time_slice = 35.0
    beam_index = 6
    # Read scenario.yaml used for the simulation to know where to find
    # the IMAS output datafile
    scenario_file = open(scenario_file_path, "r")
    config = yaml.load(scenario_file, Loader=yaml.CLoader)
    scenario_file.close()

    # Find output datafile from the configuration parameters
    output_user_or_path = ""
    if config["output_user_or_path"] == "default":
        output_user_or_path = os.getenv("USER")
        config["output_user_or_path"] = os.getenv("USER")
    else:
        output_user_or_path = config["output_user_or_path"]

    # Read the equilibrium and core_profiles IDSs from the input datafile
    input = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["input_database"],
        config["shot"],
        config["run_in"],
        config["input_user_or_path"],
    )
    input.open()
    if testmode == 1:
        time_slice = 100.0
        equilibrium = input.get_slice("equilibrium", time_slice, 2)
        core_profiles = input.get_slice("core_profiles", 100.0, 2)
    else:
        equilibrium = input.get("equilibrium")
        core_profiles = input.get("core_profiles")

    input.close()

    # Read the waves IDS from the output datafile
    output = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["output_database"],
        config["shot"],
        config["run_out"],
        config["output_user_or_path"],
    )
    output.open()
    if testmode == 1:
        waves = output.get_slice("waves", time_slice, 2)
    else:
        waves = output.get("waves")
    output.close()

    return equilibrium, core_profiles, waves
