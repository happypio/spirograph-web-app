from abc import ABC, abstractmethod

import numpy as np


class Shape(ABC):
    @abstractmethod
    def get_borders(self, quality: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Abstract method to calculate the borders of a shape.

        Parameters:
            quality (int): The number of points to generate along the border.

        Returns:
            tuple: Tuple containing the x and y coordinates of the shape's border.
        """
        pass

    @abstractmethod
    def parametric_equation(
        self,
        t: float | np.ndarray,
        speed: float,
        distance_to_border: float,
    ) -> tuple[float, float] | tuple[np.ndarray, np.ndarray]:
        """
        Abstract method to define the parametric equation of a shape.

        Parameters:
            t (float or np.ndarray): Parameter value or list of values for the parametric equation.
            speed (float): Speed factor for the parametric equation.
            distance_to_border (float): Distance from the point (pen, or hole in the shape) to the border of the shape.

        Returns:
            tuple: Tuple containing the x and y coordinates calculated by the parametric equation.
            If the t was a ndarray, it will return list of x,y coordinates for each moment.
        """

        pass

    @abstractmethod
    def circumference(self, distance_to_border: float) -> float:
        """
        Abstract method to calculate the circumference of a shape.

        Parameters:
            distance_to_border (float): Distance from the point (pen, or hole in the shape) to the border of the shape.

        Returns:
            float: Circumference of the shape.
        """
        pass


class Circle(Shape):
    def __init__(self, radius: float, color: str):
        """
        Initialize a Circle object.

        Parameters:
            radius (float): The radius of the circle.
            color (str): The color of the circle.
        """
        self.radius = radius
        self.color = color
        self.x_range = self.radius
        self.y_range = self.radius

    def get_borders(self, quality: int = 100) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculate the borders of the circle.

        It overrides the abstract method get_borders.
        """
        thetas = np.linspace(0, 2 * np.pi, quality)
        return self.parametric_equation(thetas, speed=1, distance_to_border=0)

    def parametric_equation(
        self,
        t: float | np.ndarray,
        speed: float,
        distance_to_border: float,
    ) -> tuple[float, float] | tuple[np.ndarray, np.ndarray]:
        """
        Define the parametric equation of the circle.

        It overrides the abstract method parametric_equation.
        """
        x = (self.radius + distance_to_border) * np.cos(speed * t)
        y = (self.radius + distance_to_border) * np.sin(speed * t)
        return x, y

    def circumference(self, distance_to_border: float) -> float:
        """
        Calculate the circumference of the circle.

        It overrides the abstract method circumference.
        """
        return 2 * np.pi * (self.radius + distance_to_border)


class Elipse(Shape):
    def __init__(self, a: float, b: float, color: int):
        """
        Initialize an Ellipse object.

        Parameters:
            a (float): The length of the major axis of the ellipse.
            b (float): The length of the minor axis of the ellipse.
            color (int): The color of the ellipse.
        """
        self.a = a
        self.b = b
        self.color = color

        self.x_range = self.a
        self.y_range = self.b

    def get_borders(self, quality: int = 100) -> tuple:
        """
        Calculate the borders of the ellipse.

        It overrides the abstract method get_borders.
        """
        thetas = np.linspace(0, 2 * np.pi, quality)
        return self.parametric_equation(thetas, speed=1, distance_to_border=0)

    def parametric_equation(
        self,
        t: float | np.ndarray,
        speed: float,
        distance_to_border: float,
    ) -> tuple[float, float] | tuple[np.ndarray, np.ndarray]:
        """
        Define the parametric equation of the circle.

        It overrides the abstract method parametric_equation.
        """

        x = (self.a + distance_to_border) * np.cos(speed * t)
        y = (self.b + distance_to_border) * np.sin(speed * t)
        return x, y

    def circumference(self, distance_to_border: float) -> float:
        """
        Calculate the circumference of the circle using Ramanuja Formula.

        It overrides the abstract method circumference.
        """
        return np.pi * (
            3 * (self.a + self.b + 2 * distance_to_border)
            - np.sqrt(
                (
                    3 * (self.a + distance_to_border)
                    + self.b
                    + distance_to_border
                )
                * (
                    self.a
                    + distance_to_border
                    + 3 * (self.b + distance_to_border)
                )
            )
        )
