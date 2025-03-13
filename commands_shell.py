# (venv) PS D:\Projects\news_portal\NewsPaper> python manage.py shell
# Python 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# (InteractiveConsole)
# >>> from news.models import Author, Category, Post, PostCategory, Comment
# >>> from django.contrib.auth.models import User
# >>> user1 = User.objects.create_user('usrename1')
# >>> user1
# <User: usrename1>
# >>> user2 = User.objects.create_user('usrename2')  
# >>> user2
# <User: usrename2>
# >>> author1 = Author.objects.create(rating = 0.0, user = user1)
# >>> author2 = Author.objects.create(rating = 1.0, user = user2)
# >>> category1 = Category.objects.create(name = 'Красота и здоровье')
# >>> category2 = Category.objects.create(name = 'Спорт')            
# >>> category3 = Category.objects.create(name = 'ИТ Технологии')
# >>> category4 = Category.objects.create(name = 'Образование') 
# >>> post1 = Post.objects.create(name = 'Искусственный интеллект в области медицины', text = 'Искусственный интеллект в области медицины', rating = 0.0, type = Post.paper, author = author1)
# >>> post2 = Post.objects.create(name = 'Правильное питание и спорт', text = 'Правильное питание и спорт способствуют похудению', rating = 1.0, type = Post.paper, author = author1)          
# >>> post3 = Post.objects.create(name = 'Министерство образования', text = 'Министерство образования корректирует Указ', rating = 2.0, type = Post.new, author = author2) 
# >>> post1.category.add(category3)
# >>> post2.category.add(category1, category4)
# >>> post3.category.add(category4)
# >>> comment1 = Comment.objects.create(rating = 5.0, text = 'Крутая статья', post = post1, user = user1)
# >>> comment2 = Comment.objects.create(rating = 5.0, text = 'Согласен с автором', post = post2, user = user2) 
# >>> comment3 = Comment.objects.create(rating = 1.0, text = 'Статья полный отстой', post = post2, user = user1)
# >>> comment4 = Comment.objects.create(rating = 4.0, text = 'Полезная информация!', post = post3, user = user2)
# >>> post2.dislike()
# >>> post3.like()
# >>> post1.like()
# >>> author1.update_rating()
# >>> print(author1.rating)
# 22.0
# >>> Author.objects.all().order_by('-rating').values('user__username', 'rating').first()
# >>> Post.objects.all().filter(type = Post.paper).order_by('-rating').values('datetime_in','author__user__username', 'rating', 'name', 'post__preview').first()
# >>> result = {'datetime_in': best_paper.datetime_in,'username': best_paper.author.user.username, 'rating': best_paper.rating, 'name': best_paper.name,'preview': best_paper.preview()}
# >>> print(result)
# >>>{'datetime_in': datetime.datetime(2025, 3, 13, 16, 20, 47, 319084, tzinfo=datetime.timezone.utc), 'username': 'usrename1', 'rating': 1.0, 'name': 'Искусственный интеллект в области медицины', 'preview': 'Искусственный 
# интеллект в области медицины...'}
# >>> Comment.objects.filter(post = best_paper).values('datetime_in', 'user__username', 'rating', 'text')
# <QuerySet [{'datetime_in': datetime.datetime(2025, 3, 13, 16, 21, 19, 575886, tzinfo=datetime.timezone.utc), 'user__username': 'usrename1', 'rating': 5.0, 'text': 'Крутая статья'}]>
