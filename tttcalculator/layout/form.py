from dataclasses import dataclass
from typing import Optional

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
    columns.append(Column(name="name", type=str, label="Name", width=2, help="Rider name."))
    columns.append(
        Column(
            name="power",
            type=int,
            label="40 Min. Power (W)",
            width=1,
            help="40 minute power in Watts. Can be found from the graph in the 'power' tab of the riders profile on zwiftpower.com",  # noqa: E501
        )
    )
    columns.append(
        Column(
            name="weight",
            type=int,
            label="Weight (kg)",
            width=1,
            help="Rider weight in kg, only needed for 'hilly' courses",
        )
    )
    with st.form("rider_data"):
        for rider in riders:
            with st.expander(f"Rider {rider.number+1}:", expanded=True):
                cols = st.columns(columns.widths)
                for col_name, col_type, col_label, col_idx, col_help in columns.iteritems():
                    if col_name == "number":
                        pass
                    else:
                        if col_type == int:
                            _val = cols[col_idx].number_input(
                                col_label,
                                key=f"{col_name}_{rider.number}",
                                min_value=0,
                                step=1,
                                help=col_help,
                            )
                        elif col_type == float:
                            _val = cols[col_idx].number_input(
                                col_label,
                                key=f"{col_name}_{rider.number}",
                                step=0.1,
                                min_value=0,
                                help=col_help,
                            )
                        elif col_type == str:
                            _val = cols[col_idx].text_input(col_label, key=f"{col_name}_{rider.number}", help=col_help)
                        else:
                            raise ValueError(f"Column type {col_type} not supported")

                        rider.__setattr__(col_name, _val)

        return st.form_submit_button("Submit")
