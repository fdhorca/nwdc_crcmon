# crcmon_docker

This script checks for the CRC count of each interface on a network device and displays it on a webpage. The interface and the latest error count will be displayed once the error count is above the threshold set.

Process:
- Connects to network device
- Sends command to the network device and saves the output
- Closes the connection to the network device
- Parses the output
- Compares the count with threshold limit
- Displays the output (JSON format)

Notes:
- Connecting to the network device varies (around 1 minute) - may timeout 
- Uses screen scraping (API better)
- When using, input TACACS into code (to be updated to make use of environment variable
