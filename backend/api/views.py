from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd
import io
import os
from .serializers import FileUploadSerializer
from api.utils import infer_and_convert_data_types

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        # Validate file type (check for .csv or .xlsx)
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file extension
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        file_extension = file_extension.lower()

        # Check if the file is a CSV or Excel file
        if file_extension not in ['.csv', '.xlsx']:
            return Response({"error": "Invalid file type. Only .csv and .xlsx files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed if the file is valid
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_content = uploaded_file.read()

            # Handle CSV and Excel files differently
            if file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_extension == '.xlsx':
                df = pd.read_excel(io.BytesIO(file_content))

            data_types_before = df.dtypes.astype(str).to_dict()

            # Infer and convert data types
            df = infer_and_convert_data_types(df)

            data_types_after = df.dtypes.astype(str).to_dict()

            # Replace NaN, Infinity, and -Infinity values with None
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

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
