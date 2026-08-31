import os

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from comparison import compare_documents

from database.repository import (
    get_users,
    get_documents,
    get_comparisons,
    get_comparison_results,
    create_user,
    create_document,
    create_comparison,
    create_comparison_result
)


# =========================================================
# GET - Users
# =========================================================

@api_view(["GET"])
def users_api(request):

    users = get_users()

    return Response(users)


# =========================================================
# GET - Documents
# =========================================================

@api_view(["GET"])
def documents_api(request):

    documents = get_documents()

    return Response(documents)


# =========================================================
# GET - Comparison History
# =========================================================

@api_view(["GET"])
def comparisons_api(request):

    comparisons = get_comparisons()

    return Response(comparisons)


# =========================================================
# GET - Comparison Results
# =========================================================

@api_view(["GET"])
def comparison_results_api(request):

    results = get_comparison_results()

    return Response(results)


# =========================================================
# POST - Create User
# =========================================================

@api_view(["POST"])
def create_user_api(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username:
        return Response({
            "error": "username is required"
        }, status=400)

    if not email:
        return Response({
            "error": "email is required"
        }, status=400)

    if not password:
        return Response({
            "error": "password is required"
        }, status=400)

    create_user(
        username,
        email,
        password
    )

    return Response({
        "message": "User created successfully"
    })


# =========================================================
# POST - Create Document
# =========================================================

@api_view(["POST"])
def create_document_api(request):

    user_id = request.data.get("user_id")
    document_name = request.data.get("document_name")
    file_type = request.data.get("file_type")

    if not user_id:
        return Response({
            "error": "user_id is required"
        }, status=400)

    if not document_name:
        return Response({
            "error": "document_name is required"
        }, status=400)

    if not file_type:
        return Response({
            "error": "file_type is required"
        }, status=400)

    create_document(
        user_id,
        document_name,
        file_type
    )

    return Response({
        "message": "Document created successfully"
    })


# =========================================================
# POST - Create Comparison
# =========================================================

@api_view(["POST"])
def create_comparison_api(request):

    user_id = request.data.get("user_id")
    document1_id = request.data.get("document1_id")
    document2_id = request.data.get("document2_id")
    similarity_percentage = request.data.get(
        "similarity_percentage"
    )

    if not user_id:
        return Response({
            "error": "user_id is required"
        }, status=400)

    if not document1_id:
        return Response({
            "error": "document1_id is required"
        }, status=400)

    if not document2_id:
        return Response({
            "error": "document2_id is required"
        }, status=400)

    create_comparison(
        user_id,
        document1_id,
        document2_id,
        similarity_percentage
    )

    return Response({
        "message": "Comparison created successfully"
    })


# =========================================================
# POST - Create Comparison Result
# =========================================================

@api_view(["POST"])
def create_comparison_result_api(request):

    comparison_id = request.data.get("comparison_id")
    added_lines = request.data.get("added_lines")
    deleted_lines = request.data.get("deleted_lines")
    modified_lines = request.data.get("modified_lines")

    if not comparison_id:
        return Response({
            "error": "comparison_id is required"
        }, status=400)

    create_comparison_result(
        comparison_id,
        added_lines,
        deleted_lines,
        modified_lines
    )

    return Response({
        "message": "Comparison result created successfully"
    })


# =========================================================
# POST - Document Upload
# =========================================================

@api_view(["POST"])
def document_upload_api(request):

    user_id = request.data.get("user_id")

    # Allow user_id from URL also
    if not user_id:
        user_id = request.query_params.get("user_id")

    uploaded_file = request.FILES.get("document")

    # Check user_id
    if not user_id:
        return Response({
            "error": "user_id is required"
        }, status=400)

    # Check file
    if not uploaded_file:
        return Response({
            "error": "document file is required"
        }, status=400)

    # Get file name
    document_name = uploaded_file.name

    # Get file type
    file_type = os.path.splitext(
        document_name
    )[1].replace(
        ".",
        ""
    ).upper()

    # Create media/documents folder
    upload_folder = os.path.join(
        settings.BASE_DIR,
        "media",
        "documents"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    # Create file path
    file_path = os.path.join(
        upload_folder,
        document_name
    )

    # Save uploaded file
    with open(
        file_path,
        "wb+"
    ) as destination:

        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # Save document details in database
    create_document(
        user_id,
        document_name,
        file_type
    )

    return Response({
        "message": "Document uploaded successfully",
        "document_name": document_name,
        "file_type": file_type
    })


# =========================================================
# POST - Compare Two Documents
# =========================================================

@api_view(["POST"])
def compare_documents_api(request):

    user_id = request.data.get("user_id")
    document1_id = request.data.get("document1_id")
    document2_id = request.data.get("document2_id")

    # Check user_id
    if not user_id:
        return Response({
            "error": "user_id is required"
        }, status=400)

    # Check document1_id
    if not document1_id:
        return Response({
            "error": "document1_id is required"
        }, status=400)

    # Check document2_id
    if not document2_id:
        return Response({
            "error": "document2_id is required"
        }, status=400)

    # Get documents from database
    documents = get_documents()

    document1 = None
    document2 = None

    for document in documents:

        if str(document["document_id"]) == str(document1_id):
            document1 = document

        if str(document["document_id"]) == str(document2_id):
            document2 = document

    # Check document 1
    if not document1:
        return Response({
            "error": "document1 not found"
        }, status=404)

    # Check document 2
    if not document2:
        return Response({
            "error": "document2 not found"
        }, status=404)

    # Create document 1 file path
    document1_path = os.path.join(
        settings.BASE_DIR,
        "media",
        "documents",
        document1["document_name"]
    )

    # Create document 2 file path
    document2_path = os.path.join(
        settings.BASE_DIR,
        "media",
        "documents",
        document2["document_name"]
    )

    # Check physical file 1
    if not os.path.exists(document1_path):
        return Response({
            "error": "document1 file not found"
        }, status=404)

    # Check physical file 2
    if not os.path.exists(document2_path):
        return Response({
            "error": "document2 file not found"
        }, status=404)

    # Compare documents
    result = compare_documents(
        document1_path,
        document2_path
    )

    # Save comparison history
    comparison_id = create_comparison(
        user_id,
        document1_id,
        document2_id,
        result["similarity_percentage"]
    )

    # Save comparison result
    create_comparison_result(
        comparison_id,
        result["added_lines"],
        result["deleted_lines"],
        result["modified_lines"]
    )

    # Return comparison response
    return Response({
        "message": "Documents compared successfully",
        "comparison_id": comparison_id,
        "document1": document1["document_name"],
        "document2": document2["document_name"],
        "added_lines": result["added_lines"],
        "deleted_lines": result["deleted_lines"],
        "modified_lines": result["modified_lines"],
        "similarity_percentage": result["similarity_percentage"]
    })