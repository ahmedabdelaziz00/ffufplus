ffufPlus
ffufPlus is a Python utility built to enhance the automation of fuzzing tasks with ffuf. This tool executes multiple ffuf commands in sequence with predefined URL patterns, streamlining the process of discovering hidden files, directories, and endpoints during web application reconnaissance.

Features
Automated ffuf Command Execution:
Run ffuf with a variety of URL patterns tailored for comprehensive fuzzing.
Customizable HTTP Methods:
Support for specifying HTTP request methods (default: GET).
Flexible Filtering:
Optional support for filtering results based on response line counts (-fl flag).
User-Friendly Output:
Clear and organized display of commands and results during execution.
Effortless Configuration:
Easily specify target domain, wordlist path, and additional options through command-line arguments.
Predefined URL Patterns
The tool supports fuzzing using the following URL patterns:

https://{domain}/FUZZ
https://{domain}/FUZZ/
https://{domain}/.FUZZ
https://{domain}/_FUZZ
https://{domain}/-/FUZZ
https://{domain}/_/FUZZ
https://{domain}/FUZZ//
https://{domain}/;/FUZZ
https://{domain}/.;/FUZZ
https://{domain}/.FUZZ/
https://{domain}/./FUZZ
Installation
Ensure you have Python 3.x installed.
Clone this repository:
bash
Copy code
git clone https://github.com/yourusername/ffufPlus.git
cd ffufPlus
Install ffuf (required for this tool):
bash
Copy code
sudo apt install ffuf
Usage
Run the script with the following command-line arguments:

bash
Copy code
python ffufPlus.py -d <domain> -w <wordlist> [options]
Arguments
-d, --domain: Target domain name (required).
-w, --wordlist: Path to the wordlist (required).
-fl, --filterline: Filter results by line count (optional).
-X, --method: HTTP method to use (default: GET).
Examples
Basic usage:

bash
Copy code
python ffufPlus.py -d example.com -w wordlist.txt
Specify a filter line and HTTP method:

bash
Copy code
python ffufPlus.py -d example.com -w wordlist.txt -fl 10 -X POST
Contributing
