from sqlalchemy import text
from .connection import engine


# GET - Users
def get_users():
    query = text("""
        SELECT
            user_id,
            username,
            email
        FROM users
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        users = []

        for row in result:
            users.append({
                "user_id": row.user_id,
                "username": row.username,
                "email": row.email
            })

        return users


# GET - Documents
def get_documents():
    query = text("""
        SELECT
            document_id,
            user_id,
            document_name,
            file_type,
            uploaded_at
        FROM documents
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        documents = []

        for row in result:
            documents.append({
                "document_id": row.document_id,
                "user_id": row.user_id,
                "document_name": row.document_name,
                "file_type": row.file_type,
                "uploaded_at": row.uploaded_at
            })

        return documents


# GET - Comparison History
def get_comparisons():
    query = text("""
        SELECT
            comparison_id,
            user_id,
            document1_id,
            document2_id,
            similarity_percentage,
            comparison_date
        FROM comparison_history
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        comparisons = []

        for row in result:
            comparisons.append({
                "comparison_id": row.comparison_id,
                "user_id": row.user_id,
                "document1_id": row.document1_id,
                "document2_id": row.document2_id,
                "similarity_percentage": (
                    float(row.similarity_percentage)
                    if row.similarity_percentage is not None
                    else None
                ),
                "comparison_date": row.comparison_date
            })

        return comparisons


# GET - Comparison Results
def get_comparison_results():
    query = text("""
        SELECT
            result_id,
            comparison_id,
            added_lines,
            deleted_lines,
            modified_lines,
            created_at
        FROM comparison_results
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        results = []

        for row in result:
            results.append({
                "result_id": row.result_id,
                "comparison_id": row.comparison_id,
                "added_lines": row.added_lines,
                "deleted_lines": row.deleted_lines,
                "modified_lines": row.modified_lines,
                "created_at": row.created_at
            })

        return results


# POST - Create User
def create_user(username, email, password):
    query = text("""
        INSERT INTO users
        (username, email, password)
        VALUES
        (:username, :email, :password)
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "username": username,
                "email": email,
                "password": password
            }
        )


# POST - Create Document
def create_document(user_id, document_name, file_type):
    query = text("""
        INSERT INTO documents
        (user_id, document_name, file_type)
        VALUES
        (:user_id, :document_name, :file_type)
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "user_id": user_id,
                "document_name": document_name,
                "file_type": file_type
            }
        )


# POST - Create Comparison
def create_comparison(
    user_id,
    document1_id,
    document2_id,
    similarity_percentage
):
    query = text("""
        INSERT INTO comparison_history
        (
            user_id,
            document1_id,
            document2_id,
            similarity_percentage
        )
        VALUES
        (
            :user_id,
            :document1_id,
            :document2_id,
            :similarity_percentage
        )
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "user_id": user_id,
                "document1_id": document1_id,
                "document2_id": document2_id,
                "similarity_percentage": similarity_percentage
            }
        )

        # Return newly created comparison ID
        return result.lastrowid


# POST - Create Comparison Result
def create_comparison_result(
    comparison_id,
    added_lines,
    deleted_lines,
    modified_lines
):
    query = text("""
        INSERT INTO comparison_results
        (
            comparison_id,
            added_lines,
            deleted_lines,
            modified_lines
        )
        VALUES
        (
            :comparison_id,
            :added_lines,
            :deleted_lines,
            :modified_lines
        )
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "comparison_id": comparison_id,
                "added_lines": added_lines,
                "deleted_lines": deleted_lines,
                "modified_lines": modified_lines
            }
        )