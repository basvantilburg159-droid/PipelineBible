"""
Pipe Standards Pro v12 - 3D Visualization
Interactive 3D views using matplotlib 3D toolkit
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.figure import Figure
import numpy as np
from typing import Tuple
from constants import *
from data_models import PipeSpec, BendSpec, FlangeSpec


def setup_3d_axes(fig: Figure, title: str = "") -> Axes3D:
    """Setup 3D matplotlib axes with dark theme"""
    fig.patch.set_facecolor(BG_PRIMARY)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(BG_SECONDARY)
    
    if title:
        ax.set_title(title, color=TEXT_PRIMARY,
                    fontsize=FONT_SIZE_SUBHEADER, pad=15)
    
    # Style panes
    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_facecolor((0.1, 0.1, 0.15, 0.3))
    ax.yaxis.pane.set_facecolor((0.1, 0.1, 0.15, 0.3))
    ax.zaxis.pane.set_facecolor((0.1, 0.1, 0.15, 0.3))
    
    # Style grid
    ax.grid(True, alpha=0.2, color=TEXT_DISABLED)
    
    # Style axes
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=FONT_SIZE_SMALL)
    ax.xaxis.label.set_color(TEXT_SECONDARY)
    ax.yaxis.label.set_color(TEXT_SECONDARY)
    ax.zaxis.label.set_color(TEXT_SECONDARY)
    
    return ax


def create_cylinder_mesh(center: Tuple[float, float, float],
                        radius: float, height: float,
                        num_segments: int = 32) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create 3D cylinder mesh
    
    Args:
        center: (x, y, z) center point
        radius: Cylinder radius
        height: Cylinder height along y-axis
        num_segments: Number of segments around circumference
    
    Returns:
        Tuple of (X, Y, Z) mesh arrays
    """
    cx, cy, cz = center
    
    # Create circle points
    theta = np.linspace(0, 2*np.pi, num_segments)
    y = np.array([cy, cy + height])
    
    # Create mesh grid
    Theta, Y = np.meshgrid(theta, y)
    X = cx + radius * np.cos(Theta)
    Z = cz + radius * np.sin(Theta)
    
    return X, Y, Z


