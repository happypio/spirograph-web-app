import numpy as np

from src.shapes import Circle, Shape


class CircleMotion:

    def __init__(
        self,
        orbit: Shape,
        circle: Circle,
        distance_to_border: float,
        outer: bool,
        quality: int = 5000,
    ):
        """
        Initialize CircleMotion object.

        Parameters:
            orbit (Shape): The shape representing the orbit.
            circle (Circle): The moving circle.
            distance_to_border (float): Distance from the point (pen, or hole in the circle) to the border of the circle.
            outer (bool): Flag indicating whether the circle moves outer or inner the orbit.
            quality (int, optional): Number of points used for calculation. Default is 5000.
        """

        self.orbit = orbit
        self.circle = circle

        self.distance_to_border = distance_to_border
        self.quality = quality

        self.x_range = self.orbit.x_range + 2 * self.circle.x_range
        self.y_range = self.orbit.y_range + 2 * self.circle.y_range

        self.set_up_direction(outer)
        self.calculate_point_movement()

    def set_up_direction(self, outer):
        """
        Set up direction of the motion.

        Parameters:
            outer (bool): Flag indicating whether the circle moves outer or inner the orbit.
        """

        self.direction = -1
        if outer:
            self.direction = 1

        self.orbit_speed = 1
        self.circle_speed = (
            self.direction
            * self.orbit.circumference(self.direction * self.circle.radius)
            / self.circle.circumference(0)
        )

    def calculate_trajectory(
        self, t: float | np.ndarray, distance_to_border: float
    ) -> tuple[float, float] | tuple[np.ndarray, np.ndarray]:
        """
        Calculate trajectory of the moving circle at time t.

        Parameters:
            t (float or np.ndarray): Time parameter or list of time parameters.
            distance_to_border (float): Distance from the center of the orbit to the border of the circle.

        Returns:
            tuple[float, float, float, float] or tuple[nd.nparray, nd.nparray, nd.nparray, nd.nparray] :
                Tuple containing floats or nd.nparrays (depending on what was parameter t),
                x and y coordinates of the trajectory, and x_center and y_center coordinates of the orbit.

        """
        x_center, y_center = self.orbit.parametric_equation(
            t, self.orbit_speed, self.direction * self.circle.radius
        )
        x, y = self.circle.parametric_equation(
            t, self.circle_speed, -1 * distance_to_border
        )

        x += x_center
        y += y_center

        return x, y, x_center, y_center

    def calculate_number_of_rotations(self, max_rot: int = 500) -> int:
        """
        Calculate number of rotations around bigger circle needed to converge the drawing.

        Parameters:
            max_rot (int, optional): Maximum number of rotations to check. Default is 500.

        Returns:
            int: Number of rotations needed to converge the drawing.
        """

        x_start, y_start, _, _ = self.calculate_trajectory(
            0, self.distance_to_border
        )

        for i in range(1, max_rot):
            t = 2 * i * np.pi
            x, y, _, _ = self.calculate_trajectory(t, self.distance_to_border)
            if np.isclose(y, y_start) and np.isclose(x, x_start):
                return i

        return 50  # max_rot
        # raise Exception("Could not converge the drawing")

    def calculate_point_movement(self):
        """
        Calculate movement of the point with given quality.
        It generates value_of(quality) points which can be plotted.
        """
        rotations = self.calculate_number_of_rotations()

        thetas = np.linspace(0, rotations * 2 * np.pi, self.quality)

        self.x, self.y, self.x_center, self.y_center = (
            self.calculate_trajectory(thetas, self.distance_to_border)
        )
        return self.x, self.y

    def calculate_circle_position(
        self,
        x: float,
        y: float,
        x_center: float,
        y_center: float,
        N_POINTS: int = 10,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculate position of N_POINTS on the circle based on current position of the point (x,y) and the circle center.

        Parameters:
            x (float): x coordinate of the point.
            y (float): y coordinate of the point.
            x_center (float): x coordinate of the circle center.
            y_center (float): y coordinate of the circle center.
            N_POINTS (int, optional): Number of points on the circle. Default is 10.

        Returns:
            tuple[np.ndarray, np.ndarray]: Tuple containing list of x and list of y coordinates of the circle positions.
        """
        start_angle = np.arctan2(y - y_center, x - x_center)
        thetas = np.linspace(start_angle, start_angle + 2 * np.pi, N_POINTS)

        x, y = self.circle.parametric_equation(
            thetas, 1, -self.distance_to_border
        )
        x += x_center
        y += y_center

        return x, y

    def calculate_circle_movement(
        self,
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """
        Calculate movement of the circle.

        Returns:
            tuple: Tuple containing lists of numpy ndarrays representing x and y
            coordinates of the circle movement.
        """
        xs, ys = [], []
        for x, y, x_center, y_center in zip(
            self.x, self.y, self.x_center, self.y_center
        ):
            x_circle, y_circle = self.calculate_circle_position(
                x, y, x_center, y_center
            )
            xs.append(x_circle)
            ys.append(y_circle)
        return xs, ys
