# Blog Rest Api with Flask
This is the backend for a blog-style app. User's can sign up, create posts, create & like comments on posts as well. Includes rate limiting, image uplaods, and logic to confirm a user's email address via mailgun. Access tokens are not provided unless the link sent via email is visited! If you'd like to test this app out take a look at ```example.env``` for the various environment variables needed.


## Endpoints

### /api/v1/users
<b>User's will not be able to recieve an access token until their email is verified</b>
  * ```POST``` - returns a 201 and sets location headers to the auth login endpoint
  * ```GET``` - returns a 200 and the currently signed in users profile. Gets the current user via auth headers
  * ```PUT``` - returns a 201 and sets location headers to the users endpoint. <b>requires a fresh access token</b>. 
    allows a user to update their name and/or username
  * ```DELETE``` - returns a 204 and sets location headers to the users endpoint. <b>requires a fresh access token</b>. 
    will delete a user's posts and comments as well

### /api/v1/users/<username>
  * ```GET``` returns a 200 and the users profile, or a 404 if it doesn't exist.

### /api/v1/user/activate_account/<user_id>
  * ```GET``` returns a 200, a message saying the user was activated, and sets location headers to the auth login api

### /api/v1/auth/login
  * ```POST``` returns a 200, an access token, and a refresh token if valid credentials(username and password) are provided

### /api/v1/auth/refresh
  * ```GET```:
    * <b>requires a refresh token in the headers</b>
    * will return a new access token, but this token will not be treated as fresh

### /api/v1/posts
  * ```POST``` - returns a 201 and sets location headers to the newly created post's endpoint
  * ```GET``` - returns a 200, a list of posts, and some pagination details(next_page, prev_page, has_next, has_prev)
    * can include a query string for pagination, for example ```/api/v1/posts?page_num=3&per_page=5```

### /api/v1/posts/<post_id>
  * ```GET``` - returns a 200 and the post including any associated comments. returns a 404 if no post is found
  * ```PUT``` -  returns a 204 and sets location headers to post's endpoint. will allow updates on title and content
  * ```DELETE``` - returns a 204 and sets location headers to posts endpoint. will delete any related comments

### /api/v1/posts/<post_id>/comments
  * ```POST``` - returns a 201 and sets location headers to the post's endpoint

### /api/v1/comment/<comment_id>
  * ```GET``` - returns a 200 and the comment
  * ```PUT``` - returns a 204 and sets location headers to comment's endpoint. allows updates on the comment body
  * ```DELETE``` - returns a 204 and sets location headers to posts endpoint

### /api/v1/comment/<comment_id>/like_unlike
  * ```POST``` - will either like or unlike a comment depending on whether a relationship is already created
      - returns a 201 if the comment is liked(created)
      - returns a 204 if the comment is unliked(deleted)

### /api/v1/images/upload
  * You can upload an image and then use the returned path as the "image" field for a blog post 
  * ```POST``` - will upload an image if the file extension is supported
      - returns a 201 if the image is creared and a path to the image

## Errors Status Codes
These are some of the status codes that you may encounter
  1) 400 - send for bad requests or validation errors when creating or updating database entries (posts, comments, users). will also have error messages.
  2) 401 - is sent when auth headers are missing or token has expired.
  3) 403 - sent if someone other than the resource owner is trying to make an update (eg a put request to a specific comment)
  4) 404 - sent when an enpoint isn't supported, or an entry in the database isn't found
  5) 422 - sent when a token is not properly formatted or is malformed
  6) 429 - sent if rate limits are exceeded

## Technologies Used
flask
flask-restful
flask-sqlalchemy
flask-uploads
flask-marshmallow
marshmallow
marshmallow-sqlalchemy
python-dotenv
psycopg2
flask-jwt-extended
argon2-cffi
flask-limiter
requests