"""
Pipe Standards Pro v12 - Isometric Visualization
Isometric (30° projection) technical drawings
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.figure import Figure
import numpy as np
from typing import Tuple, List
from constants import *
from data_models import PipeSpec, BendSpec, FlangeSpec


def isometric_transform(points_3d: np.ndarray) -> np.ndarray:
    """
    Transform 3D points to 2D isometric projection (30° rotation)
    
    Args:
        points_3d: Array of shape (N, 3) with x, y, z coordinates
    
    Returns:
        Array of shape (N, 2) with isometric x, y coordinates
    """
    # Isometric projection matrix (30° rotation)
    # Standard isometric: 30° angles for x and z axes
    iso_x = points_3d[:, 0] * np.cos(np.radians(30)) - points_3d[:, 2] * np.cos(np.radians(30))
    iso_y = points_3d[:, 1] + points_3d[:, 0] * np.sin(np.radians(30)) + points_3d[:, 2] * np.sin(np.radians(30))
    
    return np.column_stack([iso_x, iso_y])


def setup_iso_axes(fig: Figure, title: str = "") -> plt.Axes:
    """Setup matplotlib axes for isometric view"""
    fig.patch.set_facecolor(BG_PRIMARY)
    ax = fig.add_subplot(111)
    ax.set_facecolor(BG_SECONDARY)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, color=TEXT_DISABLED, linestyle=':')
    
    if title:
        ax.set_title(title, color=TEXT_PRIMARY,
                    fontsize=FONT_SIZE_SUBHEADER, pad=15)
    
    # Style axes
    for spine in ax.spines.values():
        spine.set_color(BG_TERTIARY)
        spine.set_linewidth(1)
    
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=FONT_SIZE_SMALL)
    ax.set_xlabel('', color=TEXT_SECONDARY)
    ax.set_ylabel('', color=TEXT_SECONDARY)
    
    return ax


def create_cylinder_isometric(center: Tuple[float, float, float],
                              radius: float, height: float,
                              num_segments: int = 32) -> Tuple[np.ndarray, List]:
    """
    Create isometric cylinder coordinates
    
    Args:
        center: (x, y, z) center point
        radius: Cylinder radius
        height: Cylinder height
        num_segments: Number of segments for circular profile
    
    Returns:
        Tuple of (3D points, face definitions)
    """
    cx, cy, cz = center
    
    # Create circle points at base
    theta = np.linspace(0, 2*np.pi, num_segments + 1)
    x_circle = radius * np.cos(theta)
    z_circle = radius * np.sin(theta)
    
    # Bottom circle
    bottom_points = np.column_stack([
        x_circle + cx,
        np.full_like(x_circle, cy),
        z_circle + cz
    ])
    
    # Top circle
    top_points = np.column_stack([
        x_circle + cx,
        np.full_like(x_circle, cy + height),
        z_circle + cz
    ])
    
    return bottom_points, top_points


def draw_pipe_isometric(fig: Figure, pipe: PipeSpec,
                       length: float = 5.0,
                       show_dimensions: bool = True) -> None:
    """
    Draw pipe in isometric view
    
    Args:
        fig: Matplotlib figure
        pipe: Pipe specification
        length: Pipe length for visualization
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_iso_axes(fig, f"Isometric View: {pipe.standard} {pipe.nps_or_dn}")
    
    outer_radius = pipe.od / 2
    inner_radius = pipe.id / 2
    
    # Create outer cylinder
    outer_bottom, outer_top = create_cylinder_isometric((0, 0, 0), outer_radius, length, 32)
    
    # Create inner cylinder (hollow)
    inner_bottom, inner_top = create_cylinder_isometric((0, 0, 0), inner_radius, length, 32)
    
    # Transform to isometric
    outer_bottom_iso = isometric_transform(outer_bottom)
    outer_top_iso = isometric_transform(outer_top)
    inner_bottom_iso = isometric_transform(inner_bottom)
    inner_top_iso = isometric_transform(inner_top)
    
    # Draw visible surfaces
    # Outer surface (right side - visible)
    visible_start = len(outer_bottom_iso) // 4
    visible_end = 3 * len(outer_bottom_iso) // 4
    
    for i in range(visible_start, visible_end - 1):
        # Create quad face
        quad = np.array([
            outer_bottom_iso[i],
            outer_bottom_iso[i+1],
            outer_top_iso[i+1],
            outer_top_iso[i]
        ])
        
        # Calculate shading based on normal
        shade_factor = 0.7 + 0.3 * ((i - visible_start) / (visible_end - visible_start))
        color = plt.cm.gray(shade_factor * 0.7)
        
        poly = Polygon(quad, facecolor=color, edgecolor=STEEL_EDGE,
                      linewidth=0.5, alpha=0.9)
        ax.add_patch(poly)
    
    # Draw top ellipse (end cap)
    ax.plot(outer_top_iso[:, 0], outer_top_iso[:, 1],
           color=STEEL_EDGE, linewidth=2)
    ax.fill(outer_top_iso[:, 0], outer_top_iso[:, 1],
           color=STEEL_OUTER, alpha=0.8)
    
    # Draw inner ellipse on top (hollow)
    ax.plot(inner_top_iso[:, 0], inner_top_iso[:, 1],
           color=STEEL_INNER, linewidth=2)
    ax.fill(inner_top_iso[:, 0], inner_top_iso[:, 1],
           color=BG_PRIMARY, alpha=1.0)
    
    # Draw wall thickness ring
    for i in range(len(inner_top_iso) - 1):
        if i % 8 == 0:  # Draw every 8th segment for clarity
            ax.plot([inner_top_iso[i, 0], outer_top_iso[i, 0]],
                   [inner_top_iso[i, 1], outer_top_iso[i, 1]],
                   color=ACCENT_STEEL, linewidth=1, alpha=0.5)
    
    # Draw visible edges
    # Right outer edge
    right_idx = len(outer_bottom_iso) // 2
    ax.plot([outer_bottom_iso[right_idx, 0], outer_top_iso[right_idx, 0]],
           [outer_bottom_iso[right_idx, 1], outer_top_iso[right_idx, 1]],
           color=ACCENT_CYAN, linewidth=2)
    
    # Left outer edge
    left_idx = 0
    ax.plot([outer_bottom_iso[left_idx, 0], outer_top_iso[left_idx, 0]],
           [outer_bottom_iso[left_idx, 1], outer_top_iso[left_idx, 1]],
           color=ACCENT_CYAN, linewidth=2, alpha=0.6)
    
    if show_dimensions:
        # Add dimension lines
        # OD dimension
        mid_top_outer = outer_top_iso[len(outer_top_iso)//2]
        mid_top_inner = inner_top_iso[len(inner_top_iso)//2]
        
        ax.annotate('', xy=(mid_top_outer), xytext=(-mid_top_outer[0], mid_top_outer[1]),
                   arrowprops=dict(arrowstyle='<->', color=ACCENT_CYAN, lw=2))
        ax.text(0, mid_top_outer[1] + 0.3,
               f'OD = {pipe.od:.3f} {"in" if pipe.standard == "ASME" else "mm"}',
               ha='center', color=ACCENT_CYAN, fontweight='bold',
               fontsize=FONT_SIZE_NORMAL,
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Length dimension
        length_y_offset = outer_bottom_iso[right_idx, 1] - 0.5
        ax.annotate('', xy=(outer_top_iso[right_idx, 0], outer_top_iso[right_idx, 1]),
                   xytext=(outer_bottom_iso[right_idx, 0], outer_bottom_iso[right_idx, 1]),
                   arrowprops=dict(arrowstyle='<->', color=ACCENT_GOLD, lw=2))
        ax.text(outer_top_iso[right_idx, 0] + 0.5,
               (outer_top_iso[right_idx, 1] + outer_bottom_iso[right_idx, 1]) / 2,
               f'L = {length:.1f} {"in" if pipe.standard == "ASME" else "mm"}',
               ha='left', color=ACCENT_GOLD, fontweight='bold',
               fontsize=FONT_SIZE_SMALL,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Info box
    info_text = f"Schedule: {pipe.schedule}\nWT: {pipe.wall_thickness:.3f} {'in' if pipe.standard == 'ASME' else 'mm'}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    # Set limits
    ax.set_xlim(-outer_radius * 3, outer_radius * 3)
    ax.set_ylim(-outer_radius * 2, length + outer_radius * 2)
    
    plt.tight_layout()


def draw_bend_isometric(fig: Figure, bend: BendSpec,
                       show_dimensions: bool = True) -> None:
    """
    Draw 90° elbow in isometric view
    
    Args:
        fig: Matplotlib figure
        bend: Bend specification
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_iso_axes(fig, f"Isometric Elbow: {bend.nps_or_dn} {bend.radius_type}")
    
    outer_radius = bend.od / 2
    center_radius = bend.radius
    
    # Create elbow path
    num_points = 32
    angles = np.linspace(0, np.pi/2, num_points)
    
    # Elbow center line path
    center_x = center_radius * np.cos(angles)
    center_y = np.zeros_like(angles)
    center_z = center_radius * np.sin(angles)
    
    # Create pipe cross-sections along the path
    num_cross_sections = 8
    selected_indices = np.linspace(0, num_points-1, num_cross_sections, dtype=int)
    
    for i, idx in enumerate(selected_indices):
        angle = angles[idx]
        
        # Create circular cross-section
        theta = np.linspace(0, 2*np.pi, 16)
        
        # Local coordinate system at this point on the bend
        # Tangent direction
        if idx < num_points - 1:
            tangent = np.array([
                center_x[idx+1] - center_x[idx],
                0,
                center_z[idx+1] - center_z[idx]
            ])
        else:
            tangent = np.array([
                center_x[idx] - center_x[idx-1],
                0,
                center_z[idx] - center_z[idx-1]
            ])
        tangent = tangent / np.linalg.norm(tangent)
        
        # Create circle perpendicular to tangent
        # Simple approximation: circle in y-plane rotated to follow bend
        for r in [outer_radius]:
            circle_y = r * np.cos(theta)
            circle_r = r * np.sin(theta)
            
            # Rotate circle to be perpendicular to path
            circle_3d = np.column_stack([
                center_x[idx] + circle_r * np.cos(angle),
                circle_y,
                center_z[idx] + circle_r * np.sin(angle)
            ])
            
            circle_iso = isometric_transform(circle_3d)
            
            # Color based on position
            shade = 0.5 + 0.5 * (i / len(selected_indices))
            color = plt.cm.gray(shade * 0.7)
            
            ax.plot(circle_iso[:, 0], circle_iso[:, 1],
                   color=STEEL_EDGE, linewidth=1.5, alpha=0.8)
            ax.fill(circle_iso[:, 0], circle_iso[:, 1],
                   color=color, alpha=0.6)
    
    # Draw center line
    center_3d = np.column_stack([center_x, center_y, center_z])
    center_iso = isometric_transform(center_3d)
    ax.plot(center_iso[:, 0], center_iso[:, 1],
           '--', color=ACCENT_CYAN, linewidth=2, label='Center Line')
    
    if show_dimensions:
        # Radius dimension
        mid_idx = len(center_iso) // 2
        origin_iso = isometric_transform(np.array([[0, 0, 0]]))[0]
        
        ax.plot([origin_iso[0], center_iso[mid_idx, 0]],
               [origin_iso[1], center_iso[mid_idx, 1]],
               'o-', color=ACCENT_GOLD, linewidth=2, markersize=4)
        ax.text(center_iso[mid_idx, 0] * 0.5, center_iso[mid_idx, 1] * 0.5,
               f'R = {center_radius:.2f} {"in" if bend.standard == "ASME" else "mm"}',
               ha='center', color=ACCENT_GOLD, fontweight='bold',
               fontsize=FONT_SIZE_NORMAL,
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Info box
    info_text = f"Type: {bend.radius_type}\nOD: {bend.od:.3f} {'in' if bend.standard == 'ASME' else 'mm'}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    # Set limits
    max_dim = max(center_radius, outer_radius) * 1.5
    ax.set_xlim(-max_dim * 0.3, max_dim * 1.2)
    ax.set_ylim(-outer_radius * 2, max_dim * 1.2)
    
    plt.tight_layout()


def draw_flange_isometric(fig: Figure, flange: FlangeSpec,
                         show_dimensions: bool = True) -> None:
    """
    Draw flange in isometric view
    
    Args:
        fig: Matplotlib figure
        flange: Flange specification
        show_dimensions: Whether to show dimension labels
    """
    ax = setup_iso_axes(fig, 
                       f"Isometric Flange: {flange.standard} {flange.nps_or_dn} Class {flange.pressure_class}")
    
    outer_radius = flange.od / 2
    thickness = flange.thickness
    bolt_circle_radius = flange.bolt_circle_dia / 2
    bolt_radius = flange.bolt_size / 2
    
    # Create flange body (disk)
    num_segments = 64
    theta = np.linspace(0, 2*np.pi, num_segments + 1)
    
    # Bottom circle
    bottom_x = outer_radius * np.cos(theta)
    bottom_y = np.zeros_like(theta)
    bottom_z = outer_radius * np.sin(theta)
    bottom_3d = np.column_stack([bottom_x, bottom_y, bottom_z])
    bottom_iso = isometric_transform(bottom_3d)
    
    # Top circle
    top_3d = bottom_3d.copy()
    top_3d[:, 1] = thickness
    top_iso = isometric_transform(top_3d)
    
    # Draw top face
    ax.fill(top_iso[:, 0], top_iso[:, 1],
           color=STEEL_OUTER, alpha=0.9, edgecolor=STEEL_EDGE, linewidth=2)
    
    # Draw raised face (smaller circle on top)
    raised_radius = outer_radius * 0.6
    raised_x = raised_radius * np.cos(theta)
    raised_z = raised_radius * np.sin(theta)
    raised_3d = np.column_stack([raised_x, np.full_like(theta, thickness), raised_z])
    raised_iso = isometric_transform(raised_3d)
    ax.plot(raised_iso[:, 0], raised_iso[:, 1],
           color=ACCENT_CYAN, linewidth=2)
    
    # Draw bolt holes on top face
    for i in range(flange.num_bolts):
        angle = 2 * np.pi * i / flange.num_bolts
        bolt_x = bolt_circle_radius * np.cos(angle)
        bolt_z = bolt_circle_radius * np.sin(angle)
        
        # Create small circle for bolt hole
        bolt_theta = np.linspace(0, 2*np.pi, 16)
        hole_x = bolt_x + bolt_radius * np.cos(bolt_theta)
        hole_y = np.full_like(bolt_theta, thickness)
        hole_z = bolt_z + bolt_radius * np.sin(bolt_theta)
        hole_3d = np.column_stack([hole_x, hole_y, hole_z])
        hole_iso = isometric_transform(hole_3d)
        
        ax.fill(hole_iso[:, 0], hole_iso[:, 1],
               color=BG_PRIMARY, edgecolor=ACCENT_GOLD, linewidth=1.5)
    
    # Draw visible side surface (partial)
    visible_start = num_segments // 4
    visible_end = 3 * num_segments // 4
    
    for i in range(visible_start, visible_end - 1, 4):
        # Draw vertical edge lines
        ax.plot([bottom_iso[i, 0], top_iso[i, 0]],
               [bottom_iso[i, 1], top_iso[i, 1]],
               color=STEEL_EDGE, linewidth=0.5, alpha=0.5)
    
    # Draw outer edge lines
    right_idx = num_segments // 2
    ax.plot([bottom_iso[right_idx, 0], top_iso[right_idx, 0]],
           [bottom_iso[right_idx, 1], top_iso[right_idx, 1]],
           color=ACCENT_CYAN, linewidth=2, alpha=0.8)
    
    if show_dimensions:
        # OD dimension
        mid_top = top_iso[len(top_iso)//2]
        ax.annotate('', xy=(mid_top), xytext=(-mid_top[0], mid_top[1]),
                   arrowprops=dict(arrowstyle='<->', color=ACCENT_CYAN, lw=2))
        ax.text(0, mid_top[1] + 0.5,
               f'OD = {flange.od:.2f} {"in" if flange.standard == "ASME" else "mm"}',
               ha='center', color=ACCENT_CYAN, fontweight='bold',
               fontsize=FONT_SIZE_NORMAL,
               bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
        
        # Thickness dimension
        edge_idx = right_idx
        ax.plot([bottom_iso[edge_idx, 0], top_iso[edge_idx, 0]],
               [bottom_iso[edge_idx, 1], top_iso[edge_idx, 1]],
               'o-', color=ACCENT_GOLD, linewidth=2, markersize=4)
        ax.text(bottom_iso[edge_idx, 0] + 0.5,
               (bottom_iso[edge_idx, 1] + top_iso[edge_idx, 1]) / 2,
               f't = {thickness:.2f}',
               ha='left', color=ACCENT_GOLD, fontweight='bold',
               fontsize=FONT_SIZE_SMALL,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Info box
    info_text = f"Bolts: {flange.num_bolts} × {flange.bolt_size:.1f}{'″' if flange.standard == 'ASME' else 'mm'}\nPressure: Class {flange.pressure_class}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=FONT_SIZE_SMALL,
           color=TEXT_SECONDARY,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor=BG_SECONDARY, alpha=0.8))
    
    # Set limits
    max_dim = outer_radius * 1.5
    ax.set_xlim(-max_dim, max_dim)
    ax.set_ylim(-outer_radius, thickness + outer_radius * 1.5)
    
    plt.tight_layout()
