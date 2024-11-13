

import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.utils import infer_and_convert_data_types
from .serializers import FileUploadSerializer
from rest_framework import status
import io

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()

            # Load the CSV file into a DataFrame
            df = pd.read_csv(io.BytesIO(file_content))

            # Process the data here (use the infer_and_convert_data_types function)
            df = infer_and_convert_data_types(df)

            # Convert the DataFrame back to JSON and send it back to the client
            response_data = df.to_dict(orient='records')
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



