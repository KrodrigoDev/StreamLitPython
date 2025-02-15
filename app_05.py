from typing import Dict, List, Any
from random import randint
import streamlit as st

st.header('Random Challenge from Instagram')

text_challenge = """
Create a function that simulates a movie theater seat reservation system.  
The system should receive a list of dictionaries representing all seats, indicating whether they are reserved or not, along with their number.  
Additionally, it should take a list of seats to be reserved by the user.  
The function should return the updated list of seat dictionaries after reservations are made  
and display an error message for each attempt to reserve an already occupied seat.
"""

st.write(text_challenge)


@st.cache_data
def generate_seat():
    seats: Dict[int, str] = {}

    # Randomly generate seats as 'open' or 'closed'
    for i in range(100):
        seats[i] = 'seat open' if randint(0, 1) == 0 else 'seat closed'

    return seats


def filter_seats(seats: Dict[int, str], condition: List[str]) -> Dict[int, str]:
    """Displays seats filtered by status"""
    return {j: k for j, k in seats.items() if k in condition}


seats = generate_seat()

st.subheader('Step One')
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    c1.container(border=True).metric('Total seats', len(seats))

    for condition, column in zip(['seat open', 'seat closed'], [c2, c3]):
        column.container(border=True).metric(condition, len(filter_seats(seats, [condition])))

    with st.expander(label='Show all seats:'):
        st.json(seats)

st.subheader('Step Two')
with st.container(border=True):
    type_seat = st.selectbox(label='Select the seat type to display:', options=['seat open', 'seat closed'])
    with st.expander(f'Showing {type_seat} seats:'):
        st.json(filter_seats(seats, [type_seat]))


def selected_seats(seats: Dict[int, str]):
    selecteds = st.multiselect(label="Select a seat:", options=seats.keys())

    if st.button('Reserve selected seats'):
        success_on_reservation = []
        error_on_reservation = []

        for selected in selecteds:
            if seats[selected] == 'seat open':
                seats[selected] = 'seat closed'
                success_on_reservation.append(str(selected))
            else:
                error_on_reservation.append(str(selected))

        if success_on_reservation:
            st.success(f"✅ Seats {', '.join(success_on_reservation)} successfully reserved!")

        if error_on_reservation:
            st.error(f"❌ These seats {', '.join(error_on_reservation)} are already taken, please select another.")

    return seats


st.subheader('Step Three')
with st.container(border=True):
    seats = selected_seats(seats)

    st.json(seats)
