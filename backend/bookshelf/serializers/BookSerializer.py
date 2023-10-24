from rest_framework import serializers

from bookshelf.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'year', 'authors', 'price']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for auther in authors_data:
            author, created =Author.objects.get_or_create(name=auther["name"])
            book.authors.add(author.id)
        return book

    def update(self, book, validated_data):
        authors_data = validated_data.pop('authors')
        authers=[]
        for auther in authors_data:
            author, created = Author.objects.update_or_create(name=auther["name"])
            authers.append(author.id)
        book.authors.set(authers)
        fields = ['title', 'year', 'price']
        for field in fields:
            try:
                setattr(book, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        book.save()
        return book
