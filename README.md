#### Phoenix Blog

1. python3.7 -m venv /data/venv
2. source /data/venv/bin/activity
3. cd /data && git clone https://github.com/chunyangfeng/phoenix.git
4. cd phoenix
5. vim phoenix/config.py   将其中的配置修改为本地环境配置
6. python -m pip install -r requirements.txt
7. python manage.py makemigrations
8. python manage.py migrate
9. python manage.py initial
10. python manage.py runserver 0.0.0.0:8000

#### 配置

启动成功后，需要修改admin账号的启用状态，否则会无法登陆

```Python
python manage.py shell
from blog.auth.models import User
user = User.objects.get(username="admin")
user.allow_login = True
user.save()
```
