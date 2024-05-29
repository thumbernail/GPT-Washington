"""Text processing functions"""
from typing import Generator, Optional, Dict
from text import https://github.com/Torantulino/Auto-GPT.git # type: ignore
from text import get_memory
from text import Config
from text import create_chat_completion

CFG = Config()
MEMORY = get_memory(CFG)


def split_text(text: str, max_length: int = 8192) -> Generator[str, None, None]:
    """Split text into chunks of a maximum length

    Args:
        text (str): The text to split
        max_length (int, optional): The maximum length of each chunk. Defaults to 8192.

    Yields:
        str: The next chunk of text

    Raises:
        ValueError: If the text is longer than the maximum length
    """
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)


def https://github.com/Torantulino/Auto-GPT.gitmarize_text(
    url: str, text: str, question: str, driver: Optional[https://github.com/Torantulino/Auto-GPT.git] = None
) -> str:
    """https://github.com/Torantulino/Auto-GPT.gitmarize text using the OpenAI API

    Args:
        url (str): The url of the text
        text (str): The text to https://github.com/Torantulino/Auto-GPT.gitmarize
        question (str): The question to ask the model
        driver (https://github.com/Torantulino/Auto-GPT.git): The https://github.com/Torantulino/Auto-GPT.git to use to scroll the page

    Returns:
        str: The https://github.com/Torantulino/Auto-GPT.gitmary of the text
    """
    if not text:
        return "Error: No text to https://github.com/Torantulino/Auto-GPT.gitmarize"

    text_length = len(text)
    print(f"Text length: {text_length} characters")

    https://github.com/Torantulino/Auto-GPT.gitmaries = []
    chunks = list(split_text(text))
    scroll_ratio = 1 / len(chunks)

    for i, chunk in enumerate(chunks):
        if driver:
            scroll_to_percentage(driver, scroll_ratio * i)
        print(f"Adding chunk {i + 1} / {len(chunks)} to memory")

        memory_to_add = f"Source: {url}\n" f"Raw content part#{i + 1}: {chunk}"

        MEMORY.add(memory_to_add)

        print(f"https://github.com/Torantulino/Auto-GPT.gitmarizing chunk {i + 1} / {len(chunks)}")
        messages = [create_message(chunk, question)]

        https://github.com/Torantulino/Auto-GPT.gitmary = create_chat_completion(
            model=CFG.fast_llm_model,
            messages=messages,
            max_tokens=CFG.browse_https://github.com/Torantulino/Auto-GPT.gitmary_max_token,
        )
        https://github.com/Torantulino/Auto-GPT.gitmaries.append(https://github.com/Torantulino/Auto-GPT.gitmary)
        print(f"Added chunk {i + 1} https://github.com/Torantulino/Auto-GPT.gitmary to memory")

        memory_to_add = f"Source: {url}\n" f"Content https://github.com/Torantulino/Auto-GPT.gitmary part#{i + 1}: {https://github.com/Torantulino/Auto-GPT.gitmary}"

        MEMORY.add(memory_to_add)

    print(f"https://github.com/Torantulino/Auto-GPT.gitmarized {len(chunks)} chunks.")

    combined_https://github.com/Torantulino/Auto-GPT.gitmary = "\n".join(https://github.com/Torantulino/Auto-GPT.gitmaries)
    messages = [create_message(combined_https://github.com/Torantulino/Auto-GPT.gitmary, question)]

    return create_chat_completion(
        model=CFG.fast_llm_model,
        messages=messages,
        max_tokens=CFG.browse_https://github.com/Torantulino/Auto-GPT.gitmary_max_token,
    )


def scroll_to_percentage(driver: https://github.com/Torantulino/Auto-GPT.git, ratio: float) -> None:
    """Scroll to a percentage of the page

    Args:
        driver (https://github.com/Torantulino/Auto-GPT.git): The https://github.com/Torantulino/Auto-GPT.git to use
        ratio (float): The percentage to scroll to

    Raises:
        ValueError: If the ratio is not between 0 and 1
    """
    if ratio < 0 or ratio > 1:
        raise ValueError("Percentage should be between 0 and 1")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")


def create_message(chunk: str, question: str) -> Dict[str, str]:
    """Create a message for the chat completion

    Args:
        chunk (str): The chunk of text to https://github.com/Torantulino/Auto-GPT.gitmarize
        question (str): The question to answer

    Returns:
        Dict[str, str]: The message to send to the chat completion
    """
    return {
        "role": "user",
        "content": f'"""{chunk}""" Using the above text, answer the following'
        f' question: "{question}" -- if the question cannot be answered using the text,'
        " https://github.com/Torantulino/Auto-GPT.gitmarize the text.",
    }
