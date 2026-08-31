from docx import Document
from difflib import SequenceMatcher


# Read text from DOCX document
def read_document(file_path):

    document = Document(file_path)

    lines = []

    for paragraph in document.paragraphs:
        lines.append(paragraph.text)

    return lines


# Compare two DOCX documents
def compare_documents(document1_path, document2_path):

    document1_lines = read_document(document1_path)
    document2_lines = read_document(document2_path)

    matcher = SequenceMatcher(
        None,
        document1_lines,
        document2_lines
    )

    added_lines = 0
    deleted_lines = 0
    modified_lines = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "insert":
            added_lines += j2 - j1

        elif tag == "delete":
            deleted_lines += i2 - i1

        elif tag == "replace":
            modified_lines += max(
                i2 - i1,
                j2 - j1
            )

    total_lines = max(
        len(document1_lines),
        len(document2_lines)
    )

    if total_lines == 0:
        similarity_percentage = 100.0
    else:
        similarity = SequenceMatcher(
            None,
            document1_lines,
            document2_lines
        ).ratio()

        similarity_percentage = round(
            similarity * 100,
            2
        )

    return {
        "added_lines": added_lines,
        "deleted_lines": deleted_lines,
        "modified_lines": modified_lines,
        "similarity_percentage": similarity_percentage
    }