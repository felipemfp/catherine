# Catherine

Catherine allows developers and students to create web, desktop and mobile applications that integrate a RESTful API.

**You do not use it for real applications**.

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