def create_torus_segment(center: Tuple[float, float, float],
                        major_radius: float, minor_radius: float,
                        angle_range: Tuple[float, float] = (0, np.pi/2),
                        num_segments: int = 32) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create torus segment mesh (for bends)
    
    Args:
        center: (x, y, z) center point
        major_radius: Torus major radius (center line radius)
        minor_radius: Torus minor radius (pipe radius)
        angle_range: (start_angle, end_angle) for bend
        num_segments: Number of segments
    
    Returns:
        Tuple of (X, Y, Z) mesh arrays
    """
    cx, cy, cz = center
    
    # Parametric angles
    u = np.linspace(angle_range[0], angle_range[1], num_segments)  # Along bend
    v = np.linspace(0, 2*np.pi, num_segments)  # Around pipe
    
    U, V = np.meshgrid(u, v)
    
    # Torus parametric equations
    X = cx + (major_radius + minor_radius * np.cos(V)) * np.cos(U)
    Y = cy + minor_radius * np.sin(V)
    Z = cz + (major_radius + minor_radius * np.cos(V)) * np.sin(U)
    
    return X, Y, Z


def draw_pipe_3d(fig: Figure, pipe: PipeSpec, length: float = 5.0,
                show_cutaway: bool = True) -> None:
    """
    Draw pipe in 3D with optional cutaway view
    
    Args:
        fig: Matplotlib figure
        pipe: Pipe specification
        length: Pipe length for visualization
        show_cutaway: Show cutaway to reveal wall thickness
    """
    ax = setup_3d_axes(fig, f"3D View: {pipe.standard} {pipe.nps_or_dn}")
    
    outer_radius = pipe.od / 2
    inner_radius = pipe.id / 2
    
    # Create outer cylinder
    X_outer, Y_outer, Z_outer = create_cylinder_mesh((0, 0, 0), outer_radius, length, 48)
    
    # Create inner cylinder
    X_inner, Y_inner, Z_inner = create_cylinder_mesh((0, 0, 0), inner_radius, length, 48)
    
    if show_cutaway:
        # Show only half of the pipe (cutaway view)
        # Mask the back half
        mask = X_outer >= 0
        X_outer_vis = np.where(mask, X_outer, np.nan)
        Z_outer_vis = np.where(mask, Z_outer, np.nan)
        
        mask_inner = X_inner >= 0
        X_inner_vis = np.where(mask_inner, X_inner, np.nan)
        Z_inner_vis = np.where(mask_inner, Z_inner, np.nan)
        
        # Plot outer surface
        ax.plot_surface(X_outer_vis, Y_outer, Z_outer_vis,
                       color=STEEL_OUTER, alpha=0.9,
                       edgecolor=STEEL_EDGE, linewidth=0.3,
                       shade=True)
        
        # Plot inner surface
        ax.plot_surface(X_inner_vis, Y_inner, Z_inner_vis,
                       color=STEEL_INNER, alpha=0.8,
                       edgecolor=STEEL_EDGE, linewidth=0.3,
                       shade=True)
        
        # Draw cut face at x=0 plane
        # Create rectangle for the cut face
        theta = np.linspace(0, 2*np.pi, 48)
        
        # Bottom cut face
        for y_pos in [0, length]:
            # Outer ring
            x_ring_outer = np.zeros_like(theta)
            y_ring_outer = np.full_like(theta, y_pos)
            z_ring_outer_out = outer_radius * np.cos(theta)
            w_ring_outer_out = outer_radius * np.sin(theta)
            
            # Filter to visible half
            visible = w_ring_outer_out >= 0
            ax.plot(x_ring_outer[visible], y_ring_outer[visible], z_ring_outer_out[visible],
                   color=STEEL_EDGE, linewidth=2)
            
            # Inner ring
            z_ring_inner = inner_radius * np.cos(theta)
            w_ring_inner = inner_radius * np.sin(theta)
            visible_inner = w_ring_inner >= 0
            ax.plot(x_ring_outer[visible_inner], y_ring_outer[visible_inner], z_ring_inner[visible_inner],
                   color=ACCENT_CYAN, linewidth=2)
            
            # Fill the annulus (wall thickness)
            # Create vertices for the cut face
            n_segments = 24
            theta_half = np.linspace(0, np.pi, n_segments)
            for i in range(n_segments - 1):
                t1, t2 = theta_half[i], theta_half[i+1]
                verts = [
                    [0, y_pos, outer_radius * np.cos(t1), outer_radius * np.sin(t1)],
                    [0, y_pos, outer_radius * np.cos(t2), outer_radius * np.sin(t2)],
                    [0, y_pos, inner_radius * np.cos(t2), inner_radius * np.sin(t2)],
                    [0, y_pos, inner_radius * np.cos(t1), inner_radius * np.sin(t1)],
                ]
                # Convert 4D to 3D by taking x, y, z (using cos for z)
                verts_3d = [[v[0], v[1], v[2]] for v in verts]
                poly = Poly3DCollection([verts_3d], alpha=0.7,
                                       facecolor=STEEL_OUTER,
                                       edgecolor=STEEL_EDGE,
                                       linewidth=0.5)
                ax.add_collection3d(poly)
    else:
        # Show full pipe
        ax.plot_surface(X_outer, Y_outer, Z_outer,
                       color=STEEL_OUTER, alpha=0.9,
                       edgecolor=STEEL_EDGE, linewidth=0.3,
                       shade=True)
    
    # Add dimension annotations
    # OD annotation
    ax.text(outer_radius * 1.2, 0, 0,
           f'OD: {pipe.od:.3f} {"in" if pipe.standard == "ASME" else "mm"}',
           color=ACCENT_CYAN, fontsize=FONT_SIZE_SMALL,
           bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Length annotation
    ax.text(0, length/2, outer_radius * 1.5,
           f'Length: {length:.1f} {"in" if pipe.standard == "ASME" else "mm"}',
           color=ACCENT_GOLD, fontsize=FONT_SIZE_SMALL,
           bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set equal aspect ratio and limits
    max_dim = max(outer_radius * 2, length)
    ax.set_xlim(-outer_radius * 1.5, outer_radius * 1.5)
    ax.set_ylim(-outer_radius, length + outer_radius)
    ax.set_zlim(-outer_radius * 1.5, outer_radius * 1.5)
    
    ax.set_xlabel('X', fontsize=FONT_SIZE_SMALL)
    ax.set_ylabel('Y (Length)', fontsize=FONT_SIZE_SMALL)
    ax.set_zlabel('Z', fontsize=FONT_SIZE_SMALL)
    
    # Set viewing angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()


def draw_bend_3d(fig: Figure, bend: BendSpec) -> None:
    """
    Draw 90° elbow in 3D
    
    Args:
        fig: Matplotlib figure
        bend: Bend specification
    """
    ax = setup_3d_axes(fig, f"3D Elbow: {bend.nps_or_dn} {bend.radius_type}")
    
    outer_radius = bend.od / 2
    center_radius = bend.radius
    
    # Create torus segment for outer surface
    X_outer, Y_outer, Z_outer = create_torus_segment(
        (0, 0, 0), center_radius, outer_radius, (0, np.pi/2), 32
    )
    
    # Plot outer surface
    ax.plot_surface(X_outer, Y_outer, Z_outer,
                   color=STEEL_OUTER, alpha=0.9,
                   edgecolor=STEEL_EDGE, linewidth=0.3,
                   shade=True)
    
    # Draw center line for reference
    theta_center = np.linspace(0, np.pi/2, 50)
    x_center = center_radius * np.cos(theta_center)
    y_center = np.zeros_like(theta_center)
    z_center = center_radius * np.sin(theta_center)
    
    ax.plot(x_center, y_center, z_center,
           '--', color=ACCENT_CYAN, linewidth=3, label='Center Line')
    
    # Add tangent pipes at ends
    tangent_length = outer_radius * 3
    
    # Entry pipe (along X axis)
    X_entry, Y_entry, Z_entry = create_cylinder_mesh(
        (center_radius, 0, 0), outer_radius, tangent_length, 24
    )
    # Rotate to align with X axis
    Y_entry_rot = Y_entry - tangent_length
    X_entry_rot = X_entry + Y_entry_rot
    Y_entry_rot = np.zeros_like(Y_entry)
    
    ax.plot_surface(X_entry_rot, Y_entry_rot, Z_entry,
                   color=STEEL_OUTER, alpha=0.8,
                   edgecolor=STEEL_EDGE, linewidth=0.3)
    
    # Exit pipe (along Z axis)
    X_exit, Y_exit, Z_exit = create_cylinder_mesh(
        (0, 0, center_radius), outer_radius, tangent_length, 24
    )
    # Rotate to align with Z axis
    Y_exit_rot = Y_exit - tangent_length
    Z_exit_rot = Z_exit + Y_exit_rot
    Y_exit_rot = np.zeros_like(Y_exit)
    
    ax.plot_surface(X_exit, Y_exit_rot, Z_exit_rot,
                   color=STEEL_OUTER, alpha=0.8,
                   edgecolor=STEEL_EDGE, linewidth=0.3)
    
    # Add dimension annotation
    ax.text(center_radius * 0.7, 0, center_radius * 0.7,
           f'R: {center_radius:.2f} {"in" if bend.standard == "ASME" else "mm"}',
           color=ACCENT_GOLD, fontsize=FONT_SIZE_NORMAL,
           bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set limits
    max_dim = center_radius + outer_radius + tangent_length
    ax.set_xlim(-outer_radius, max_dim)
    ax.set_ylim(-outer_radius * 2, outer_radius * 2)
    ax.set_zlim(-outer_radius, max_dim)
    
    ax.set_xlabel('X', fontsize=FONT_SIZE_SMALL)
    ax.set_ylabel('Y', fontsize=FONT_SIZE_SMALL)
    ax.set_zlabel('Z', fontsize=FONT_SIZE_SMALL)
    
    # Set viewing angle
    ax.view_init(elev=25, azim=35)
    
    plt.tight_layout()


def draw_flange_3d(fig: Figure, flange: FlangeSpec, show_bolts: bool = True) -> None:
    """
    Draw flange in 3D
    
    Args:
        fig: Matplotlib figure
        flange: Flange specification
        show_bolts: Whether to render bolt holes
    """
    ax = setup_3d_axes(fig,
                      f"3D Flange: {flange.standard} {flange.nps_or_dn} Class {flange.pressure_class}")
    
    outer_radius = flange.od / 2
    thickness = flange.thickness
    bolt_circle_radius = flange.bolt_circle_dia / 2
    bolt_radius = flange.bolt_size / 2
    
    # Create main flange disk
    X_flange, Y_flange, Z_flange = create_cylinder_mesh(
        (0, 0, 0), outer_radius, thickness, 64
    )
    
    ax.plot_surface(X_flange, Y_flange, Z_flange,
                   color=STEEL_OUTER, alpha=0.9,
                   edgecolor=STEEL_EDGE, linewidth=0.3,
                   shade=True)
    
    # Draw raised face (smaller elevated circle on top)
    raised_radius = outer_radius * 0.6
    raised_height = thickness * 0.1
    X_raised, Y_raised, Z_raised = create_cylinder_mesh(
        (0, thickness, 0), raised_radius, raised_height, 48
    )
    
    ax.plot_surface(X_raised, Y_raised, Z_raised,
                   color=STEEL_INNER, alpha=1.0,
                   edgecolor=STEEL_EDGE, linewidth=0.5,
                   shade=True)
    
    # Draw bolt holes
    if show_bolts:
        for i in range(flange.num_bolts):
            angle = 2 * np.pi * i / flange.num_bolts
            bolt_x = bolt_circle_radius * np.cos(angle)
            bolt_z = bolt_circle_radius * np.sin(angle)
            
            # Create bolt hole cylinder
            X_bolt, Y_bolt, Z_bolt = create_cylinder_mesh(
                (bolt_x, 0, bolt_z), bolt_radius, thickness, 12
            )
            
            ax.plot_surface(X_bolt, Y_bolt, Z_bolt,
                           color=BG_PRIMARY, alpha=1.0,
                           edgecolor=ACCENT_GOLD, linewidth=1)
    
    # Draw center bore
    bore_radius = outer_radius * 0.3
    X_bore, Y_bore, Z_bore = create_cylinder_mesh(
        (0, 0, 0), bore_radius, thickness, 32
    )
    
    ax.plot_surface(X_bore, Y_bore, Z_bore,
                   color=BG_PRIMARY, alpha=1.0,
                   edgecolor=ACCENT_CYAN, linewidth=1)
    
    # Add bolt circle reference line
    theta_bc = np.linspace(0, 2*np.pi, 100)
    x_bc = bolt_circle_radius * np.cos(theta_bc)
    z_bc = bolt_circle_radius * np.sin(theta_bc)
    y_bc = np.full_like(theta_bc, thickness + raised_height + 0.01)
    
    ax.plot(x_bc, y_bc, z_bc, '--', color=ACCENT_CYAN, linewidth=1, alpha=0.5)
    
    # Add dimension annotations
    ax.text(outer_radius * 1.2, thickness/2, 0,
           f'OD: {flange.od:.2f} {"in" if flange.standard == "ASME" else "mm"}',
           color=ACCENT_CYAN, fontsize=FONT_SIZE_SMALL,
           bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    ax.text(0, thickness + raised_height + 0.5, outer_radius * 0.8,
           f'{flange.num_bolts} Bolts\nM{flange.bolt_size:.0f}',
           color=ACCENT_GOLD, fontsize=FONT_SIZE_SMALL,
           bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_PRIMARY, alpha=0.8))
    
    # Set limits
    max_dim = outer_radius * 1.5
    ax.set_xlim(-max_dim, max_dim)
    ax.set_ylim(-thickness, thickness + raised_height + max_dim * 0.5)
    ax.set_zlim(-max_dim, max_dim)
    
    ax.set_xlabel('X', fontsize=FONT_SIZE_SMALL)
    ax.set_ylabel('Y (Thickness)', fontsize=FONT_SIZE_SMALL)
    ax.set_zlabel('Z', fontsize=FONT_SIZE_SMALL)
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()


def enable_interactive_rotation(fig: Figure):
    """
    Enable interactive rotation for 3D plots
    (Automatically handled by matplotlib navigation toolbar)
    """
    # This is handled automatically by matplotlib's 3D toolkit
    # Users can rotate by clicking and dragging
    pass
