from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation


models = dict(ieee123=u'_C1C3E687-6FFD-C753-582B-632A27E28507',
              ieee8500=u'_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3',
              ieee13nodeckt=u'_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62')
run_config_123 = {
    "power_system_config": {
        "GeographicalRegion_name": "_73C512BD-7249-4F50-50DA-D93849B89C43",
        "SubGeographicalRegion_name": "_1CD7D2EE-3C91-3248-5662-A43EFEFAC224",
        "Line_name": "_C1C3E687-6FFD-C753-582B-632A27E28507"
    },
    "application_config": {
        "applications": []
    },
    "simulation_config": {
        "simulation_id": "12345678",
        "simulation_name": "ieee123demo",
        "start_time": "1562453292",
        "duration": "300",
        "simulator": "GridLAB-D",
        "timestep_frequency": "1000",
        "timestep_increment": "1000",
        "run_realtime": True,
        "simulation_name": "ieee123",
        "power_flow_solver_method": "NR",
        
    },
    "test_config": {
        "events": [],
        "appId": "_C1C3E687-6FFD-C753-582B-632A27E28507"
    }
}

def start_simulation()
    gapps = GridAPPSD()
    request = {"configurationType":"CIM Dictionary","parameters":{"model_id":"_C1C3E687-6FFD-C753-582B-632A27E28507"}}
    simulation = Simulation(gapps, run_config_123)
    simulation.start_simulation()
    # print(simulation.simulation_id)
    return simulation.simulation_id

start_simulation()