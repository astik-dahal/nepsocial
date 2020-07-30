# from flask import Flask
# app = Flask(__name__)

posts = {
    'title':
    'Hello world',
    'content':
    '''Lorem ipsum dolor sit amet consectetur adipisicing elit.
     Laudantium tenetur quaerat in blanditiis ullam impedit exercitationem quasi, 
     sunt totam, nihil quia ipsa nobis aspernatur, assumenda culpa architecto modi
      rem ratione itaque repudiandae quae neque. Recusandae ea distinctio corporis
       at sed temporibus ducimus praesentium debitis? Saepe non sapiente beatae 
       porro labore, et ad tempore commodi optio deleniti nulla ut quo facilis 
       praesentium recusandae consectetur. Vel repellat iure explicabo suscipit
        eveniet? Voluptate mollitia unde nobis dolores. Obcaecati asperiores ipsam
         eius architecto eum quae at rem deleniti ut praesentium, nulla quidem
         '''
}
content = posts.get('content')
Prv = (content[:112]+"..") if len(content)>114 else content
# contentPrv = Prv.replace('\n', '')
contentPrv = Prv.replace('\n', '')
print(contentPrv)

