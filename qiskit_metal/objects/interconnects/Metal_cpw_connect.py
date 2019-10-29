# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


'''
@date: 2019
@author: Zlatko K Minev
modified: Thomas McConkey 2019/10/15
'''
# pylint: disable=invalid-name

from numpy import array
from ..base_objects.Metal_Object import Metal_Object, Dict
from ...config import DEFAULT_OPTIONS
from ...draw_cpw import parse_options_user, CAP_STYLE, JOIN_STYLE, meander_between, draw_cpw_trace, LineString, to_Vec3D


DEFAULT_OPTIONS['Metal_cpw_connect'] = Dict(
    connector1='[INPUT NAME HERE]',
    connector2='[INPUT NAME HERE]',
    connector1_leadin='200um',
    connector2_leadin='200um',
    cpw=Dict(),
    meander=Dict(),
    _calls=['meander_between', 'connectorCPW_plotme',
            'draw_cpw_trace', 'basic_meander']  # usef only for debug internal refernece here
)
'''
 connector1 : connector 1 from which to begin drawing the CPW
 connector2 : connectors 2 where to end the drawing of the CPW
'''


class Metal_cpw_connect(Metal_Object):
    '''

Description:
    ----------------------------------------------------------------------------
    Creates a meandered CPW transmission line between two 'connector' points.
    The transmission line is drawn from "connector1" to "connector2". These are
    tracked in the design dictionary which must also have been passed in.

    Total length of the meander is found from;

Options (Metal_cpw_connect):
    connector1: string of the name of the starting connector point (as listed in design.connectors dictionary)
    connector2: string of the name of the ending connector point (as listed in design.connectors dictionary)
    connector1/2_leadin: 'buffer' length of straight CPW transmission line from the connector point

    Convention: Values (unless noted) are strings with units included,
                (e.g., '30um')

    options_cpw: See options for draw_cpw_trace:
    options_meander: meander_between

    You must pass in the design object, which keeps tracks of all the connects

    Conect named control points: connector1 ---> connector2,
    '''

    _img = 'Metal_cpw_connect.png'

    _options_inherit = dict(
        cpw='draw_cpw_trace',
        meander='basic_meander',
    )

    def __init__(self, design, name=None, options=None):

        if name is None:
            name = 'cpw_'+options.connector1+'_'+options.connector2

        super().__init__(design, name, options=options)

        self.check_connector_name()

        self.make()

    def check_connector_name(self):
        if self.options.connector1 is '' or self.options.connector1  is '[INPUT NAME HERE]':
            raise Exception(
                'ERROR: You did not provide a name for the leading connector connector1')
        if self.options.connector1 is '' or self.options.connector2 is '[INPUT NAME HERE]':
            raise Exception(
                'ERROR: You did not provide a name for the second connector connector2')
        assert self.options.connector1 in self.get_connectors(
        ), f'Connector name {self.options.connector1} not in the set of connectors defined {self.get_connectors().keys()}'
        assert self.options.connector2 in self.get_connectors(
        ), f'Connector name {self.options.connector2} not in the set of connectors defined {self.get_connectors().keys()}'

    def make(self):
        connector1_leadin_dist, connector2_leadin_dist = parse_options_user(self.design.params.variables,
            self.options, 'connector1_leadin, connector2_leadin')

        # connectors
        connectors = self.get_connectors()
        c1 = connectors[self.options.connector1]
        c2 = connectors[self.options.connector2]
        #print( connector1_leadin_dist, connector2_leadin_dist, c1,c2, self.options.connector1)

        points0 = array([  # control points (user units)
            c1['pos'],
            c1['pos'] + c1['normal']*connector1_leadin_dist,
            c2['pos'] + c2['normal']*connector2_leadin_dist,
            c2['pos']
        ])

        if connector2_leadin_dist < 0:
            points0 = points0[:-1]

        # Control line
        self.points_meander = array(
            meander_between(self.design, points0, 1, self.options.meander))
        self.objects.cpw_line = LineString(self.points_meander)

        # For metal
        self.options.cpw = {
            **DEFAULT_OPTIONS['draw_cpw_trace'], **self.options.cpw, 'name': self.name}
        cpw_width, cpw_gap = parse_options_user(self.design.params.variables,
            self.options.cpw, 'trace_center_width, trace_center_gap')
        self.objects.trace_center = self.objects.cpw_line.buffer(
            cpw_width/2, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre)
        self.objects.trace_gap = self.objects.trace_center.buffer(
            cpw_gap,  cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre)

    def hfss_draw(self):
        options = self.options.cpw

        def to_vec3D(vec):
            return to_Vec3D(self.design, options, vec)

        draw_cpw_trace(self.design, to_vec3D(self.points_meander), options)