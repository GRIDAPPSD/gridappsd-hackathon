import json
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
        "start_time": "1570041113",
        "duration": "120",
        "simulator": "GridLAB-D",
        "timestep_frequency": "1000",
        "timestep_increment": "1000",
        "run_realtime": True,
        "simulation_name": "ieee123",
        "power_flow_solver_method": "NR",
        "model_creation_config": {
            "load_scaling_factor": "1",
            "schedule_name": "ieeezipload",
            "z_fraction": "0",
            "i_fraction": "1",
            "p_fraction": "0",
            "randomize_zipload_fractions": False,
            "use_houses": False
        }
    },
    "test_config": {
        "events": [],
        "appId": ""
    },
    "service_configs": [{
        "id": "gridappsd-sensor-simulator",
        "user_options": {
            "sensors-config": {
                "_99db0dc7-ccda-4ed5-a772-a7db362e9818": {
                    "nominal-value": 100,
                    "perunit-confidence-band": 0.02,
                    "aggregation-interval": 5,
                    "perunit-drop-rate": 0.01
                },
                "_ee65ee31-a900-4f98-bf57-e752be924c4d": {},
                "_f2673c22-654b-452a-8297-45dae11b1e14": {}
            },
            "random-seed": 0,
            "default-aggregation-interval": 30,
            "passthrough-if-not-specified": False,
            "default-perunit-confidence-band": 0.01,
            "default-perunit-drop-rate": 0.05
        }
    }]
}

gapps = GridAPPSD()
request = {"configurationType":"CIM Dictionary","parameters":{"model_id":"_C1C3E687-6FFD-C753-582B-632A27E28507"}}
simulation = Simulation(gapps, run_config_123)
simulation.start_simulation()
