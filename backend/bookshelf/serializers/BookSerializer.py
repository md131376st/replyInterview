from rest_framework import serializers

from bookshelf.models import Book, Author, Review


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
        authors_data = self.validated_data.pop('authors')
        authors = []
        for author in authors_data:
            author, created = Author.objects.update_or_create(name=author["name"])
            authors.append(author)

        for author in authors:
            book.authors.add(author)
        for author in book.authors.all():
            if author not in authors:
                book.authors.remove(author)

        # Update the book fields
        fields = ['title', 'year', 'price']
        for field in fields:
            try:
                setattr(book, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass

        # Save the book to the database
        book.save()

        return book


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review', 'rate', 'book', 'user']