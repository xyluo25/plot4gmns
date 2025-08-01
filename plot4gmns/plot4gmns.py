# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, December 4th 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from pathlib import Path
import numpy as np
import pandas as pd
from typing import Union
from .network import MultiNet
from .utility_lib import generate_absolute_path, update_filename, path2linux
from .func_lib import (
    extract_coordinates_by_network_mode,
    extract_coordinates_by_node_types,
    extract_coordinates_by_link_types,
    extract_coordinates_by_link_lane,
    extract_coordinates_by_link_free_speed,
    extract_coordinates_by_link_length,
    extract_coordinates_by_link_attr_distribution,
    extract_coordinates_by_poi_type,
    extract_coordinates_by_poi_attr_distribution,
    count_demand_matrix,
    extract_coordinates_by_demand_OD)
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.collections import PolyCollection
import os


def show_network_by_modes(mnet: MultiNet,
                          modes: list = None,
                          fig_obj: plt = None,
                          isSave2png: bool = True,
                          output_dir: str = None) -> plt:
    """draw network links of different modes

    Args:
        mnet (MultiNet): MultiNet object
        modes (list): list of network modes to display. Defaults to ['all'].
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if modes is None:
        modes = ['all']

    if output_dir is None:
        output_dir = Path.cwd()

    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_network_mode(mnet, modes)

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(file_name="network_by_mode.png",
                                             folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_node_types(mnet: MultiNet,
                               osm_highway: list,
                               fig_obj: plt = None,
                               isSave2png: bool = True,
                               output_dir: str = None) -> plt:
    """draw network nodes according to specified node types

    Args:
        mnet (MultiNet): MultiNet object
        osm_highway (list): list of network node types to display.
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()

    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if isinstance(osm_highway, str):
        osm_highway_ = [osm_highway]
    elif isinstance(osm_highway, list):
        osm_highway_ = osm_highway
    else:
        raise Exception("TypeError: str or list is expected ")

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        extract_coordinates_by_node_types(mnet, osm_highway_)
        for id in range(len(mnet.node.x_coords)):
            x_coords = mnet.node.x_coords[id]
            y_coords = mnet.node.y_coords[id]
            highway_type = osm_highway_[id]
            if len(x_coords) > 0:
                ax.scatter(x_coords,
                           y_coords,
                           marker=mnet.style.node_style.markers[highway_type],
                           c=mnet.style.node_style.colors[highway_type],
                           s=mnet.style.node_style.size,
                           edgecolors=mnet.style.node_style.edgecolors,
                           zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(file_name="network_by_node_type.png",
                                             folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure, dpi=mnet.style.dpi)
        print(f"Successfully save figure to {path_figure}")

    return plt


def show_network_by_link_types(mnet: MultiNet,
                               link_types: list,
                               fig_obj: plt = None,
                               isSave2png: bool = True,
                               output_dir: str = None) -> plt:
    """draw network nodes according to specified link types
    Args:
        mnet (MultiNet): MultiNet object
        link_types (list): list of network link types to display.
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if isinstance(link_types, str):
        link_types_ = [link_types]
    elif isinstance(link_types, list):
        link_types_ = link_types
    else:
        raise Exception("TypeError: str or list is expected ")

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    extract_coordinates_by_link_types(mnet, link_types_)

    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_type.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_lanes(mnet: MultiNet,
                               min_lanes: int,
                               max_lanes: int,
                               fig_obj: plt = None,
                               isSave2png: bool = True,
                               output_dir: str = None) -> plt:
    """draw network links according to specified link lane number
    Args:
        mnet (MultiNet): MultiNet object
        min_lanes (int): Minimum number of lanes to display
        max_lanes (int): Maximum number of lanes to display
        fig_obj (plt): Figure object to draw on
        isSave2png (bool): Whether to save the figure as a PNG
        output_dir (str): Directory to save the figure

    Returns:
        plt: Figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if min_lanes > max_lanes:
        print("ValueError: 'min_lanes' should not less than 'max_lanes' ")
    extract_coordinates_by_link_lane(mnet, (min_lanes, max_lanes))

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_lane.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_free_speed(mnet: MultiNet,
                                    min_free_speed: int,
                                    max_free_speed: int,
                                    fig_obj: plt = None,
                                    isSave2png: bool = True,
                                    output_dir: str = None) -> plt:
    """draw network links according to specified link free speed

    Args:
        mnet (MultiNet): MultiNet object
        min_free_speed (int): Minimum free speed of links to display
        max_free_speed (int): Maximum free speed of links to display
        fig_obj (plt): Figure object to draw on
        isSave2png (bool): Whether to save the figure as a PNG
        output_dir (str): Directory to save the figure

    Returns:
        plt: Figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if min_free_speed > max_free_speed:
        print("ValueError: 'min_lanes' should not less than 'max_lanes' ")
    extract_coordinates_by_link_free_speed(
        mnet, (min_free_speed, max_free_speed))

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_free_speed.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_length(mnet: MultiNet,
                                min_length: int,
                                max_length: int,
                                fig_obj: plt = None,
                                isSave2png: bool = True,
                                output_dir: str = None) -> plt:
    """draw network links according to specified link free speed
    Args:
        mnet (MultiNet): MultiNet object
        min_length (int): Minimum length of links to display
        max_length (int): Maximum length of links to display
        fig_obj (plt): Figure object to draw on
        isSave2png (bool): Whether to save the figure as a PNG
        output_dir (str): Directory to save the figure

    Returns:
        plt: Figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if min_length > max_length:
        print("ValueError: 'min_lanes' should not less than 'max_lanes' ")
    extract_coordinates_by_link_length(mnet, (min_length, max_length))

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))
    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_length.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_lane_distribution(mnet: MultiNet,
                                           fig_obj: plt = None,
                                           isSave2png: bool = True,
                                           output_dir: str = None) -> plt:
    """draw network links according to the distribution of number of link lanes

    Args:
        mnet (MultiNet): MultiNet object
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_link_attr_distribution(mnet, 'lanes')

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        max_v, min_v = max(mnet.link.attr_distribution), min(mnet.link.attr_distribution)
        w = np.array(mnet.link.attr_distribution) / max_v * 4.5 + 0.5
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=w,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    # add legend
    proxies = [Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=0.5),
               Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=5)]
    ax.legend(proxies, ['%s:%.4f' % ('lanes', min_v), '%s:%.4f' % ('lanes', max_v)], loc='upper right')
    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_lane_distribution.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_free_speed_distribution(mnet: MultiNet,
                                                 fig_obj: plt = None,
                                                 isSave2png: bool = True,
                                                 output_dir: str = None) -> plt:
    """draw network links according to the distribution of link free speed

    Args:
        mnet (MultiNet): MultiNet object
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """
    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_link_attr_distribution(mnet, 'free_speed')

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        max_v, min_v = max(mnet.link.attr_distribution), min(mnet.link.attr_distribution)
        w = np.array(mnet.link.attr_distribution) / max_v * 4.5 + 0.5
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=w,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    # add legend
    proxies = [Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=0.5),
               Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=5)]
    ax.legend(proxies, ['%s:%.4f' % ('free speed', min_v), '%s:%.4f' % ('free speed', max_v)], loc='upper right')
    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_free_speed_distribution.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_link_capacity_distribution(mnet: MultiNet,
                                               fig_obj: plt = None,
                                               isSave2png: bool = True,
                                               output_dir: str = None) -> plt:
    """draw network links according to the distribution of link capacity

    Args:
        mnet (MultiNet): MultiNet object
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """
    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_link_attr_distribution(mnet, 'capacity')

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        max_v, min_v = max(mnet.link.attr_distribution), min(mnet.link.attr_distribution)
        w = np.array(mnet.link.attr_distribution) / max_v * 4.5 + 0.5
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=w,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    # add legend
    proxies = [Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=0.5),
               Line2D([0, 1], [0, 1], color=mnet.style.link_style.linecolor, linewidth=5)]
    ax.legend(proxies, ['%s:%.4f' % ('capacity', min_v), '%s:%.4f' % ('capacity', max_v)], loc='upper right')
    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_link_capacity_distribution.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_poi_types(mnet: MultiNet,
                              poi_type: Union[str, list],
                              fig_obj: plt = None,
                              isSave2png: bool = True,
                              output_dir: str = None) -> plt:
    """draw network according to the specified POI types

    Args:
        mnet (MultiNet): MultiNet object
        poi_type (Union[str, list]): POI type or list of POI types to display.
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    if isinstance(poi_type, str):
        poi_type_ = [poi_type]
    elif isinstance(poi_type, list):
        poi_type_ = poi_type
    else:
        raise Exception("TypeError: str or list is expected ")
    extract_coordinates_by_poi_type(mnet=mnet, poi_type=poi_type_)

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        ax.add_collection(
            PolyCollection(mnet.POI.poi_coords,
                           alpha=0.7,
                           facecolors=mnet.style.poi_style.facecolor,
                           edgecolors=mnet.style.poi_style.edgecolor,
                           zorder=0))

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_poi_type.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_poi_production_distribution(mnet: MultiNet,
                                                fig_obj: plt = None,
                                                isSave2png: bool = True,
                                                output_dir: str = None) -> plt:
    """draw network according to the distribution of poi production

    Args:
        mnet (MultiNet): MultiNet object
        fig_obj (plt): figure object (plt). If not None, will continue to draw
            elements on the existing figure object. Defaults to None.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_poi_attr_distribution(mnet=mnet, column='production')

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        poly_coll = PolyCollection(mnet.POI.poi_coords,
                                   alpha=0.7,
                                   array=np.array(mnet.POI.attr_distribution),
                                   cmap=mnet.style.cmap,
                                   edgecolors=mnet.style.poi_style.edgecolor,
                                   zorder=0)
        ax.add_collection(poly_coll)
        fig.colorbar(poly_coll, ax=ax)

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_poi_production_distribution.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_poi_attraction_distribution(mnet: MultiNet,
                                                fig_obj: plt = None,
                                                isSave2png: bool = True,
                                                output_dir: str = None) -> plt:
    """draw network according to the distribution of poi attraction

    Args:
        mnet (MultiNet): MultiNet object
        fig_obj (plt): figure object (plt). If not None, will continue to draw
            elements on the existing figure object. Defaults to None.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_poi_attr_distribution(mnet=mnet, column='attraction')

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    # draw network nodes
    if mnet.node_loaded:
        ax.scatter(mnet.node.x_coords,
                   mnet.node.y_coords,
                   marker=mnet.style.node_style.markers['other'],
                   c=mnet.style.node_style.colors['other'],
                   s=mnet.style.node_style.size,
                   edgecolors=mnet.style.node_style.edgecolors,
                   zorder=2)

    # draw network links
    if mnet.link_loaded:
        ax.add_collection(
            LineCollection(mnet.link.link_coords,
                           colors=mnet.style.link_style.linecolor,
                           linewidths=mnet.style.link_style.linewidth,
                           zorder=1))

    # draw network pois
    if mnet.POI_loaded:
        poly_coll = PolyCollection(mnet.POI.poi_coords,
                                   alpha=0.7,
                                   array=np.array(mnet.POI.attr_distribution),
                                   cmap=mnet.style.cmap,
                                   edgecolors=mnet.style.poi_style.edgecolor,
                                   zorder=0)
        ax.add_collection(poly_coll)
        fig.colorbar(poly_coll, ax=ax)

    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_poi_attraction_distribution.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_demand_matrix_heatmap(mnet: MultiNet,
                                       annot: bool = False,
                                       isSave2png: bool = True,
                                       output_dir: str = None) -> plt:
    """draw network according to the distribution of poi attraction

    Args:
        mnet (MultiNet): MultiNet object
        annot (bool): If True, write the data value in each cell. Defaults to False.
        isSave2png (bool): If True, save the figure to a png file. Defaults to True.
        output_dir (str): Directory to save the figure. Defaults to None.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    count_demand_matrix(mnet)
    max_vol = np.max(mnet.demand.demand_matrix.reshape(1, -1))
    min_vol = np.min(mnet.demand.demand_matrix.reshape(1, -1))
    labels = [str(i + 1) for i in range(mnet.zone.value.shape[0])]
    df = pd.DataFrame(mnet.demand.demand_matrix, index=labels, columns=labels)

    plt.figure(figsize=(mnet.style.figure_size), dpi=mnet.style.dpi)
    sns.heatmap(data=df, vmax=max_vol, vmin=min_vol, annot=annot, cmap=mnet.style.cmap)

    sns.set(font_scale=1.5)
    plt.rc('font', family='Times New Roman', size=6)
    plt.xlabel('to_zone_id')
    plt.ylabel('from_zone_id')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_demand_matrix_heatmap.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt


def show_network_by_demand_OD(mnet: MultiNet,
                              load_zone: bool = True,
                              load_network: bool = False,
                              fig_obj: plt = None,
                              isSave2png: bool = True,
                              output_dir: str = None) -> plt:
    """draw network according to the distribution of poi attraction

    Args:
        mnet (MultiNet): MultiNet object
        load_zone (bool): if True, draw the zone grid. Defaults to True.
        load_network (bool): if True, draw the network as the background. Defaults to False
        fig_obj (plt): figure object (plt). If not None, will continue to draw elements on the existing figure object.
        isSave2png (bool): if True, save the figure to a png file. Defaults to True.
        output_dir (str): directory to save the figure. Defaults to None, which means the current working directory.

    Returns:
        plt: figure object with the drawn network
    """

    if output_dir is None:
        output_dir = Path.cwd()
    if not Path(output_dir).exists():
        output_dir = Path.cwd()

    extract_coordinates_by_demand_OD(mnet, load_zone, load_network)

    if fig_obj:
        # get ax from fog_obj and add more data later
        ax = fig_obj.gca()
        fig = fig_obj
    else:
        # create an empty fig and ax and add data later
        fig, ax = plt.subplots(figsize=mnet.style.figure_size, dpi=mnet.style.dpi)

    if load_network:
        # draw network nodes
        if mnet.node_loaded:
            ax.scatter(mnet.node.x_coords,
                       mnet.node.y_coords,
                       marker=mnet.style.node_style.markers['other'],
                       c=mnet.style.node_style.colors['other'],
                       s=mnet.style.node_style.size,
                       edgecolors=mnet.style.node_style.edgecolors,
                       zorder=2)
        # draw network links
        if mnet.link_loaded:
            ax.add_collection(
                LineCollection(mnet.link.link_coords,
                               colors=mnet.style.link_style.linecolor,
                               linewidths=mnet.style.link_style.linewidth,
                               zorder=1))
        # draw network pois
        if mnet.POI_loaded:
            ax.add_collection(
                PolyCollection(mnet.POI.poi_coords,
                               alpha=0.7,
                               facecolors=mnet.style.poi_style.facecolor,
                               edgecolors=mnet.style.poi_style.edgecolor,
                               zorder=0))
    if load_zone:
        ax.add_collection(
            PolyCollection(mnet.zone.zone_coords,
                           facecolors='none',
                           linewidths=mnet.style.zone_style.linewidth,
                           edgecolors=mnet.style.zone_style.edgecolors,
                           facecolor='none',
                           zorder=3)
        )
        for label in mnet.zone.zone_names:
            plt.annotate(
                str(label[0]),
                xy=(label[1], label[2]),
                xytext=(label[1], label[2]),
                weight='bold',
                color=mnet.style.zone_style.fontcolor,
                fontsize=mnet.style.zone_style.fontsize)

    # plot network demand flow
    w = np.array(mnet.demand.demand_OD_vol) / max(mnet.demand.demand_OD_vol) * 4.5 + 0.5
    ax.add_collection(LineCollection(mnet.demand.demand_OD_coords, colors='orange', linewidths=w, zorder=2))

    # add legend
    proxies = [Line2D([0, 1], [0, 1], color='orange', linewidth=0.5),
               Line2D([0, 1], [0, 1], color='orange', linewidth=5)]
    ax.legend(proxies, ['%s:%.4f' % ('volume', min(mnet.demand.demand_OD_vol)),
                        '%s:%.4f' % ('volume', max(mnet.demand.demand_OD_vol))])
    # set axis
    ax.autoscale_view()
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.tight_layout()

    if isSave2png:
        path_figure = generate_absolute_path(
            file_name="network_by_demand_od.png",
            folder_name=path2linux(os.path.join(output_dir, "p4g_fig_results")))
        plt.savefig(path_figure)
        print(f"The image has been saved to the designated location: {path_figure}")

    return plt
