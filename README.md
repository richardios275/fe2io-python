# fe2io-python
 FE2.IO RBX-2-Web Player Client recreated with Python and Qt

## Usage
Just run the program! Duh.
Unless you want to get real fancy.

### Launch options
`-u` / `-username`: Specify Roblox username\
`-v` / `--volume`: Specify Player volume\
`-s` / `--server`: Specify server (Options: `fe2io` / `lbio`)\
`--autoconnect`: Automatically connect to server (`-u` needs to be specified)

## Installation

### Windows
Download the latest release from the [Releases](https://github.com/richardios275/fe2io-python/releases) page.

### Other Platforms

1. Install Python: [Python Downloads](https://www.python.org/downloads/)
2. Open a terminal or command prompt.
3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:

    On Windows:

    ```ps1
    .\venv\Scripts\activate
    ```
    On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```
        
        

4. Install dependencies:

```bash
pip install -r requirements.txt
```
Run the application:

```bash
python sources/main.py
```


## Contributing

We welcome contributions to enhance fe2io-python. Here are some ways you can contribute:

-The code ofc (good luck fixing my spaghetti code LOL)

-Report Issues

-Editing .ui Files

Install Qt Designer to edit them: 
```bash
pip install pyqt6-tools
```
Launch:
```bash
pyqt6-tools designer
```


Translations (currently broken lol)

    Find the locales directory.
    Duplicate the existing language file (e.g., en_US.json) and translate the strings.
    Make a pull request with your translated file.

Other Contributions

Feel free to open an issue or pull request for any other improvements or features you'd like to contribute.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

This project is not endorsed, nor is it affiliated with Crazyblox Ltd. FE2.io and its logo are copyright of Crazyblox Ltd
(C) Crazyblox Ltd 2024
