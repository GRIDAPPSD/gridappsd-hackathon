import json
from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation


run_config_9500 = """
{
    "power_system_config":{
        "GeographicalRegion_name":"_73C512BD-7249-4F50-50DA-D93849B89C43",
        "SubGeographicalRegion_name":"_A1170111-942A-6ABD-D325-C64886DC4D7D",
        "Line_name":"_AAE94E4A-2465-6F5E-37B1-3E72183A4E44"},
    "application_config":{"applications":[]},
    "simulation_config":{
        "start_time":"1373814570",
        "duration":"1200",
        "simulator":"GridLAB-D",
        "timestep_frequency":"1000",
        "timestep_increment":"1000",
        "run_realtime":true,
        "simulation_name":"test9500new",
        "power_flow_solver_method":"NR",
        "model_creation_config":{
            "load_scaling_factor":"1",
            "schedule_name":"ieeezipload",
            "z_fraction":"0","i_fraction":"1","p_fraction":"0","randomize_zipload_fractions":false,"use_houses":false}},
    "test_config":{
        "events":[{
            "message":{
                "forward_differences":[{
                    "object":"_792127B0-9B3E-43EC-9D23-FD46F5A2F20D",
                    "attribute":"Switch.open","value":1}],
                "reverse_differences":[{"object":"_792127B0-9B3E-43EC-9D23-FD46F5A2F20D",
                                        "attribute":"Switch.open",
                                        "value":0
                                       }]
            },
            "event_type":"ScheduledCommandEvent",
            "occuredDateTime": 1373814600,
            "stopDateTime": 1373817600}],
        
        "appId":""
    },
    "service_configs":[]
}
"""
gapps = GridAPPSD()

simulation = Simulation(gapps, run_config_9500)
simulation.start_simulation()
