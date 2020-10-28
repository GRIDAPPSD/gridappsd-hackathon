# -------------------------------------------------------------------------------
# Copyright (c) 2017, Battelle Memorial Institute All rights reserved.
# Battelle Memorial Institute (hereinafter Battelle) hereby grants permission to any person or entity
# lawfully obtaining a copy of this software and associated documentation files (hereinafter the
# Software) to redistribute and use the Software in source and binary forms, with or without modification.
# Such person or entity may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and may permit others to do so, subject to the following conditions:
# Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimers.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials provided with the distribution.
# Other than as used herein, neither the name Battelle Memorial Institute or Battelle may be used in any
# form whatsoever without the express written consent of Battelle.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# General disclaimer for use with OSS licenses
#
# This material was prepared as an account of work sponsored by an agency of the United States Government.
# Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any
# of their employees, nor any jurisdiction or organization that has cooperated in the development of these
# materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for
# the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process
# disclosed, or represents that its use would not infringe privately owned rights.
#
# Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer,
# or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United
# States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by BATTELLE for the
# UNITED STATES DEPARTMENT OF ENERGY under Contract DE-AC05-76RL01830
# -------------------------------------------------------------------------------
"""
Created on Jan 19, 2018

@author: Craig Allwardt, Shiva Poudel
"""

__version__ = "0.0.8"

import argparse
import json
import logging
import sys
import time

from gridappsd import GridAPPSD, DifferenceBuilder, utils, GOSS, topics
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic

DEFAULT_MESSAGE_PERIOD = 5

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#                     format="%(asctime)s - %(name)s;%(levelname)s|%(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S")
# Only log errors to the stomp logger.
logging.getLogger('stomp.py').setLevel(logging.ERROR)

_log = logging.getLogger(__name__)


class LearnPlatform(object):
    """ A simple class that handles publishing forward and reverse differences

    The object should be used as a callback from a GridAPPSD object so that the
    on_message function will get called each time a message from the simulator.  During
    the execution of on_meessage the `CapacitorToggler` object will publish a
    message to the simulation_input_topic with the forward and reverse difference specified.
    """

    def __init__(self, simulation_id, gridappsd_obj, ACline, obj_msr_loadsw):
        """ Create a ``CapacitorToggler`` object

        This object should be used as a subscription callback from a ``GridAPPSD``
        object.  This class will toggle the capacitors passed to the constructor
        off and on every five messages that are received on the ``fncs_output_topic``.

        Note
        ----
        This class does not subscribe only publishes.

        Parameters
        ----------
        simulation_id: str
            The simulation_id to use for publishing to a topic.
        gridappsd_obj: GridAPPSD
            An instatiated object that is connected to the gridappsd message bus
            usually this should be the same object which subscribes, but that
            isn't required.
        """
        self._gapps = gridappsd_obj
        self._simulation_id = simulation_id
        self._ACline = ACline
        self._obj_msr_loadsw = obj_msr_loadsw
        self._message_count = 0
        self._last_toggle_on = False
        self._open_diff = DifferenceBuilder(simulation_id)
        self._close_diff = DifferenceBuilder(simulation_id)
        self._publish_to_topic = simulation_input_topic(simulation_id)
        self._flag = 0
        self._start_time = 0
        _log.info("Building cappacitor list")
        

    def on_message(self, headers, message):
        """ Handle incoming messages on the simulation_output_topic for the simulation_id

        Parameters
        ----------
        headers: dict
            A dictionary of headers that could be used to determine topic of origin and
            other attributes.
        message: object
            A data structure following the protocol defined in the message structure
            of ``GridAPPSD``.  Most message payloads will be serialized dictionaries, but that is
            not a requirement.
        """

        if type(message) == str:
            message = json.loads(message)


        # Some demo for understanding object and measurement mrids. Print the status of several switches       
        timestamp = message["message"] ["timestamp"]
        meas_value = message['message']['measurements']
        
        # Find interested mrids. We are only interested in Pos of the switches
        ds = [d for d in self._obj_msr_loadsw if d['type'] == 'Pos']
        
        # Store the open switches
        Loadbreak = []
        for d1 in ds:                
            if d1['measid'] in meas_value:
                v = d1['measid']
                p = meas_value[v]
                if p['value'] == 0:
                    Loadbreak.append(d1['eqname'])

        print('.....................................................')
        print('The total number of open switches:', len(set(Loadbreak)))
        print(timestamp, set(Loadbreak))

        self._flag += 1
        # Open one of the switches
        if self._flag == 5:
            swmrid = '_BC63E102-37AD-4269-BB19-8351403B9B60'
            self._open_diff.add_difference(swmrid, "Switch.open", 1, 0)
            msg = self._open_diff.get_message()
            print(msg)
            self._gapps.send(self._publish_to_topic, json.dumps(msg))  

            swmrid = '_7262F9C3-2E8B-4069-AA13-BF4A655ACE35'
            self._open_diff.add_difference(swmrid, "Switch.open", 0, 1)
            msg = self._open_diff.get_message()
            print(msg)
            self._gapps.send(self._publish_to_topic, json.dumps(msg))              
        
        # python runsample.py 858290661 '{"power_system_config":  {"Line_name":"_C1C3E687-6FFD-C753-582B-632A27E28507"}}'
        

