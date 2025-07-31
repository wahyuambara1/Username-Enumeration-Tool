# Username Enumeration Pentest Tool

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This tool is a Python script developed for educational purposes to demonstrate the **Username Enumeration** vulnerability, which arises from verbose error messages on login pages.

## ⚠️ Ethical Disclaimer

This tool is intended for educational use and for authorized penetration testing only. Unauthorized use of this tool against systems you do not have permission to test is illegal and unethical. The author is not responsible for any misuse or damage caused by this program.

---

## Features

* **Multithreading**: Utilizes `ThreadPoolExecutor` to perform checks concurrently, significantly speeding up the enumeration process.
* **Flexible Arguments**: Implements `argparse` for robust command-line argument parsing, allowing for easy changes to the target URL, wordlist, and other parameters.
* **Colored Output**: Uses `colorama` to differentiate between `[VALID]`, `[INVALID]`, and `[ERROR]` statuses for better readability.
* **Error Handling**: Includes `try...except` blocks to gracefully handle connection issues or invalid server responses.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/Username-Enumeration-Tool.git](https://github.com/YourUsername/Username-Enumeration-Tool.git)
    cd Username-Enumeration-Tool
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the script from your terminal, providing the target URL and the path to the wordlist file.

```bash
python enum_tool.py -u <TARGET_URL> -w <PATH_TO_WORDLIST> [options]
```

**Example Command:**
```bash
python enum_tool.py -u [http://target.lab/login.php](http://target.lab/login.php) -w usernames.txt -t 50
```

**Command-line Arguments:**
* `-u`, `--url`: **(Required)** The full URL to the login endpoint.
* `-w`, `--wordlist`: **(Required)** The path to the text file containing a list of usernames.
* `-e`, `--error-string`: The specific error message that indicates an invalid username.
* `-t`, `--threads`: The number of concurrent threads to use (default: 10).

---

## Vulnerability Concept: Username Enumeration

This vulnerability occurs when an application provides different responses for failed login attempts with an invalid username versus a valid username.

* **Invalid Username**: The server responds -> "User does not exist."
* **Valid Username, Invalid Password**: The server responds -> "Incorrect password."

This discrepancy allows an attacker to compile a list of valid usernames without needing to know any passwords, which is often the first step for a brute-force or password-spraying attack.

## Mitigation

To prevent this vulnerability, applications should always return a **generic error message** for all failed login conditions, such as: **"Invalid username or password."**
