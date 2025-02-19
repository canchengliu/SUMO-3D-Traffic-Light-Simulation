import traci
import subprocess
import time

def run_simulation():
    # Path to the SUMO configuration file
    sumo_config_file = 'map.sumocfg'

    # Start SUMO in GUI mode with the configuration file
    sumo_binary = "sumo-gui"

    # Launch SUMO-GUI with TraCI port 4001
    sumo_cmd = [sumo_binary, "-c", sumo_config_file, "--remote-port", "4001", "--step-length", "0.02"]
    process = subprocess.Popen(sumo_cmd)

    try:
        # Wait for SUMO to initialize
        time.sleep(2)  
        main(process)
    finally:
        process.terminate()

def main(process):
    traci.init(port=4001)
    step = 0
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            if step % 10 == 0:
                tl_ids = traci.trafficlight.getIDList()
                print(f"\nStep {step}: Traffic Light Phases")
                for tl_id in tl_ids:
                    phase_idx = traci.trafficlight.getPhase(tl_id)
                    state = traci.trafficlight.getRedYellowGreenState(tl_id)
                    print(f"  {tl_id}: Phase {phase_idx} - State {state}")
            step += 1
    finally:
        traci.close()
        process.kill()

if __name__ == "__main__":
    run_simulation()


# sumo-gui -c map.sumocfg --start --remote-port 4001 --step-length 0.02