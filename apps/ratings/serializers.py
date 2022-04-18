from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.SerializerMethodField(read_only=True)
    opponent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        # exclude these two fields
        exclude = ["updated_at", "pkid"]

    # when creating a serializer. The name of the method has to start with "get_"and the end, the name of the serializer above "rater"
    def get_rater(self, obj):
        # rater: ForeignKey(AUTH_USER_MODEL)  (((USER: username..))
        return obj.rater.username

    def get_opponent(self, obj):
        # opponent: ForeignKey(Profile) (((Profile: user = OneToOneField(User,..)))
        return obj.opponent.user.username



