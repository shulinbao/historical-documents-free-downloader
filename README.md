# Historical Document Downloader

## Compiled Binary File

If you just want to use the software, please click [here](https://github.com/shulinbao/historical-documents-free-downloader/releases/download/test/downloader.exe) to download the compiled binary file: `downloader.exe`.

如果你只是想使用程序，而不想二次开发，请直接点击链接 [下载](https://github.com/shulinbao/historical-documents-free-downloader/releases/download/test/downloader.exe) 并使用即可。

**Please note that the server address should only include the IP and port (e.g., ip:port), not the website URL!**

请注意，服务器地址只能填ip:端口，不能填网址！

## Overview

This is a Python-based GUI downloader application designed to interact with the API of a historical document database developed by a Chinese company. The application allows users to search for historical documents and download them as PDF files. The downloader does not require login and provides a user-friendly interface to search, select, and download documents.

**Important Note**: Please ensure that you have the right to download the documents before using this program.

---

## Features

- **Search for Documents**: Allows users to search for historical documents based on categories and keywords.
- **Download Documents**: Users can select one or more documents from the search results and download them as PDF files.
- **Server Configuration**: The server address can be easily updated to match the API endpoint of the historical document database.
- **Progress Tracking**: The app includes a progress bar to track the download status of selected documents.
- **PDF Merging**: The application automatically merges downloaded pages into a single PDF for each document.

---

## Requirements

- Python 3.x
- Tkinter (for the GUI interface)
- Requests (for making HTTP requests)
- PyPDF2 (for handling PDF files)

To install the required dependencies, you can use `pip`:

```bash
pip install requests PyPDF2
```

---

## Setup

1. **Clone or Download the Repository**: Download or clone this repository to your local machine.

2. **Modify Server Address**:  
   The script uses a default server address `0.0.0.0:7777`. You need to modify this to the correct server address for the historical document database you wish to access.  
   In the script, locate this line:
   
   ```python
   default_server_address = "0.0.0.0:7777"
   ```

   Replace `0.0.0.0:7777` with the actual ip. For example:

   ```python
   default_server_address = "1.2.3.4:7777"
   ```

3. **Run the Application**:
   After ensuring that you have set up the server address correctly, run the Python script:

   ```bash
   python downloader.py
   ```

   This will open the GUI window where you can search and download documents.

---

## How to Use

1. **Update Server Address**:
   - In the main window, you can update the server address by entering the new address and clicking "更新地址" (Update Address).

2. **Search for Documents**:
   - Select the desired category from the dropdown.
   - Enter a search keyword in the "搜索内容" (Search Content) box.
   - Click the "搜索" (Search) button to retrieve matching records.

3. **Select Documents**:
   - After searching, the results will be displayed in a list.
   - Use Ctrl or Shift to select multiple records.

4. **Download Documents**:
   - Click the "下载选中记录" (Download Selected Records) button to download the selected documents.
   - The progress bar will show the download progress. The documents will be saved as PDF files with their titles as filenames.

---

## Important Notes

- **Check Download Rights**: Ensure that you have the proper rights or permissions to download documents from the database.
- **Server Configuration**: The server address in the script should point to an accessible API endpoint that allows searching and downloading documents.
- **Error Handling**: The application provides error messages in case of issues, such as invalid server address, failed requests, or download errors.

---

## Troubleshooting

- **Invalid Server Address**: Ensure that the server address is correctly set and reachable. If the server is down, the app may not function properly.
- **Empty Search Results**: If no records are found, double-check your search terms or category selection. Make sure the database contains documents matching your search.
- **Download Failures**: If the download fails for a document, check the server response code and make sure that the document is accessible through the API.

---

## License

This project is open-source and can be freely modified and distributed. However, ensure that you comply with the terms and conditions of the historical document database API when using this tool.

