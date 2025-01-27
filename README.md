# Bulk-Email-Enrichment-via-ReverseContact-API
A Python tool that enriches email data using the ReverseContact API. It processes email addresses from a CSV file, fetches personal and company details, and outputs enriched data as a CSV file. The solution uses asynchronous requests to handle large datasets efficiently.

## Features
- Enriches email addresses with data from the ReverseContact API.
- Outputs enriched data in CSV format.
- Displays progress during the enrichment process.
- Handles API errors gracefully.

## Requirements
- Python 3.6 or higher
- Required Python packages:
  - `aiohttp` (for asynchronous HTTP requests)
  - `pandas` (for CSV processing)
  - `tqdm` (for progress bar)
  - `tkinter` (for file dialog)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository-name.git
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the ReverseContact API:
    - Replace the `API_KEY` in the script with your own ReverseContact API key. **Ensure that your API key is kept private and not shared publicly.**

4. Run the script:
    ```bash
    python your_script_name.py
    ```

## How It Works
- You upload a CSV file containing email addresses.
- The script calls the ReverseContact API for each email and retrieves enriched data.
- The enriched data is saved to a new CSV file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
