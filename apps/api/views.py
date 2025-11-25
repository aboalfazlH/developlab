from django.views.generic import View
from django.http import JsonResponse
import faker


class FrontFakeObjectsView(View):
    def get(self, request, count_article=0,count_user=0, *args, **kwargs):
        data = {"status":200,"users": [],"articles":[],"description":f"create {count_article} article and {count_user} user successfully"}
        fake = faker.Faker("fa-IR")

        for _ in range(1, count_user + 1):
            data["users"].append(
                {
                    "username": f"u_{_}",
                    "email": fake.email(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "online": fake.boolean(),
                }
            )
            for _ in range(1, count_article + 1):
                data["articles"].append(
                    {
                        "title":fake.text(),
                        "description": fake.texts(),
                        "author": f"{fake.first_name()} {fake.last_name()}",
                        "write_date": fake.date_time(),
                        "pin": fake.boolean(),
                        "active": fake.boolean(),
                        "verify": fake.boolean(),
                    }
                )


        return JsonResponse(data, safe=False)

