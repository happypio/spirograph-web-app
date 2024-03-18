from pathlib import Path

import numpy as np

from src.motions import CircleMotion
from src.shapes import Shape


class DrawController:
    """Manages drawing parameters and generates HTML view."""

    def __init__(
        self,
        orbit: Shape,
        motions: list[CircleMotion],
        drawing_speed: int,
        show_borders: bool,
        animate: bool,
        html_file: str,
    ):
        """
        Initialize DrawController object.

        Parameters:
            orbit (Shape): Orbit object representing the spirograph orbit.
            motions (List[CircleMotion]): List of CircleMotion objects representing the movements of circles.
            drawing_speed (int): Speed of drawing.
            show_borders (bool): Boolean indicating whether to show orbit borders.
            animate (bool): Boolean indicating whether to animate the drawing.
            html_file (str): Path to the HTML file template.
        """
        self.orbit = orbit
        self.motions = motions
        self.drawing_speed = drawing_speed
        self.show_borders = show_borders
        self.animate = animate
        self.html_file = Path(html_file).read_text()

    def get_borders(self) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """
        Get borders of the orbit.

        Returns:
            tuple[list[np.ndarray], list[np.ndarray]]: Tuple containing list of x and list of y coordinates of the orbit's borders.
        """
        if self.show_borders:
            xs, ys = self.orbit.get_borders()
            return list(xs), list(ys)
        else:
            return [], []

    def get_circles_animations(
        self,
    ) -> tuple[list[list[list[float]]], list[list[list[float]]]]:
        """
        Get orbiting circles animations.

        Returns:
            tuple[list[list[list[float]]], list[list[list[float]]]]:
                Tuple containing lists of animations of each orbiting circle.
                Each animation is a list of list[floats] - each lists[floats] represents position in time of orbiting circle.
        """
        circles_xs, circles_ys = [], []
        for m in self.motions:
            xs, ys = m.calculate_circle_movement()
            xs = list(map(list, xs))
            ys = list(map(list, ys))
            circles_xs.append(xs)
            circles_ys.append(ys)
        return circles_xs, circles_ys

    def get_points_movements(
        self,
    ) -> tuple[list[list[float]], list[list[float]]]:
        """
        Get point (drawing pen) animations.

        Returns:
            tuple[list[list[float]], list[list[float]]]:
                Tuple containing lists of animations of each pen in orbiting circle.
                Each animation is a list[floats] - lists[floats] represents subsequent positions in time of pen in orbiting circle.
        """
        movements_x, movements_y = [], []
        for m in self.motions:
            xs, ys = m.calculate_point_movement()
            movements_x.append(list(xs))
            movements_y.append(list(ys))
        return movements_x, movements_y

    def get_colors(self) -> list[int]:
        """
        Get colors of circles.

        Returns:
            list[int]: list containing colors of circles.
        """
        colors = []
        for m in self.motions:
            colors.append(m.circle.color)

        return colors

    def get_ranges(self) -> tuple[list[float], list[float]]:
        """
        Get ranges of x and y coordinates.

        Returns:
            tuple[list[float], list[float]]: Tuple containing x and y ranges.
        """
        x_range, y_range = 0, 0
        for m in self.motions:
            if m.x_range > x_range:
                x_range = m.x_range
            if m.y_range > y_range:
                y_range = m.y_range

        return [-x_range, x_range], [-y_range, y_range]

    def prepare_parameters(self) -> list:
        """
        Prepare parameters for the HTML template.

        Returns:
            list: List of prepared parameters.
        """
        b_x, b_y = self.get_borders()
        circles_xs, circles_ys = self.get_circles_animations()
        movements_x, movements_y = self.get_points_movements()
        border_color = self.orbit.color
        movements_colors = self.get_colors()
        x_ranges, y_ranges = self.get_ranges()

        num_parameters = [
            self.show_borders,
            self.animate,
            self.drawing_speed,
        ]
        str_parameterts = list(
            map(
                str,
                [
                    border_color,
                    x_ranges,
                    y_ranges,
                    movements_colors,
                    b_x,
                    b_y,
                    circles_xs,
                    circles_ys,
                    movements_x,
                    movements_y,
                ],
            )
        )

        return num_parameters + str_parameterts

    def submit_parameters(self) -> str:
        """
        Submit prepared parameters.

        Returns:
            str: Prepared HTML file.
        """
        prepared_html_file = self.html_file % tuple(self.prepare_parameters())

        return prepared_html_file
