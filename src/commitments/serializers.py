from rest_framework import serializers
from commitments.models import Commitment, CommitmentReadability

class CommitmentCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Commitment
        fields = ('id', 'user', 'message', 'created_ts',)

    def create(self, validated_data):
        commitment = Commitment.objects.create(**validated_data)
        commitment.generate_commitment_value()
        commitment.save()
        return commitment

class CommitmentListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Commitment
        fields = ('id', 'user',)

class CommitmentDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Commitment
        fields = ('id', 'user', 'commitment_value',)

class CommitmentDetailReadableSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Commitment
        fields = ('id', 'user', 'commitment_value', 'message', 'created_ts',)

class CommitmentReadabilitySerializer(serializers.ModelSerializer):
    commitment = serializers.ReadOnlyField(source='commitment.id')
    readable = serializers.ReadOnlyField()
    class Meta:
        model = CommitmentReadability
        fields = ('commitment', 'readable')
