from bs4 import BeautifulSoup


def make_plain_text(text: str) -> str:
    """
    This function uses BeautifulSoup to parse the input HTML
    and extract the plain text content.

    :param text: str - The HTML formatted text to be converted.
    :return: str - The plain text extracted from the HTML input.
    """
    raw_content = text
    soup = BeautifulSoup(raw_content, 'html.parser')
    return soup.get_text()


eligible_frame_titles = {
    "Copy of Noun",
    "Copy of Word",
    "Copy of Verb conjugation"}


def is_title_match(item_title: str) -> bool:
    """
    Checks if the given title is in the predefined set of titles to match.
    """
    return item_title in eligible_frame_titles


def gather_plain_text_from_frame(client, board_id: str, frame_id: str) -> str:
    """
    Collects and concatenates all plain text within a frame.
    """
    frame_items = client.get_all_items_within_frame(board_id=board_id, parent_item_id=frame_id)
    full_plain_text = " ".join(make_plain_text(item.data.actual_instance.content) for item in frame_items)
    return full_plain_text
