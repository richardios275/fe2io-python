# fe2io-python
 FE2.IO RBX-2-Web Player Client recreated with Python and Qt

## Installation

### Windows

Download the latest release from the [Releases]() page.

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

-The code ofc

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


Translations

    Find the locales directory.
    Duplicate the existing language file (e.g., en_US.json) and translate the strings.
    Make a pull request with your translated file.

Other Contributions

Feel free to open an issue or pull request for any other improvements or features you'd like to contribute.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

(C) Crazyblox Ltd 2023