def get_meas_mrid(gapps, model_mrid, topic):
    
    message = {
        "modelId": model_mrid,
        "requestType": "QUERY_OBJECT_MEASUREMENTS",
        "resultFormat": "JSON",
        "objectType": "ACLineSegment"}
    obj_msr_ACline = gapps.get_response(topic, message, timeout=10)
    obj_msr_ACline = obj_msr_ACline['data']
    # Chose specific measurement mrid. Screen out those whose type is not PNV. For example,
    obj_msr_ACline = [k for k in obj_msr_ACline if k['type'] == 'PNV']

    message = {
        "modelId": model_mrid,
        "requestType": "QUERY_OBJECT_MEASUREMENTS",
        "resultFormat": "JSON",
        "objectType": "SynchronousMachine"}     
    obj_msr_sync = gapps.get_response(topic, message, timeout=5)   
    obj_msr_sync = obj_msr_sync['data']

    message = {
        "modelId": model_mrid,
        "requestType": "QUERY_OBJECT_MEASUREMENTS",
        "resultFormat": "JSON",
        "objectType": "PowerElectronicsConnection"}     
    obj_msr_inv = gapps.get_response(topic, message, timeout=5)   
    obj_msr_inv = obj_msr_inv['data']

    message = {
        "modelId": model_mrid,
        "requestType": "QUERY_OBJECT_MEASUREMENTS",
        "resultFormat": "JSON",
        "objectType": "LoadBreakSwitch"}     
    obj_msr_loadsw = gapps.get_response(topic, message, timeout=180) 
    obj_msr_loadsw = obj_msr_loadsw ['data']
   
    
    query = """
    PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX c:  <http://iec.ch/TC57/CIM100#>
    SELECT ?cimtype ?name ?bus1 ?bus2 ?id WHERE {
    SELECT ?cimtype ?name ?bus1 ?bus2 ?phs ?id WHERE {
    VALUES ?fdrid {"%s"}  # 9500 node
    VALUES ?cimraw {c:LoadBreakSwitch c:Recloser c:Breaker}
    ?fdr c:IdentifiedObject.mRID ?fdrid.
    ?s r:type ?cimraw.
    bind(strafter(str(?cimraw),"#") as ?cimtype)
    ?s c:Equipment.EquipmentContainer ?fdr.
    ?s c:IdentifiedObject.name ?name.
    ?s c:IdentifiedObject.mRID ?id.
    ?t1 c:Terminal.ConductingEquipment ?s.
    ?t1 c:ACDCTerminal.sequenceNumber "1".
    ?t1 c:Terminal.ConnectivityNode ?cn1. 
    ?cn1 c:IdentifiedObject.name ?bus1.
    ?t2 c:Terminal.ConductingEquipment ?s.
    ?t2 c:ACDCTerminal.sequenceNumber "2".
    ?t2 c:Terminal.ConnectivityNode ?cn2. 
    ?cn2 c:IdentifiedObject.name ?bus2
        OPTIONAL {?swp c:SwitchPhase.Switch ?s.
        ?swp c:SwitchPhase.phaseSide1 ?phsraw.
        bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) }
    } ORDER BY ?name ?phs
    }
    GROUP BY ?cimtype ?name ?bus1 ?bus2 ?id
    ORDER BY ?cimtype ?name
        """ % model_mrid
    results = gapps.query_data(query, timeout=60)
    results_obj = results['data']
    sw_data = results_obj['results']['bindings']
    switches = []
    for p in sw_data:
        sw_mrid = p['id']['value']
        fr_to = [p['bus1']['value'].upper(), p['bus2']['value'].upper()]
        message = dict(name = p['name']['value'],
                    mrid = sw_mrid,
                    sw_con = fr_to)
        switches.append(message) 
    
    return obj_msr_ACline, obj_msr_loadsw


def _main():
    _log.debug("Starting application")
    print("Application starting!!!-------------------------------------------------------")
    global message_period
    parser = argparse.ArgumentParser()
    parser.add_argument("simulation_id",
                        help="Simulation id to use for responses on the message bus.")
    parser.add_argument("request",
                        help="Simulation Request")
    parser.add_argument("--message_period",
                        help="How often the sample app will send open/close capacitor message.",
                        default=DEFAULT_MESSAGE_PERIOD)
    opts = parser.parse_args()
    listening_to_topic = simulation_output_topic(opts.simulation_id)
    message_period = int(opts.message_period)
    sim_request = json.loads(opts.request.replace("\'",""))
    model_mrid = sim_request["power_system_config"]["Line_name"]
    _log.debug("Model mrid is: {}".format(model_mrid))
    gapps = GridAPPSD(opts.simulation_id, address=utils.get_gridappsd_address(),
                      username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    topic = "goss.gridappsd.process.request.data.powergridmodel"
    
    # Run several query to extract the model information
    ACline, obj_msr_loadsw = get_meas_mrid(gapps, model_mrid, topic)

    # Subscribe to simulation output and interface to platform
    toggler = LearnPlatform(opts.simulation_id, gapps, ACline, obj_msr_loadsw)
    gapps.subscribe(listening_to_topic, toggler)
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    _main()
