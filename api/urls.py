from django.urls import path

from .views import (
    users_api,
    documents_api,
    comparisons_api,
    comparison_results_api,
    create_user_api,
    create_document_api,
    create_comparison_api,
    create_comparison_result_api,
    document_upload_api,
    compare_documents_api
)


urlpatterns = [

    # GET APIs
    path("users/", users_api),
    path("documents/", documents_api),
    path("comparisons/", comparisons_api),
    path("comparison-results/", comparison_results_api),

    # POST APIs
    path("users/create/", create_user_api),
    path("documents/create/", create_document_api),
    path("comparisons/create/", create_comparison_api),
    path("comparison-results/create/", create_comparison_result_api),

    # Document Upload
    path("documents/upload/", document_upload_api),

    # Document Comparison
    path("documents/compare/", compare_documents_api),
]