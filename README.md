http://nepsocial.herokuapp.com/
# nepsocial
NEPSOCIAL, a simple social media for greater cause

#API DOCUMENTATION
<br>
-Add basic auth header with registered username and password<br>
-Get a token from /api/token<br>
-Use the token as username and password field can be any random string<br>
```
'/api/token', methods = ['POST']

-Use Case:
 get a valid token

Returns a token for API validation  

```
```
'/api/users', methods=['GET']

-Use Case:
get complete user's datalist

```
```
'/api/users/<int:user_id>', methods=['GET']

-Use Case:
get specific user's data

```
```
'/api/users', methods=['POST']

-Use Case:
add a new user

-Parameters:
{
  username:['username'],
  email:['email@email.com'],
  password:['password'],
  profile_image:['filename'],
  confirmed:[True],
}

```
```
'/api/users/<int:user_id>', methods=['PUT']

-Use Case:
update an existing user

-Parameters:
{
  username:['username'],
  email:['email@email.com'],
  password:['password'],
  profile_image:['filename.JPG'] or ['filename.PNG'],
  confirmed:[True] or [False],
}

```
```
'/api/users/<int:user_id>', methods=['DELETE']

-Use case:
 delete an user

```
```
'/api/posts', methods=['GET']

-Use Case:
 get all posts

```
```
'/api/posts/<int:post_id>', methods=['GET']

-Use Case:
 get specific post

```
```
'/api/posts', methods=['POST']

-Use case:
 add a post

-Parameters:
{
  title:['title'],
  content:['content'],
  category:['Public'] or ['Private'],
  image_file:['filename.JPG'] or ['filename.PNG'],
  user_id:['1'],
}

```
```
'/api/posts/<int:post_id>', methods=['PUT']

-Use case:
 update a post

-Parameters:
{
  title:['title'],
  content:['content'],
  category:['Public'] or ['Private'],
  image_file:['filename.JPG'] or ['filename.PNG'],
  user_id:['1'],
}

```
```
'/api/posts/<int:post_id>', methods=['DELETE']

-Use Case:
 delete a post
 
```
```
'/api/postlikes', methods=['GET']

-Use case:
 see post likes and liked by

```
```
'/api/<int:user_id>/<int:post_id>/<action>', methods=['POST']

-Use Case:
 like a specific post given post id and user id
 
-Parameters:
{
  post = ['1'],
  user = ['3'],
}
```
