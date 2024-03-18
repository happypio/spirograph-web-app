from abc import ABC, abstractmethod

import streamlit as st

from src.const_params import avail_colors
from src.shapes import Circle, Elipse, Shape


class AbstractShapeOrbitView(ABC):

    def __init__(self, orbit_color: int):
        """
        Initialize ShapeOrbitView object.

        Parameters:
            orbit_color (int): The color of the orbit.
        """
        self.orbit_color = orbit_color

    @abstractmethod
    def show_inputs(self):
        """
        Show input elements for selecting orbit properties.
        """
        pass

    def create_orbit(self) -> tuple[Shape, int]:
        """
        Create orbit based on user inputs.

        Returns:
            tuple[Shape, int]: Tuple containing the initialized orbit Shape object and the integer maximum radius
            which denotes the maximum radius of the orbiting circle.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """String representation."""
        pass


class CircleOrbitView(AbstractShapeOrbitView):

    def __init__(self, orbit_color: int):
        """
        Initialize CircleOrbitView object.
        """
        super().__init__(orbit_color)

    def show_inputs(self):
        """
        Show input elements for selecting orbit circle properties.
        """
        self.orbit_radius = st.number_input(
            key="orbit_radius",
            min_value=5,
            max_value=200,
            value=96,
            label="Select radius of orbit circle:",
        )

    def create_orbit(self) -> tuple[Circle, int]:
        """
        Create orbit circle based on user inputs.

        Returns:
            tuple[Circle, int]: Tuple containing the initialized orbit Circle object and the integer maximum radius.
        """
        orbit = Circle(self.orbit_radius, avail_colors[self.orbit_color])
        max_radius = int(self.orbit_radius)
        return orbit, max_radius

    def __str__(self) -> str:
        """String representation."""
        return "Circle Orbit"


class ElipseOrbitView(AbstractShapeOrbitView):

    def __init__(self, orbit_color: int):
        """
        Initialize ElipseOrbitView object.
        """
        super().__init__(orbit_color)

    def show_inputs(self):
        """
        Show input elements for selecting orbit ellipse properties.
        """
        col1, col2 = st.columns(2)

        with col1:
            self.a = st.number_input(
                key="Elipse_a",
                min_value=5,
                max_value=200,
                value=96,
                label="Select width of orbit elipse:",
            )

        with col2:
            self.b = st.number_input(
                key="Elipse_b",
                min_value=5,
                max_value=200,
                value=96,
                label="Select height of orbit elipse:",
            )

    def create_orbit(self) -> tuple[Elipse, int]:
        """
        Create orbit ellipse based on user inputs.

        Returns:
            tuple[Elipse, int]: Tuple containing the initialized orbit Elipse object and integer the maximum radius.
        """
        orbit = Elipse(self.a / 2, self.b / 2, avail_colors[self.orbit_color])
        max_radius = int(min(self.a, self.b) / 2)
        return orbit, max_radius

    def __str__(self):
        """String representation."""
        return "Elipse Orbit"


class OrbitView:
    def __init__(self):
        """
        Initialize ObjectView object.

        This is a factory for creating orbits. If you want to extend available orbits
        just add your custom_shape orbit view class which extends the CustomOrbitView abstract class to the list of orbits.
        """
        self.list_of_orbits: list[AbstractShapeOrbitView] = [
            CircleOrbitView,
            ElipseOrbitView,
        ]

    def show_inputs(self):
        """
        Show input elements for selecting orbit properties.
        """
        st.write("#### Main settings")
        self.columns = st.columns(5)
        with self.columns[0]:
            self.show_borders = st.toggle("Show orbit borders")
        with self.columns[1]:
            self.animate = st.toggle("Animate")
        with self.columns[2]:
            self.orbit_color = st.selectbox(
                key="orbit_color",
                label="Select color of orbit circle:",
                options=avail_colors.keys(),
                index=0,
            )
        with self.columns[3]:
            self.speed = st.number_input(
                key="speed",
                label="Select speed of animation:",
                min_value=1,
                max_value=200,
                value=2,
            )
        with self.columns[4]:
            self.number_of_circles = st.number_input(
                min_value=0,
                max_value=5,
                value=1,
                label="How many circles you want to use?",
            )

        orbit_type = st.selectbox(
            label="Select orbit shape",
            options=self.list_of_orbits,
            format_func=lambda x: str(x(self.orbit_color)),
        )

        orbit_view = orbit_type(self.orbit_color)
        orbit_view.show_inputs()
        self.orbit, self.max_radius = orbit_view.create_orbit()
