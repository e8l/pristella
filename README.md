# pristella
Web Cam Server as a Twitter Client.

## limitation
I'm **novice** in Python.
So, there may be many mistakes or bad writings.

# Prepare

## Twitter
Create Twitter account and get an app's consumer key & consumer secret.

Then, update config/settings.json.
```javascript
{
  "consumer_key": "put your consumer_key",
  "consumer_secret": "put your consumer_secret",
  //
  // ... other settings
  //
}
```

## Install dependencies
```bash
$ pip install python-daemon
$ pip install -e git+https://github.com/litl/rauth.git#egg=rauth
```

## Authorization(Optional)
```bash
$ bin/authorization
```

# Usage
```bash
$ bin/pristella
```

# Dependencies
- Python3 (>=3.4.3 ?)
- rauth
- python-daemon

**We must install latest version rauth from GitHub repository.**
- [rauth](https://github.com/litl/rauth)

# License
MIT
