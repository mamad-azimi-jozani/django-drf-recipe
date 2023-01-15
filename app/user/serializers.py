from django.contrib.auth import \
    (get_user_model,
     authenticate)
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data = {
            'email': validated_data['email'],
            'password': make_password(password),
            'name': validated_data['name'],
        }
        return get_user_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        print(user, 'hiiiiiiiiiiiiow')
        if not user:
            msg = _('unable to authenticate with provided credential :/')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



