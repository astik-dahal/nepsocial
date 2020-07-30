# nepsocial
NEPSOCIAL, a simple social media for greater cause

/api/token
-get a valid token

'/api/users', methods=['GET']
-get complete user's datalist

'/api/users/<int:user_id>', methods=['GET']
-get specific user's data


'/api/users', methods=['POST']
-add a new user

'/api/users/<int:user_id>', methods=['PUT']
-update an existing user

'/api/users/<int:user_id>', methods=['DELETE']
-delete an user

'/api/posts', methods=['GET']
-get all posts

'/api/posts/<int:post_id>', methods=['GET']
-get specific post

'/api/posts', methods=['POST']
-add a post

'/api/posts/<int:post_id>', methods=['PUT']
-update a post

'/api/posts/<int:post_id>', methods=['DELETE']
-delete a post

'/api/postlikes', methods=['GET']
-see post likes and liked by

'/api/<int:user_id>/<int:post_id>/<action>', methods=['POST']
-like a specific post
