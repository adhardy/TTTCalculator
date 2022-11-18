from typing import Optional
from dataclasses import dataclass
import streamlit as st

from tttcalculator.riders import Riders


@dataclass
class Column:
    name: str
    type: type
    width: float
    label: Optional[str] = None
    help: str = ""

    def __post_init__(self):
        if self.label is None:
            self.label: str = self.name


class Columns:
    def __init__(self, columns: Optional[list[Column]] = None):

        self.columns: list[Column] = columns or []

    def __iter__(self):
        return iter(self.columns)

    def iteritems(self):
        yield from ((column.name, column.type, column.label, i, column.help) for i, column in enumerate(self.columns))

    def __getitem__(self, key: str) -> Column:

        if isinstance(key, str):
            # If key is a string, try to find a column with that name
            try:
                return self.get_by_name(key)
            except KeyError:
                try:
                    return self.get_by_label(key)
                except KeyError:
                    raise KeyError(f"Column {key} not found in names or labels")

        elif isinstance(key, int):
            # If key is an int, try to find a column with that index
            return self.columns[key]

        else:
            raise KeyError(f"Column {key} not found")

    def get_by_name(self, name: str) -> Column:
        for column in self.columns:
            if column.name == name:
                return column
        raise KeyError(f"Column {name} not found")

    def get_by_label(self, label: str) -> Column:
        for column in self.columns:
            if column.label == label:
                return column
        raise KeyError(f"Column with label {label} not found")

    def append(self, column: Column):
        self.columns.append(column)

    def __len__(self):
        return len(self.columns)

    @property
    def widths(self):
        return [column.width for column in self.columns]


def rider_form_layout(riders: Riders):

    columns = Columns()
    # these need to correspond to the Rider dataclass
    columns.append(Column(name="number", type=int, label="Rider Number", width=0.8))
    columns.append(Column(name="name", type=str, label="Name", width=2))
    columns.append(
        Column(
            name="weight",
            type=int,
            label="Weight (kg)",
            width=1,
            help="Rider weight in kg, only needed for 'hilly' courses",
        )
    )
    columns.append(Column(name="power", type=int, label="40 Min. Power (W)", width=1))

    with st.form("rider_data"):
        st.header("Rider Data")
        cols = st.columns(columns.widths)

        for col_name, col_type, col_label, col_idx, col_help in columns.iteritems():
            cols[col_idx].write(col_label)

            for rider in riders:
                if col_name == "number":
                    cols[col_idx].text_input(
                        col_label,
                        key=f"{col_name}_{rider.number}",
                        label_visibility="collapsed",
                        placeholder=rider.number + 1,
                        disabled=True,
                        help=col_help,
                    )
                else:
                    if col_type == int:
                        _val = cols[col_idx].number_input(
                            col_label,
                            key=f"{col_name}_{rider.number}",
                            label_visibility="collapsed",
                            step=1,
                            min_value=0,
                        )
                    elif col_type == float:
                        _val = cols[col_idx].number_input(
                            col_label,
                            key=f"{col_name}_{rider.number}",
                            label_visibility="collapsed",
                            step=0.1,
                            min_value=0,
                        )
                    elif col_type == str:
                        _val = cols[col_idx].text_input(
                            col_label, key=f"{col_name}_{rider.number}", label_visibility="collapsed"
                        )
                    else:
                        raise ValueError(f"Column type {col_type} not supported")

                    rider.__setattr__(col_name, _val)

        return st.form_submit_button("Submit")
