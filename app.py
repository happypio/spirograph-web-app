import streamlit as st

from src.const_params import quality
from src.controllers import DrawController
from src.object_views import CircleView
from src.orbit_views import OrbitView

# Set page configuration
st.set_page_config(layout="wide")

# Display header
st.header("SPIROGRAPH")

# Initialize OrbitView
orbit_view = OrbitView()
orbit_view.show_inputs()

# Button to stop drawing
st.button("Stop drawing")

# Display circles form
circles = []
with st.form(key="create-spirograph"):
    columns = st.columns(4)
    for i in range(orbit_view.number_of_circles):
        circle_view = CircleView(
            i, columns, 1, max_radius=orbit_view.max_radius
        )
        circle_view.show_inputs()
        circles.append(circle_view)

    submitted = st.form_submit_button("Show drawing")

# When form submitted, generate motions and display drawing
if submitted:
    motions = []
    for circle_view in circles:
        motion = circle_view.submit(orbit_view.orbit, quality)
        motions.append(motion)

    draw_controller = DrawController(
        orbit_view.orbit,
        motions,
        orbit_view.speed,
        orbit_view.show_borders,
        orbit_view.animate,
        "src/html_views/plots.html",
    )

    html_file = draw_controller.submit_parameters()
    st.components.v1.html(html_file, height=2000)
