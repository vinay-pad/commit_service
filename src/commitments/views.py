from django.shortcuts import render
from rest_framework import generics
from commitments.models import Commitment, CommitmentReadability
from commitments.serializers import CommitmentListSerializer, \
                                    CommitmentDetailSerializer,\
                                    CommitmentCreateSerializer, \
				    CommitmentReadabilitySerializer,\
                                    CommitmentDetailReadableSerializer, \
                                    CommitmentVerificationSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsCommitmentOwner
from .custom_exceptions import RequestProcessed

class CommitmentList(generics.ListCreateAPIView):
    queryset = Commitment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """
            Use different serializers for GET vs POST since not everybody can
            see the message until its revealed
        """
        if self.request.method == 'GET':
            return CommitmentListSerializer
        if self.request.method == 'POST':
            return CommitmentCreateSerializer

    def get_permissions(self):
        """
            Use different permission classes since only an authenticated user can
            post a message
        """
        if self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)
        if self.request.method == 'GET':
            self.permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        return super(CommitmentList, self).get_permissions()

class CommitmentDetail(generics.RetrieveAPIView):
    queryset = Commitment.objects.all()

    def get_serializer_class(self):
        """
            Use different serializers for GET vs POST since not everybody can
            see the message until its revealed
        """
        commitment_id = self.kwargs['pk']
        commitment = Commitment.objects.get(id=commitment_id)
        try:
            CommitmentReadability.objects.get(commitment=commitment)
            return CommitmentDetailReadableSerializer
        except CommitmentReadability.DoesNotExist:
            return CommitmentDetailSerializer

class CommitmentVerificationDetail(generics.RetrieveAPIView):
    queryset = Commitment.objects.all()
    serializer_class = CommitmentVerificationSerializer

    def get_queryset(self):
        commitment_id = self.kwargs['pk']
        commitment = Commitment.objects.get(id=commitment_id)
        commitment_value = self.request.query_params.get('commitment_value', None)
        if  commitment_value:
            commitment.verify(commitment_value)
        else:
            commitment.verify(commitment.commitment_value)
        return Commitment.objects.filter(id=commitment_id)

class CommitmentReadabilityCreate(generics.CreateAPIView):
    queryset = CommitmentReadability.objects.all()
    serializer_class = CommitmentReadabilitySerializer
    permission_classes = (IsCommitmentOwner,)

    def perform_create(self, serializer):
        commitment_id = self.kwargs['pk']
        commitment = Commitment.objects.get(id=commitment_id)
        try:
            cr = CommitmentReadability.objects.get(commitment=commitment_id)
            raise RequestProcessed()
        except CommitmentReadability.DoesNotExist:
            serializer.save(commitment=commitment, readable='True')
