"""
    :author:        Jacob Whetham
    :version:       1.0.0, 04 JAN 2024
    :desc:          This file handles the frontend of the Inventory Management System (website).
"""

# Imports
import pandas                                               # Allows for use of Pandas (Data Frames).
from dash import Dash, dash_table, dcc, html                # Allows use of Dash functionality.
from dash.dependencies import Input, Output, State          # Allows use of Dash dependencies for callbacks.
import inventory_management_backend as imb                  # Allows use of the Inventory Management backend service.

app = Dash(name="Inventory Management System", prevent_initial_callbacks="initial_duplicate")  # Creates a Dash app.


def start():
    """
        Creates the formatting of the Dash app before starting the app.
    """

    # Sets the layout for the app.
    app.layout = app.layout = html.Div([
        # Creates the header.
        html.Div(id="header", children=[
            # The title.
            html.Center(html.B(html.H1("Sample Inventory Management Dashboard")))
        ], style={"display": "flex", "justifyContent": "center", "flexDirection": "column"}),

        # Creates the login section.
        html.Div(id="login_container", children=[
           # A table to organize the login section.
           html.Table(children=[
              html.Tr(children=[
                  # This cell holds the input fields for the username and password.
                  html.Td(children=[dcc.Input(id="input_username", placeholder="Username", type="text", style={"display": "inline"}),
                                    dcc.Input(id="input_password", placeholder="Password", type="password", style={"display": "inline"}),
                  ]),

                  # This cell holds the login/logout button.
                  html.Td(children=[html.Button(id="button_login", children="Login",
                                                style={"float": "right"}, n_clicks=0),

                                    html.Button(id="button_drop_database", children="Delete Database",
                                                style={"display": "none"}, n_clicks=0)])
              ]),
           ]),

           # A header to act as an error message.
           html.H2(id="h2_login_error", children="")
        ]),

        # Creates the table section (shows database data).
        html.Div(id="table_container", children=[
            # The table to hold the data.
            dash_table.DataTable(
                id="table",
                columns=[] if imb.logged_in else [],
                data=None,
                row_selectable = "single",
                selected_rows = [0],
                page_size = 25,
                sort_action = "native",
                sort_mode = "multi",
                filter_action = "native",
                style_table = {"overflowX": "auto"}
            ),

            html.Br()  # A line break for formatting.
        ]),

        # A container to hold the section to modify the table.
        html.Div(id="modification_form_container", children=[
            # The input fields for the modifications.
            dcc.Input(id="input_product_name", type="text", placeholder="Product Name", style={"display": "none"}),
            dcc.Input(id="input_product_quantity", type="text", placeholder="Quantity", style={"display": "none"}),
            dcc.Input(id="input_product_price", type="text", placeholder="Price", style={"display": "none"}),

            # The buttons to declare what kind of modification is to be made.
            html.Button(id="button_update", children="Update Values", n_clicks=0, style={"display": "none"}),
            html.Button(id="button_delete", children="Delete Entry", n_clicks=0, style={"display": "none"}),
            html.Button(id="button_add", children="Add Entry", n_clicks=0, style={"display": "none"})
        ])
], style={"background": "#348AA7"})

    app.run_server(host="0.0.0.0", port="8050", debug=True)  # Starts the app.


