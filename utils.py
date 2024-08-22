def format_hashtag(tag: str) -> str:
    """
    Convert a tag to a formatted hashtag.
    
    Args:
        tag (str): The original tag to format usually in format "Tag Name".
        
    Returns:
        str: The formatted hashtag to format "#tagname"
    """
    return f'#{tag.replace(" ", "").lower()}'