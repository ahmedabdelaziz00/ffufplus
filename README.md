# FFUFPlus

**FFUFPlus** is an enhanced automation script built to simplify and extend the functionality of [FFUF](https://github.com/ffuf/ffuf). It automates multiple directory fuzzing patterns, making it a powerful and efficient script for penetration testers and security researchers.

---

## Update

  1. **Improved Logging:**

     - Added logging for better control and visibility of script execution.
     - Logs include information about commands being executed and any errors encountered.
  
  2. **Default Extensions:**
  
     - Introduced a (`-e`) argument for specifying file extensions.
     - Default extensions set to .php,.json,.asp,.aspx,.jsp,.bak,.old.
     - Users can customize or add more extensions via the -e option.
  
  3. **Timeout Support:**
  
     - Added a (`--timeout`) argument to specify the maximum execution time for each ffuf command (default: 60 seconds).
  
  4. **Fallback to POST Method:**
  
     - If the user does not specify a request method (-X), the script defaults to GET and then repeats the execution using the POST method.
  
  5. **Other Enhancements:**
  
     - Improved code structure for readability and maintainability.
     - Updated help messages to reflect new features.

---

##  Features

- Automates FFUF executions for various URL patterns:
  - `/FUZZ`, `//FUZZ`, `/.FUZZ`, `/_FUZZ`, `///FUZZ`, and more!
- Supports optional filters based on the number of response lines (`-fl`).
- Allows flexible HTTP methods (`-X`), with `GET` as the default.
- Intuitive and user-friendly command-line interface (CLI).
- Displays each executed command for better debugging and clarity.

---

##  Installation

1. **Clone the Repository:**
   
```bash  
git clone https://github.com/ahmedabdelaziz00/ffufplus.git
```
 ## usage
Basic Syntax
```
python ffufPlus.py -d <domain> -w <wordlist>
```


## Optional Parameters 

- (`-fl`)Filter by the number of response lines.	-fl 10
- (`-X`)	HTTP method (GET, POST, etc.). Default is GET.

## Examples

```
python ffufPlus.py -d example.com -w wordlist.txt

python ffufPlus.py -d example.com -w wordlist.txt -fl 15 -X POST

```

## How It Works

**FFUFPlus** generates and executes **FFUF** commands for a range of URL patterns. It uses the following predefined patterns:
- `https://<domain>/FUZZ`
- `https://<domain>//FUZZ`
- `https://<domain>/.FUZZ`
- `https://<domain>/_FUZZ`
- `https://<domain>//.FUZZ`
- `...and more!`

## Example Output

```
===============================
Running Command:
ffuf -u https://example.com/FUZZ -w wordlist.txt -X GET
===============================

===============================
Running Command:
ffuf -u https://example.com//FUZZ -w wordlist.txt -X GET
===============================
```