@app.callback(
    # The elements that will be updated by the returned values.
    [Output("table", "data", allow_duplicate=True),
     Output("table", "columns", allow_duplicate=True),
     Output("button_update", "n_clicks"),
     Output("button_delete", "n_clicks"),
     Output("button_add", "n_clicks")],

    # The elements that will call this function when interacted with and be passed in as arguments.
    [Input("button_update", "n_clicks"),
     Input("button_delete", "n_clicks"),
     Input("button_add", "n_clicks")],

    # The elements that will be passed to this function as arguments (will not call the function directly).
    [State("input_product_name", "value"),
     State("input_product_price", "value"),
     State("input_product_quantity", "value"),
     State("table", "derived_virtual_data"),
     State("table", "derived_virtual_selected_rows")],

    prevent_initial_call=True  # Prevents this function from running when the Dash app starts.
)
def button_pressed(update_clicks : int, delete_clicks : int, add_clicks : int, product_name : str, product_price : str,
                   product_quantity : str, all_rows, selected_row) -> (dict, list, int, int, int):
    """
        Performs the necessary modification depending on the button that was pressed.

        :param update_clicks:                   The number of times the update modification button was clicked.
        :param delete_clicks:                   The number of times the delete modification button was clicked.
        :param add_clicks:                      The number of times the add modification button was clicked.
        :param product_name:                    The name specified in the product name input field.
        :param product_price:                   The price specified in the product price input field.
        :param product_quantity:                The quantity specified in the product quantity input field.
        :param all_rows:                        All the rows within the table.
        :param selected_row:                    The currently selected row.
        :return (dict, list, int, int, int):    The dictionary of the data to populate the table.
                                                The composition of the columns.
                                                Reset the update button click count.
                                                Reset the delete button click count.
                                                Reset the add button click count.
    """
    # If the user is not logged in,
    if not imb.logged_in:
        return None, [], 0, 0, 0  # Returns default (empty) data to prevent unauthorized access.

    # The below code only runs if the user is logged in.

    frame = pandas.DataFrame(all_rows).iloc[selected_row]  # Builds a DataFrame from locating the selected row within all the rows.
    id = frame["product_id"].tolist()  # Gets the product ID from the frame.

    # If the update button was pressed,
    if update_clicks == 1:
        # Makes an attempt,
        try:
            product_price = float(product_price)  # Converts the price to a float value.
            product_quantity = int(product_quantity)  # Converts the quantity to an integer value.

            # Updates the selected entry with the data from the input fields.
            imb.update({"product_id" : id[0]},
                       {"$set": {"product_name": product_name, "product_price": product_price, "product_quantity": product_quantity}})

        # If something failed,
        except Exception:
            print("Cannot convert!")  # Output an error.

    # Otherwise if the delete button was pressed,
    elif delete_clicks == 1:
        imb.delete({"product_id": id[0]})  # Deletes the selected entry.

    # Otherwise if the add button was pressed,
    elif add_clicks == 1:
        # Makes an attempt,
        try:
            product_price = float(product_price)  # Converts the price into a float value.
            product_quantity = int(product_quantity)  # Converts the price into an integer value.

            frame = pandas.DataFrame(all_rows).iloc[-1]  # Builds a DataFrame from the last entry in the table.
            id = frame["product_id"].tolist()  # Gets the product ID from the DataFrame.

            # Creates a new entry into the database from the data in the input fields.
            imb.create({"product_id": id + 1, "product_name": product_name, "product_price": product_price,
                        "product_quantity": product_quantity})

        # If something failed,
        except Exception:
            print("Cannot convert!")  # Output an error.

    df = imb.get_data_frame(imb.read())  # Gets the DataFrame from reading all the data in the database.
    table_data = imb.convert_dataframe_to_dict(df)  # Converts the DataFrame to a dictionary.

    # Returns the data to populate the table and reset the buttons.
    return table_data, [{"id": i, "name": i, "deletable": False, "selectable": True} for i in df.columns],\
           0, 0, 0


