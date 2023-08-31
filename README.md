# Country Information Management System

This project is a simple Python program that allows you to manage and store country information in an SQLite database. You can add countries, capitals, and populations to the database, retrieve data, and visualize population information using charts.

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependencies by running:
- pip3 install requests
- pip3 install matplotlib
- pip3 install sqlite3
- pip3 install numpy
- pip3 install pillow


## Usage

1. Run the `main.py` script to interact with the program.
2. The program prompts you to enter the name of a country. You can add multiple countries one by one.
3. Type "end" when prompted for the country name to finish adding data.
4. After entering the data, you can choose to retrieve country information or quit the program.
5. If you choose to retrieve information, a bar chart showing population data will be displayed.

## Modules

### `main.py`

This module contains the main interactive script of the program. It allows you to input country and capital information, add it to the database, and retrieve data.

### `countries_function.py`

This module includes various functions used by the main script to handle data. It provides functions for initializing the database, retrieving information, saving country and capital data, and more.

### `countries_test.py`

This module includes functions for testing countries_function.py

## Dependencies

- `sqlite3`: SQLite is used to manage the database.
- `matplotlib`: Matplotlib is used to create bar charts for data visualization.
- `requests`: Requests is used to fetch country data from an external API.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
