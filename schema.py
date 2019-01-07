import graphene
import books.schema
import authors.schema
import genres.schema
import views.schema
import series.schema
import publications.schema


class Query(
    books.schema.BookQuery,
    books.schema.BookRatingQuery,
    books.schema.BookFilterQuery,
    authors.schema.AuthorQuery,
    authors.schema.AuthorRatingQuery,
    authors.schema.AuthorFilterQuery,
    genres.schema.GenreQuery,
    views.schema.ViewQuery,
    publications.schema.PublicationQuery,
    graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class RootMutation(
    books.schema.BookMutation,
    authors.schema.AuthorMutation,
    series.schema.SeriesMutation,
    views.schema.ViewMutation,
    publications.schema.PublicationMutation,
    publications.schema.UserMutation,
    graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=RootMutation, auto_camelcase=False)