@app.callback(
    # The elements that will be updated with the returned values.
    [Output("table", "data", allow_duplicate=True),
     Output("table", "columns", allow_duplicate=True),
     Output("h2_login_error", "children"),
     Output("button_login", "children"),

     Output("input_username", "style"),
     Output("input_password", "style"),

     Output("input_product_name", "style"),
     Output("input_product_quantity", "style"),
     Output("input_product_price", "style"),
     Output("button_update", "style"),
     Output("button_delete", "style"),
     Output("button_add", "style"),
     Output("button_drop_database", "style")],

    # The elements that will call this function when interacted with and get passed as arguments.
    [Input("button_login", "n_clicks")],

    # The elements that will be passed to this function as arguments.
    [State("input_username", "value"),
     State("input_password", "value")],

    prevent_initial_call=True  # Prevents this function from calling when the Dash app starts.
)
def login_pressed(login_clicks : int, username : str, password : str) -> (dict, list, str, str, dict,
                                                                          dict, dict, dict, dict,
                                                                          dict, dict, dict, dict):
    """
        Performs the necessary login function when the button is pressed.

        :param login_clicks:                    The number of times the login/logout button was pressed.
        :param username:                        The username entered in the input field.
        :param password:                        The password entered in the input field.
        :return (dict, list, int,
                 str, str, dict,
                 dict, dict, dict,
                 dict, dict, dict,
                 dict, dict):                   The dictionary to populate the table data.
                                                The list to define the columns of the table.
                                                The error occurred when trying to log in (if any).
                                                The text of the login button.
                                                The dictionary to set the visibility of the username input.
                                                The dictionary to set the visibility of the password input.
                                                The dictionary to set the visibility of the product name input.
                                                The dictionary to set the visibility of the product quantity input.
                                                The dictionary to set the visibility of the product price input.
                                                The dictionary to set the visibility of the update button.
                                                The dictionary to set the visibility of the delete button.
                                                The dictionary to set the visibility of the add button.
                                                The dictionary to set the visibility of the drop database button.
    """

    columns = []  # Holds the column definition for each row.
    table_data = None  # Holds the data to populate the table.
    error_message = ""  # Holds any error message encountered.
    login_button_text = "Login"  # Holds the text to apply to the login button.
    visibility_input_fields = {"display": "inline"}  # Holds the visibility of the login input fields.
    visibility_modification_fields = {"display": "none"}  # Holds the visibility of the modification input fields.

    # If the user is logged in when the login (logout) button is pressed,
    if imb.logged_in:
        imb.logout()  # Starts the logout process.

    # Otherwise (the user is logged out when the login button is pressed),
    else:
        # If the username and password are both valid (not empty),
        if username and password:
            imb.login(username, password)  # Starts the login process using the data from the login input fields.

        # The below code exists to determine if the login process failed.

        # If the user is not logged in:
        if not imb.logged_in:
            error_message = "Invalid Credentials!" # Updates the error message.

    # If the user is logged in,
    if imb.logged_in:
        df = imb.get_data_frame(imb.read())  # Gets a DataFrame from the entire database.
        table_data = imb.convert_dataframe_to_dict(df)  # Converts the DataFrame into a dictionary.
        error_message = ""  # Resets the error message (no error occurred).
        login_button_text = "Logout"  # Update the text of the login/logout button.

        # Sets the data for each column in the DataFrame.
        columns = [
            {"id": i, "name": i, "deletable": False, "selectable": True} for i in df.columns
        ]

        # Updates the visibility of the fields.
        visibility_input_fields = {"display": "none"}
        visibility_modification_fields = {"display": "inline"}

    # Otherwise (the user is not logged in),
    else:
        table_data = None  # Resets the table data (nothing should be populated when the user is logged out).
        login_button_text = "Login"  # Resets the text of the login button.

        # Updates the visibility of the fields.
        visibility_input_fields = {"display": "inline"}
        visibility_modification_fields = {"display": "none"}

    # Returns all the data to update the app.
    return table_data, columns, error_message, login_button_text, visibility_input_fields, visibility_input_fields, \
           visibility_modification_fields, visibility_modification_fields, visibility_modification_fields, \
           visibility_modification_fields, visibility_modification_fields, visibility_modification_fields, \
           visibility_modification_fields


@app.callback(
    # The elements that are updated with the returned values.
    Output("table", "style_data_conditional"),

    # The elements that call the function when interacted with.
    Input("table", "selected_rows"),

    prevent_initial_call=True  # Prevents this function from being called when the Dash server starts.
)
def update_form(selected_rows):
    """
        Changes the color of the selected row for visual appeal.

        :param selected_rows:   The row that is currently selected.
        :return list:           A list of the color style data for every cell in the current row.
    """

    # If there is currently no selected row,
    if selected_rows is None:
        styles = []  # Sets the style data to be empty.

    # Otherwise (a row is selected),
    else:
        # Updates the style data for every cell in the row.
        styles = [{"if": {"row_index": i}, "background_color": "#348AA7"} for i in selected_rows]

    return styles  # Returns the style data.


@app.callback(
    # The elements that are updated with the returned values.
    Output("button_login", "n_clicks", allow_duplicate=True),

    # The elements that call the function when interacted with.
    Input("button_drop_database", "n_clicks"),

    prevent_initial_call=True  # Prevents this function from being called when the Dash server starts.
)
def delete_database(drop_clicks : int) -> int:
    """
        Deletes the database and user that the program created.

        :param drop_clicks:     The number of clicks of the drop database button.
        :return:                Resets the number of clicks of the login button.
    """
    imb.deleteDatabase()  # Calls for the database to be deleted.

    return 0  # Returns 0 to update the clicks of the login button (will call the login_pressed() function to log the user out).
