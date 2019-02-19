# Blog Rest Api with Flask
This is the backend for a blog-style app. User's can sign up, create posts, create & like comments on posts as well.


## Endpoints
  ### /api/v1/users
    * ```POST``` - returns a 201 and sets location headers to the auth login endpoint
    * ```GET``` - returns a 200 and the currently signed in users profile. Gets the current user via auth headers
    * ```PUT``` - returns a 201 and sets location headers to the users endpoint. **requires a fresh access token**. allows a user to update their name and/or username
    * ```DELETE``` - returns a 204 and sets location headers to the users endpoint. **requires a fresh access token**. will delete a user's posts and comments as well
  ### /api/v1/users/<username>
    * ```GET``` returns a 200 and the users profile, or a 404 if it doesn't exist.
  ### /api/v1/auth/login:
    * ```POST``` returns a 200, an access token, and a refresh token if valid credentials(username and password) are provided
  ### ``/api/v1/auth/refresh
    * ```GET```:
      * **requires a refresh token in the headers**
      * will return a new access token, but this token will not be treated as fresh
  ### /api/v1/posts
    * ```POST```: 
      * returns a 201 and sets location headers to the newly created post's endpoint
      * returns a 400 and error messages for any validation errors
    * ```GET``` - returns a 200, a list of posts, and some pagination details(next_page, prev_page, has_next, has_prev)
      * can include a query string for pagination, for example ```/api/v1/posts?page_num=3&per_page=5```
  ### /api/v1/post/<post_id>
    * ```GET``` - returns a 200 and the post including any associated comments. returns a 404 if no post is found
    * ```PUT```: 
      * returns a 204 and sets location headers to post's endpoint. will allow updates on title and content
      * returns a 403 if someone other than the post author is sending the request
    * ```DELETE``` - : 
      * returns a 204 and sets location headers to posts endpoint. will allow updates on title and content
      * returns a 403 if someone other than the post author is sending the request

## Technologies Used
flask
flask-restful
flask-sqlalchemy
flask-marshmallow
marshmallow
marshmallow-sqlalchemy
python-dotenv
psycopg2
flask-jwt-extended
argon2-cffi
flask-limiter