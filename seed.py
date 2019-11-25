import models
from playhouse.shortcuts import model_to_dict


def seed_database():
    # brad = models.User.create(email = 'bffd@b.com', password = '123', nickname = 'brad')
    # post1 = models.Post.create(
    #     img='someurl',
    #     nameOfFish='Trout',
    #     description='Big boi',
    #     gear='Bare hands',
    #     user=brad
    # )

    # post2 = models.Post.create(
    #     img='someurl',
    #     nameOfFish='Speckled Trou',
    #     description='Bigger boi',
    #     gear='Bare hands',
    #     user=brad
    # )

    # print(post1)
    # print(post2)

    # print(model_to_dict(brad, backrefs=True))
    brad = models.User.get(id=1)

    brads_posts = models.Post.select().where(models.Post.user==brad.id)

    print([model_to_dict(post) for post in brads_posts])

if __name__ == "__main__":
    seed_database()
