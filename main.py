import traci
import sumolib
import time

# Path to the SUMO configuration file
sumo_config_file = 'map.sumocfg'

# Start SUMO in GUI mode with the configuration file
sumo_binary = "sumo-gui"  # Use "sumo" for non-GUI mode, "sumo-gui" for GUI mode

def print_traffic_light_phases():
    # Get the list of all traffic lights in the network
    traffic_lights = traci.trafficlight.getIDList()
    
    for light_id in traffic_lights:
        # Get the current phase of the traffic light
        phase = traci.trafficlight.getPhase(light_id)
        print(f"Traffic Light {light_id}: Current Phase = {phase}")

# sumo-gui -c map.sumocfg --start --remote-port 4001 --step-length 0.02
def run_simulation():
    # Start the SUMO simulation with the provided configuration file
    traci.start([sumo_binary, "-c", sumo_config_file, "--remote-port", "4001", "--step-length", "0.02"])
    
    # Start the simulation loop
    step = 0
    while step < traci.simulation.getMinExpectedNumber():
        traci.simulationStep()  # Perform a single simulation step
        time.sleep(0.5)

        # Print the traffic light phases every 10 steps
        if step % 10 == 0:
            print(f"Step {step}:")
            print_traffic_light_phases()

        step += 1
    
    # Close the simulation after running the loop
    traci.close()

if __name__ == "__main__":
    run_simulation()


# sumo-gui -c map.sumocfg --start --remote-port 4001 --step-length 0.02