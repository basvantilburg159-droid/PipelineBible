"""
Pipe Standards Pro v12 - 2D Visualization
2D cross-section and technical drawings with modern styling
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge, FancyBboxPatch
from matplotlib.figure import Figure
import numpy as np
from typing import Optional, Tuple
from constants import *
from data_models import PipeSpec, BendSpec, FlangeSpec


def setup_2d_axes(fig: Figure, title: str = "") -> plt.Axes:
    """Setup matplotlib axes with dark theme"""
    fig.patch.set_facecolor(BG_PRIMARY)
    ax = fig.add_subplot(111)
    ax.set_facecolor(BG_SECONDARY)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, color=TEXT_DISABLED)
    
    if title:
        ax.set_title(title, color=TEXT_PRIMARY, 
                    fontsize=FONT_SIZE_SUBHEADER, pad=15)
    
    # Style spine colors
    for spine in ax.spines.values():
        spine.set_color(BG_TERTIARY)
        spine.set_linewidth(1)
    
    # Style tick colors
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=FONT_SIZE_SMALL)
    
    return ax


def draw_pipe_cross_section(fig: Figure, pipe: PipeSpec, 
                           show_dimensions: bool = True) -> None:
    """
    Draw pipe cross-section with wall thickness
    
    Args:
        fig: Matplotlib figure
        pipe: Pipe specification
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_2d_axes(fig, f"Pipe Cross-Section: {pipe.standard} {pipe.nps_or_dn}")
    
    # Calculate radii
    outer_radius = pipe.od / 2
    inner_radius = pipe.id / 2
    
    # Draw outer circle (steel)
    outer_circle = Circle((0, 0), outer_radius,
                          facecolor=STEEL_OUTER,
                          edgecolor=STEEL_EDGE,
                          linewidth=2,
                          alpha=0.9,
                          label='Outer Surface')
    ax.add_patch(outer_circle)
    
    # Draw inner circle (hollow)
    inner_circle = Circle((0, 0), inner_radius,
                          facecolor=BG_PRIMARY,
                          edgecolor=STEEL_INNER,
                          linewidth=2,
                          alpha=1.0,
                          label='Inner Surface')
    ax.add_patch(inner_circle)
    
    # Add wall thickness visualization with gradient effect
    # Create annulus with multiple rings for gradient
    num_rings = 5
    for i in range(num_rings):
        r_outer = outer_radius - (i * pipe.wall_thickness / num_rings)
        r_inner = outer_radius - ((i + 1) * pipe.wall_thickness / num_rings)
        if r_inner < inner_radius:
            r_inner = inner_radius
        
        alpha_val = 0.7 - (i * 0.1)
        ring = Circle((0, 0), r_outer,
                     facecolor='none',
                     edgecolor=STEEL_EDGE,
                     linewidth=0.5,
                     alpha=alpha_val)
        ax.add_patch(ring)
    
    if show_dimensions:
        # Outer diameter dimension
        ax.plot([-outer_radius, outer_radius], [0, 0],
               'o-', color=ACCENT_CYAN, linewidth=2, markersize=4)
        ax.text(0, outer_radius * 0.2, f'OD = {pipe.od:.3f} {"in" if pipe.standard == "ASME" else "mm"}',
               ha='center', va='bottom', color=ACCENT_CYAN,
               fontsize=FONT_SIZE_NORMAL, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Inner diameter dimension
        ax.plot([-inner_radius, inner_radius], 
               [inner_radius * 0.5, inner_radius * 0.5],
               'o-', color=ACCENT_GOLD, linewidth=2, markersize=4)
        ax.text(0, inner_radius * 0.7, f'ID = {pipe.id:.3f} {"in" if pipe.standard == "ASME" else "mm"}',
               ha='center', va='bottom', color=ACCENT_GOLD,
               fontsize=FONT_SIZE_NORMAL, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Wall thickness dimension
        angle = 45
        rad_angle = np.radians(angle)
        x_outer = outer_radius * np.cos(rad_angle)
        y_outer = outer_radius * np.sin(rad_angle)
        x_inner = inner_radius * np.cos(rad_angle)
        y_inner = inner_radius * np.sin(rad_angle)
        
        ax.plot([x_inner, x_outer], [y_inner, y_outer],
               'o-', color=ACCENT_STEEL, linewidth=2, markersize=4)
        ax.text(x_outer * 1.2, y_outer * 1.2,
               f'WT = {pipe.wall_thickness:.3f} {"in" if pipe.standard == "ASME" else "mm"}',
               ha='left', va='bottom', color=ACCENT_STEEL,
               fontsize=FONT_SIZE_NORMAL, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set limits with padding
    max_radius = outer_radius * 1.5
    ax.set_xlim(-max_radius, max_radius)
    ax.set_ylim(-max_radius, max_radius)
    
    # Add info box
    info_text = f"Schedule: {pipe.schedule}\nArea: {pipe.cross_section_area:.2f} sq.{' in' if pipe.standard == 'ASME' else ' mm'}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    plt.tight_layout()


def draw_bend(fig: Figure, bend: BendSpec, show_dimensions: bool = True) -> None:
    """
    Draw bend/elbow in 2D
    
    Args:
        fig: Matplotlib figure
        bend: Bend specification
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_2d_axes(fig, f"90° Elbow: {bend.nps_or_dn} {bend.radius_type}")
    
    outer_radius = bend.od / 2
    inner_radius = (bend.od - 2 * bend.wall_thickness) / 2
    center_radius = bend.radius
    
    # Draw center line arc
    theta = np.linspace(0, np.pi/2, 50)
    x_center = center_radius * np.cos(theta)
    y_center = center_radius * np.sin(theta)
    ax.plot(x_center, y_center, '--', color=ACCENT_CYAN, linewidth=2,
           label='Center Line', alpha=0.7)
    
    # Draw outer arc
    outer_r = center_radius + outer_radius
    x_outer = outer_r * np.cos(theta)
    y_outer = outer_r * np.sin(theta)
    ax.plot(x_outer, y_outer, '-', color=STEEL_EDGE, linewidth=3)
    
    # Draw inner arc
    inner_r = center_radius - outer_radius
    x_inner = inner_r * np.cos(theta)
    y_inner = inner_r * np.sin(theta)
    ax.plot(x_inner, y_inner, '-', color=STEEL_EDGE, linewidth=3)
    
    # Draw side walls
    ax.plot([x_outer[0], x_inner[0]], [y_outer[0], y_inner[0]],
           '-', color=STEEL_EDGE, linewidth=3)
    ax.plot([x_outer[-1], x_inner[-1]], [y_outer[-1], y_inner[-1]],
           '-', color=STEEL_EDGE, linewidth=3)
    
    # Fill elbow area with gradient
    # Create filled region
    theta_fill = np.linspace(0, np.pi/2, 50)
    for i, t in enumerate(theta_fill):
        alpha_val = 0.5 + 0.3 * (i / len(theta_fill))
        x1 = inner_r * np.cos(t)
        y1 = inner_r * np.sin(t)
        x2 = outer_r * np.cos(t)
        y2 = outer_r * np.sin(t)
        ax.plot([x1, x2], [y1, y2], '-', color=STEEL_OUTER,
               linewidth=1.5, alpha=alpha_val * 0.5)
    
    if show_dimensions:
        # Center radius dimension
        mid_idx = len(x_center) // 2
        ax.plot([0, x_center[mid_idx]], [0, y_center[mid_idx]],
               'o-', color=ACCENT_GOLD, linewidth=2, markersize=4)
        ax.text(x_center[mid_idx] * 0.5, y_center[mid_idx] * 0.5,
               f'R = {center_radius:.2f} {"in" if bend.standard == "ASME" else "mm"}',
               ha='center', va='bottom', color=ACCENT_GOLD,
               fontsize=FONT_SIZE_NORMAL, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Pipe diameter
        ax.text(outer_r * 0.8, outer_r * 0.1,
               f'OD = {bend.od:.3f} {"in" if bend.standard == "ASME" else "mm"}',
               ha='center', color=ACCENT_CYAN,
               fontsize=FONT_SIZE_SMALL,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set equal aspect and limits
    max_dim = outer_r * 1.2
    ax.set_xlim(-max_dim * 0.2, max_dim)
    ax.set_ylim(-max_dim * 0.2, max_dim)
    
    # Info box
    arc_length = bend.arc_length
    info_text = f"Type: {bend.radius_type}\nArc Length: {arc_length:.2f} {'in' if bend.standard == 'ASME' else 'mm'}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    plt.tight_layout()


def draw_flange(fig: Figure, flange: FlangeSpec, 
               show_dimensions: bool = True) -> None:
    """
    Draw flange face view in 2D
    
    Args:
        fig: Matplotlib figure
        flange: Flange specification
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_2d_axes(fig, f"Flange: {flange.standard} {flange.nps_or_dn} Class {flange.pressure_class}")
    
    outer_radius = flange.od / 2
    bolt_circle_radius = flange.bolt_circle_dia / 2
    bolt_radius = flange.bolt_size / 2
    
    # Draw outer flange circle
    outer_circle = Circle((0, 0), outer_radius,
                          facecolor=STEEL_OUTER,
                          edgecolor=STEEL_EDGE,
                          linewidth=3,
                          alpha=0.9)
    ax.add_patch(outer_circle)
    
    # Draw raised face (smaller inner circle)
    raised_face_radius = outer_radius * 0.6
    raised_face = Circle((0, 0), raised_face_radius,
                         facecolor=STEEL_INNER,
                         edgecolor=STEEL_EDGE,
                         linewidth=2,
                         alpha=0.8)
    ax.add_patch(raised_face)
    
    # Draw bolt circle (dashed)
    bolt_circle = Circle((0, 0), bolt_circle_radius,
                         facecolor='none',
                         edgecolor=ACCENT_CYAN,
                         linewidth=1.5,
                         linestyle='--',
                         alpha=0.6)
    ax.add_patch(bolt_circle)
    
    # Draw bolt holes
    for i in range(flange.num_bolts):
        angle = 2 * np.pi * i / flange.num_bolts
        x = bolt_circle_radius * np.cos(angle)
        y = bolt_circle_radius * np.sin(angle)
        
        bolt_hole = Circle((x, y), bolt_radius,
                          facecolor=BG_PRIMARY,
                          edgecolor=ACCENT_GOLD,
                          linewidth=2)
        ax.add_patch(bolt_hole)
        
        # Draw bolt threads (simplified)
        thread_circle = Circle((x, y), bolt_radius * 0.7,
                              facecolor='none',
                              edgecolor=ACCENT_GOLD,
                              linewidth=0.5,
                              alpha=0.5)
        ax.add_patch(thread_circle)
    
    # Center bore
    bore_radius = outer_radius * 0.3
    bore = Circle((0, 0), bore_radius,
                 facecolor=BG_PRIMARY,
                 edgecolor=TEXT_SECONDARY,
                 linewidth=2,
                 linestyle=':')
    ax.add_patch(bore)
    
    if show_dimensions:
        # Outer diameter
        ax.plot([-outer_radius, outer_radius], [0, 0],
               'o-', color=ACCENT_CYAN, linewidth=2, markersize=4)
        ax.text(0, -outer_radius * 0.15, 
               f'OD = {flange.od:.2f} {"in" if flange.standard == "ASME" else "mm"}',
               ha='center', va='top', color=ACCENT_CYAN,
               fontsize=FONT_SIZE_NORMAL, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Bolt circle diameter
        ax.plot([0, bolt_circle_radius], [0, 0],
               'o-', color=ACCENT_GOLD, linewidth=1.5, markersize=3)
        ax.text(bolt_circle_radius * 0.5, bolt_circle_radius * 0.15,
               f'BCD = {flange.bolt_circle_dia:.2f}',
               ha='center', color=ACCENT_GOLD,
               fontsize=FONT_SIZE_SMALL,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set limits
    max_radius = outer_radius * 1.3
    ax.set_xlim(-max_radius, max_radius)
    ax.set_ylim(-max_radius, max_radius)
    
    # Info box
    info_text = f"Bolts: {flange.num_bolts} × M{flange.bolt_size:.0f}\nThickness: {flange.thickness:.2f} {'in' if flange.standard == 'ASME' else 'mm'}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    plt.tight_layout()


def draw_flow_diagram(fig: Figure, flow_data: dict) -> None:
    """
    Draw flow visualization diagram
    
    Args:
        fig: Matplotlib figure
        flow_data: Dictionary with flow parameters
    """
    ax = setup_2d_axes(fig, "Flow Analysis")
    
    # Draw simplified pipe with flow
    pipe_length = 10
    pipe_id = flow_data.get('pipe_id', 1.0)
    velocity = flow_data.get('velocity', 2.0)
    
    # Pipe walls
    ax.add_patch(Rectangle((-pipe_length/2, -pipe_id/2), pipe_length, pipe_id/10,
                          facecolor=STEEL_OUTER, edgecolor=STEEL_EDGE, linewidth=2))
    ax.add_patch(Rectangle((-pipe_length/2, pipe_id/2 - pipe_id/10), pipe_length, pipe_id/10,
                          facecolor=STEEL_OUTER, edgecolor=STEEL_EDGE, linewidth=2))
    
    # Flow arrows
    num_arrows = 8
    for i in range(num_arrows):
        x = -pipe_length/2 + (i + 0.5) * pipe_length / num_arrows
        # Parabolic velocity profile (higher in center)
        y_positions = np.linspace(-pipe_id/2 + pipe_id/10, pipe_id/2 - pipe_id/10, 5)
        for y in y_positions:
            # Length proportional to distance from wall
            dist_from_center = abs(y)
            arrow_length = velocity * (1 - dist_from_center / (pipe_id/2)) * 0.5
            ax.arrow(x, y, arrow_length, 0,
                    head_width=pipe_id/20, head_length=arrow_length/5,
                    fc=ACCENT_CYAN, ec=ACCENT_CYAN, alpha=0.7)
    
    # Labels
    reynolds = flow_data.get('reynolds', 10000)
    regime = flow_data.get('regime', 'Turbulent')
    
    info_text = f"Velocity: {velocity:.2f} m/s\nReynolds: {reynolds:.0f}\nRegime: {regime}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_NORMAL,
           color=TEXT_PRIMARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.9))
    
    ax.set_xlim(-pipe_length/2 * 1.2, pipe_length/2 * 1.2)
    ax.set_ylim(-pipe_id, pipe_id)
    ax.set_aspect('auto')
    
    plt.tight_layout()
