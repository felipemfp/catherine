# Catherine

Catherine allows developers and students to create web, desktop and mobile applications that integrate a RESTful API.

**You do not use it for real applications**.

## Catherine on Local

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisities

- Python 3.4 (or later)
- pip
- virtualenv (optional)

Once you have all, go to the terminal (or similar):

```
$ git clone https://github.com/felipemfp/catherine.git
$ cd catherine
$ virtualenv env
$ . env/bin/activate
$ pip install -r requirements.txt
```

### Running

At the first time, you'll need to create the database:

```
$ python catherine.py migrate
```

Then you are able to run the API:

```
$ python catherine.py
```

Notes: running on your local machine, Catherine will make use of SQLite. But about the authentication, responses e requests are the same of [Catherine API on Heroku](#Catherine API on Heroku) until you change that.

## [Catherine API on Heroku](//catherine-api.herokuapp.com/)

### Authentication
Catherine makes use of the open standard JSON Web Tokens to provide secure information. [Read more](https://jwt.io/introduction/).

### Response Formatting (JSON)
All response is formatted in JSON (JavaScript Object Notation) and UTF-8 encoded.

### API Request

All request should include a JSON Web Token in header, except to login or register user.

Error messages are simple and like:

```json
{
  "error": "405: Method Not Allowed"
}
```

## Thanks to...

- [Francisco Bento](//github.com/chicobentojr)

## Contributing

Just send a pull request and explain about.

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details
