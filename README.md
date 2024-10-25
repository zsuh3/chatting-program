# Chat Program

## Overview
* 1-1 chatting program using python
* program consists of client and server
* clients can register and login
* clients and server can be run on the same computer
* connection between server and client is encrypted
* messages received and sent between client

## Getting Started

### How to install

Make sure you have the following installed:
- Python 3.7 or higher
- OpenSSL
- Virtualenv (optional)

1. Clone the repository:

```commandline
git clone https://github.com/zsuh3/chatting-program
```

2. Navigate into the root directory:

```commandline
cd chatting-program/
```

3. Create a virtual environment (optional):

```commandline
python -m venv venv
```

> Note:
> If ```python``` or ```python3``` is an alias for a different version, you should use ```python3.7```.

4. Activate the virtual environment (if you did step 3):

```commandline
source venv/bin/activate
```

5. Configure SSL Certificate:

```commandline
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
```

This should generate a cert.pem file in the root directory.

### How to run

#### Run the Server

1. Navigate to the server directory:

```commandline
cd server/
```

2. Start the server (run the following):

```commandline
python server.py
```

> Note:
> If ```python``` or ```python3``` is an alias for a different version, you should use ```python3.7```.

#### Run the first Client

1. In a new terminal, navigate to the client directory:

```commandline
cd client/
```

2. Run the following:

```commandline
python client.py
```

> Note:
> If ```python``` or ```python3``` is an alias for a different version, you should use ```python3.7```.

#### Run the second Client

Repeat "Run the first Client".

1. In a new terminal, navigate to the client directory.

```commandline
cd client/
```

2. Run the following:

```commandline
python client.py
```

> Note:
> If ```python``` or ```python3``` is an alias for a different version, you should use ```python3.7```.

### Important Notes:

* Make sure you run the server before running the client.
* You can verify your Python version using any of the following:
```commandline
python --version
python3 --version
python3.7 --version
```

