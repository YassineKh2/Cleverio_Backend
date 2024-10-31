from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Art, Comment
from .serializers import ArtSerializer, CommentSerializer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
#import torch



# Create Art
@api_view(['POST'])
def create_art(request):
    serializer = ArtSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save without user since it's static for now
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Read Art (List)
@api_view(['GET'])
def list_arts(request):
    arts = Art.objects.all()
    serializer = ArtSerializer(arts, many=True)
    return Response(serializer.data)


# Read Art (Detail)
@api_view(['GET'])
def detail_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
    except Art.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArtSerializer(art)
    return Response(serializer.data)


# Update Art
@api_view(['PUT'])
def update_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
    except Art.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArtSerializer(art, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Art
@api_view(['DELETE'])
def delete_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
        art.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Art.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)






@api_view(['GET'])
def list_comments(request, art_id):
    comments = Comment.objects.filter(art_id=art_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_comment(request, art_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, art_id=art_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  # This is correct

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)  # Ensure this line is indented properly

# Comment Functions
@api_view(['POST'])
def create_comment(request, art_id):
    data = request.data.copy()
    data['art'] = art_id  # Automatically set the art field from the URL parameter
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())



@api_view(['POST'])
def create_comment(request, art_id):
    data = request.data.copy()
    data['art'] = art_id  # Automatically set the art field from the URL parameter
    
    # Moderate content before saving
    moderation_results = moderate_content([data.get('content', '')])
    inappropriate_content = [
        label for label, probability in moderation_results[0]['moderation']
        if label == 'inappropriate' and probability > 0.5  # Adjust threshold as needed
    ]
    
    # Block inappropriate content
    if inappropriate_content:
        return Response({"detail": "Content flagged as inappropriate."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save comment if content is appropriate
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation")
tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")

def moderate_content(texts):
    //
    Process a list of text inputs for moderation using KoalaAI's Text-Moderation model.
    
    Args:
        texts (list): List of text strings to moderate.
        
    Returns:
        list: List of dictionaries with labels and probabilities for each text.
//
    results = []

    for text in texts:
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt")
        
        # Run the model on the tokenized input
        outputs = model(**inputs)
        
        # Get the predicted logits and apply softmax to convert to probabilities
        probabilities = torch.softmax(outputs.logits, dim=-1).squeeze()
        
        # Retrieve labels from the model config
        id2label = model.config.id2label
        labels = [id2label[idx] for idx in range(len(probabilities))]
        
        # Combine labels and probabilities, then sort by probability in descending order
        label_prob_pairs = list(zip(labels, probabilities.tolist()))
        label_prob_pairs.sort(key=lambda item: item[1], reverse=True)
        
        # Append sorted results to the final output
        result = {"text": text, "moderation": label_prob_pairs}
        results.append(result)

    return results

"""
