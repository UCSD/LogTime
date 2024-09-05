
# Log Time CLI Tool for ITS PRO

## Overview
The Log Time CLI tool streamlines the process of logging time to ITS PRO (Jira) issues directly from the command line.

## Requirements
- **Python 3**

## Installation
1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/UCSD/LogTime.git
   ```
2. **Navigate to the project directory** and install the required dependencies:
   ```bash
   cd LogTime
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** at the root of your project directory. This file will store your ITS PRO domain and Access Token.

   Obtain the following credentials:
   - **ITS PRO Domain**: Visit the [Log Time Documentation](https://ucsdcollab.atlassian.net/wiki/spaces/FHIS/pages/1499693369/Log+Time) to get your ITS PRO Domain.
   - **Personal Access Token**: Generate your token through the [Log Time Documentation](https://ucsdcollab.atlassian.net/wiki/spaces/FHIS/pages/1499693369/Log+Time).

   Add the following to your `.env` file, replacing the placeholders, including the `< >`, with the value of your ITS PRO domain and access token:
   ```
   ITS_PRO_DOMAIN=<YOUR_ITS_PRO_DOMAIN>
   ITS_PRO_ACCESS_TOKEN=<YOUR_ITS_PRO_ACCESS_TOKEN>
   ```

## Make the Tool Accessible from the Command Line
### For MacOS:
To simplify using the tool, create an alias so you can run the tool using a shorter command, like `lt`:

```bash
echo 'alias "lt"="python3 '"$(pwd)"'/log-time.py"' >> ~/.zshrc
source ~/.zshrc
```

### For Windows:
1. Open **PowerShell**.
2. Add the following alias to your PowerShell profile:
   ```powershell
   echo 'Set-Alias lt "python C:\path\to\log-time.py"' >> $PROFILE
   ```
   Replace `C:\path\to\log-time.py` with the full path to your `log-time.py` script.
3. Restart PowerShell or reload the profile:
   ```powershell
   . $PROFILE
   ```

## Usage
Once you have the alias set up, you can log time using the following command:

```bash
lt <ITS PRO Issue ID> <Time Spent> ["Description"]
```
For example:
```bash
lt SVCOPS-407 30 "Completed initial setup"
```
This command logs 30 minutes to ITS PRO issue `SVCOPS-407`.
- `<ITS PRO Issue ID`: Your ITS PRO issue ID (e.g., `SVCOPS-407`).
- `<Time Spent>`: Time spent working on the issue (e.g., 30 or 30m for 30 minutes; 2 or 2h for 2 hours).
- `["Description"]`: An optional description that details the work related to the time logged.
## License
	MIT
