Przejdź na stronę https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/.

Następnie zarejestruj się https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/signup/. Użyj JSONA. Przykład : {"username" : "example",
"password" : "example123"}

Po rejestracji wyświetą się Twoje dane. Skopiuj refresh i acces key w bezpieczne miejsce, aby móc korzystać z funkcji Api. Twój acces token będzie ważny 30 min. 
Po tym czasie będziesz musiał zrobic refresh. Przejdź do edpointu /token/refresh/ i tam wpisz refresh token.  Po 24 godzinach acces token wygasa i trzeba założyć nowy token pod linkiem https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/token/.
Tam będziesz musiał wpisać swoje dane np: {"username" : "example", "password" : "example123"}. Następnie token zostanie wygenerowany.

Otwórz program np. Postman.
Wybierz metodę np: GET i wpisz w ścieżkę URL adres strony wraz z endpointem.
Przed naciśnięciem Send wejdź w zakładkę "Authorization". Ustaw "Auth type" na "Bearer Token", a następnie wklej swój acces token.
Teraz możesz korzystać z api.


Mając aktywny acces token możesz korzystać z endpointów pondanych na głównej stronie. 

Co oznaczają URL:

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com//blogposts/ - Metoda post dodaje Twój post, aby dodać wpisz np. {"title" : "example", "content" : "example", "Categories" : "Sport"}.
Metoda Get wyświetla wszystkie posty.

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/blogposts/<uuid:pk>/ - Wyświetla post po wpisaniu uuid w polu "<uuid:pk>". Można wykonać metodę GET,PUT,DELETE, jeżeli jesteś autorem postu, lub superuserem.

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/comment/ - Wyświetla komentarze, oraz można dodac komentarz np: {"blog_post" : "<uuid>", "content" : "example"}.

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/comment/<uuid:pk>/ - Wyświetla komentarz po wpisaniu uuid w polu "<uuid:pk>". Można wykonać metodę GET,PUT,DELETE, jeżeli jesteś autorem postu, lub superuserem.

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/like/ - Metoda GET wyświetla lajki użytkowników. Metoda POST możesz dać swojego lajka do posta wpisując {"blog_post" : "<uuid>"}

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/like/<int:pk>/delete/ - Usuwanie swojego lajka, bądź lajków innych użytkowników, jeżeli jestes superuserem.

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/post_filter_by/<str:category_name>/- Wyświetla posty po danej kategorii np: Sport, Finances, Adventures

LOGOUT:

https://blogpost-api-project-rb-795ff4c0aa1e.herokuapp.com/logout/ - Metodą POST : {"refresh" : "<refresh token>"} możesz się wylogować.


