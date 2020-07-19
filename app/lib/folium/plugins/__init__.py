# -*- coding: utf-8 -*-

"""
Folium plugins
--------------

Wrap some of the most popular leaflet external plugins.

"""

from .antpath import AntPath
from .polyline_offset import PolyLineOffset
from .beautify_icon import BeautifyIcon
from .boat_marker import BoatMarker
from .draw import Draw
from .dual_map import DualMap
from .fast_marker_cluster import FastMarkerCluster
from .feature_group_sub_group import FeatureGroupSubGroup
from .float_image import FloatImage
from .fullscreen import Fullscreen
from .geocoder import Geocoder
from .heat_map import HeatMap
from .heat_map_withtime import HeatMapWithTime
from .locate_control import LocateControl
from .marker_cluster import MarkerCluster
from .measure_control import MeasureControl
from .minimap import MiniMap
from .mouse_position import MousePosition
from .pattern import CirclePattern, StripePattern
from .polyline_text_path import PolyLineTextPath
from .scroll_zoom_toggler import ScrollZoomToggler
from .search import Search
from .semicircle import SemiCircle
from .terminator import Terminator
from .time_slider_choropleth import TimeSliderChoropleth
from .timestamped_geo_json import TimestampedGeoJson
from .timestamped_wmstilelayer import TimestampedWmsTileLayers

__all__ = [
    'AntPath',
    'BeautifyIcon',
    'BoatMarker',
    'CirclePattern',
    'Draw',
    'DualMap',
    'FastMarkerCluster',
    'FeatureGroupSubGroup',
    'FloatImage',
    'Fullscreen',
    'Geocoder',
    'HeatMap',
    'HeatMapWithTime',
    'LocateControl',
    'MarkerCluster',
    'MeasureControl',
    'MiniMap',
    'MousePosition',
    'PolyLineTextPath',
    'PolyLineOffset',
    'ScrollZoomToggler',
    'Search',
    'SemiCircle',
    'StripePattern',
    'Terminator',
    'TimeSliderChoropleth',
    'TimestampedGeoJson',
    'TimestampedWmsTileLayers',
]
