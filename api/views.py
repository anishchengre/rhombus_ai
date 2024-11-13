from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd
import io
from .serializers import FileUploadSerializer
from api.utils import infer_and_convert_data_types

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

            # Capture data types before inference and convert to string for JSON serialization
            data_types_before = df.dtypes.astype(str).to_dict()

            # Process the data here (use the infer_and_convert_data_types function)
            df = infer_and_convert_data_types(df)

            # Capture data types after inference and convert to string for JSON serialization
            data_types_after = df.dtypes.astype(str).to_dict()

            # Replace NaN, Infinity, and -Infinity values with None (or another value)
            df = df.applymap(lambda x: None if isinstance(x, float) and (pd.isna(x) or x == float('inf') or x == float('-inf')) else x)

            # Handle categorical columns
            for column in df.columns:
                if pd.api.types.is_categorical_dtype(df[column]):
                    # Add '' as a category to categorical columns
                    df[column] = df[column].cat.add_categories('')
                # Fill NaN values with '' (or any other value like 0)
                df[column] = df[column].fillna('')

            # Convert the DataFrame back to JSON and send it back to the client
            response_data = {
                'data': df.to_dict(orient='records'),
                'data_types_before': data_types_before,
                'data_types_after': data_types_after
            }

            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
