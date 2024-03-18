import streamlit as st

from src.const_params import avail_colors
from src.motions import CircleMotion
from src.shapes import Circle, Shape


class CircleView:

    def __init__(
        self, id: int, columns: st.columns, min_radius: int, max_radius: int
    ):
        """
        Initialize CircleView object.

        Parameters:
            id (int): Identifier for the CircleView object.
            columns (st.columns): Streamlit columns object (with at least 4 columns) to organize input elements.
            min_radius (int): Minimum value for the radius input.
            max_radius (int): Maximum value for the radius input.
        """
        self.id = id
        self.columns = columns
        self.min_radius = min_radius
        self.max_radius = max_radius

    def show_inputs(self):
        """
        Show input elements for selecting circle properties.
        """
        with self.columns[0]:
            self.radius = st.number_input(
                key=f"radius_{self.id}",
                min_value=self.min_radius,
                max_value=self.max_radius - 1,
                value=max(
                    min(
                        int((self.max_radius) / 4) + self.id,
                        self.max_radius - 1,
                    ),
                    1,
                ),
                label="Select radius:",
            )
        with self.columns[1]:
            self.color = st.selectbox(
                key=f"color_{self.id}",
                label="Select color:",
                options=avail_colors.keys(),
                index=self.id + 1,
            )
        with self.columns[2]:
            self.pen_distance = st.number_input(
                key=f"pen_distance_{self.id}",
                min_value=0.0,
                max_value=float(self.radius),
                value=float(self.radius),
                label="Distance from center",
                step=0.25,
            )
        with self.columns[3]:
            c = st.container(border=True)
            c.write("")
            self.outer = c.toggle(
                key=f"outer_{self.id}",
                label="Outside roll",
            )

    def submit(self, orbit: Shape, quality: int) -> CircleMotion:
        """
        Submit circle motion parameters based on user inputs.

        Parameters:
            orbit: The orbit shape for the circle motion.
            quality (int): Quality parameter for the motion calculation.

        Returns:
            CircleMotion: The initialized CircleMotion object
            with given orbit and submitted circle.
        """
        circle = Circle(self.radius, avail_colors[self.color])

        distance_to_border = self.radius - self.pen_distance

        motion = CircleMotion(
            orbit, circle, distance_to_border, self.outer, quality=quality
        )

        return motion
