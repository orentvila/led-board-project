#!/usr/bin/env python3
"""
3D Cube Animation for LED Board
Features rotating 3D cube with perspective projection
"""

import time
import numpy as np
import math
from .base_animation import BaseAnimation
import config

class Cube3DAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the 3D cube animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'cube_edge': (255, 255, 255),    # White cube edges
            'cube_face1': (255, 100, 100),  # Red face
            'cube_face2': (100, 255, 100),  # Green face
            'cube_face3': (100, 100, 255),  # Blue face
            'cube_face4': (255, 255, 100),  # Yellow face
            'cube_face5': (255, 100, 255),  # Magenta face
            'cube_face6': (100, 255, 255),  # Cyan face
        }
        
        # 3D cube vertices (8 corners)
        self.cube_vertices = np.array([
            [-1, -1, -1],  # 0: bottom-left-back
            [ 1, -1, -1],  # 1: bottom-right-back
            [ 1,  1, -1],  # 2: top-right-back
            [-1,  1, -1],  # 3: top-left-back
            [-1, -1,  1],  # 4: bottom-left-front
            [ 1, -1,  1],  # 5: bottom-right-front
            [ 1,  1,  1],  # 6: top-right-front
            [-1,  1,  1],  # 7: top-left-front
        ])
        
        # Cube faces (6 faces, each with 4 vertices)
        self.cube_faces = [
            [0, 1, 2, 3],  # Back face
            [4, 7, 6, 5],  # Front face
            [0, 4, 5, 1],  # Bottom face
            [2, 6, 7, 3],  # Top face
            [0, 3, 7, 4],  # Left face
            [1, 5, 6, 2],  # Right face
        ]
        
        # Face colors
        self.face_colors = [
            self.colors['cube_face1'],  # Back
            self.colors['cube_face2'],  # Front
            self.colors['cube_face3'],  # Bottom
            self.colors['cube_face4'],  # Top
            self.colors['cube_face5'],  # Left
            self.colors['cube_face6'],  # Right
        ]
        
        # Animation parameters
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.scale = 8
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
    def rotate_point(self, point, rx, ry, rz):
        """Rotate a 3D point around X, Y, and Z axes."""
        x, y, z = point
        
        # Rotation around X axis
        cos_x, sin_x = math.cos(rx), math.sin(rx)
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
        
        # Rotation around Y axis
        cos_y, sin_y = math.cos(ry), math.sin(ry)
        x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
        
        # Rotation around Z axis
        cos_z, sin_z = math.cos(rz), math.sin(rz)
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
        
        return np.array([x, y, z])
    
    def project_3d_to_2d(self, point_3d):
        """Project 3D point to 2D screen coordinates."""
        x, y, z = point_3d
        
        # Simple perspective projection
        if z > -0.1:  # Avoid division by zero
            z = -0.1
        
        # Perspective projection
        screen_x = int(self.center_x + (x * self.scale) / (-z + 2))
        screen_y = int(self.center_y + (y * self.scale) / (-z + 2))
        
        return (screen_x, screen_y)
    
    def get_face_normal(self, face_vertices):
        """Calculate the normal vector of a face to determine visibility."""
        if len(face_vertices) < 3:
            return np.array([0, 0, 0])
        
        # Get three points of the face
        p1, p2, p3 = face_vertices[0], face_vertices[1], face_vertices[2]
        
        # Calculate two edge vectors
        edge1 = p2 - p1
        edge2 = p3 - p1
        
        # Cross product to get normal
        normal = np.cross(edge1, edge2)
        
        # Normalize
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm
        
        return normal
    
    def draw_line(self, frame, p1, p2, color):
        """Draw a line between two points."""
        x1, y1 = p1
        x2, y2 = p2
        
        # Handle edge cases
        if x1 == x2 and y1 == y2:
            # Single point
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                frame[y1, x1] = color
            return
        
        if x1 == x2:
            # Vertical line
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2 + 1):
                if 0 <= x1 < self.width and 0 <= y < self.height:
                    frame[y, x1] = color
            return
        
        if y1 == y2:
            # Horizontal line
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                if 0 <= x < self.width and 0 <= y1 < self.height:
                    frame[y1, x] = color
            return
        
        # General line drawing algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        if dx > dy:
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            for x in range(x1, x2 + 1):
                y = int(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = color
        else:
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            for y in range(y1, y2 + 1):
                x = int(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = color
    
    def draw_face(self, frame, face_vertices, color):
        """Draw a filled face."""
        if len(face_vertices) < 3:
            return
        
        # Simple polygon filling
        # Get bounding box
        xs = [v[0] for v in face_vertices]
        ys = [v[1] for v in face_vertices]
        
        min_x, max_x = int(min(xs)), int(max(xs))
        min_y, max_y = int(min(ys)), int(max(ys))
        
        # Fill the polygon
        for y in range(max(0, min_y), min(self.height, max_y + 1)):
            for x in range(max(0, min_x), min(self.width, max_x + 1)):
                if self.point_in_polygon(x, y, face_vertices):
                    frame[y, x] = color
    
    def point_in_polygon(self, x, y, vertices):
        """Check if a point is inside a polygon."""
        n = len(vertices)
        inside = False
        
        p1x, p1y = vertices[0]
        for i in range(1, n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def create_cube_frame(self):
        """Create a single frame of the rotating 3D cube."""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Rotate all vertices
        rotated_vertices = []
        for vertex in self.cube_vertices:
            rotated = self.rotate_point(vertex, self.rotation_x, self.rotation_y, self.rotation_z)
            rotated_vertices.append(rotated)
        
        # Project to 2D
        projected_vertices = []
        for vertex in rotated_vertices:
            screen_pos = self.project_3d_to_2d(vertex)
            projected_vertices.append(screen_pos)
        
        # Draw faces (back to front for proper depth)
        face_depths = []
        for i, face in enumerate(self.cube_faces):
            face_vertices_3d = [rotated_vertices[j] for j in face]
            face_vertices_2d = [projected_vertices[j] for j in face]
            
            # Calculate face depth (average Z)
            avg_z = sum(vertex[2] for vertex in face_vertices_3d) / len(face_vertices_3d)
            face_depths.append((i, avg_z, face_vertices_2d))
        
        # Sort faces by depth (back to front)
        face_depths.sort(key=lambda x: x[1])
        
        # Draw faces
        for face_idx, depth, face_vertices_2d in face_depths:
            # Check if face is visible (normal pointing towards camera)
            face_vertices_3d = [rotated_vertices[j] for j in self.cube_faces[face_idx]]
            normal = self.get_face_normal(face_vertices_3d)
            
            # Face is visible if normal Z component is positive
            if normal[2] > 0:
                color = self.face_colors[face_idx]
                self.draw_face(frame, face_vertices_2d, color)
        
        # Draw edges
        for face in self.cube_faces:
            for i in range(len(face)):
                p1 = projected_vertices[face[i]]
                p2 = projected_vertices[face[(i + 1) % len(face)]]
                self.draw_line(frame, p1, p2, self.colors['cube_edge'])
        
        return frame
    
    def run(self, duration=30):
        """Run the 3D cube animation."""
        print(f"🎲 Starting 3D Cube animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Create frame
            frame = self.create_cube_frame()
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update rotation
            self.rotation_x += 0.02
            self.rotation_y += 0.03
            self.rotation_z += 0.01
            
            # Keep rotations in range
            self.rotation_x = self.rotation_x % (2 * math.pi)
            self.rotation_y = self.rotation_y % (2 * math.pi)
            self.rotation_z = self.rotation_z % (2 * math.pi)
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🎲 3D Cube animation completed ({frame_count} frames)")
        self.cleanup()
